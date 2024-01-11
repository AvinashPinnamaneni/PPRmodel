# importing packages
import simpy # Package used for discrete simulation
import numpy as np # package used for computations 
import pandas as pd # Package used for data pre-processing
import matplotlib.pyplot as plt # package used for visualization of data
import os # for accessing windows directories

## Importing the path of current working directory
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory

# import local defined functions
import LESFunctions 
from PPR.Functions import *
from PPR import Products
from PPR import Processes
from PPR import Resources

product_directory_path = 'H:/My Drive/Thesis/Simulation/customSim/LES/systemDefinition/productDomain'
process_directory_path = 'H:/My Drive/Thesis/Simulation/customSim/LES/systemDefinition/processDomain'
resource_directory_path = 'H:/My Drive/Thesis/Simulation/customSim/LES/systemDefinition/resourceDomain'

# -------------Modelling the Product domain-------------
productClasses = get_classes(Products) # populating the classes available in the product domain

for product_class in productClasses:
    if os.path.isfile(os.path.join(product_directory_path, product_class + '.xlsx')):     # check if the excel sheet is available for each class

        # if the sheet is available, create objects from each of the rows of the sheet
        pass
    else:
        # creating new sheet, when the desired sheet is not available which is an excel file with attributes of the class as headers
        create_excel_sheet(product_class, product_directory_path + f'{product_class}.xlsx')
        


# -------------Modelling the Process domain-------------
processClasses = get_classes(Processes) # populating the classes available in the process domain
for process_class in processClasses:
    pass


# -------------Modelling the Resource domain-------------
resourceClasses = get_classes(Resources) # populating the classes available in the resource domain
for resource_class in resourceClasses:
    pass

env = simpy.Environment()