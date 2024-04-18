# award_system.py

class AwardSystem:
    def __init__(self):
        ''' Description: Initialize empty array housing scholarship ID's in order of priority from scholarship_overview_template.xlsx'''
        self.award_order = []


    def to_dict(self):
        return {
            "award_order": self.award_order
        }
    
    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.award_order = data['award_order']
        return obj

    def order_scholarships(self, scholarshipTab):
        ''' Description: Order scholarships by priority
            Args: scholarshipTab
        '''
        self.award_order = sorted(scholarshipTab, key=lambda x: -x.priority, reverse=True)

    def award_scholarship_with_budget(self, scholarship, studentTab):
        for student_id in scholarship.studentOrder:
            student = studentTab[student_id]
            if scholarship.working_budget <= 0:
                break
            elif student.working_budget <= 0:
                continue
            self.allocate_award(scholarship, student)
        
    def award_scholarship_with_limit(self, scholarship, studentTab):
        awards_given = 0
        initial_awards = {} # Track how much each student initiaially receives
        
        #First pass: Allocate awards to students in order of priority from studentOrder until the number of awards given is equal to the number of awards allowed
        for student_id in scholarship.studentOrder:
            if awards_given >= scholarship.num_awards or scholarship.working_budget <= 0:
                break
            student = studentTab[student_id]
            if student.working_budget > 0:
                awarded_amount = self.allocate_award(scholarship, student)
                if awarded_amount > 0:
                    awards_given += 1
                    initial_awards[student_id] = awarded_amount
        
        #Second pass: If scholarship working budget remains, distribute remaining budget evenly to students who received awards in the first pass
        if awards_given == scholarship.num_awards and scholarship.working_budget > 0:
            even_share = scholarship.working_budget / awards_given
            for student_id in initial_awards:
                student = studentTab[student_id]
                self.allocate_additional_award(scholarship, student, round(even_share))
        
    
    def allocate_award(self, scholarship, student):
        award_amount = min(scholarship.working_budget, student.working_budget)
        scholarship.working_budget -= award_amount
        student.working_budget -= award_amount
        scholarship.awards[student.student_id] = award_amount
        student.awarded[scholarship.scholarship_id] = award_amount
        return award_amount

    def allocate_additional_award(self, scholarship, student, even_share):
        scholarship.working_budget -= even_share
        student.working_budget -= even_share
        scholarship.awards[student.student_id] += even_share
        student.awarded[scholarship.scholarship_id] += even_share
        

    def award_scholarships(self, scholarshipTab, studentTab):
        for scholarship in scholarshipTab:
            if scholarship.num_awards == -1:
                self.award_scholarship_with_budget(scholarship, studentTab)
            else:
                self.award_scholarship_with_limit(scholarship, studentTab)