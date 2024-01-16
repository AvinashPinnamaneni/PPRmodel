# Importing packages
import simpy
import numpy as np
import matplotlib.pyplot as plt
from PPR.Functions import *

## Importing the path of current working directory
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory

## importing the local defined functions
# from PPR.Processes import *
# from PPR.Resources import *

# This program defines a class hierarchy for managing product information at various hierarchical levels.
# The class hierarchy includes ProductFamily, Variant, Assembly, Component, and Order, representing different levels of product details.
# Product refers to the overall product or output product of the system, and intermediate products are assemblies and components.

class ProductFamily:
    # Product family the company produces
    def __init__(
        self,
        env,
        name = 'default_name',
        id = 'default_id',
        variants = [],
        **kwargs
        ):

        self.env = env
        self.name = name  # Name of the product
        self.id = id  # ID of the product
        self.variants = variants if variants is not None else []  # List of variants of the product family
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)

    def add_variant(self, variant):
        self.variants.append(variant)


class Variant:# Class for product variant, an extension of the product object
    def __init__(
        self,
        env,
        variant_id = 'default_id',
        name= 'default_name',
        product_family = 'default_product_family',  # Used for backtracing to the product family the variant belongs to
        skills = [], # list of necessary skills
        assemblies = {}, # assembly_name : qty
        **kwargs
        ):
        
        self.env = env
        self.name = name
        self.variant_id = variant_id
        self.product_family = product_family
        self.skills = skills if skills is not None else []
        self.assemblies = assemblies if assemblies is not None else {}
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)

    def add_assembly(self, assembly):
        self.assemblies.update(assembly)

    def add_dimensions(self, dimension):
        self.dimensions.update(dimension)


class Order:
    # Instance of a product variant ordered by the customer containing all the details of the order
    def __init__(
        self,
        env,
        order_date= 'default_date',
        name= 'default_name',
        order_id= 'default_id',
        variant= {}, # variant_name : qty
        **kwargs
        ):

        self.env = env
        self.order_date = order_date  # Date of the order
        self.name = name  # Name of the product
        self.order_id = order_id  # ID of the product
        self.variant = variant  # List of variants of the product family
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)


class Assembly:
    # Class for sub-assemblies
    def __init__(
        self,
        env,
        name= 'default_name',
        components = {}, #  component_name : qty
        upstream_processes = [], # functionality for nesting of processes to create a network is not modelled  
        downstream_processes = [],
        skills = [],
        **kwargs
        ):

        self.env = env
        self.name = name
        self.skills = skills
        self.components = components if components is not None else {}
        self.upstream_processes = upstream_processes if upstream_processes is not None else []
        self.downstream_processes = downstream_processes if downstream_processes is not None else []
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)

    def define_processes(self, upstream_processes=None, downstream_processes=None):
        if upstream_processes:
            self.upstream_processes.append(upstream_processes)
        if downstream_processes:
            self.downstream_processes.append(downstream_processes)

    def add_component(self, component):
        self.components.update(component)

    def add_skill(self, skill):
        self.skills.append(skill)


class Component:
    # Class for components where the specifications are customizable
    def __init__(
        self,
        env,
        name = 'default_name',
        component_id = 'default_id',
        downstream_processes = [], # since components are considered to be the initial parts, they will only have a downstream processes
        component_cost = 0,
        component_type = None, # component type might include: gas, part, liquid etc.
        **kwargs
        ):
        self.env = env
        self.name = name
        self.component_id = component_id
        self.downstream_processes = downstream_processes if downstream_processes is not None else []
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)

        if component_cost:
            self.component_cost = component_cost
        else:
            self.component_cost = evaluate_cost(self)
        self.component_type = component_type
        


    def define_processes(self, downstream_processes):
        for process in downstream_processes:
            self.downstream_processes.append(downstream_processes)

    def add_specification(self, specification):
        self.components.update(specification)

    def add_component_feature(self, feature):
        self.component_features.append(feature)
