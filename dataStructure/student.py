"""
This module contains the Student class which represents a student.
"""

# x = new(Student)
# x.first_name = "John"
class Student:
    """
    The Student class represents a student.
    """
    def __init__(self, first_name, last_name, student_id):
        """
        Initializes a new instance of the Student class.

        :param first_name: The first name of the student.
        :param last_name: The last name of the student.
        :param student_id: The unique identifier of the student.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.attributes = set()
        self.applications = {}

    def add_attribute(self, attribute):
        """
        Adds an attribute to the student.

        :param attribute: The attribute to add.
        """
        self.attributes.add(attribute)

    def remove_attribute(self, attribute):
        """
        Removes an attribute from the student.

        :param attribute: The attribute to remove.
        """
        self.attributes.discard(attribute)

    def search_attributes(self, attribute):
        """
        Searches for an attribute in the student's attributes.

        :param attribute: The attribute to search for.
        :return: True if the attribute is found, False otherwise.
        """
        return attribute in self.attributes

    def add_application(self, application):
        """
        Adds an application to the student's applications.

        :param application: The application to add.
        """
        self.applications[application.scholarship_id] = application

    def remove_application(self, scholarship_id):
        """
        Removes an application from the student's applications.

        :param scholarship_id: The unique identifier of the scholarship being applied to.
        """
        if scholarship_id in self.applications:
            del self.applications[scholarship_id]

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.student_id})'
    