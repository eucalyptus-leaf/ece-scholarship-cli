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
            "attributes": self.attributes
        }
    
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
        student.attributes = data['attributes']
        return student

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
    
    def __getitem__(self, key):
        """
        Gets the value of an attribute.
        """
        header = self._headers.get_header(key)
        return self.attributes[header]
    
    def __setitem__(self, key, value):
        """
        Sets the value of an attribute.
        """
        header = self._headers.get_header(key)
        self.attributes[header] = value

    def __delitem__(self, key):
        """
        Deletes an attribute.
        """
        header = self._headers.get_header(key)
        del self.attributes[header]

    def search_attributes(self, key):
        """
        Searches if a key is in the student's attributes.
        return: True if the key is found, False otherwise.
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
        return f'(ID#{self.student_id}) {self.first_name} {self.last_name} | Application ID: {self.application_id} Budget: ${self.budget}'
