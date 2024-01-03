import numpy as np
from functions import *
# Process domain conceding the process information segregated into different hierarchical levels(operation -> Process -> Task)
# Validation of skills has to be done here
# definition of a class of operation

class Operation():
    def __init__(self, env, name = 'operation', id = 'id', processes = [], attributes = {}):
        self.name = name
        self.id = id
        self.processes = processes
        self.attributes = attributes
        _create_attributes(self, attributes)

        # definition of network of operations
        self.input_operations = []
        self.next_operations = []

    # operation is an aggregation of processes
    def add_process(self, process):
        self.processes.append(process)
    
    def execute_operation(self, env, processes):
        for process in processes:
           process.execute_process(self, env)
    
    def add_input_operations(self, Operation):
        self.input_operations.append(Operation)

    def add_next_operations(self, Operation):
        self.next_operations.append(Operation)

class Process():
    def __init__(self, name='process', resources={}, tasks = [], attributes = {}):
        self.name = name
        self.resources = resources
        self.tasks = tasks
        self.input_products = {}
        self.output_products = {}
        self.input_processes = []
        # Next processes depends on the product the process contains
        self.next_processes = []
        # create attributes from the attribute list passed initially
        self.attributes = attributes
        _create_attributes(self, attributes)
    
    def add_input_process(self, process):
        self.input_processes.append(process)

    def add_next_process(self, process):
        self.next_processes.append(process)

    def add_task(self, task):
        self.tasks.append(task)
        
    def add_resource(self,resource):
        self.resources.update(resource)
    
    def execute_process(self, env, tasks):
        for task in tasks:
           task.execute_task(self, env)

class Task():
    def __init__(self, env, name = 'task', id = 'id', skills = [], attributes = {}, input_product = []):
        self.name = name
        self.id = id    
        self.skills = skills
        self.attributes = attributes
        self.input_product = input_product
        # The object only accepts the processing time pre-calculated. 
        # Which means, functions must be defined during the modelling of production system populating the times automatically
        self.task_time = env.tbl_proc_time(self.name, product)

        _create_attributes(self, attributes)

        
    def add_skill(self, skill):
        self.skills.append(skill)
    
    def execute_task(self, env):
           yield env.timeout(task_time)