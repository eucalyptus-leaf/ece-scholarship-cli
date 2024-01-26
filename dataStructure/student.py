"""
This module contains the Student class which represents a student.
"""

# x = new(Student)
# x.first_name = "John"
class Student:
    """
    The Student class represents a student.
    """
    def __init__(self):
        """
        Initializes a new instance of the Student class.

        :param first_name: The first name of the student.
        :param last_name: The last name of the student.
        :param student_id: The unique identifier of the student.
        """
        self.first_name = "Empty"
        self.last_name = "Empty"
        self.student_id = -1
        self.application_id = -1
        self.email = "Empty"
        self.budget = -1
        self.attributes = dict()

    def add_attribute(self, attribute):
        """
        Adds an attribute to the student.

        :param attribute: The attribute to add.
        """
        self.attributes.update(attribute)

    def remove_attribute(self, attribute):
        """
        Removes an attribute from the student.

        :param attribute: The attribute to remove.
        """
        self.attributes.update(attribute)

    def search_attributes(self, attribute):
        """
        Searches for an attribute in the student's attributes.

        :param attribute: The attribute to search for.
        :return: True if the attribute is found, False otherwise.
        """
        return attribute in self.attributes

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.student_id})'
    