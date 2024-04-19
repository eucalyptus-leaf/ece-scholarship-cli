from src.budget_system import StudentBudget
import pandas as pd
import datetime

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

    

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "student_id": self.student_id,
            "application_id": self.application_id,
            "email": self.email,
            "budget": self._budget.to_dict(),
            "priority": self.priority,
            "awarded": self.awarded,
            "attributes": {key: self._convert_value(value) for key, value in self.attributes.items()}
        }
    
    def _convert_value(self, value):
        """
        Convert non-JSON serializable objects to a JSON-serializable format.
        Specifically handle pandas.Timestamp objects here.
        """
        if isinstance(value, (pd.Timestamp, datetime.datetime)):
            return value.isoformat()  # Convert Timestamp to ISO format string
        return value
    
    @classmethod
    def from_dict(cls, data, headers):
        student = cls(
            headers,
            StudentBudget.from_dict(data['budget']),
            data['first_name'],
            data['middle_name'],
            data['last_name'],
            data['student_id'],
            data['application_id'],
            data['email']
        )
        student.priority = data['priority']
        student.awarded = data['awarded']
        student.attributes = {key: cls._revert_value(value) for key, value in data['attributes'].items()}
        return student
    
    @classmethod
    def _revert_value(cls, value):
        """
        Revert values from string format back to their original types if necessary.
        Specifically handle converting ISO format strings back to pandas.Timestamp.
        """
        try:
            pd.to_datetime(value)
        except ValueError:
            return value

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
        Returns: Value of attribute
        Error State: None
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
    
    def all_info_str(self):
        # Print all the information of the student
        string = "Student ID: " + str(self.student_id) + "\n"
        string += "Application ID: " + str(self.application_id) + "\n"
        string += "Name: " + self.first_name + " " + self.middle_name + " " + self.last_name + "\n"
        string += "Email: " + self.email + "\n"
        string += "Budget: $" + str(self.budget) + "\n"
        string += "Attributes:\n"
        for key, value in self.attributes.items():
            string += "\t" + key + ": " + str(value) + "\n"
        string += "Awards:\n"
        string += self.awarded_str()
        return string
    
    def awarded_str(self):
        # Print the scholarships awarded to the student
        string = ""
        if self.awarded:
            for scholarship_id, amount in self.awarded.items():
                string += "\tScholarship (" + str(scholarship_id) + ") awarded $" + str(amount) + "\n"
        else:
            string += "\tNo scholarships awarded this student."
        return string
    
    def qualify_str(self):
        # Print the scholarships the student qualifies for
        string = ""
        if self.priority:
            for scholarship_id in self.priority:
                string += "\tScholarship (" + str(scholarship_id) + ")\n"
        else:
            string += "\tStudent does not qualify for any scholarships."
        return string

    def quick_info_str(self):
        # Print the student's information
        string = str(self) + "\n"
        string += "Attributes:\n"
        string += "\tEmail: " + self.email + "\n"
        string += "\tCumulative GPA: " + str(self[64]) + "\n" # Cumulative GPA
        string += "\tExpected Graduation Date: " + str(self[83]) + "\n" # Expected Grad Date
        return string
    
    def student_scholarship_info_str(self):
        # Print the student's information
        string = str(self) + "\n"
        string += "Scholarship Awarded:\n"
        string += self.awarded_str()
        string += "Scholarships Qualified:\n"
        string += self.qualify_str()
    
    def __str__(self):
        """
        Description: Prints student object
        Args: None
        Returns: String containing student name, ID, and budget
        Error State: None
        """
        return f'(ID#{self.student_id}) {self.first_name} {self.last_name} | Application ID: {self.application_id} Budget: ${self.budget}'
