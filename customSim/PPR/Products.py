# Importing packages
import pandas as pd
import sys

## Importing the path of current working directory
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory

from PPR.Functions import *

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
        upstream_processes = [], # functionality for nesting of processes to create a network is not modelled  
        downstream_processes = [],
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
        self.upstream_processes = upstream_processes if upstream_processes is not None else []
        self.downstream_processes = downstream_processes if downstream_processes is not None else []
        self.features = features
        self.skills = skills
        self.contents = contents if contents is not None else {}
        self.dimensions = dimensions
        self.specifications = specifications
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