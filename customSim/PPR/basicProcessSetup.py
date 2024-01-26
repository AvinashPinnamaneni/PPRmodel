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

for domain in domains:
    domain.object_list = model_domain(env, domain, directory_path) # defines objects based on the attributes defined in the excel sheet
    # print(f'modelled {domain}')
    # print(f'The objects of the domain: {domain.__name__} are {domain.object_list}') # prints the objects created while the domains are modelled

object_list = Product.object_list + Process.object_list + Resource.object_list 


'''
- process_map is a nested list with processes modelled on main branch as object and sub-processes modelled as a dictionary with key as part of spine .
- Resources such as buffers can be added to peocess flow model, to which the upstream and downstream processes are generated during runtime.
- Process serves as a pivot connecting resources and products and hence processes are being simulated.
'''

# definition of process flow model
process_flow_model = {'proc_1':[['proc_2', 'proc_3', 'proc_4', 'proc_5', 'res_5'], ['proc_6', 'proc_7', 'proc_8', 'proc_9']] } # define the process model as a nested list

processes = map_processes(process_flow_model, object_list) # generates the upstream and downstream processes based on process flow model


# adding mapping data back to the excel sheet
for domain in domains:
    if domain.__name__ in ['Process', 'Resource']:
        file_path = os.path.join(directory_path, f'{domain.__name__}.xlsx')
        # print(object for object in domain.object_list)
        for object in domain.object_list:
            upstream_proc = []
            downstream_proc = []
            print(object.upstream_processes)
'''
            for process in object.upstream_processes:
                upstream_proc.append(process.name)
            for process in object.downstream_processes:
                downstream_proc.append(process.name)
            
            add_data_to_excel(file_path, 'id', object.id, 'upstream_processes', str(upstream_proc))
            add_data_to_excel(file_path, 'id', object.id, 'downstream_processes', str(downstream_proc))


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