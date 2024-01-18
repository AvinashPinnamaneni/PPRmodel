All the domaains are modelled in PPR folder
## Domains:  
    Product Domain, Process domain, Resource domain

### Domain Structure:
    Domains:
        Classes:
            Attributes : data type 
            Methods (arguments)



1. ________Product domain________
     ProductFamily:
        self
        env
        name : string
        id : string
        variants : list
        
        add_variant(self, variant)

     Variant:
        self
        env
        variant_id : string
        name : string
        product_family : string
        skills : list
        assemblies : dictionary {assembly : qty}

        add_assembly(self, assembly)
        add_dimensions(self, dimension)

     Order:
        self
        env
        order_date : string
        name : string
        order_id : string
        variant : list

     Assembly:
        self
        env
        name : string
        components : dictionary {component : qty}
        upstream_processes : list
        downstream_processes : list
        skills : list
        dimensions : dictionary {dimension : value}

        define_processes(self, upstream_processes, downstream_processes)
        add_component(self, component)
        add_skill(self, skill)

     Component:
        self
        env
        name : string
        component_id : string
        downstream_processes : list
        component_cost : int
        component_type : string

        define_processes(self, downstream_processes)
        add_specification(self, specification)
        add_component_feature(self, feature)

2. ________Process domain________
     Operation:
        self
        env
        id : string
        name : string
        stations : list
        upstream_operations : list 
        downstream_operations : list
        input_products : dict {product_id: qty}
        output_products : dict {product_id: qty}
        resources : dict {resource_id : qty}
        processes : list
        skills : list
        supplies : dict {supply : qty}

     Process:
         self
         env
         id : string
         name : string
         upstream_operations : list
         downstream_operations : list
         input_products : dict {product_id: qty}
         output_products : dict {product_id: qty}
         resources : dict {resource_id: qty}
         supplies : dict {supply_id : qty}
         tasks : list
         skills : list

         add_tasks(self, tasks) => tasks is a list
     
     Task:
         self
         env
         id : string
         name : string
         resources : dict {resource_id : qty}
         skills : list
         stations : list
         consumables : dict {consumable_id : qty}
         supplies : dict {supply_id : qty}
         proc_time : string


3. ________Resource domain________
     ManufacturingSystem:
        self
        env
        id : string
        name : string
        cells : dict {cell_id : qty}

        add_cell(self, cell)
    
     Cell:
        self
        id
        name  : string
        stations : dict {station_id : qty}
        skills : list

        add_station(self, station)
     
      Machine:
        self
        env
        id : string
        name : string
        capacity : int
        supplies : dict {supply_id : qty}
        consumables : dict {consumable_id : qty}
        skills : list
     
     Supplies: 
        self
        env
        id : string
        capacity : int
        material_nature : list

     Consumable:
        self
        env
        id : string
        name : string
        capacity : int
        material_nature : list

### Functions:
    add_attribute(self, attribute)
    update_resources(processObject, objectsList)
    update_supplies(processObject, objectsList)
    update_skills(processObject, objectsList)
    add_kwargs(object, **kwargs) -- This function is being called for every init method of the class, to add kwargs as attributes for a class
    get_classes(library_module)
    get_attributes(class_type)
    evaluate_cost(object)

