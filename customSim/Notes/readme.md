## Modelling and Discrete event simulation of a Production system
The current simulation framework is based on PPR design philosophy, where the discrete simulation is executed through the package called "Simpy". The production model is used for the optimnal selection of resources and machine sof a new production system whichcan bve extended further for different viewpoints, such as Optimization of production scheduling and Supply chain planning.

## introduction:
- Classification of domains as per Product/Process/Resource framework availabel under the link: https://doi.org/10.1016/j.cirpj.2018.01.001

## Programming structure:
- ** Refer _init_ method of the class for the structure and attributes of a class **
- Feel free to extend the class attributes, methods and other functionalities. 
- I have added **kwargs for all the classes which might make it flexible for the definition of additional attributes during instantiation of a class to make an object.
- Each of the objects has their methods defined in their respective classes. Please refer to the methods for functionality.

## Domain classification:
### Product Domain
**Structure:**
- The product domain is structured as "Product family -> Product variant -> Assembly -> Product component".
- An order is an aggregation of dicfferent product variants which can be maped to their respective product families through variant attribute(product_variant).
- The products are total output of a production system. The Assemblies and components can be considered as intermediate products.
- The components and assemblies has an attribute "order_id" which links them to the order they are reserved for during the manufacturing operation through processing steps can be defined.
- In house made components are considered as assemblies and outsourced components are considered as components, which requires no resources => they don't have upstream processes but will have downstream process.

#### Objects of product domain:
- **ProductFamily**: Contains information of the family of products.
- **Variant**: actual product which is an instance and exclusive to a product family.
- **Order**: Collection of different variants from different product families, usually from a customer.
- **Assembly**: Sub assembly of a given variant, which is an  aggregation of components.
- **Component**: A single part which forms an assembly. A part can have different processes for different product outputs.

 
### Process Domain
**Structure:**
- Process domain cosists of information pertaining to the processing steps of a product 

#### objects of process domain:
- **Operation**: Aggregation of processes. for example: preparation of casing, preparation of core etc.
- **Process**: Collection of tasks for the preparation of a product. for example: preparation casing welding, core forming etc.
- **Task**: indivudual processing steps, typically on the scale of a machine. for example: 


### Resource Domain
**Structure:**
- Resource domain 
- simpy resources are supplies and machines.
- simpy containers are components and sub-assemblies.

#### objects of Resource domain:
- **ManufacturingSystem**: Refers to a single factory.
- **Cell**: An ensemble consisting of several stations, collection of cells make a manufacturing system.
- **Station**: Collection of set of machines for the execution of certain operations.
- **Machine**: Lowest level of the manufacturing system, which takes in consumables and supplies for the execution of operations.
- **Supplies**: Items necessary for the manufacturing process but are not directly incorporated into the final product, such as filler wire, fasteners etc.
- **Consumables**: Items that are used up in the manufacturing process and are typically consumed or depleted with use, such as compressed air, machine repair consumables, machine maintenance effort etc.


## General notes:
- 

## Important notes:
- By default, component cost is set to zero which has to be defined during the instantiation of component.