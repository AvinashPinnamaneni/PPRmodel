The following work is a Masters thesis topic, implementing multi obkective optimization to enable cross domain consideration for decision making to stay inline with goal of the organization.
The production system is modelled using PPR concept which aligns well with RAMI 4.0 architecture enabling the production system adapt to the I 4.0 philosophy.

## Domain classification:
### Product Domain
The product domain is structured as "Product family -> Product variant -> Assembly -> Product component" an "Order" consists of variant ID through which the product family and list of sub-assemblies and components can be populated.
- The products are total output of a production system. The Assemblies and components can be considered as intermediate products.
- The components and assemblies has an attribute "order_id" which links them to the order they are reserved for during the manufacturing operation through processing steps can be defined.
- In house made components are considered as assemblies and outsourced components are considered as components, which requires no resources => they don't have upstream processes but will have downstream process.|
 
### Process Domain

### Resource Domain
- simpy resources are supplies and machines
- simpy containers are components and sub-assemblies 

## General notes:




## Important:
- By default, component cost is set to zero which has to be defined during the instantiation of component.