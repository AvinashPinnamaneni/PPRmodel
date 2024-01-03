The following project is meant for the simulation and optimization of a production system for the evaluation of multiple KPIs, 
used for multiple objective optimization.
The underlying concept of the model is based on the modelling philosophy of PPR concept where all the domains are connected 
using skills through liaisons with reference available under
## Domain classification:
### Product Domain
The Product domain interacts with the process domain  and resource domains through Operations and skills
The product domain is structured as "Product family -> Product variant -> Assembly -> Product component"
- Each Product variant is connected to process domain through a list of operations
- Each assembly is related to resource domain by skills through liaisons.
 
### Process Domain

### Resource Domain

## General notes:
- A table of task name(rows), product(columns) and processing time must be defined for different products and tasks has by the name "tbl_proc_time".
- Please note that the task name matching the task name list has to be provided for the table, else it returns an error.
