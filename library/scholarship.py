from library.budget_system import ScholarshipBudget
from library.student import Student
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
        self.awards = dict()
        self.studentOrder = []
        self.students = dict()


    def to_dict(self):
        # Convert the scholarship to a dictionary
        scholarship_dict = {
            "Headers" : self._headers.to_dict(),
            "Scholarship ID": self.scholarship_id,
            "Name": self.name,
            "Budget": self._budget.to_dict(),
            "Number of Awards Allowed": self.num_awards,
            "Priority": self.priority,
            "Criteria": self.criteria,
            "Awards": self.awards,
            "Student Order": self.studentOrder,
            "Students": self.students
        }
        return scholarship_dict
    
    @classmethod
    def from_dict(cls, data, headers):
        scholarship = cls(
            headers,
            ScholarshipBudget.from_dict(data['budget']),
            data['scholarship_id'],
            data['name'],
            data['num_awards'],
            data['priority']
        )
        scholarship.criteria = data['criteria']
        scholarship.awards = data['awards']
        scholarship.studentOrder = data['studentOrder']
        scholarship.students = {k: Student.from_dict(v, headers) for k, v in data['students'].items()}
        return scholarship
    
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

    def __str__(self):
        return f"(ID#{self.scholarship_id}) {self.name} | Budget: ${self.budget}, Number of Awards Allowed: {self.num_awards}, Priority: {self.priority}"
        
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
        if student_id not in self.studentOrder:
            self.studentOrder.append(student_id)


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
    
    def sort_students(self):
        """ Sorts the studentOrder list based on student scores, graduation dates, GPAs, and how many scholarships they qualify for. """
        try:
            self.studentOrder.sort(key=lambda student_id: (
                -self.students[student_id][4],  # Higher quality points are better
                self.students[student_id][83].toordinal(),  # Earlier dates are better
                -self.students[student_id][64],  # Higher GPA is better
                len(self.students[student_id].priority) # Fewer scholarships in priority is better
            ))
        except Exception as e:
            print(f"Error during sorting: {e}")

    def all_info_str(self):
        # Print all the information of the scholarship
        string = "Scholarship ID: " + str(self.scholarship_id) + "\n"
        string += "Name: " + self.name + "\n"
        string += "Budget: $" + str(self.budget) + "\n"
        string += "Number of Awards Allowed: " + str(self.num_awards) + "\n"
        string += "Priority: " + str(self.priority) + "\n"
        string += "Criteria:\n"
        for key, value in self.criteria.items():
            string += "\t" + key + ": " + str(value) + "\n"
        string += "Student Order:\n"
        for student_id in self.studentOrder:
            string += "\t" + str(self.students[student_id]) + "\n"
        string += "Qualified Students:\n"
        string += self.students_str()
        string += "Student Awards:\n"
        string += self.awards_str()
        return string

    def scholarship_student_info_str(self):
        # Print the scholarship's information
        string = str(self) + "\n"
        string += "Student Awarded:\n"
        string += self.awards_str()
        string += "Qualified Students:\n"
        string += self.students_str()
        return string
    
    def students_str(self):
        # Print the students qualified for this scholarship
        string = ""
        if self.students:
            for student_id, student in self.students.items():
                string += "\t" + str(student) + "\n"
        else:
            string += "\tNo students qualified for this scholarship."
        return string

    def awards_str(self):
        # Print the students awarded this scholarship
        string = ""
        if self.awards:
            for student_id, amount in self.awards.items():
                string += "\tStudent (" + str(student_id) + ") awarded $" + str(amount) + "\n"
        else:
            string += "\tNo students awarded by this scholarship."
        return string
            