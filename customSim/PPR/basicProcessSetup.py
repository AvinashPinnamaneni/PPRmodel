import ast
import simpy
import pandas as pd
import sys 
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim')

from PPR.PPRClasses import *
from PPR.Functions import *
import utils

'''
- process_map is a nested list with processes modelled on main branch as object and sub-processes modelled as a dictionary with key as part of spine .
- Resources such as buffers can be added to peocess flow model, to which the upstream and downstream processes are generated during runtime.
- Process serves as a pivot connecting resources and products and hence processes are being simulated.
'''

directory_path = '../customSim/LES/systemDefinition'

env = simpy.Environment()

domains = get_classes(PPRClasses) # generating the domains which are defined as classes in upstream_process

process_flow_model = make_process_flow_model(env, domains, directory_path) # domains are being modelled when the processes are being mapped

object_list = Product.object_list + Process.object_list + Resource.object_list


processes = map_processes(process_flow_model, object_list) # generates the upstream and downstream processes based on process flow model and returns the list of processes

for domain in domains:
    if domain.__name__ in ['Process', 'Resource']:
        for obj in domain.object_list:
            # Filter out string objects from upstream_processes list
            upstream_processes = [process for process in obj.upstream_processes if not isinstance(process, str)]
            # Filter out string objects from downstream_processes list
            downstream_processes = [process for process in obj.downstream_processes if not isinstance(process, str)]
            # print(obj.name, upstream_processes, downstream_processes)




'''

def simulate_factory(env, processes, orders):
    for order in orders:
        # write code for getting th eproduct list and start processing of the product
        pass
        
    for process in processes:
        execute_process(process)
    
def execute_process(env, process):
    print(f'executing {process.id}')

def initiate_order(env, order):
    pass



env.process(simulate_factory(processes)) # 'Process' 'object' list is generated from the excel sheets
env.run(until = 10)

'''


