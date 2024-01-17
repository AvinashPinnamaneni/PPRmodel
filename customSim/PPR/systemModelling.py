# importing packages
import simpy
import pandas as pd
import os
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim')

# import local defined functions 
from PPR import Products
from PPR import Processes
from PPR import Resources
from PPR.Functions import *
from PPR.Products import *
from PPR.Processes import *
from PPR.Resources import *

'''
Steps for modelling the domains:
- Step 1: Population of all the classes of the domain which can form objects
- Step 2: Generation of attributes defined in the class in the constructor function
- Step 3: check for the availability of a dataframe(df) for the definition of objects.
- Step 4: Create an object for each row of the dataframe.
- Step 5: Create an empty excel sheet if the required df is not available, with class attributes as columns.
- Step 6: Add new columns, if the df misses some attributes of the class.

Notes:
- By default, the dataframes are considered to be in .xlsx format. Please Check "file_path" variable in the domain to modify the file format.
- Please refer the datatypes of all the attributes before modelling the production system in the sheet.
- Validation of value for attributes is not modelled, which can be addded as extension in future versions.
- Additional attributes for the object can be given in kwargs which will be converted to attributes by a function.
'''

env = simpy.Environment()
# Specification of path for the directories of product, process and resources 
product_directory_path = '../customSim/LES/systemDefinition/productDomain'
process_directory_path = '../customSim/LES/systemDefinition/processDomain'
resource_directory_path = '../customSim/LES/systemDefinition/resourceDomain'

# -------------Modelling the Product domain-------------
productClasses = get_classes(Products) # generating classes available in the product domain

for product_class in productClasses: # iterating through each of the classes

    object_list = globals()[f'{product_class.__name__}_list'] = []

    file_path = os.path.join(product_directory_path, f'{product_class.__name__}.xlsx') # file path of excel sheet for the given class

    attribute_list = product_class(env).attributes # list of atributes of a class
    
    if os.path.isfile(file_path):  # if sheet exists at given path
        product_class_df = pd.read_excel(file_path) # import excel sheet as a pandas dataframe

        for attribute in attribute_list: # iterating through attributes of the class and add missing columns corresponding to attributes

            if attribute not in product_class_df.columns:

                product_class_df[f'{attribute}'] = [] # adding attributes as index in the dataframe

                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:  # Replacing the excel sheet with updated dataframe            
                    product_class_df.to_excel(writer, sheet_name=f'{product_class.__name__}', index=True)
        i = 1
        # Creating instances of the object
        for index, row in product_class_df.iterrows():
            # Create an instance of the class dynamically based on class name
            product_class_instance = globals()[f'product_class_instance{i}'] = product_class(env)  

            for col_name, value in row.items():  # Iterate through each column of the DataFrame 

                if hasattr(product_class_instance, col_name):  # Check if the attribute exists in the class

                    setattr(product_class_instance, col_name, value) # Set the attribute value in the class instance

                else:

                    print(f"Warning: Attribute '{col_name}' does not exist in class '{product_class}'")
    

            # Do something with the product_class_instance, e.g., append it to a list or use it as needed
            object_list.append(product_class_instance)

            print(f"Instance of {product_class}: {product_class_instance.__dict__}")
            i = i+1

    else:
        new_df = pd.DataFrame({})  # create an empty pandas dataframe
        
        for attribute in attribute_list:
                new_df[f'{attribute}'] = [] # adding attributes as index in the dataframe

                with pd.ExcelWriter(file_path, engine='openpyxl') as writer: # Replacing the excel sheet with updated dataframe 
                    new_df.to_excel(writer, sheet_name=f'{product_class.__name__}', index=True)

        print(f'added the sheet {product_class.__name__}. Please update the sheet for added functionality')

        
# -------------Modelling the Process domain-------------
            
processClasses = get_classes(Processes) # generating classes available in the product domain

