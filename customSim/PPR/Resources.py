# Importing packages
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim') ## importing the path of current working directory

# Importing local functions
from PPR.Functions import *


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

class Resource:
    def __init__(self,
                 env,
                 id = 'default_id',
                 name = 'default_name',
                 type = 'default_type', # can be processing machine, material handling equipment, consumable etc.
                 material_nature = 'default_nature', # nature of material such as gases, metal, magnetic etc.
                 units = 'default_units', # units of measurement
                 cost_per_unit = 0,
                 capacity = float('inf'), # capacity of the resource
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
        self.capacity = capacity
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



