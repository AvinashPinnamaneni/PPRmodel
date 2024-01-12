# importing packages
import simpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

env = simpy.Environment()

product_directory_path = 'H:/My Drive/Thesis/Simulation/customSim/LES/systemDefinition/productDomain'
process_directory_path = 'H:/My Drive/Thesis/Simulation/customSim/LES/systemDefinition/processDomain'
resource_directory_path = 'H:/My Drive/Thesis/Simulation/customSim/LES/systemDefinition/resourceDomain'

# -------------Modelling the Product domain-------------
productClasses = get_classes(Products) # populating the classes available in the product domain

for product_class in productClasses:

    print()

    # dynamic filepath based on class
    file_path = os.path.join(product_directory_path, f'{product_class.__name__}.xlsx')

    if os.path.isfile(file_path):  # check for the availability of sheet
        print(f'excel file found for {product_class.__name__}')
        product_class_df = pd.read_excel(file_path)

        # Get the column headers from the DataFrame
        column_headers = product_class_df.columns.tolist()
        print(f'column headers are:{column_headers}')
        # getting the list of attributes defined in the class
        attribute_list = product_class(env).attributes
        print(f'attributes are:{attribute_list}')

        # iterate through each row of the dataframe
        for index, row in product_class_df.iterrows():

            # Create an instance of the class dynamically based on class name
            product_class_instance = product_class(env)

             # Iterate through each column of the DataFrame
            for col_name, value in row.items():

                # Check if the attribute exists in the class
                if hasattr(product_class_instance, col_name):

                    # Set the attribute value in the class instance
                    setattr(product_class_instance, col_name, value)

                else:

                    print(f"Warning: Attribute '{col_name}' does not exist in class '{product_class}'")

                    product_class_df.to_excel(file_path, index=False)
                    print(f"Updated Excel file saved with added columns.")
            
             # Do something with the product_class_instance, e.g., append it to a list or use it as needed
            print(f"Instance of {product_class}: {product_class_instance.__dict__}")

    else:
        print(f"Excel file not found for product class: {product_class} at {file_path}")
       
        
# -------------Modelling the Process domain-------------
processClasses = get_classes(Processes) # populating the classes available in the process domain
for process_class in processClasses:
    pass

# -------------Modelling the Resource domain-------------
resourceClasses = get_classes(Resources) # populating the classes available in the resource domain
for resource_class in resourceClasses:
    pass