for process_class in processClasses: # iterating through each of the classes

    object_list = globals()[f'{process_class.__name__}_list'] = []

    file_path = os.path.join(process_directory_path, f'{process_class.__name__}.xlsx') # file path of excel sheet for the given class

    attribute_list = process_class(env).attributes # list of atributes of a class
    
    if os.path.isfile(file_path):  # if sheet exists at given path
        process_class_df = pd.read_excel(file_path) # import excel sheet as a pandas dataframe

        for attribute in attribute_list: # iterating through attributes of the class and add missing columns corresponding to attributes

            if attribute not in process_class_df.columns:

                process_class_df[f'{attribute}'] = [] # adding attributes as index in the dataframe

                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:  # Replacing the excel sheet with updated dataframe            
                    process_class_df.to_excel(writer, sheet_name=f'{process_class.__name__}', index=True)

        # Creating instances of the object
        for index, row in process_class_df.iterrows():

            process_class_instance = process_class(env)  # Create an instance of the class dynamically based on class name

            for col_name, value in row.items():  # Iterate through each column of the DataFrame 

                if hasattr(process_class_instance, col_name):  # Check if the attribute exists in the class

                    setattr(process_class_instance, col_name, value) # Set the attribute value in the class instance

                else:

                    print(f"Warning: Attribute '{col_name}' does not exist in class '{process_class}'")
    

            # Do something with the process_class_instance, e.g., append it to a list or use it as needed
            object_list.append(process_class_instance)

            print(f"Instance of {process_class}: {process_class_instance.__dict__}")

    else:
        new_df = pd.DataFrame({})  # create an empty pandas dataframe
        
        for attribute in attribute_list:
                new_df[f'{attribute}'] = [] # adding attributes as index in the dataframe

                with pd.ExcelWriter(file_path, engine='openpyxl') as writer: # Replacing the excel sheet with updated dataframe 
                    new_df.to_excel(writer, sheet_name=f'{process_class.__name__}', index=True)

        print(f'added the sheet {process_class.__name__}. Please update the sheet for added functionality')


# -------------Modelling the Resource domain-------------
resourceClasses = get_classes(Resources) # populating the classes available in the resource domain

for resource_class in resourceClasses:
    object_list = globals()[f'{resource_class.__name__}_list'] = []

    file_path = os.path.join(resource_directory_path, f'{resource_class.__name__}.xlsx') # file path of excel sheet for the given class

    attribute_list = resource_class(env).attributes # list of atributes of a class
    
    if os.path.isfile(file_path):  # if sheet exists at given path
        resource_class_df = pd.read_excel(file_path) # import excel sheet as a pandas dataframe

        for attribute in attribute_list: # iterating through attributes of the class and add missing columns corresponding to attributes

            if attribute not in resource_class_df.columns:

                resource_class_df[f'{attribute}'] = [] # adding attributes as index in the dataframe

                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:  # Replacing the excel sheet with updated dataframe            
                    resource_class_df.to_excel(writer, sheet_name=f'{resource_class.__name__}', index=True)

        # Creating instances of the object
        for index, row in resource_class_df.iterrows():

            resource_class_instance = resource_class(env)  # Create an instance of the class dynamically based on class name

            for col_name, value in row.items():  # Iterate through each column of the DataFrame 

                if hasattr(resource_class_instance, col_name):  # Check if the attribute exists in the class

                    setattr(resource_class_instance, col_name, value) # Set the attribute value in the class instance

                else:

                    print(f"Warning: Attribute '{col_name}' does not exist in class '{resource_class}'")
    

            # Do something with the resource_class_instance, e.g., append it to a list or use it as needed
            object_list.append(resource_class_instance)

            print(f"Instance of {resource_class}: {resource_class_instance.__dict__}")

    else:
        new_df = pd.DataFrame({})  # create an empty pandas dataframe
        
        for attribute in attribute_list:
                new_df[f'{attribute}'] = [] # adding attributes as index in the dataframe

                with pd.ExcelWriter(file_path, engine='openpyxl') as writer: # Replacing the excel sheet with updated dataframe 
                    new_df.to_excel(writer, sheet_name=f'{resource_class.__name__}', index=True)

        print(f'added the sheet {resource_class.__name__}. Please update the sheet for added functionality')
