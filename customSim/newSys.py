import simpy 
import numpy as np
import utils

np.random.seed(0)

## Declaration of environment variables
maintainers = 5 ## number of available maintainers in the company, considering each maintainer can execute one action
spares_capacity = 20  ## holding capacity of spares
initial_spares = 20  ## initial spares in hand before starting the process
repair_time = 3*utils.MIN ## generalized repair time

## Declaration of dimensions as dictionary
dims = {'length': 10 ,'width':10 , 'height':10 }

## Declaration of costs as dictionary
costs = {'spare':30 ,'machine':5000 , 'runnning':3000 , 'repair':50 , 'purchase':10 }

## Declaration of consumables as dictionary
consumables = {'filler':10 ,'gas':40 , 'spray':3 }

## Declaration of supplies as dictionary
supplies = {'compressed air':40 , 'energy':30 ,'heat':0 }