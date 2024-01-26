# Importing packages
import simpy
import pandas as pd
import sys

## Importing the path of current working directory
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory

from PPR.Functions import *
'''
- The domains classses are defined below which are Products, Processes and Resources. 
- Apart from these domains, we have additional suplement classes such as orders and skills(TBD) which are necessary for the modelling the functionality.
'''

# ____________ Product Domain ____________
'''
 The class hierarchy is structured as ProductFamily -> Variant and Product. Order is an aggregation of different product variants.
 Product refers to the overall product or output product of the system, and intermediate products are modelled as assemblies and components.
'''

class Product:
    def __init__(
        self,
        env,
        id = 'default-id',
        name= 'default_name',
        type = 'default_type', # could be product, sub-assembly, component etc.
        sourcing = 'inhouse', # could be in_house or out_sourced 
        cost = 0,
        features = [],
        skills = [],
        contents = {}, #  contents : qty, for assemblies, contents could be components
        dimensions = {},
        specifications = {}   
        ):

        self.env = env
        self.id = id
        self.name = name
        self.type = type
        self.sourcing = sourcing 
        self.cost = cost
        self.upstream_processes = []
        self.downstream_processes = []
        self.features = features
        self.skills = skills
        self.contents = contents if contents is not None else {}
        self.dimensions = dimensions
        self.specifications = specifications

        if self.type == 'component':
            self.container = simpy.Container(env, capacity = 5, init = 5)

        self.attributes = list(locals().keys())[1:]


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

    def add_feature(self, features):
        if isinstance(features, list):
            for feature in features:
                if feature in self.features:
                    print(f'{feature} already exists in the feature list')
                else:
                    self.features.append(feature)
        else:
            raise TypeError("expecting a list for the features")

    def add_skill(self, skills):
            if isinstance(skills, list):
                for skill in skills:
                    if skill in self.skills:
                        print(f'{skill} already exists for the resource')
                    else:
                        self.skills.append(skill)
            else :
              raise TypeError("Invalid datatype for the skills list, expected lists")
    
    def add_content(self, contents):
        if isinstance(contents, dict):
            for key, value in contents:
                if key in self.contents.keys(): # check if the part is already a part of the product
                    ValueError(f'{key} is already defined for the product. Please change the part count in the product definition sheet')
                else:
                    self.contents[key] = value # updation of dictionary with additional parts being added
        else:
            raise TypeError("Invalid datatype for the resources, expected dictionary")
                
    def add_dimension(self, dimensions):
        if isinstance(dimensions, dict):
            for key, value in dimensions:
                if key in self.dimensions.keys(): # check if the dimension already exists 
                    ValueError(f'{key} is already defined for the product. Please change this in the product definition sheet ')
                else:
                    self.dimensions[key] = value # updation of dictionary with additional dimensions being added
        else:
            raise TypeError("Invalid datatype for the resources, expected dictionary")

    def add_specification(self, specifications):
        if isinstance(specifications, dict):
            for key, value in specifications:
                if key in self.specifications.keys(): # check if the specification already exists 
                    ValueError(f'{key} is already defined for the product. Please change this in the product definition sheet ')
                else:
                    self.specifications[key] = value # updation of dictionary with additional dimensions being added
        else:
            raise TypeError("Invalid datatype for the resources, expected dictionary")


class Order:
    # Contains order data such as customer, variants ordered, qty, etc.
    def __init__(
        self,
        env,
        order_date= 'default_date',
        customer_name= 'default_name',
        order_id= 'default_id',
        product= {} # variant_name : qty
        ):

        self.env = env
        self.order_date = order_date  # Date of the order
        self.customer_name = customer_name  # Name of the customer
        self.order_id = order_id  # ID of the product
        self.product = product  # dictionary of the variants ordered
        self.attributes = list(locals().keys())[1:]

# ____________ Process domain ____________
'''
- Resources of Simpy are referred to as machines in a station which are limited in capacity or availability.
- Containers are referred to as a storage of components required for operations. 

- Maintenance operations can also be modelled as a process 

'''
# process domain consist of Operations -> processes -> tasks, with decreasing hierarchical level

