# importing packages
import simpy
import numpy as np
import matplotlib.pyplot as plt
from PPR.Functions import * 

## Importing the path of current working directory
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory

# import local defined functions
# from PPR.LESFunctions import *
# from PPR.Functions import *
# from PPR.Products import *
# from PPR.Resources import *


'''
- Resources of Simpy are referred to as machines in a station which are limited in capacity or availability.
- Containers are referred to as a storage of components required for operations. 

- Maintenance operations can also be modelled as a process 

'''

# --------------Modelling of process domain--------------
# process domain consist of Operations -> processes -> tasks, with decreasing hierarchical level

class Operation: # Operation is a collection of processes => Collection of stations
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name',
                 stations = [], 
                 upstream_operations = [], 
                 downstream_operations = [], 
                 input_products = {}, # components or sub-assemblies : qty
                 output_products = {}, # output sub-assemblies : qty
                 resources = {}, # resource name : consumption 
                 processes = [], # list of possible processes in the operation 
                 skills = [], 
                 supplies = {}, # Supplies : qty
                 **kwargs
                 ):
        
        self.env = env
        self.id = id
        self.name = name
        self.stations = stations
        self.upstream_operations = upstream_operations
        self.downstream_operations = downstream_operations
        self.input_products = input_products
        self.output_products = output_products
        self.resources = resources
        self.processes = processes
        self.skills = skills
        self.supplies = supplies
        self.attributes = list(locals().keys())[1:]

        add_kwargs(self, **kwargs)
        update_supplies(self, processes)
        update_resources(self, processes)
        update_skills(self, processes)


class Process: # process is a collection of tasks => usually involves multiple machines of a single station
    def __init__(self,
                 env, 
                 id = 'default_id',
                 name = 'default_name', 
                 upstream_operations = [], 
                 downstream_operations = [], 
                 input_products = {}, # input products are components and sub-assemblies which are simpy containers
                 output_products = {}, # output products are definitely sub-assemblies as the components undergo inhouse processing
                 resources = {}, # resources could be machines and supplies which are simpy resources
                 supplies = {},
                 tasks = [], 
                 skills = [],
                 **kwargs
                 ):
            
        self.env = env
        self.id = id
        self.name = name
        self.upstream_operations = upstream_operations
        self.downstream_operations = downstream_operations
        self.input_products = input_products
        self.output_products = output_products
        self.resources = resources
        self.tasks = tasks 
        self.skills = skills
        self.supplies = supplies
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)
        update_supplies(self, tasks)
        update_resources(self, tasks)
        update_skills(self, tasks)
    
    def update_tasks(self, tasks): # function to add tasks for the process during run time
        if isinstance(tasks, list):
            self.tasks.append(tasks)
        else:
            raise TypeError("Invalid datatype for the tasks list, expected lists")


class Task: # task is a sequence of steps to do for execution of a process => usually done by a single machine
    def __init__(self, 
                env, 
                id = 'default_id', 
                name = 'default_name', 
                resources = {},       # The machines necessary for the execution of task.
                skills = [],
                stations = [],
                consumables = {}, # consumable name : qty 
                supplies = {}, # supplies : qty
                proc_time = 0,
                **kwargs
                ):
                
        self.env = env
        self.id = id 
        self.name= name
        self.stations = stations
        self.skills = skills
        self.consumables = consumables
        self.supplies = supplies
        self.resources = resources     
        self.supplies = supplies
        self.proc_time = proc_time
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)
