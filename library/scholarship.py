from library.budget_system import ScholarshipBudget
"""
This module contains the Scholarship class which represents a scholarship.
"""

class Scholarship:
    """
    The Scholarship class represents a scholarship.
    """
    def __init__(self, headers, budget, scholarship_id=0, name="None", num_awards=0, priority=0):
        """
        Initializes a new instance of the Scholarship class.

        :param scholarship_id: A unique identifier for the scholarship.
        :param name: The name of the scholarship.
        :param budget: The budget of the scholarship.
        :param num_awards: The number of awards offered by the scholarship.
        :param priority: The priority of the scholarship.
        """
        self._headers = headers
        self.scholarship_id = scholarship_id
        self.name = name
        self._budget = ScholarshipBudget(budget)
        self.num_awards = num_awards
        self.priority = priority
        self.criteria = dict()
        self.students = dict()

    @property
    def budget(self):
        """
        Gets the total budget of the scholarship.

        :return: The total budget of the scholarship.
        """
        return self._budget.budget
    
    @budget.setter
    def budget(self, value):
        """
        Sets the total budget of the scholarship.

        :param value: The total budget of the scholarship.
        """
        self._budget.budget = value

    @property
    def working_budget(self):
        """
        Gets the working budget of the scholarship.

        :return: The working budget of the scholarship.
        """
        return self._budget.working_budget
    
    @working_budget.setter
    def working_budget(self, value):
        """
        Sets the working budget of the scholarship.

        :param value: The working budget of the scholarship.
        """
        self._budget.working_budget = value


    def __getitem__(self, header_name):
        # Use overview headers for normalization and lookup
        normalized_header = self._headers.get_normalized_overview_header(header_name)
        return self.criteria.get(normalized_header)

    def __setitem__(self, header_name, value):
        # Use overview headers for normalization and setting values
        normalized_header = self._headers.get_normalized_overview_header(header_name)
        self.criteria[normalized_header] = value

    def remove_criteria(self, header_name):
        # Use overview headers for normalization and removal
        normalized_header = self._headers.get_normalized_overview_header(header_name)
        if normalized_header in self.criteria:
            del self.criteria[normalized_header]


    def search_criteria(self, criteria):
        """
        Searches for a criteria in the scholarship's criteria.

        :param criteria: The criteria to search for.
        :return: True if the criteria is found, False otherwise.
        """
        return criteria in self.criteria
    

    def add_student(self, student_id, student):
        """
        Adds a student to the scholarship's ordered linked-list of students.

        :param student_id: The unique identifier of the student to add.
        """
        self.students.update({student_id: student})


    def remove_student(self, student_id):
        """
        Removes student from the scholarship's ordered linked-list of students.

        :param student_id: The unique identifier of the student applying.
        """
        self.students.pop(student_id, None)

    def search_student(self, student_id):
        """
        Searches for a student in the scholarship's linked-list of students.

        :param student_id: The unique identifier of the student to search for.
        :return: True if the student is found, False otherwise.
        """
        return student_id in self.students


    def compare_students(self, student1, student2):
        # This method should return a positive number if student1 is more qualified than student2,
        # a negative number if student2 is more qualified than student1, and 0 if they are equally qualified.
        # The criteria for comparison will depend on the specific criteria for the scholarship.
        """ TODO: Implement a method for determing how the criterion match and how they compare """
        
        # sort by quality
        # sort by graduation date
        # sort by GPA

        score1 = (student1.attributes['Qualification Points'] + student1.attributes['Graduation Date'] + student1.attributes['GPA'])/3
        score2 = (student2.attributes['Qualification Points'] + student2.attributes['Graduation Date'] + student2.attributes['GPA'])/3

        return score1 - score2
