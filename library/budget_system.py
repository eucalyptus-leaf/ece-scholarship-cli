# budget_system.py
from datetime import datetime
import math
from . import hashtab
from . import student
from . import scholarship



class BudgetSystem:
    department_budget = 0
    
    def __init__(self, capacity=0):
        self.working_budget = capacity
    
    def calculate_scholarship_amount(self, gpa):
        max_amount = 4000  # Maximum amount for a 4.0 GPA
        min_gpa_for_award = round(3.5,1)
        min_amount = 1000  # Minimum amount for the lowest eligible GPA

        if gpa < min_gpa_for_award:
            # If GPA is below the threshold for awarding, return 0 or a predefined minimum amount
            return 0

        # Standard reduction for each tenth of a GPA below 4.0
        reduction_per_tenth = (max_amount - min_amount) / ((round(4.0,1) - min_gpa_for_award) * 10)
        reduction = (round(4.0,1) - (math.floor(gpa*10)/10)) * 10 * reduction_per_tenth
        scholarship_amount = int(max_amount - reduction)

        # Ensure the scholarship amount does not fall below the minimum amount
        if scholarship_amount < min_amount:
            scholarship_amount = min_amount

        return scholarship_amount
        
    def check_department_budget(self):
        # Implement your logic to check if the department's budget is exceeded
        # Return True if exceeded, False otherwise
        return self.working_budget > self.department_budget
    
    def calculate_department_budget(self, scholarshipHashTab):
        self.department_budget = 0
        for scholarship in scholarshipHashTab:
            self.department_budget += scholarship.budget
        if self.department_budget == 0:
            print ("Scholarship budgets empty.")
            return False
        return True
    
    def reduce_award_amount(self, studentTab, gpa, h):
        # Reduce the award amount for all students with the specified GPA
        reduction_amount = 200  # Determine the amount or percentage of reduction
        min_hit = False
        # Define the lower bound of the GPA range
        if gpa > 3.6:
            lower_bound = round(gpa - 0.1,1)
        else:
            lower_bound = round(3.5,1)

        print("Reducing award amount for students with GPA between ", lower_bound, " and ", gpa, " by ", reduction_amount, " each.")

        for student in studentTab:
            student_gpa = (student.attributes[h.headers[64]])
            if lower_bound < student_gpa <= gpa:
                student.budget -= reduction_amount
                if student.budget < 500:
                    student.budget = 500
                    min_hit = True
                print("Reducing award amount for student ", student.student_id, " by ", reduction_amount, ". New budget: ", student.budget)
        return min_hit
    
    def recalculate_working_budget(self, studentTab):
        # Recalculate the total working budget after adjustments
        self.working_budget = 0
        print("Reseting Working Budget to recalculate. Recalculating the working budget.")
        for student in studentTab:
            self.working_budget += student.budget
        print("Working Budget recalculated: ", self.working_budget)
        return
    
    def adjust_awards_for_budget(self, studentTab, h):
        # Implement the logic to adjust the awards for students when the budget is exceeded starting with students with 3.5 GPA moving up when student at GPA is reduced to 500
        gpa = round(3.6, 1)
        while self.check_department_budget():
            print("Budget ", self.department_budget, " exceeded. Currently, ", self.working_budget, " Adjusting awards for students with GPA: ", gpa)
            min_hit = self.reduce_award_amount(studentTab, gpa, h)
            print("Mininmum hit: ", min_hit)
            self.recalculate_working_budget(studentTab)
            if min_hit:
                gpa = round(gpa + 0.1, 1)
            if gpa > round(4.0, 1):
                break
        return
    
    def calculate_student_budget(self, studentTab, h):
        current_year = datetime.now().year

        for student in studentTab:
            gpa = float(student.attributes[h.headers[64]])
            grad_date = student.attributes[h.headers[83]]
            year = grad_date.year
            month = grad_date.month

            # # Check if the GPA is eligible for a scholarship
            # if gpa >= 3.5:
            # Calculate the scholarship amount based on GPA
            scholarship_amount = int(self.calculate_scholarship_amount(gpa))

            # Halve the amount if the student graduates in December of the current year
            if year == current_year and month > 5:
                scholarship_amount /= 2

            student.budget = scholarship_amount

            # Update the working budget
            self.working_budget += student.budget
            
        # Check if the department's budget is exceeded
        if self.check_department_budget():
            # Handle the situation when the budget is exceeded
            self.adjust_awards_for_budget(studentTab, h)

        return True
    
    def initialize_budget_system(self, studentHashTab, scholarshipHashTab, h):
        self.calculate_department_budget(scholarshipHashTab)
        self.calculate_student_budget(studentHashTab, h)
        return True
