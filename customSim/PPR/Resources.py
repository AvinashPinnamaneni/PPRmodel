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

- The hierarchy of the resource domain is defined as Manufacturing System(factory) -> cells -> Stations -> Machines
'''
 

class ManufacturingSystem:
    def __init__(self, name, stations=[], attributes = {}):
        self.name = name
        self.stations = stations if stations else []
        self.attributes = attributes

    def add_station(self, station):
        self.stations.append(station)

class Cell:
    def _init_():
        pass

class Station:
    def __init__(self, name, resource_components=[], attributes = {}):
        self.name = name
        self.resource_components = resource_components if resources else []
        self.attributes = attributes

    def add_resource_component(self, resource):
        self.resources.append(resource)

class Skill:
    def __init__(self, name, attributes = {}):
        self.name = name       
        self.attributes = attributes