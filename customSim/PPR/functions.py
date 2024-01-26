import ast
import simpy
import pandas as pd
import inspect
import os
import sys

# Importing the path of the current working directory
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim')

from PPR import PPRClasses
from PPR.PPRClasses import *
from PPR.Functions import *

def add_attribute(self, attribute):
    """Add attributes to an object during runtime."""
    if not isinstance(attribute, dict):
        raise ValueError("Attribute should be a dictionary")

    for key, value in attribute.items():
        setattr(self, key, value)
        self.attributes[key] = value 


def get_classes(library_module):
    """Return a list of classes available in the module."""
    classes = []
    for name, obj in inspect.getmembers(library_module):
        if inspect.isclass(obj):
            classes.append(obj)
    return classes


def get_attributes(class_type):
    """Get attributes of a class type."""
    attributes = class_type().attributes
    return attributes


def evaluate_cost(object):
    """Evaluate the cost based on the list of components being used in case of assemblies and products."""
    pass


def model_domain(env, domain, directory_path):
    """Model a domain and create instances of the object."""
    object_list = []
    file_path = f'{directory_path}/{domain.__name__}.xlsx'
    attribute_list = domain(env).attributes
    
    if os.path.isfile(file_path):
        class_df = pd.read_excel(file_path, usecols=lambda x: 'Unnamed' not in x)

        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            for attribute in attribute_list:
                if attribute not in class_df.columns:
                    new_column = pd.Series(name=attribute, dtype=object)
                    class_df = pd.concat((class_df, new_column), axis=1)

            class_df.to_excel(writer, sheet_name=f'{domain.__name__}', index=True)

        for index, row in class_df.iterrows():
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
        new_df = pd.DataFrame({})

        for attribute in attribute_list:
            new_df[f'{attribute}'] = []

        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            new_df.to_excel(writer, sheet_name=f'{domain.__name__}', index=True)

        print(f'Added the sheet: {domain.__name__}. Please update the sheet.')
    return object_list


def map_processes(process_flow_model, object_list):
    """Generate upstream and downstream processes for each process."""
    processes = []

    for process_id, network in process_flow_model.items():
        input_processes = network[0]
        output_processes = network[1]
        
        print(get_name_list(get_process_object(process_id, object_list).upstream_processes))
        upstream_processes = define_upstream(process_id, input_processes, object_list)
        print(get_name_list(get_process_object(process_id, object_list).upstream_processes))
        downstream_processes = define_downstream(process_id, output_processes, object_list)

        current_process = get_process_object(process_id, object_list)
        
        # Check if the current process is not already in the list before appending
        if current_process not in processes:
            processes.append(current_process)

    # Add upstream and downstream processes to the list
    processes = processes + upstream_processes + downstream_processes

    for process in processes:
        if process is not None:
            # Get lists of names for upstream and downstream processes
            upstream_processes = get_name_list(process.upstream_processes)
            downstream_processes = get_name_list(process.downstream_processes)
            # print(f'{process.name}: {upstream_processes}, {downstream_processes}')

        else:
            print("No production objects defined.")

# Function to get a list of names from a list of objects or strings
def get_name_list(list_of_objects):
    """Return a list of names from a list of objects or strings."""
    name_list = []
    for obj in list_of_objects:
        if hasattr(obj, 'name'):
            name_list.append(obj.name)
        else:
            name_list.append(str(obj))  # Convert non-object elements to string
    return name_list


def get_process_object(process_id, object_list):
    """Return the process object matching the given id."""
    return next((obj for obj in object_list if obj.id == process_id), None)


def define_upstream(process_id, input_processes, object_list):

    process_list = []
    current_process = get_process_object(process_id, object_list)
    
    if current_process is not None:

        for input_process_id in input_processes:
            input_process_object = get_process_object(input_process_id, object_list)

            if input_process_object is not None:
                if input_process_object not in current_process.upstream_processes:
                    current_process.upstream_processes.append(input_process_object)

                if current_process not in input_process_object.downstream_processes:
                    input_process_object.downstream_processes.append(current_process)


                process_list.append(input_process_object)
            else:
                print(f"Warning: Process with ID {input_process_id} not found in object_list")


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

def make_process_flow_model(env, domains, directory_path):
    process_flow_model = {} 
    # generating process flow model from
    for domain in domains:
        domain.object_list = model_domain(env, domain, directory_path) # defines objects based on the attributes defined in the excel sheet
        if domain.__name__ in ['Process', 'Resource']:
            for object in domain.object_list:
                upstream_process_list = []
                downstream_process_list = []
                for process in object.upstream_processes:
                    upstream_process_list.append(process)

                for process in object.downstream_processes:
                    downstream_process_list.append(process)


                process_map = {str(object.name) : [upstream_process_list, downstream_process_list]}
                process_flow_model.update(process_map)
    return process_flow_model