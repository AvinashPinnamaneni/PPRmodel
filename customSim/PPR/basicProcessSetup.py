import ast
import simpy
import pandas as pd
import sys 
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim')

from PPR.PPRClasses import *
from PPR.Functions import *
import utils

env = simpy.Environment()


domains = get_classes(PPRClasses) # generating the domains which are defined as classes in PPRClasses
# print(f'The domains are: {domains}')

directory_path = '../customSim/LES/systemDefinition'

# importing data from excel formatted as {'object_id' : [[],[]]}
process_flow_model = make_process_flow_model(env, domains, directory_path)

print(process_flow_model)

object_list = Product.object_list + Process.object_list + Resource.object_list 


'''
- process_map is a nested list with processes modelled on main branch as object and sub-processes modelled as a dictionary with key as part of spine .
- Resources such as buffers can be added to peocess flow model, to which the upstream and downstream processes are generated during runtime.
- Process serves as a pivot connecting resources and products and hence processes are being simulated.
'''
'''
# process flow model generated from excel as it is the front end

processes = map_processes(process_flow_model, object_list) # generates the upstream and downstream processes based on process flow model




def simulate_factory(env, processes, orders):
    for order in orders:
        initiate_order(env, order)
        
    for process in processes:
        execute_process(process)
    
def execute_process(env, process):
    print(f'executing {process.id}')

def initiate_order(env, order):
    pass



env.process(simulate_factory(processes)) # 'Process' 'object' list is generated from the excel sheets
env.run(until = 10)
'''