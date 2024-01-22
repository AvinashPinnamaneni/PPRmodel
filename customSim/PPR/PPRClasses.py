# Importing packages
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
        product_family = 'default_product_family',  # Used for backtracing to the product family the variant belongs to
        type = 'default_type', # could be product, sub-assembly, component etc.
        sourcing = 'inhouse', # could be in_house or out_sourced 
        cost = 0,
        features = [],
        skills = [],
        contents = {}, #  contents : qty, for assemblies, contents could be components
        dimensions = {},
        specifications = {},
        **kwargs
        ):

        self.env = env
        self.id = id
        self.name = name
        self.product_family = product_family
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
        if self.type == 'standard_part':
            self.container = make_container(env, self)
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
        product= {}, # variant_name : qty
        **kwargs
        ):

        self.env = env
        self.order_date = order_date  # Date of the order
        self.customer_name = customer_name  # Name of the customer
        self.order_id = order_id  # ID of the product
        self.product = product  # dictionary of the variants ordered
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)


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
        self.operating_status = operating_status
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

# ____________ Resource domain ____________
        
'''
- resource domain defined in the paper is not adequate enough for clear explaination of resources. 
- Resources are classified based on flow of contents as:
    1. discrete - That which are measured in number of parts
    2. flow type - the measurement metrics depends on the material in use. typically lts/min or kgs/min etc., to generalize the current use case, we are considering units/min
        The units of measurement can be integers or float depending on the context.
- Classification based on the utility:
    1. Fixed asset such as machines.
    2. Supplies such as energy, compressed air, gasess etc.
    3. Input parts required for the execution of proces such as fasteners, bearings, maintenance parts etc.

Supplies are part of the final product but are not directly involved, such as welding filler wire, 
Consumables are not part of final product but have influences on the integration of the product, such as packaging material, machining tool, welding gas, compressed air

- The hierarchy of the resource domain is defined as Manufacturing System(factory) -> cells -> Stations -> Machines
'''

class Resource:
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name',
                 type = 'default_type', # can be processing machine, material handling equipment, consumable etc.
                 material_nature = 'default_nature', # nature of material such as gases, metal, magnetic etc.
                 units = 'default_units', # units of measurement
                 cost_per_unit = 0,
                 availability = True,
                 staged_products = {},
                 capacity = float('inf'), # capacity of the resource
                 container = object, 

                 skills = [],
                 aggregates = {}, # individual elements which on combination will form the resource
                 **kwargs):

        self.env = env
        self.id = id
        self.name = name
        self.type = type
        self.material_nature = material_nature
        self.units = units
        self.cost_per_unit = cost_per_unit
        self.availability = availability # is set dynamically during the execution of process
        self.staged_products = staged_products
        self.capacity = capacity
        self.container = container
        self.skills = skills if skills else []  # List to hold skills associated with the cell
        self.aggregates = aggregates if aggregates else []  # List to hold cells within the manufacturing system
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)


    def add_skill(self, skills):
            if isinstance(skills, list):
                for skill in skills:
                    if skill in self.skills:
                        print(f'{skill} already exists for the resource')
                    else:
                        self.skills.append(skill)
            else :
              raise TypeError("Invalid datatype for the skills list, expected lists")

    def add_aggregate(self, aggregates):
        if isinstance(aggregates, dict):
            for key, value in aggregates:
                if key in self.aggregates.keys(): # check if the dimension already exists 
                    ValueError(f'{key} is already defined for the product. Please change this in the product definition sheet ')
                else:
                    self.aggregates[key] = value # updation of dictionary with additional dimensions being added
        else:
            raise TypeError("Invalid datatype for the resources, expected dictionary")



