# budget_system.py
import math
from datetime import datetime


class BudgetSystem:
    '''Description: Manages and calculation total budgets based on different criteria'''
    _instance = None
    total_department_budget = 0 # Total budget for the department
    currentBudget = 0   # monnies left in the total budget

    def __init__(self):
        return
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BudgetSystem, cls).__new__(cls)
            cls._instance.total_department_budget = 0
            cls._instance.currentBudget = 0
        return cls._instance
    
    def to_dict(self):
        return {
            "total_department_budget": self.total_department_budget,
            "currentBudget": self.currentBudget
        }
    
    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.total_department_budget = data['total_department_budget']
        instance.currentBudget = data['currentBudget']
        return instance

    def total_department_budget_exceeded(self):
        ''' Description: Check if department total budget is exceeded
            Return: Returns true is bedgets is exceeded or false otherwise
            Args: None
            Error State: None
        '''
        return self.total_department_budget < self.currentBudget
    
    def calculate_total_department_budget(self, scholarshipTab):
        ''' Description: Calculates the total budget od department
            Args: scholarshipTab
            Return: Returns total budget number
            Error State: Prints scholarship budget empty
        '''
        self.total_department_budget = 0
        for scholarship in scholarshipTab:
            self.total_department_budget += scholarship.budget
        if self.total_department_budget == 0:
            print ("Scholarship budgets empty. Department's current total budget: ", self.total_department_budget)
            return False
        return True
    
    def reduce_student_scholarship_budget_by_gpa(self, h, studentTab, gpa, reduction_amount, percentage = False):
        ''' Description: Reduce the award amount for all students with the lower than specified GPA
            Args: h, studentTab, gpa, reduction_amount, percentage
            Return: min_hit: The amount to reduce 
            Error State: None
        '''
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
        ''' Description: Recalcuates the current award budget after adjustments
            Args: studentTab
            Return: None
            Error State: None
        '''
        self.currentBudget = 0
        print("Reseting Working Budget to recalculate. Recalculating the working budget.")
        for student in studentTab:
            self.currentBudget += student.budget
        print("Current award budget recalculated. New award budget: ", self.currentBudget)
        return
    
    def adjust_awards_for_budget(self, h, studentTab, percentage = None, amount = None):
        ''' Description: Implements logic to adjust the award for students when the budget is exceeded starting with students with 3.5 GPA moving up when student at GPA is reduced to 500
            Args: h, studentTab, percentage, amount
            Return: None
            Error State: None 
        '''
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
    
    def calculate_every_students_budget(self, h, studentTab): 
        ''' Description: Calculates budget for students based on GPA and graduation date
            Args: studentTab
            Return: True is not exceeded, False otherwise
            Error State: None
        '''
        for student in studentTab:
            gpa = round(float(student.attributes[h.headers[64]]),1) # Cumulative GPA rounded to the nearest tenth
            grad_date = student.attributes[h.headers[83]]

            # Check if the GPA is eligible for a scholarship
            # if gpa >= 3.5:
            # Calculate the scholarship amount based on GPA
            scholarship_amount = int(student.budgetObj.calculate_budget(grad_date, gpa))

            student.budget = scholarship_amount
            student.working_budget = scholarship_amount
            self.currentBudget += scholarship_amount
            #print("Student ", student.student_id, " has a budget of ", student.budget)

        # Check if the department's budget is exceeded
        if self.total_department_budget_exceeded():
            return False
        else: return True
    
    def init_budget_system(self, h, studentHashTab, scholarshipHashTab, if_reduction_amount = None, if_reduction_percentage = None):
        ''' Description: Initializes the budget system, calculates total budget, and adjusts if exceeded
            Args: h, studentHashTab, scholarshipHashTab, if_reduction_amount
            Return: True if sucessfully initialized
            Error State: None
        '''
        self.calculate_total_department_budget(scholarshipHashTab)
        print("Total department budget: ", self.total_department_budget)
        budget_exceeded=self.calculate_every_students_budget(h, studentHashTab)
        print("Budget for each student calculated. Budget exceeded: ", budget_exceeded)
        if budget_exceeded:
            print("Budget exceeded. Adjusting awards for students.")
            self.adjust_awards_for_budget(h, studentHashTab, if_reduction_amount, if_reduction_percentage)
        return True
    

class StudentBudget:
    '''Class to initialize and calculate budget for each student based on their qualifications'''
    def __init__(self, budgetSystem):
        ''' Description: Initializes a student budget 
            Args: budgetSystem
            Return: None
            Error State: None 
        '''
        self.access = budgetSystem
        self.budget = 0
        self.working_budget = 0

    def to_dict(self):
        return {
            "budget": self.budget,
            "working_budget": self.working_budget
        }
    
    @classmethod
    def from_dict(cls, data):
        obj = cls(BudgetSystem())
        obj.budget = data['budget']
        obj.working_budget = data['working_budget']
        return obj


    def calculate_budget(self, expected_grad_date, cumulative_gpa): 
        ''' Description: Calculates the budget for a student based on GPA and graduation date
            Args: expected_grad_date, cumulative_gpa
            Return: budget: Calculated budget for student
            Error State: None
        '''
        current_year = datetime.now().year
        current_month = datetime.now().month
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

class ScholarshipBudget:
    '''Class to intialize the initial budget for scholarships'''
    def __init__(self, budgetSystem):
        ''' Description: Initialize the scholarship budget
            Args: budgetSystem
            Return: None
            Error State: None 
        '''        
        self.access = budgetSystem
        self.budget = 0
        self.working_budget = 0

    def to_dict(self):
        return {
            "budget": self.budget,
            "working_budget": self.working_budget
        }
    
    @classmethod
    def from_dict(cls, data):
        obj = cls(BudgetSystem())
        obj.budget = data['budget']
        obj.working_budget = data['working_budget']
        return obj