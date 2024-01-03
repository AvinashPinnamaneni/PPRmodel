# import local defined functions
# from PPR.LESFunctions import *
from PPR.functions import *
from PPR.Products import *
from PPR.Processes import *
from PPR.Resources import *
from PPR.Collections import *

# importing packages
import simpy
import numpy as np
import matplotlib.pyplot as plt

# Modelling of product domain
# Hierarchy of product domain is "Product -> Variant -> Sub-Assemblies -> Components"
# definition of products
P1 = Product(env, 'HST', 'HST_1', [Intelli, Sharp, Savvy], {color: 'white'})

# Definition of variants
intelli = Variant('intelli',
                    HST_intelli,
                    {Casing_intelli : 1, Control_intelli : 1, Core_intelli : 1, Auxialaries_intelli : 1},
                    {} )

sharp = Variant('sharp',
                    HST_sharp,
                    {Casing_sharp : 1, Control_sharp: 1, Core_sharp : 1, Auxialaries_sharp : 1},
                    {} )

savvy = Variant('savvy',
                    HST_savvy,
                    {Casing_savvy : 1, Control_savvy: 1, Core_savvy : 1, Auxialaries_savvy : 1},
                    {} )

# Definition of skills for Sub-Assemblies:
casing_intelli_skills = ['plate_corner_fitting', 'corner_seam_welding', 'pipe_plate_welding', 'planar_plate_cutting', 'multi_axial_drilling']
casing_sharp_skills = ['plate_corner_fitting', 'corner_seam_welding', 'pipe_plate_welding', 'planar_plate_cutting', 'multi_axial_drilling']
casing_savvy_skills = ['plate_corner_fitting', 'corner_seam_welding', 'pipe_plate_welding', 'planar_plate_cutting', 'multi_axial_drilling']

Control_intelli_skills = []
Control_sharp_skills = []
Control_savvy_skills = []

Core_intelli_skills = []
Core_sharp_skills = []
Core_savvy_skills = []

Auxialaries_intelli_skills = []
Auxialaries_sharp_skills = []
Auxialaries_savvy_skills = []

# Definition of components for Sub-Assemblies:
casing_intelli_components={'front_plate_2350' : 1, 'back_plate_2350' : 1, 'side_left_plate_1500' : 1, 'side_right_plate_1500' : 1, 'bottom_plate_2350' :1, 'top_plate_2350' : 1, 'front_bottom_corner_plate_2350' : 2, 'side_bottom_corner_plate' : 2, 'vertical_corner_plate' : 4, 'corner_plate_closure' : 4, 'heating_elements_port' : 16, 'control_elements_port' : 1}
casing_sharp_components = {'front_plate_1850' : 1, 'back_plate_1850' : 1, 'side_left_plate_1500' : 1, 'side_right_plate_1500' : 1, 'bottom_plate_1850' :1, 'top_plate_1850' : 1, 'front_bottom_corner_plate_1850' : 2, 'side_bottom_corner_plate' : 2, 'vertical_corner_plate' : 4, 'corner_plate_closure' : 4, 'heating_elements_port' : 12, 'control_elements_port' : 1}
casing_savvy_components = {'front_plate_1350' : 1, 'back_plate_1350' : 1, 'side_left_plate_1500' : 1, 'side_right_plate_1500' : 1, 'bottom_plate_1350' :1, 'top_plate_1350' : 1, 'front_bottom_corner_plate_1350' : 2, 'side_bottom_corner_plate' : 2, 'vertical_corner_plate' : 4, 'corner_plate_closure' : 4, 'heating_elements_port' : 8, 'control_elements_port' : 1}

Control_intelli_components = {'intelli_control' : 1}
Control_sharp_components = {'sharp_control' : 1}
Control_savvy_components = {'savvy_control' : 1}

Core_intelli_components = {'heating_core' : 4}
Core_sharp_components = {'heating_core' : 3}
Core_savvy_components = {'heating_core' : 2}

Auxialaries_intelli_components = {'energy_source' : 1}
Auxialaries_sharp_components = {'energy_source' : 1}
Auxialaries_savvy_components = {'energy_source' : 1}

# Definition of operations for Sub-Assemblies:
casing_intelli_operations = []
casing_sharp_operations= []
casing_savvy_operations= []

Control_intelli_operations = []
Control_sharp_operations = []
Control_savvy_operations = []

Core_intelli_operations = []
Core_sharp_operations = []
Core_savvy_operations = []

Auxialaries_intelli_operations = []
Auxialaries_sharp_operations = []
Auxialaries_savvy_operations = []

# Definition of sub-assemblies : Casing, Control components, Core and Insulation, Auxialaries
Casing_intelli = Assembly('Casing_intelli', casing_intelli_skills, casing_intelli_components, casing_intelli_operations)
Casing_sharp = Assembly('Casing_sharp', casing_sharp_skills, casing_sharp_components, casing_sharp_operations)
Casing_savvy = Assembly('Casing_savvy', casing_savvy_skills, casing_savvy_components, casing_savvy_operations)

Control_intelli = Assembly('Control_intelli', Control_intelli_skills, Control_intelli_components, Control_intelli_operations)
Control_sharp = Assembly('Control_sharp',Control_sharp_skills, casing_sharp_components, Control_sharp_operations )
Control_savvy = Assembly('Control_savvy', Control_savvy_skills, Control_savvy_components, Control_savvy_operations)

Core_intelli = Assembly('Core_intelli', Core_intelli_skills, casing_intelli_components, Core_intelli_operations)
Core_sharp = Assembly('Core_sharp', Core_sharp_skills, Core_sharp_components, Core_sharp_operations)
Core_savvy = Assembly('Core_savvy', Core_savvy_skills, Core_savvy_components, Core_savvy_operations)

