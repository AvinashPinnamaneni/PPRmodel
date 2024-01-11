# Importing packages
import simpy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import inspect

## Importing the path of current working directory
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory

# function to add attributes to an object during run time
def add_attribute(self, attribute):
    if not isinstance(attribute, dict):
        raise ValueError("Attribute should be a dictionary")

    for key, value in attributes.items():
        setattr(self, key, value)
        self.attributes[key] = value 


# definition of function for the creation of attributes from the dictionary for any given object
def _create_attributes(self, attributes):
    if not isinstance(attribute, dict):
        raise ValueError("Attribute should be a dictionary")

    for key, value in attributes.items():
        if self._is_valid_attribute(key, value):
            setattr(self, key, value)
            self.attributes[key] = value  # Update the attributes dictionary in the class
    

## processObject is the object to which the list is being updated and objectsList is the list of objects of lower hierarchical level
def update_resources(processObject, objectsList): # Updates the resources of the object bsaed on the objects of lower hierarchical level
    if isinstance(objectsList, list):
        for process in objectsList:
            processObject.resources.update(process.resources)
    elif not isinstance(objectsList, list) and not isinstance(objectsList, tuple) and not isinstance(objectsList, dict) and not isinstance(objectsList, set):
        processObject.resources.update(process.resources)
    else:
        raise TypeError("Invalid datatype for 'processes'. It should be a list or a single object.")


def update_supplies(processObject, objectsList):
    if isinstance(objectsList, list):
        for process in objectsList:
            processObject.supplies.update(process.resources)
    elif not isinstance(objectsList, list) and not isinstance(objectsList, tuple) and not isinstance(objectsList, dict) and not isinstance(objectsList, set):
        processObject.supplies.update(process.resources)
    else:
        raise TypeError("Invalid datatype for 'skills'. It should be a list or a single object.")


## Updating the skills based on the objects of lower hierarchy
def update_skills(processObject, objectsList):
    if isinstance(objectsList, list):
        for process in objectsList:
            processObject.skills.update(process.resources)
    elif not isinstance(objectsList, list) and not isinstance(objectsList, tuple) and not isinstance(objectsList, dict) and not isinstance(objectsList, set):
        processObject.skills.update(process.resources)
    else:
        raise TypeError("Invalid datatype for 'skills'. It should be a list or a single object.")

def add_kwargs(object, **kwargs):
    for key, value in kwargs.items():
        if hasattr(self, key): # Check if the attribute already exists
            raise ValueError(f"Attribute '{key}' already exists in the class.")
        else:  
            setattr(self, key, value) # Add the attribute to the object

def get_classes(library_module):  # function which returns the list of classes available in the module
    classes = []
    for name, obj in inspect.getmembers(library_module):
        if inspect.isclass(obj):
            classes.append(name)

    return classes

def get_class_attributes(class_instance): # Function which returns attributes of a class
    class_attributes = {}
    class_signature = inspect.signature(class_instance.__init__)

    for parameter_name, parameter in class_signature.parameters.items():
        if parameter_name != 'self':  # Exclude the 'self' parameter
            class_attributes[parameter_name] = parameter.default

    return class_attributes

def create_excel_sheet(class_instance, file_path):
    # populating non callable attributes of the class instance passed
    attributes = [attr for attr in dir(class_instance) if not callable(getattr(class_instance, attr)) and not attr.startswith("__")]

    # Create an empty DataFrame with attribute names as columns
    df = pd.DataFrame(columns=attributes)

    # Write DataFrame to Excel file
    df.to_excel(file_path, index=False)
    print(f"Excel sheet '{file_path}' created successfully.")
