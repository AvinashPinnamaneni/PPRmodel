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

# Modelling of process domain
# Hierarchy of product domain is "Product -> Variant -> Sub-Assemblies -> Components"
# definition of products
casing_mfg = Operation(env, 'casing_manufacturing', 'operation_1', [plate_cutting, plate_fitting, ports_fitting, seam_welding, circumferential_welding], {})


