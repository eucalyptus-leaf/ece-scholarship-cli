"""
This module contains the Student class which represents a student.
"""

# x = new(Student)
# x.first_name = "John"
class Student:
    """
    The Student class represents a student.
    """
    def __init__(self, first_name="Empty", last_name="Empty", student_id=-1, application_id=-1, email="Empty", budget=-1):
        """
        Initializes a new instance of the Student class.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.application_id = application_id
        self.email = email
        self.budget = budget
        self.attributes = dict()

    def add_attribute(self, key, value):
        """
        Adds an attribute to the student.
        """
        self.attributes[key] = value

    def remove_attribute(self, key):
        """
        Removes an attribute from the student.
        """
        self.attributes.pop(key, None)

    def search_attributes(self, key):
        """
        Searches for an attribute key in the student's attributes.
        """
        return key in self.attributes

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.student_id})({self.budget})'
