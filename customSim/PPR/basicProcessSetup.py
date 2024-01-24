import simpy
import pandas as pd
import sys 
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim')

from PPR.PPRClasses import *
from PPR.Functions import *
import utils

env = simpy.Environment()


domains = get_classes(PPRClasses) # generating the domains which are defined as classes in PPRClasses
print(f'The domains are: {domains}')


for domain in domains:
    domain.object_list = model_domain(env, domain) # defines objects based on the attributes defined in the excel sheet
    print(f'The objects of the domain: {domain} are {domain.object_list}') # prints the objects created while the domains are modelled

'''
- process_map is a nested list with processes modelled on main branch as object and sub-processes modelled as a dictionary with key as part of spine .
- Resources such as buffers can be added to peocess flow model, to which the upstream and downstream processes are generated during runtime.
'''

process_flow_model = ['proc_1', 'proc_2', 'proc_3', 'proc_4', 'proc_5', 'proc_6', 'proc_7', 'proc_8', 'proc_9'] # define the process model as a nested list

stations = define_process(process_flow_model) # generates the upstream and downstream processes based on process flow model


def simulate_factory(object_list): # executes all the processes defined in the process object list
    for station in object_list:
        execute_process(station)

def execute_process(processes):
    for process in processes:
        if isinstance(process, list):
            execute_process(process)
        else:
            # write program for the execution of actual process
            pass

env.process(simulate_factory(stations)) # Process object list is generated from the excel sheets
env.run(until = utils.YEAR)
