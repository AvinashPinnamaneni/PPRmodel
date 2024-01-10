## Meeting for 04-01-2023:
### Progress of work:
- I have worked extensively in the exploration of Simantha package which turns out to be out of date and requires a lot of effort to customize the code for the present scenario.
- A package called Simpy turns out to be a more efficient solution for DES allowing for the modelling of PPR.
- I have modelled PPR classes following the paper which defined the architecture of PPR Domain and trying to model the current factory into the model
## Questions:
- The hierarchy of product domain follows as Product -> Variants -> Sub-Assemblies -> Components -> intermediate products(generated during different component states during processing) => each component can have different processing steps based on the product it is assigned to. Since I am following top down approach, how can I determine the processing step for a component considering the assigned product?
**Ans**: Don't complicate the structure as these operations could be explored in the further stages. Stick to minimum viable program to explain the structure.

## Meeting for 18-01-2023:
### Progress of work:
- Product class is meant to define overall output product of the system where as the intermediate products are defined as assemblies and components considering the reference which defines PPR in hierarchical model.
- 