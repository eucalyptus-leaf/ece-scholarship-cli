# student.py

class Student:
    # Init variables that every student has but are different for each
    def __init__(self, firstName, lastName, ID):
        self.firstName = firstName
        self.lastName = lastName
        self.ID = ID
        self.attributes = set()

    # Student Methods
    def search_attributes(self, attribute):
        for n in self.attributes:
            if n in attribute:
                return True
        return False
    
    def add_attribute(self, attribute):
        self.attributes.append(attribute)
        return

    def delete_attribute(self, attribute):
        if attribute in self.attributes:
            self.attributes.discard(attribute)
            return True
        else: return False