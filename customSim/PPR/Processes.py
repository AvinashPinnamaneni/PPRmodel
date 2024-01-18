# importing packages
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory

from PPR.Functions import * 

'''
- Resources of Simpy are referred to as machines in a station which are limited in capacity or availability.
- Containers are referred to as a storage of components required for operations. 

- Maintenance operations can also be modelled as a process 

'''

# --------------Modelling of process domain--------------
# process domain consist of Operations -> processes -> tasks, with decreasing hierarchical level

class Process:
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name',
                 proc_time = 0, # time in secs
                 operating_cost = 0,
                 operators = 0, # quantity of number of operators required for the process
                 upstream_processes = [], 
                 downstream_processes = [], 
                 sub_processes = [], # list of sub-processes or processing steps
                 skills = [], 
                 input_products = {}, # components or sub-assemblies : qty
                 output_products = {}, # output sub-assemblies : qty
                 resources = {}, # resource name : consumption 
                 **kwargs
                 ):
        
        self.env = env
        self.id = id
        self.name = name
        self.proc_time = proc_time
        self.operating_cost = operating_cost
        self.operators = operators
        self.upstream_processes = upstream_processes
        self.downstream_processses = downstream_processes
        self.input_products = input_products
        self.output_products = output_products
        self.resources = resources
        self.sub_processes = sub_processes
        self.skills = skills
        self.resources = resources
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)


    def define_processes(self, upstream_processes, downstream_processes):  
        if upstream_processes:
            if isinstance(upstream_processes, list):  
              for process in upstream_processes:
                if process in self.upstream_processes:
                    print(f'{process} already exists in upstream process list')
              else:
                    self.upstream_processes.append(upstream_processes)
            else:
                raise TypeError("Invalid datatype for the upstream processes list, expected lists")
            
        if downstream_processes:
            if isinstance(downstream_processes, list):  
              for process in downstream_processes:
                if process in self.downstream_processes:
                    print(f'{process} already exists in upstream process list')
              else:
                    self.downstream_processes.append(downstream_processes)
            else:
                raise TypeError("Invalid datatype for the downstream processes list, expected lists")

    def add_sub_processes(self, add_sub_processes): # function to add tasks for the process during run time
        if isinstance(add_sub_processes, list):
            self.sub_processes.append(add_sub_processes)
        else:
            raise TypeError("Invalid datatype for the sub processes list, expected lists")
    
    def add_skill(self, skills):
            if isinstance(skills, list):
                for skill in skills:
                    if skill in self.skills:
                        print(f'{skill} already exists for the resource')
                    else:
                        self.skills.append(skill)
            else :
              raise TypeError("Invalid datatype for the skills list, expected lists")

    def add_products(self, input_products, output_products):
        if isinstance(input_products, list):    
            for product in input_products:
                if product in self.input_products:
                        print(f'{product} already defined in input products. Please modify the quantity in the master sheet')
                else:
                    self.input_products.append(product)
        else:
            raise TypeError("Invalid datatype for the input products list, expected lists")
        
        if isinstance(output_products, list):
            for product in output_products:
                if product in self.output_products:
                    print(f'{product} already defined in output products. Please modify the quantity in the master sheet')
                else:
                    self.output_products.append(product)
        else:
            raise TypeError("Invalid datatype for the output products list, expected lists")
    

    def add_resources(self, resources):
        if isinstance(resources, dict):
            for key, value in resources:
                if key in self.resources.keys(): # check if the specification already exists 
                    ValueError(f'{key} is already defined for the resource. Please change value in the resource definition sheet ')
                else:
                    self.resources[key] = value # updation of dictionary with additional dimensions being added
        else:
            raise TypeError("Invalid datatype for the resources, expected dictionary")
