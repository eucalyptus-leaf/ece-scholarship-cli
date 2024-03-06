"""
This module contains the Student class which represents a student.
"""

# x = new(Student)
# x.first_name = "John"
class Student:
    """
    The Student class represents a student.
    """
    def __init__(self, fn="Empty", ln="Empty", mn="Empty", sid=-1, aid=-1, e="Empty", b=-1):
        """
        Initializes a new instance of the Student class.
        """
        self.first_name = fn
        self.middle_name = mn
        self.last_name = ln
        self.student_id = sid
        self.application_id = aid
        self.email = e
        self.budget = b
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
