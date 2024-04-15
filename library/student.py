from library.budget_system import StudentBudget

"""
This module contains the Student class which represents a student.
"""

# x = new(Student)
# x.first_name = "John"
class Student:
    """
    The Student class represents a student.
    """
    def __init__(self, headers, budget, fn="Empty", ln="Empty", mn="Empty", sid=0, aid=0, e="Empty"):
        """
        Initializes a new instance of the Student class.
        """
        self._headers = headers
        self.first_name = fn
        self.middle_name = mn
        self.last_name = ln
        self.student_id = sid
        self.application_id = aid
        self.email = e
        self._budget = StudentBudget(budget)
        self.priority = 0
        self.awarded = dict()
        self.attributes = dict()

    @property
    def ids(self):
        """
        Gets the student and application IDs.
        """
        return (self.student_id, self.application_id)
    
    @property
    def budget(self):
        """
        Gets the student's budget.
        """
        return self._budget.budget
    
    @budget.setter
    def budget(self, value):
        """
        Sets the student's budget.
        """
        self._budget.budget = value

    @property
    def working_budget(self):
        """
        Gets the student's working budget.
        """
        return self._budget.working_budget
    
    @working_budget.setter
    def working_budget(self, value):
        """
        Sets the student's working budget.
        """
        self._budget.working_budget = value

    @property
    def budgetObj(self):
        """
        Gets the student's budget system.
        """
        return self._budget
    
    def remove_attribute(self, header_name):
        normalized_header = self._headers.get_normalized_header(header_name)
        if normalized_header in self.attributes:
            del self.attributes[normalized_header]

     # Use property for convenient access
    def __getitem__(self, header_name):
        normalized_header = self._headers.get_normalized_header(header_name)
        return self.attributes.get(normalized_header)

    def __setitem__(self, header_name, value):
        normalized_header = self._headers.get_normalized_header(header_name)
        self.attributes[normalized_header] = value

    def search_attributes(self, key):
        """
        Searches if a key is in the student's attributes.
        return: True if the key is found, False otherwise.
        """
        return key in self.attributes

    def __str__(self):
        return f'{self.first_name} {self.last_name} (ID#{self.student_id})(${self.budget})'
