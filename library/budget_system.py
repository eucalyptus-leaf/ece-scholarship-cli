# budget_system.py
from . import hashtab
from . import student
from . import scholarship


class BudgetSystem:
    department_budget = -1
    def __init__(self, capacity=-1):
        working_budget = capacity

    def check_department_budget(self):
        if self.working_budget > self.department_budget:
            raise ValueError("Department budget exceeded")
        return False

    def calculate_student_budget(self, studentHashTab):
        for student in studentHashTab:
            gpa = (float)(student.attributes['Cumulative GPA'])
            year, month = student.attributes['Expected Grad Date']

            if month == 12 and gpa >= 4.0 and year == 2023:                 # December graduation with 4.0 GPA
                student.budget = 4000                                       # Half of the maximum allotted amount
                self.working_budget += student.budget

            if month == 5 and gpa == 4.0:                                   # May graduation with 4.0 GPA
                student.budget = 2000                                       # Maximum allotted amount
                self.working_budget += student.budget

            if month == 12 and year == 2024 and gpa == 4.0:                 # December graduation with GPA decrease in the following academic year
                student.budget = 4000
                self.working_budget += student.budget

            if month == 5 and year == 2024 and gpa == 4.0:                  # May graduation with GPA decrease in the following academic year
                student.budget = 3000
                self.working_budget += student.budget

            if month == 12 and gpa <= 4.0 and gpa > 3.8 and year == 2023:
                student.budget = 3500
                self.working_budget += student.budget

            if month == 12 and gpa <= 3.8 and gpa > 3.6 and year == 2023:
                student.budget = 3000
                self.working_budget += student.budget

            if month == 12 and gpa <= 3.6 and gpa > 3.4 and year == 2023:
                student.budget = 2500
                self.working_budget += student.budget
            else:
                student.budget = 1000                                       # Default case if none of the conditions are met
                self.working_budget += student.budget
                
            self.check_department_budget()

        return False