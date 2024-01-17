# importing packages
import sys
sys.path.insert(1, 'H:/My Drive/Thesis/Simulation/customSim')

# importing local libraries
from PPR.systemModelling import *
from PPR.Functions import *
from PPR.Products import *
from PPR.Processes import *
from PPR.Resources import *

env = simpy.Environment()

# Specification of path for the directories of product, process and resources 
product_directory_path = '../customSim/LES/systemDefinition/productDomain'
process_directory_path = '../customSim/LES/systemDefinition/processDomain'
resource_directory_path = '../customSim/LES/systemDefinition/resourceDomain'
