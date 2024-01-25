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


def add_kwargs(object, **kwargs):
    for key, value in kwargs.items():
        if hasattr(object, key): # Check if the attribute already exists
            raise ValueError(f"Attribute '{key}' already exists in the class.")
        else:  
            setattr(object, key, value) # Add the attribute to the object


def get_classes(library_module):  # function which returns the list of classes available in the module
    classes = []
    for name, obj in inspect.getmembers(library_module):
        if inspect.isclass(obj):
            classes.append(obj)

    return classes


def get_attributes(class_type):
    return class_type().attributes


def evaluate_cost(object):
    # to evaluate the cost based on the list of components being used in case of assemblies and products
    pass


def model_domain(env, domain_class):
    object_list = []
    directory_path = '../customSim/LES/systemDefinition'
    file_path = os.path.join(directory_path, f'{domain_class.__name__}.xlsx') # file path of excel sheet for the given class

    attribute_list = domain_class(env).attributes # list of atributes of a class
    
    if os.path.isfile(file_path):  # if sheet exists at given path
        class_df = pd.read_excel(file_path, usecols=lambda x: 'Unnamed' not in x) # import excel sheet as a pandas dataframe

        for attribute in attribute_list: # iterating through attributes of the class and add missing columns corresponding to attributes
            if attribute not in class_df.columns:
                new_column = pd.Series(name=attribute, dtype=object)  # Create a new column with the required name
                class_df = pd.concat((class_df, new_column), axis=1) # adding attributes as index in the dataframe

                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:  # Replacing the excel sheet with updated dataframe            
                    class_df.to_excel(writer, sheet_name=f'{domain_class.__name__}', index=True)
        
        # Creating instances of the object
        for index, row in class_df.iterrows():
            # Create an instance of the class dynamically based on class name
            class_instance = domain_class(env)  

            for col_name, value in row.items():  # Iterate through each column of the DataFrame 
                if col_name != 'kwargs':
                    if hasattr(class_instance, col_name):  # Check if the attribute exists in the class
                        setattr(class_instance, col_name, value) # Set the attribute value in the class instance
                        print(type(getattr(class_instance, col_name)))
                    else:
                        setattr(class_instance, col_name, value)
                        print(f'new attribute:{col_name} is added to an instance of {domain_class}')
    
            object_list.append(class_instance)  # Adding the object to object list

            print(f"Instance of {domain_class}: {class_instance.__dict__}")
           

    else:
        new_df = pd.DataFrame({})  # create an empty pandas dataframe
        
        for attribute in attribute_list:
                new_df[f'{attribute}'] = [] # adding attributes as index in the dataframe

                with pd.ExcelWriter(file_path, engine='openpyxl') as writer: # Replacing the excel sheet with updated dataframe 
                    new_df.to_excel(writer, sheet_name=f'{domain_class.__name__}', index=True)

        print(f'Added the sheet: {domain_class.__name__}. Please update the sheet for added functionality')
    return object_list


def map_processes(process_flow_model, object_list): # generates upstream and downstream processes for each of the processes
    processes = []
    for process_id, network in process_flow_model.items():
        print('process mapping called')
        input_processes  = network[0]
        output_processes  = network[1]
        upstream_processes = define_upstream(process_id, input_processes, object_list)
        downstream_processes = define_downstream(process_id, output_processes, object_list)
        processes.append(upstream_processes + downstream_processes)
    processes  = list(set(processes)) # removes duplicate processes in the list


def get_process_object(process_id, object_list):
    return next((obj for obj in object_list if obj.id == process_id), None) # returns process object matching the id passed


def define_upstream(process_id, input_processes, object_list):
    process_list = []
    current_process = get_process_object(process_id, object_list)
    process_list.append(process_id)
    for input_process_id in input_processes:

        input_process = get_process_object(input_process_id, object_list)

        if input_process_id not in [id for obj in object_list for id in dir(input_process.upstream_processes)]:
            print(f'{type(current_process)}, {type(current_process.upstream_processes)}')
            current_process.upstream_processes.append(input_process) # adding input process object for upstream of current process
   
        if process_id not in [id for obj in object_list for id in dir(input_process.downstream_processes)]:
            input_process.downstream_processes.append(current_process) # adding current process object for downstream of input process
        
        process_list.append(input_process)
    return process_list
       

def define_downstream(process_id, output_processes, object_list):
    process_list = []
    current_process = get_process_object(process_id, object_list)
    process_list.append(process_id)
    for output_process_id in output_processes:

        output_process = get_process_object(output_process_id, object_list)

        if output_process_id not in [id for obj in object_list for id in dir(output_process.upstream_processes)]:
            current_process.upstream_processes.append(output_process) # adding input process object for upstream of current process
   
        if process_id not in [id for obj in object_list for id in dir(output_process.downstream_processes)]:
            output_process.downstream_processes.append(current_process) # adding current process object for downstream of input process
        
        process_list.append(output_process)
    return process_list



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