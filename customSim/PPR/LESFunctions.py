# import local defined functions
from PPR.functions import *
from PPR.LESFunctions import *
from PPR.Products import *
from PPR.Processes import *
from PPR.Resources import *
from PPR.Collections import *

# importing packages
import simpy
import numpy as np
import matplotlib.pyplot as plt

# function for automated generation of assemblies and components for Heat Storage System HST_1
# function varies for different products and product configurations
# The sub assemblies necessary for the system are: Tub, Top plate, control, Core, Insulation
# total components is defined in the system definition as list
def create_assemblies(variants, total_components):
    for variant in variants:
        assemblies = {}
        variant_components = generate_components(components, variant)
        # creation of  tub sub-assembly
        assemblies[f'Tub_{variant.name}']  = Assembly(f'tub_{variant.id}', 
                                                        [seamWelding, plateFitting, multiAxialDrilling, laserCutting, portWelding],
                                                        variant_components['tub_components'], 
                                                        [])
        # creation of  top plate
        assemblies[f'top_plate_{variant.name}']  = Assembly(f'top_plate_{variant.id}', 
                                                        [plateFitting, multiAxialDrilling, laserCutting, portWelding],
                                                        variant_components['top_plate_components'], 
                                                        [])
        # creation of  top plate
        assemblies[f'control_{variant.name}']  = Assembly(f'top_plate_{variant.id}', 
                                                        [plateFitting, multiAxialDrilling, laserCutting, portWelding],
                                                        variant_components['control_components'], 
                                                        [])
        # creation of  top plate
        assemblies[f'core_insulation_{variant.name}']  = Assembly(f'top_plate_{variant.id}', 
                                                        [plateFitting, multiAxialDrilling, laserCutting, portWelding],
                                                        variant_components['core_insulation_components'], 
                                                        [])
        # creation of  top plate
        assemblies[f'external_fitting_{variant.name}']  = Assembly(f'top_plate_{variant.id}', 
                                                        [plateFitting, multiAxialDrilling, laserCutting, portWelding],
                                                        variant_components['external_fitting_components'], 
                                                        [])
        variant.assemblies.update(assemblies)

    return total_components

# function for the assignment or creation of components for assemblies
def generate_components(total_components, variant):
    variant_components = {}

    # declaration of tub components
    tub_components = {
    # naming format for casing plates: name_length1_length2_serialNumber : quantity
     f'side_plate_1_{variant.width}_{variant.height}': 1,
     f'side_plate_2_{variant.width}_{variant.height}': 1,
     f'face_plate_1_{variant.length}_{variant.height}': 1,
     f'face_plate_2_{variant.length}_{variant.height}': 1,
     f'bottom_plate_{variant.length}_{variant.width}': 1,
    # corner plates, naming convention => platePosition_plateLength : quanitity
    f'corner_plate_bottom_{variant.length}' : 1,
    f'corner_plate_bottom_{variant.width}' : 1,
    f'corner_plate_vertical_{variant.width}': 1,
    'corner_plate_top' : 1
    }
    
    # dictionary for top plate components
    top_plate_components = {
        f'top_plate_{variant.length}_{variant.width}' : 1,
        f'top_port' : 6
    }

    # dictionary for control components
    control_components = {
            f'control_{variant.name}' : 1, 
            # add sensors as necessary
    }

    # dictionary for core and insulation
    core_insulation_components = {
        f'top_plate_{variant.coreType}' : 1,
        f'heating_elements' : variant.heatingElements
    }

    # dictionary for external fitting components
    external_fitting_components = {
        # external components has to be populated in the later steps
    }

    # populating dictionary of all the components in the format => {subassy : {components:quantity}}
    variant_components['tub_components'] = tub_components
    variant_components['top_plate_components'] = top_plate_components
    variant_components['control_components'] = control_components
    variant_components['core_insulation_components'] = core_insulation_components
    variant_components['external_fitting_components'] = external_fitting_components
    

    # checking for the presence of component in component library(total_components)
    for sub_assembly in variant_components.iteritems():
        validate_component(total_components, sub_assembly, variant_components(sub_assembly), variant)

    return  variant_components

# function to check for the availability of components in the library, unavailability adds new components to the list.
# "variant_components" is a dictionary of a single sub assembly
def validate_component(total_components, sub_assembly, sub_assembly_components, variant):
    for index in sub_assembly_components.iteritems(): # index is the name or ID of the component
        component_id = index
        if index in total_components: # checking for the presence of component in components list
            print("Component record exists, adding current variant to variant list of component")
            
        else:
           variable_name = create_component(component_id, sub_assembly, variant)


    # Creating a dictionary
    variables = {}

    # Using a string as a key to store a value
    variable_name = "my_variable"
    variables[variable_name] = 10

# function for the creation of component
def create_component(sub_assembly, variant):
    if sub_assembly == 'tub_components':
        new_component = Component(f'')
        return new_component
    elif sub_assembly == 'top_plate_components':
        new_component = Component()
        return new_component
    elif sub_assembly == 'control_components':
        new_component = Component()
        return new_component
    elif sub_assembly == 'core_insulation_components':
        new_component = Component()
        return new_component
    elif sub_assembly == 'external_fitting_components':
        new_component = Component()
        return new_component
    else:
        return "unable to find name of sub-assembly, try modifying create_component function"