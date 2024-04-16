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
        self.studentOrder = []
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

    def __str__(self):
        return f"({self.scholarship_id}) {self.name} | Budget: ${self.budget}, Awards: {self.num_awards}"
        
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
        """ Sorts the studentOrder list based on student scores, graduation dates, and GPAs. """
        try:
            self.studentOrder.sort(key=lambda student_id: (
                -self.students[student_id][4],  # Higher points are better
                self.students[student_id][83].toordinal(),  # Earlier dates are better
                -self.students[student_id][64],  # Higher GPA is better
            ))
        except Exception as e:
            print(f"Error during sorting: {e}")

    def find_priority_students(self):
        """ using the len() of students[student_id].priority to get the number of scholarships a student is qualified for, students with less scholarships in their priority member variable are prioritized. Thus the studentOrder list is re-ordered with priority student closer to the front of the list."""
        try:
            self.studentOrder.sort(key=lambda student_id: len(self.students[student_id].priority))
        except Exception as e:
            print(f"Error during sorting: {e}")

            