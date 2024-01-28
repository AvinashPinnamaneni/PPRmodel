- process states must be defined before and after the timeout function. 
    For example: the resource state must be set to occupied before timeout and active post timeout.

env.process(generator_function) will execute the specified generator function. This method will be prevalent in the definition of simulation methodology.

Normal predefined events can be processed in Environment, realtime simulations can be executed using RealtimeEnvironment

SimPy defines three categories of resources:
**Resources** – can be used by a limited number of processes at a time (e.g., a gas station with a limited number of fuel pumps).

**Containers** – model the production and consumption of a homogeneous, undifferentiated bulk. It may either be continuous (like water) or discrete (like apples).

**Stores** – allow the production and consumption of Python objects.

Skills essentially denotes the possibility of execution of a process using a resource on a given product. The possibility of execution is defined/validated in task which relates processes with skills.

### Python functions and methods to remember:
"globals()[variablenameinstring]" accesses the object through the variable name which equals to the string value

object.__class__.__name__ returns the name of the class


for making a product, call for the product and back trace the processes required for making the product, like if the output product of a process is know, get the information of input products and eventually backtrace the process to initial porocess and execute the process from beginning to order the compoents, parts and consumables.
Procedure for initiation of order:
- Order contains information about the list of products ordered along with other order related data. 
- The product list has to be acquired for each of the orders.
- Each of the product will have it's upstream and downstream process mapped through the upstream and downstream processes of the process and resource which specifies how we

Add an attribute of consumption of resources for the product as to what is actually planned and what is really happening.