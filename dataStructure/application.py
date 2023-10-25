"""
This module contains the Application class which represents a student's application
to a scholarship.
"""

class Application:
    """
    The Application class represents a student's application to a scholarship.
    TODO: convert the attributes to a dictionary set to allow for key lookups -- we'll assign each header a key value ( probably just its number in excel )
    """
    def __init__(self, application_id, student_id, scholarship_id):
        """
        Initializes a new instance of the Application class.

        :param application_id: A unique identifier for the application.
        :param student_id: The unique identifier of the student applying.
        :param scholarship_id: The unique identifier of the scholarship being applied to.
        """
        self.application_id = application_id
        self.student_id = student_id
        self.scholarship_id = scholarship_id
        self.attributes = set()

    def add_attribute(self, attribute):
        """
        Adds an attribute to the application.

        :param attribute: The attribute to add.
        """
        self.attributes.add(attribute)

    def remove_attribute(self, attribute):
        """
        Removes an attribute from the application.

        :param attribute: The attribute to remove.
        """
        self.attributes.discard(attribute)

    def search_attributes(self, attribute):
        """
        Searches for an attribute in the application.

        :param attribute: The attribute to search for.
        :return: True if the attribute is found, False otherwise.
        """
        return attribute in self.attributes
