## Progress of work:
- I have worked extensively in the exploration of Simantha package which turns out to be out of date and requires a lot of effort to customize the code for the present scenario.
- A package called Simpy turns out to be a more efficient solution for DES allowing for the modelling of PPR.
- I have modelled PPR classes following the paper which defined the architecture of PPR Domain and trying to model the current factory into the model
## Questions:
- To whch class should I assign the parts coming out of the store? "Resources" or "Products". For example: fasteners, fittings etc.
- The hierarchy of product domain follows as Product -> Variants -> Sub-Assemblies -> Components -> intermediate products(generated during different component states during processing) => each component can have different processing teps based on the product it is assigned to. Since I am following top down approach, how can I determine the processing step for a component considering the assigned product?