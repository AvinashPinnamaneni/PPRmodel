from functions import *
# Product domain conceding the product information segregated into different hierarchical levels
# definition of a class for product family
# Heirarchy: Product -> Variant -> Assembly -> Component -> ComponentFeature
class Product:
    def __init__(self,
                 env,
                 name = 'product_name',
                 id = 'id',
                 previous_process = [],
                 next_process = [],
                 attributes = {}):

        self.name = name # name of the product
        self.id = id # id of the product
        self.previous_process = previous_process
        self.next_process = next_process
        self.attributes = attributes
        _create_attributes(self, attributes)

    def add_variants(self, variant):
        self.variants.append(variant)
    
    def define_processes(self, previous_steps =[], next_steps = []):
        self.previous_steps.append(previous_steps)
        self.next_steps.append(next_steps)

class IntermediateProducts():
   def __init(self, name = 'intermediate_product', id = 'intermediate_product', attributes = {}):
    self.name = name
    self.id = id
    _create_attributes(self, attributes)
'''            
# definition of class for product variant which is an extension of product object
class Variant:
    def __init__(self, 
                name = 'product_variant',
                variant_id = 'id',
                assemblies = {},
                attributes = {}):

        self.name = name
        self.assemblies = assemblies
        self.attributes = attributes
        _create_attributes(self, attributes)
        
    def add_assembly(self, assembly):
        self.assemblies.update(assembly)

    def add_dimensions(self, dimension):
        self.dimensions.update(dimension)
    

# definition of class for sub-assemblies
class Assembly:
    def __init__(self, 
                 id = 'id',
                 skills = [],
                 components = {},
                 operations = [],
                 attributes = {}):
        self.id = id
        self.skills = skills
        self.components = components
        self.attributes = attributes
        self.operations = operations
        _create_attributes(self, attributes)
        
    def add_component(self, component):
        self.components.update(component) 
        
    def add_skill(self, skill):
        self.skills.append(skill) 
 
# definition of class for the components where the specifications are customizable
class Component:
    def __init__(self, 
                name='assembly_component', 
                assembly_component_id = 'assembly_component_id',
                component_id = 'id',
                specifications = {},
                component_features = [],
                component_type = default,
                attributes = {}):

        self.name = name
        self.component_id = id
        self.assembly_component_id = assembly_component_id
        self.specifications = specifications
        self.component_features = component_features
        self.attributes = attributes
        self.component_type = component_type
        self.variants = []
        _create_attributes(self, attributes)

        if component_type == plate:
            self.cost = attributes['length'] *  attributes['width'] *  attributes['thick'] *  8 * 10^-6 * 0.7
        elif component_type == port:
            self.cost = 50 # improve the function for dynamic pricing based on the part number
        else:
            self.cost = 0
       
        
    def add_specification(self, specification):
        self.components.update(specification) 

    def add_component_feature(self, feature):
        self.component_features.append(feature)   

# Component feature class enables the further detailing of the component
# Current application do not demand the necessity of component feature and so, it is not used.

'''
