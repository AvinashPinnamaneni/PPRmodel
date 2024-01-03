# importing classes and functions defined for the environment
from Processes import *
from Products import *
from Resources import *
from functions import *
# importing supporting packages
import simpy
import numpy as np

# creating instances of Products
# need to define Product, Variant, Assembly, Component, ComponentFeature
P1 = Product('VHST', VHST_1, [V1, V2, V3], {'color':'Red'})
V1 = Variant('Small', V_1, {A1:2, A2:4, A3:5}, [OP1, OP2, OP5], {'Length': 1000, 'width': 500, 'height': 1500}, {'Stiffeners': True, 'CornerPlates': True})
V2 = Variant('Medium', V_2, {A1:2, A2:4, A3:5}, [OP1, OP2, OP5], {'Length': 1000, 'width': 500, 'height': 1500}, {'Stiffeners': True, 'CornerPlates': True})
V3 = Variant('Large', V_3, {A1:2, A2:4, A3:5}, [OP1, OP2, OP5], {'Length': 1000, 'width': 500, 'height': 1500}, {'Stiffeners': True, 'CornerPlates': True})
A1 = Assembly('Tub', [SeamWelding,tigWelding, Fitting], {C1:2, C2:2, C3:1})

# creating instances of Processes

# creating instances of Resources