# Importing packages
import numpy as np
from PPR.Functions import *

## Importing the path of current working directory
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory

## importing local defined functions and domains
# from PPR.Processes import *
# from PPR.Products import *
# from PPR.Functions import *
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
 ## ------------definition of resource domain------------

class ManufacturingSystem:
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name',
                 cells = {},
                 **kwargs):

        self.env = env
        self.id = id
        self.name = name
        self.cells = cells if cells else []  # List to hold cells within the manufacturing system
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)

    def add_cell(self, cell):
        """Add a cell to the manufacturing system"""
        self.cells.append(cell)


class Cell:
    def __init__(self,
                 id = 'default_id',
                 name = 'default_name',
                 stations = {},
                 skills = [],
                 **kwargs):
        
        self.id = id
        self.name = name
        self.stations = stations if stations else []  # List to hold stations within the cell
        self.skills = skills if skills else []  # List to hold skills associated with the cell
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)

    def add_station(self, station):
        self.stations.append(station)


class Station:
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name',
                 machines = {},
                 skills = [],
                 **kwargs):
    
        self.env = env
        self.id = id
        self.name = name
        self.machines = machines
        self.skills = skills if skills else []  # List to hold skills associated with the station
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)


class Machine:
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name', 
                 capacity = float('inf'),
                 supplies = {},
                 consumables = {},
                 skills = [],
                 **kwargs):

        self.env = env
        self.id = id
        self.name = name
        self.capacity = capacity
        self.supplies = supplies
        self.consumables = consumables
        self.skills = skills if skills else []  # List to hold skills associated with the machine
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)

## Supplies includes fasteners, paint, welding electrodes etc. which are part of final product
class Supplies:
    def __init__(self,
                 id = 'default_id',
                 capacity = float('inf'),
                 material_nature = [], # a material can have multiple natures
                 **kwargs):

        self.env = env
        self.id = id
        self.capacity = capacity
        self.material_nature = material_nature  # Type of material nature the supply represents
        self.attributes = list(locals().keys())[1:]
        add_kwargs(self, **kwargs)

## Consumables includes resources which dries up such as compressed air, energy, welding gas etc. which are not part of final product
class Consumable:
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name', 
                 capacity = float('inf'),
                 material_nature = [],
                 **kwargs):
            
            self.env = env
            self.id = id
            self.name = name
            self.capacity = capacity
            self.material_nature = material_nature  # Type of material nature the supply represents
            self.attributes = list(locals().keys())[1:]
            add_kwargs(self, **kwargs)


