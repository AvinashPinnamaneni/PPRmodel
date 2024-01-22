import simpy
import pandas as pd
import sys 
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim')

from PPR.PPRClasses import *
from PPR.Functions import *

# definition of functions
def execute_process(env, process, input_products, resources):
    
    for input_product in input_products:
        input_product.container.get(1)

    for resource in resources:
        resource.container.get()


env = simpy.Environment()
    

# definition of products:

'''
- Product domain is defined in the increasing hierarchical level, where smaller parts and sub-assemblies are defined first, followed by main product or assembly.
- Container for a product is created if the product is an off the shelf component.
'''

nozzle_25 = Product(env, 'nozzle_25', '25nb_nozzle', 'fitting', 'standard_part', 'in_house', 0)
nozzle_40 = Product(env, 'nozzle_40', '40nb_nozzle', 'fitting', 'standard_part', 'in_house', 0)
nozzle_50 = Product(env, 'nozzle_50', '50nb_nozzle', 'fitting', 'standard_part', 'in_house', 0)
bottom_leg_100 = Product(env, 'bleg_100', '100nb_bottom_leg', 'fitting', 'standard_part', 'in_house', 0)
main_shell_1 = Product(env, '1kl_shell', '1kl_main_shell', 'tanks', 'sub_part', 'in_house', 0)
dish_1_1 = Product(env, '1kl_dish', '1kl_top_dish', 'tanks', 'sub_part', 'in_house', 0)
dish_1_2 = Product(env, '1kl_dish', '1kl_bottom_dish', 'tanks', 'sub_part', 'in_house', 0, contents={nozzle_25 : 2, nozzle_40 : 3, nozzle_50 : 4})
tank_1 = Product(env, '1kl_rcvr', '1kl_receiver', 'tanks', 'main_product', 'in_house', 0, contents={main_shell_1 : 2, dish_1_1 : 1, dish_1_2 : 1})


# definition of resources

# definition of processes



# making containers for a list of products