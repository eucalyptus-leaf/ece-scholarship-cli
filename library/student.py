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
        Description: Initializes a new instance of the Student class.
        Args: headers: Headers to parse data
              budget: Student Budget
              fn: First name
              ln: Last name
              mn: Middle name
              sid: Student ID
              aid: Application ID
              e: Student email address
        Returns: None
        Error State: None
        """
        self._headers = headers
        self.first_name = fn
        self.middle_name = mn
        self.last_name = ln
        self.student_id = sid
        self.application_id = aid
        self.email = e
        self._budget = StudentBudget(budget)
        self.priority = []
        self.awarded = dict()
        self.attributes = dict()

    @property
    def ids(self):
        """
        Description: Gets the student and application IDs.
        Args: None
        Returns: Tuple containing student ID and application ID
        Error State: None 
        """
        return (self.student_id, self.application_id)
    
    @property
    def budget(self):
        """
        Description: Gets the student's budget.
        Args: None
        Returns: 
        Error State: 
        """
        return self._budget.budget
    
    @budget.setter
    def budget(self, value):
        """
        Description: Sets the student's budget.
        Args: value: budget to set
        Returns: None
        Error State: None
        """
        self._budget.budget = value

    @property
    def working_budget(self):
        """
        Description: Gets the student's working budget.
        Args: None
        Returns: Student's budget
        Error State: None
        """
        return self._budget.working_budget
    
    @working_budget.setter
    def working_budget(self, value):
        """
        Description: Sets the student's working budget.
        Args: value: budget to set
        Returns: None
        Error State: None 
        """
        self._budget.working_budget = value

    @property
    def budgetObj(self):
        """
        Description: Gets the student's budget system.
        Args: None
        Returns: Student budget system
        Error State: None
        """
        return self._budget
    
    def __getitem__(self, key):
        """
        Description: Gets the value of an attribute.
        Args: key: index of attribute
        Returns: 
        Error State: 
        """
        header = self._headers.get_header(key)
        return self.attributes[header]
    
    def __setitem__(self, key, value):
        """
        Description: Sets the value of an attribute.
        Args: key: index of attribute
              value: budget to set
        Returns: None
        Error State: None
        """
        header = self._headers.get_header(key)
        self.attributes[header] = value

    def __delitem__(self, key):
        """
        Description: Deletes an attribute.
        Args: key: index of attribute
        Returns: None
        Error State: None
        """
        header = self._headers.get_header(key)
        del self.attributes[header]

    def search_attributes(self, key):
        """
        Description: Searches if a key is in the student's attributes.
        Args: key: index of attribute
        Returns: True if the key is found, False otherwise.
        Error State: None
        """
        return key in self.attributes

    def __str__(self):
        """
        Description: Prints student object
        Args: None
        Returns: String containing student name, ID, and budget
        Error State: None
        """
        return f'{self.first_name} {self.last_name} (ID#{self.student_id})(${self.budget})'
