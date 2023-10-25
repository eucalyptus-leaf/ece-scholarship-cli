"""
This module contains the Scholarship class which represents a scholarship.
"""

from linked_list import LinkedList

class Scholarship:
    """
    The Scholarship class represents a scholarship.
    """
    def __init__(self, scholarship_id, name, budget, num_awards, priority, criteria=None):
        """
        Initializes a new instance of the Scholarship class.

        :param scholarship_id: A unique identifier for the scholarship.
        :param name: The name of the scholarship.
        :param budget: The budget of the scholarship.
        :param num_awards: The number of awards offered by the scholarship.
        :param priority: The priority of the scholarship.
        """
        self.scholarship_id = scholarship_id
        self.name = name
        self.budget = budget
        self.num_awards = num_awards
        self.priority = priority
        self.criteria = set()
        self.students = LinkedList()

    def add_criteria(self, criteria):
        """
        Adds a criteria to the scholarship.

        :param criteria: The criteria to add.
        """
        self.criteria.add(criteria)
        

    def remove_criteria(self, criteria):
        """
        Removes a criteria from the scholarship.

        :param criteria: The criteria to remove.
        """
        self.criteria.discard(criteria)


    def search_criteria(self, criteria):
        """
        Searches for a criteria in the scholarship's criteria.

        :param criteria: The criteria to search for.
        :return: True if the criteria is found, False otherwise.
        """
        return criteria in self.criteria
    

    def add_student(self, student_id):
        """
        Adds a student to the scholarship's ordered linked-list of students.

        :param student_id: The unique identifier of the student to add.
        """
        self.students.insert_sorted(student_id)


    def remove_student(self, student_id):
        """
        Removes student from the scholarship's ordered linked-list of students.

        :param student_id: The unique identifier of the student applying.
        """
        self.students.remove(student_id)


    def compare_students(self, student1, student2):
        # This method should return a positive number if student1 is more qualified than student2,
        # a negative number if student2 is more qualified than student1, and 0 if they are equally qualified.
        # The criteria for comparison will depend on the specific criteria for the scholarship.
        """ TODO: Implement a method for determing how the criterion match and how they compare """
        
        return student2.qualityscore - student1.qualityscore
