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
        Description: Initializes a new instance of the Scholarship class.
        Args: scholarship_id: A unique identifier for the scholarship.
               name: The name of the scholarship.
               budget: The budget of the scholarship.
               num_awards: The number of awards offered by the scholarship.
               priority: The priority of the scholarship.
        Returns: None
        Error State: None
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
        Description: Gets the total budget of the scholarship.
        Args: None
        Returns: The total budget of the scholarship
        Error State: None 
        """
        return self._budget.budget
    
    @budget.setter
    def budget(self, value):
        """
        Description: Sets the total budget of the scholarship.
        Aergs: value: The total budget of the scholarship.
        Returns: None
        Error State: None
        """
        self._budget.budget = value

    @property
    def working_budget(self):
        """
        Description: Gets the working budget of the scholarship.
        Args: None
        Returns: The working budget of the scholarship
        Error State: None
        """
        return self._budget.working_budget
    
    @working_budget.setter
    def working_budget(self, value):
        """
        Description: Sets the working budget of the scholarship.
        Args: value: The working budget of the scholarship.
        Returns: None
        Error State: None
        """
        self._budget.working_budget = value

    def __str__(self):
        """
        Description: Returns a string representation of the scholarship object
        Args: None
        Returns: String contatining the schoalrhip ID, name, budget, and number of awards
        Error State: None
        """
        return f"({self.scholarship_id}) {self.name} | Budget: ${self.budget}, Awards: {self.num_awards}"
        
    def search_criteria(self, criteria):
        """
        Description: Searches for a criteria in the scholarship's criteria.
        Args: criteria: The criteria to search for.
        Returns: True if the criteria is found, False otherwise.
        Error State: None
        """
        return criteria in self.criteria
    

    def add_student(self, student_id, student):
        """
        Description: Adds a student to the scholarship's ordered linked-list of students.
        Args: student_id: The unique identifier of the student to add.
        Returns: None
        Error State: None
        """
        self.students.update({student_id: student})
        if student_id not in self.studentOrder:
            self.studentOrder.append(student_id)


    def remove_student(self, student_id):
        """
        Description: Removes student from the scholarship's ordered linked-list of students.
        Args: student_id: The unique identifier of the student applying.
        Returns: None
        Error State: None
        """
        self.students.pop(student_id, None)

    def search_student(self, student_id):
        """
        Description: Searches for a student in the scholarship's linked-list of students.
        Args: student_id: The unique identifier of the student to search for.
        Returns: True if the student is found, False otherwise.
        Error State: None
        """
        return student_id in self.students
    
    def sort_students(self):
        """
        Description: Sorts the studentOrder list based on student scores, graduation dates, GPAs, and how many scholarships they qualify for.
        Args: None
        Returns: None
        Error State: None
        """
        try:
            self.studentOrder.sort(key=lambda student_id: (
                -self.students[student_id][4],  # Higher quality points are better
                self.students[student_id][83].toordinal(),  # Earlier dates are better
                -self.students[student_id][64],  # Higher GPA is better
                len(self.students[student_id].priority) # Fewer scholarships in priority is better
            ))
        except Exception as e:
            print(f"Error during sorting: {e}")

            
