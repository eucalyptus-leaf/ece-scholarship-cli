# budget_system.py
import math
from datetime import datetime


class BudgetSystem:
    total_department_budget = 0 # Total budget for the department
    currentBudget = 0   # monnies left in the total budget

    def __init__(self):
        return

    def total_department_budget_exceeded(self):
        # Implement your logic to check if the department's total budget is exceeded
        # Return True if exceeded, False otherwise
        return self.total_department_budget < self.currentBudget
    
    def calculate_total_department_budget(self, scholarshipTab):
        self.total_department_budget = 0
        for scholarship in scholarshipTab:
            self.total_department_budget += scholarship.budget
        if self.total_department_budget == 0:
            print ("Scholarship budgets empty. Department's current total budget: ", self.total_department_budget)
            return False
        return True
    
    def reduce_student_scholarship_budget_by_gpa(self, h, studentTab, gpa, reduction_amount, percentage = False):
        # Reduce the award amount for all students with the lower than specified GPA
        
        # Define the lower bound of the GPA range
        if gpa > 3.6:
            lower_bound = round(gpa - 0.1,1)
        else:
            lower_bound = round(3.5,1)

        print("Reducing award amount for students with GPA between ", lower_bound, " and ", gpa, " by ", reduction_amount, " each.")

        for student in studentTab:
            student_gpa = student.attributes[h.headers[64]]
            if student_gpa < gpa and student_gpa >= lower_bound:
                if percentage:
                    student.budget = round(student.budget * (1-reduction_amount), -1)
                else:
                    student.budget -= reduction_amount
                if student.budget < 500:
                    student.budget = 0
                    min_hit = True
                student.working_budget = student.budget
                print("Reducing award amount for student ", student.student_id, " by ", reduction_amount, ". New budget: ", student.budget)
        return min_hit
    
    def recalculate_current_budget(self, studentTab):
        # Recalculate the current award budget after adjustments
        self.currentBudget = 0
        print("Reseting Working Budget to recalculate. Recalculating the working budget.")
        for student in studentTab:
            self.currentBudget += student.budget
        print("Current award budget recalculated. New award budget: ", self.currentBudget)
        return
    
    def adjust_awards_for_budget(self, h, studentTab, percentage = None, amount = None):
        # Implement the logic to adjust the awards for students when the budget is exceeded starting with students with 3.5 GPA moving up when student at GPA is reduced to 500
        gpa = round(3.6, 1)
        while self.total_department_budget_exceeded():
            print("Budget ", self.total_department_budget, " exceeded. Currently, ", self.currentBudget, " Adjusting awards for students with GPA lower than ", gpa)
            if percentage is not None:
                min_hit = self.reduce_student_scholarship_budget_by_gpa(h, studentTab, gpa, percentage, True)
            elif amount is not None:
                min_hit = self.reduce_student_scholarship_budget_by_gpa(h, studentTab, gpa, amount, False)
            else: # default to $200 reduction
                min_hit = self.reduce_student_scholarship_budget_by_gpa(h, studentTab, gpa, 200)

            print("Mininmum hit: ", min_hit, " Removing students with GPA lower than ", gpa, " from the running.")
            self.recalculate_current_budget(studentTab)
            if min_hit:
                gpa = round(gpa + 0.1, 1)
            if gpa > round(4.0, 1):
                break
        return
    
    def calculate_every_students_budget(self, h, studentTab): # should only be run once at initialization of the budget system
        current_year = datetime.now().year

        for student in studentTab:
            gpa = round(float(student.attributes[h.headers[64]]),1) # Cumulative GPA rounded to the nearest tenth
            grad_date = student.attributes[h.headers[83]]
            year = grad_date.year
            month = grad_date.month

            # # Check if the GPA is eligible for a scholarship
            # if gpa >= 3.5:
            # Calculate the scholarship amount based on GPA
            scholarship_amount = int(student.budgetObj.calculate_scholarship_amount(gpa))

            # Halve the amount if the student graduates in December of the current year
            if year == current_year and month > 5:
                scholarship_amount /= 2

            student.budget = scholarship_amount
            student.working_budget = scholarship_amount
            self.currentBudget += scholarship_amount
            #print("Student ", student.student_id, " has a budget of ", student.budget)

        # Check if the department's budget is exceeded
        if self.total_department_budget_exceeded():
            return False
        else: return True
    
    def init_budget_system(self, h, studentHashTab, scholarshipHashTab, if_reduction_amount = None, if_reduction_percentage = None):
        self.calculate_total_department_budget(scholarshipHashTab)
        print("Total department budget: ", self.total_department_budget)
        budget_exceeded=self.calculate_every_students_budget(h, studentHashTab)
        print("Budget for each student calculated. Budget exceeded: ", budget_exceeded)
        if budget_exceeded:
            print("Budget exceeded. Adjusting awards for students.")
            self.adjust_awards_for_budget(h, studentHashTab, if_reduction_amount, if_reduction_percentage)
        return True
    

class StudentBudget:
    def __init__(self, budgetSystem):
        self.access = budgetSystem
        self.budget = 0
        self.working_budget = 0


    def calculate_budget_loevan(expected_grad_date, cumulative_gpa): # loevan code
        current_year = 2023
        current_month = 3
        #current_year = datetime.now().year
        #current_month = datetime.now().month
        grad_year = expected_grad_date.year
        grad_month = expected_grad_date.month
        
        if grad_year == current_year and grad_month >= current_month:
            years_until_graduation = 0
        else:
            years_until_graduation = max(0, (grad_year - current_year) - int(grad_month < current_month))
        
        if years_until_graduation <= 0:
            budget = 2000
        elif years_until_graduation == 1:
            budget = 4000
        elif years_until_graduation == 2:
            budget = 3000
        elif years_until_graduation == 3:
            budget = 2000
        else:
            budget = 0
        
        # Adjust budget based on GPA
        if 3.9 <= cumulative_gpa <= 4.0:
            budget -= 0
        elif 3.8 <= cumulative_gpa < 3.9:
            budget -= 500
        elif 3.7 <= cumulative_gpa < 3.8:
            budget -= 1000
        elif 3.6 <= cumulative_gpa < 3.7:
            budget -= 1500
        elif 3.5 <= cumulative_gpa < 3.6:
            budget -= 2000
        
        # Ensure minimum budget
        if budget < 1000:
            budget = 1000
        
        return budget
    
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
        scholarship_amount = round((max_amount - reduction), 0)

        # Ensure the scholarship amount does not fall below the minimum amount
        if scholarship_amount < min_amount:
            scholarship_amount = min_amount

        return scholarship_amount

class ScholarshipBudget:
    def __init__(self, budgetSystem):
        self.access = budgetSystem
        self.budget = 0
        self.working_budget = 0