Auxialaries_intelli = Assembly('Auxialaries_intelli', Auxialaries_intelli_skills, Auxialaries_intelli_components, Auxialaries_intelli_operations)
Auxialaries_sharp = Assembly('Auxialaries_sharp', Auxialaries_sharp_skills, Auxialaries_sharp_operations, Auxialaries_sharp_operations)
Auxialaries_savvy = Assembly('Auxialaries_savvy', Auxialaries_savvy_skills, Auxialaries_savvy_components, Auxialaries_savvy_operations)

# definition of components:
total_components = [] # can be populated locally else populated by create_assemblies function

# -----------------Casing components-----------------
# The height and width of all the variants is considered to be 1500 by default
# Front plate:
front_plate_2350 = Component('front_plate_2350', 'fp_v1', {}, [], plate, {'length' : 2350, 'width' : 1500, 'thick' : 5})
front_plate_1850 = Component('front_plate_1850', 'fp_v2', {}, [], plate, {'length' : 1850, 'width' : 1500, 'thick' : 5})
front_plate_1350 = Component('front_plate_1350', 'fp_v3', {}, [], plate, {'length' : 1350, 'width' : 1500, 'thick' : 5})

# Back plate:
back_plate_2350 = Component('back_plate_2350', 'bp_v1', {}, [], plate, {'length' : 2350, 'width' : 1500, 'thick' : 5})
back_plate_1850 = Component('back_plate_1850', 'bp_v2', {}, [], plate, {'length' : 1850, 'width' : 1500, 'thick' : 5})
back_plate_1350 = Component('back_plate_1350', 'bp_v3', {}, [], plate, {'length' : 1350, 'width' : 1500, 'thick' : 5})

# Bottom plate:
bottom_plate_2350 = Component('bottom_plate_2350', 'btp_v1', {}, [], plate, {'length' : 2350, 'width' : 1500, 'thick' : 5})
bottom_plate_1850 = Component('bottom_plate_1850', 'btp_v2', {}, [], plate, {'length' : 1850, 'width' : 1500, 'thick' : 5})
bottom_plate_1350 = Component('bottom_plate_1350', 'btp_v3', {}, [], plate, {'length' : 1350, 'width' : 1500, 'thick' : 5})

# Top plate:
top_plate_2350 = Component('top_plate_2350', 'tp_v1', {}, [], plate, {'length' : 2350, 'width' : 1500, 'thick' : 5})
top_plate_1850 = Component('top_plate_1850', 'tp_v2', {}, [], plate, {'length' : 1850, 'width' : 1500, 'thick' : 5})
top_plate_1350 = Component('top_plate_1350', 'tp_v3', {}, [], plate, {'length' : 1350, 'width' : 1500, 'thick' : 5})

# side plates:
side_right_plate_1500 = Component('right_plate_1500', 'rp', {}, [], plate, {'length' : 1500, 'width' : 1500, 'thick' : 5})
side_left_plate_1500 = Component('left_plate_1500', 'lp', {}, [], plate, {'length' : 1500, 'width' : 1500, 'thick' : 5})

# Vertical corner plates
vertical_corner_plate = Component('corner_plate', 'cp', {}, [], plate, {'length' : 1500, 'width' : 250, 'thick' : 5})

# side bottom corner plate
side_bottom_corner_plate = Component('side_bottom_corner_plate', 'sbcp', {}, [], plate, {'length' : 1500, 'width' : 250, 'thick' : 5})

# Front and back bottom corner plates
front_bottom_corner_plate_2350 = Component('front_bottom_corner_plate_2350', 'fbcp_v1', {}, [], plate, {'length' : 2350, 'width' : 250, 'thick' : 5})
front_bottom_corner_plate_1850 = Component('front_bottom_corner_plate_1850', 'fbcp_v2', {}, [], plate, {'length' : 1850, 'width' : 250, 'thick' : 5})
front_bottom_corner_plate_1350 = Component('front_bottom_corner_plate_1350', 'fbcp_v3', {}, [], plate, {'length' : 1350, 'width' : 250, 'thick' : 5})

# Top corner plate closure
corner_plate_closure = Component('top_corner_plate', 'tcp', {}, [], plate, {'length' : 250, 'width' : 250, 'thick' : 5})

# definition of ports used for fitting control and heating elements
# vacuum_port = Component('vacuum_port', 'vp_1', {}, [fitting, out_sourced, welded])
heating_elements_port = Component('heating_elements_port', 'hep_1', {}, [], port, {'cost' : 120})
control_elements_port = Component('control_elements_port', 'cep_1', {}, [], port, {'cost' : 120})

# -----------------control components-----------------
intelli_control = Component('intelli_control', 'controller_1', {'input_power' : '5v, 2A'}, [electronics, processing_device, Iot_enabled])
sharp_control = Component('sharp_control', 'controller_2', {'input_power' : '5v, 2A'}, [electronics, processing_device, Iot_enabled])
savvy_control = Component('savvy_control', 'controller_3', {'input_power' : '5v, 2A'}, [electronics, processing_device, Iot_enabled])

# -----------------core components-----------------
heating_core = Component('heating_core', 'core_1', {'dimensions' : {'length' : 500, 'width' : 1250, 'height' : 1250}, 'heating_elements' : 4}, [outsourced, block, brittle] )

# -----------------Auxiliaries-----------------
energy_source = Component('energy_source', 'source_1', {'power_rating' : '5KW', 'voltage_rating' : '220V, AC'}, [renewable_energy])