# Importing packages
import ast
import simpy
import pandas as pd
import inspect
import os


## Importing the path of current working directory
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory


from PPR import PPRClasses
from PPR.PPRClasses import *
from PPR.Functions import *

# function to add attributes to an object during run time
def add_attribute(self, attribute):
    if not isinstance(attribute, dict):
        raise ValueError("Attribute should be a dictionary")

    for key, value in attribute.items():
        setattr(self, key, value)
        self.attributes[key] = value 


def get_classes(library_module):  # function which returns the list of classes available in the module
    classes = []
    for name, obj in inspect.getmembers(library_module):
        if inspect.isclass(obj):
            classes.append(obj)

    return classes


def get_attributes(class_type):
        attributes = class_type().attributes
        return attributes


def evaluate_cost(object):
    # to evaluate the cost based on the list of components being used in case of assemblies and products
    pass


def model_domain(env, domain, directory_path):
    object_list = []
    file_path = f'{directory_path}/{domain.__name__}.xlsx' # file path of excel sheet for the given class
    attribute_list = domain(env).attributes # list of atributes of a class
    
    if os.path.isfile(file_path):  # if sheet exists at the given path
        class_df = pd.read_excel(file_path, usecols=lambda x: 'Unnamed' not in x)  # import excel sheet as a pandas dataframe

        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:  # Open Excel writer outside the loop
            for attribute in attribute_list:  # iterating through attributes of the class and add missing columns corresponding to attributes
                if attribute not in class_df.columns:
                    new_column = pd.Series(name=attribute, dtype=object)  # Create a new column with the required name
                    class_df = pd.concat((class_df, new_column), axis=1)  # adding attributes as an index in the dataframe

            class_df.to_excel(writer, sheet_name=f'{domain.__name__}', index=True)  # Write the updated dataframe to the Excel file

        
        # Creating instances of the object
        for index, row in class_df.iterrows():
            # Create an instance of the class dynamically based on class name
            class_instance = domain(env)  
            for col_name, value in row.items():
                if col_name != 'kwargs':
                    if hasattr(class_instance, col_name):
                        attribute_type = getattr(class_instance, col_name)
                        
                        if isinstance(attribute_type, (dict, list)):
                            setattr(class_instance, col_name, ast.literal_eval(value))
                        else:
                            setattr(class_instance, col_name, value)
                    else:
                        setattr(class_instance, col_name, value)
                        print(f'new attribute:{col_name} is added to an instance of {domain}')
            object_list.append(class_instance)
           
    else:
        new_df = pd.DataFrame({})  # create an empty pandas dataframe
        
        for attribute in attribute_list:
                new_df[f'{attribute}'] = [] # adding attributes as index in the dataframe

        with pd.ExcelWriter(file_path, engine='openpyxl') as writer: # Replacing the excel sheet with updated dataframe 
            new_df.to_excel(writer, sheet_name=f'{domain.__name__}', index=True)

        print(f'Added the sheet: {domain.__name__}. Please update the sheet.')

    return object_list


def map_processes(process_flow_model, object_list): # generates upstream and downstream processes for each of the processes
    processes = []
    for process_id, network in process_flow_model.items():
        input_processes  = network[0]
        output_processes  = network[1]
        upstream_processes = define_upstream(process_id, input_processes, object_list)
        downstream_processes = define_downstream(process_id, output_processes, object_list)
        
        # adding current process to the list
        current_process = get_process_object(process_id, object_list)
        if current_process not in processes:
                processes.append(current_process)

    processes = processes + upstream_processes + downstream_processes

    for process in processes:
        if process is not None:
            upstream_processes = get_name_list(process.upstream_processes)
            downstream_processes = get_name_list(process.downstream_processes)
            print(f'{process.name}: {upstream_processes}, {downstream_processes}')
        else:
            print("No production objects defined.")

        
     

def get_name_list(list_of_objects):
    name_list = []
    for object in  list_of_objects:
        name_list.append(object.name)
    return name_list

def get_process_object(process_id, object_list):
    return next((obj for obj in object_list if obj.id == process_id), None) # returns process object matching the id passed


