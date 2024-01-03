# function to add attributes to an object during run time
def add_attribute(self, attribute):
    if not isinstance(attribute, dict):
        raise ValueError("Attribute should be a dictionary")

    for key, value in attributes.items():
        setattr(self, key, value)
        self.attributes[key] = value 

# definition of function for the creation of attributes from the dictionary for any given object
def _create_attributes(self, attributes):
    if not isinstance(attribute, dict):
        raise ValueError("Attribute should be a dictionary")

    for key, value in attributes.items():
        if self._is_valid_attribute(key, value):
            setattr(self, key, value)
            self.attributes[key] = value  # Update the attributes dictionary in the class
    