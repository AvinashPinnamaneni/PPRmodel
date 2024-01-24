# Importing packages
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

# generates upstream and downstream processes as objects for processes using process flow model
def define_process(process_flow_model): # generate upstream and downstream processes based on process flow model
    stations = []
    for process_object in process_flow_model:
        if isinstance(process_object, dict):
            sub_processes = process_object[(list(process_object.keys())[0])] # returns the list of sub-processes
            define_process(sub_processes)
        else:
            process_object.upstream_processes = [previous_process]
            process_object.downstream_processes = [get_downstream(process_flow_model, process_object)]
        previous_process = next((proc_obj for proc_obj in process_flow_model if proc_obj.id==str(process_object)), None)
        stations.append(process_object)
    return stations
        
def get_downstream(process_flow_model, process):
    if isinstance(process_flow_model[process_flow_model.index(process) + 1], dict):
        return  next((proc_obj for proc_obj in process_flow_model if proc_obj.id==str(process_flow_model[process_flow_model.index(process) + 1].keys())), None)
    else:
        return next((proc_obj for proc_obj in process_flow_model if proc_obj.id==str(process_flow_model[process_flow_model.index(process) + 1])), None)

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