def define_upstream(process_id, input_processes, object_list):
    process_list = []
    current_process = get_process_object(process_id, object_list)
    if current_process is not None:

        for input_process_id in input_processes:
            input_process_object = get_process_object(input_process_id, object_list)

            # if input_process_object is not None:
            if input_process_object not in current_process.upstream_processes:
                current_process.upstream_processes.append(input_process_object)

            if current_process not in input_process_object.downstream_processes:
                input_process_object.downstream_processes.append(current_process)

            process_list.append(input_process_object)
    return process_list

       

def define_downstream(process_id, output_processes, object_list):
    process_list = []
    current_process = get_process_object(process_id, object_list)

    if current_process is not None:

        for output_process_id in output_processes:
            output_process_object = get_process_object(output_process_id, object_list)

            if output_process_object is not None:
                if output_process_object not in current_process.downstream_processes:
                    current_process.downstream_processes.append(output_process_object)

                if current_process not in output_process_object.upstream_processes:
                    output_process_object.upstream_processes.append(current_process)

                process_list.append(output_process_object)
            else:
                print(f"Warning: Process with ID {output_process_id} not found in object_list")

    return process_list



def add_data_to_excel(file_path, search_column, search_value, target_column, data_to_add):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, usecols=lambda x: 'Unnamed' not in x)

        # Find the index of the row based on the value of the search_column
        index_to_update = df.index[df[search_column] == search_value].tolist()

        # Check if the row was found
        if index_to_update:
            # Get the existing list as a string from the specified cell
            existing_list_str = df.at[index_to_update[0], target_column]

            # Convert the string to a list using ast.literal_eval
            existing_list = ast.literal_eval(existing_list_str)

            # Update the list (add new elements, remove duplicates, etc.)
            for element in data_to_add:
                if element not in existing_list:
                    existing_list.append(element)

            # Convert the updated list back to a string
            updated_list_str = str(existing_list)

            # Add the updated string to the target_column in the selected row
            df.at[index_to_update[0], target_column] = updated_list_str

            # Write the updated DataFrame back to the Excel file
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, index=False)

            print(f"Data added successfully for {search_column}={search_value}.")
        else:
            print(f"Row not found for {search_column}={search_value}.")

    except Exception as e:
        print(f"Error: {e}")






'''
------------ Function for making contianer ------------
def make_container(env, product):
    return simpy.Container(env, capacity = 5, init = 5)
    pass
    
------------ Function for addding resource to a process ------------
## processObject is the object to which the list is being updated and objectsList is the list of objects of lower hierarchical level
def update_resources(processObject, objectsList): # Updates the resources of the object bsaed on the objects of lower hierarchical level
    if isinstance(objectsList, list):
        for process in objectsList:
            processObject.resources.update(process.resources)
    elif not isinstance(objectsList, list) and not isinstance(objectsList, tuple) and not isinstance(objectsList, dict) and not isinstance(objectsList, set):
        processObject.resources.update(process.resources)
    else:
        raise TypeError("Invalid datatype for 'processes'. It should be a list or a single object.")

------------ Function for adding supplies to an object ------------
def update_supplies(processObject, objectsList):
    if isinstance(objectsList, list):
        for process in objectsList:
            processObject.supplies.update(process.resources)
    elif not isinstance(objectsList, list) and not isinstance(objectsList, tuple) and not isinstance(objectsList, dict) and not isinstance(objectsList, set):
        processObject.supplies.update(process.resources)
    else:
        raise TypeError("Invalid datatype for 'skills'. It should be a list or a single object.")

------------ Function for adding skills to an object ------------
## Updating the skills based on the objects of lower hierarchy
def update_skills(processObject, objectsList):
    if isinstance(objectsList, list):
        for process in objectsList:
            processObject.skills.update(process.resources)
    elif not isinstance(objectsList, list) and not isinstance(objectsList, tuple) and not isinstance(objectsList, dict) and not isinstance(objectsList, set):
        processObject.skills.update(process.resources)
    else:
        raise TypeError("Invalid datatype for 'skills'. It should be a list or a single object.")
'''