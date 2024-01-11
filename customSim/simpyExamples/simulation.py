import simpy 
import numpy as np
import utils

np.random.seed(0)

def factory_run(env, repairers, spares,costs, machine_list):
    for key, value in costs.items():
        setattr(self, key, value)
    cost = 0

    for machines in machine_list:
        env. process(operate_machine(env, repairers, spares, part))
    
    while True:
        cost += maintainers.repair * repair_time * maintainers + maintainers.purchase * spares_capacity
        yield env.timeout(utils.DAY)

## function for the operation of a machine
def operate_machine(env, repairers, spares, part):
    pass

## assignment of simpy method to a variable
env = simpy.Environment()

## Declaration of resources
maintainer = simpy.Resource(env, capacity = maintainers)

spares = simpy.Container(env, init = initial_spares, capacity = spares_capacity)

class maintainers:
    def __init__(self, name, ID, cost):
        self.name = name
        self.ID = ID
        for key, value in cost.items():
            setattr(self, key, value)

class part:
    def __init__(self, name, ID, dims):
        self.name = name
        self.ID = ID
        for key, value in dims.items():
            setattr(self, key, value)

class spares:
    def __init__ (self, name, ID, cost):
        self.name = name
        self.ID = ID
        self.cost = cost.get(ID)

class consumables:
    def __init__(self, name, ID, cost):
        self.name = name
        self.ID = ID
        self.cost = cost.get(ID)

## simulation of factory process
env.process(factory_run(env, repairers, spares))

env.run(until = WEEK)