class Process:
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name',
                 proc_time = 0, # time in secs
                 operating_cost = 0,
                 operators = 0, # quantity of number of operators required for the process
                 operating_status = False,
                 upstream_processes = [], 
                 downstream_processes = [], 
                 sub_processes = {}, # list of sub-processes or processing steps
                 skills = [], 
                 input_products = {}, # components or sub-assemblies : qty
                 output_products = {}, # output sub-assemblies : qty
                 resources = {} # resource name : consumption 
                 ):
        
        self.env = env
        self.id = id
        self.name = name
        self.proc_time = proc_time
        self.operating_cost = operating_cost
        self.operators = operators
        self.operating_status = operating_status
        self.upstream_processes = upstream_processes
        self.downstream_processes = downstream_processes
        self.input_products = input_products
        self.output_products = output_products
        self.resources = resources
        self.sub_processes = sub_processes
        self.skills = skills
        self.resources = resources
        self.attributes = list(locals().keys())[1:]


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

    def add_sub_processes(self, sub_processes): # function to add tasks for the process during run time
        if isinstance(sub_processes, dict):
            self.sub_processes.update(sub_processes)
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

# ____________ Resource domain ____________
        
'''
- resource domain defined in the paper is not adequate enough for clear explaination of resources. 
- Resources are classified based on flow of contents as:
    1. discrete - That which are measured in number of parts
    2. flow type - the measurement metrics depends on the material in use. typically units/sec. 
                 - To discretize the object flow, units/sec is considered for capacity definition and utilization

- Classification based on the utility:
    1. Fixed asset such as machines.
    2. Supplies such as energy, compressed air, gasess etc.
    3. Input parts required for the execution of proces such as fasteners, bearings, maintenance parts etc.

** Important**:
- Make sure to validate the avaialability of part in the resource before making a get_ request
- In case of definition of stations, machines are to be added as aggregates 
'''

class Resource:
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name',
                 type = 'default_type', # can be machine, supply etc.
                 units = 'default_units', # units of measurement
                 cost_per_unit = 0,
                 parts = {},
                 capacity = float('inf'),
                 holding_capacity = 1,
                 upstream_processes = [],
                 downstream_processes = [],
                 skills = [],
                 aggregates = {} # individual elements which on combination will form the resource
                 ):

        self.env = env
        self.id = id
        self.name = name
        self.type = type
        self.units = units
        self.cost_per_unit = cost_per_unit
        self.parts = parts
        self.capacity = capacity
        self.upstream_processes = upstream_processes
        self.downstream_processes = downstream_processes
        self.holding_capacity = holding_capacity, # part holding capacity
        self.skills = skills if skills else []  # List to hold skills associated with the cell
        self.aggregates = aggregates if aggregates else []  # List of sub-resources or machines
        self.attributes = list(locals().keys())[1:]
        self.add_resource()


    def add_skill(self, skills):
            if isinstance(skills, list):
                for skill in skills:
                    if skill in self.skills:
                        print(f'{skill} already exists for the resource')
                    else:
                        self.skills.append(skill)
            else :
              raise TypeError("Invalid datatype for the skills list, expected lists")

    def add_aggregate(self, aggregates): # add machines or resources to a station or resource
        if isinstance(aggregates, dict):
            for key, value in aggregates:
                if key in self.aggregates.keys(): # check if the dimension already exists 
                    ValueError(f'{key} is already defined for the product. Please change this in the product definition sheet ')
                else:
                    self.aggregates[key] = value # updation of dictionary with additional dimensions being added
        else:
            raise TypeError("Invalid datatype for the resources, expected dictionary")

    def add_resource(self):
        if self.type == 'supplies': # Assignment of containers and resources of simpy package
            self.resource = simpy.Resource(self.env, self.capacity)

        elif self.type == 'machine': # machine itself is a resource and it has capacity of holding resources 
            self.container = simpy.Container(self.env, self.holding_capacity, 0) # initially, the resource has no part in it  
            self.resource = simpy.Resource(self.env, self.capacity)
        else:
            self.container = simpy.Container(self.env, float('inf'), 0) # represents the cases such as buffers and part stores


    def put_part(self, part, qty): # id of the part should be passed as object to increment the parts in the resource 
        yield self.container.put(qty) # wiating for the space to be available
        if part.id in list(self.parts.keys()):
            self.parts[part.id] = self.parts[part.id] + qty 
        else:
            self.parts[part.id] = qty # adding a new part to the resource

    def get_part(self, part, qty):
        if self.container.level > qty:    # validation for availability of requested number of parts in the container
            if part.id in list(self.parts.keys()):
                self.parts[part.id] = self.parts[part.id] - qty
                yield self.container.get(qty)
                return True
            else:
                return False         
