class ManufacturingSystem:
    def __init__(self, name, stations=[], attributes = {}):
        self.name = name
        self.stations = stations if stations else []
        self.attributes = attributes

    def add_station(self, station):
        self.stations.append(station)

class Station:
    def __init__(self, name, resource_components=[], attributes = {}):
        self.name = name
        self.resource_components = resource_components if resources else []
        self.attributes = attributes

    def add_resource_component(self, resource):
        self.resources.append(resource)


class ResourceComponent:
    def __init__(self, name, resource_type, capabilities=[], attributes = {}):
        self.name = name
        self.resource_type = resource_type
        self.capabilities = capabilities if capabilities else []
        self.attributes = attributes


    def add_capability(self, capability):
        self.capabilities.append(capability)


class NonControlComponent:
    def __init__(self, name, attributes = {}):
        self.name = name
        self.attributes = attributes



class ProcessComponent:
    def __init__(self, name, attributes = {}):
        self.name = name
        self.attributes = attributes



class Sensor:
    def __init__(self, name, sensor_type, attributes = {}):
        self.name = name
        self.sensor_type = sensor_type
        self.attributes = attributes



class ControlComponent:
    def __init__(self, name, control_type, attributes = {}):
        self.name = name
        self.control_type = control_type
        self.attributes = attributes



class Skill:
    def __init__(self, name, attributes = {}):
        self.name = name       
        self.attributes = attributes



class State:
    def __init__(self, name, attributes = {}):
        self.name = name
        self.attributes = attributes


class ElementType:
    def __init__(self, name, attributes = {}):
        self.name = name
        self.attributes = attributes