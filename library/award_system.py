# award_system.py

class AwardSystem:
    def __init__(self):
        self.awarded = {}

    def award_scholarships_loevan(self, h, studentTab, scholarshipTab, budgetSystem):
        # Award scholarships to students based on Loevan's algorithm
        for scholarship in scholarshipTab: # for each scholarship
            if scholarship.scholarship_id not in self.awarded: # if scholarship has not been awarded
                self.awarded[scholarship.scholarship_id] = {} # add scholarship to awarded list
            for student in scholarship.students.values(): # get each student object
                if scholarship.working_budget == 0:
                    print("Scholarship " + str(scholarship.scholarship_id) + " has been fully awarded.")
                    break
                elif scholarship.working_budget <= 0:
                    print("Error in scholarship " + str(scholarship.scholarship_id) + " budget. Budget is negative.")
                    break
                else: 
                    if student.working_budget > 0: # if student needs more money
                        if scholarship.working_budget >= student.working_budget: # if scholarship has enough or more than enough money
                            scholarship.working_budget -= student.working_budget # subtract the student's budget from the scholarship's budget
                            student.awarded[scholarship.scholarship_id] = student.working_budget # award the student the scholarship
                            self.awarded[scholarship.scholarship_id][student.student_id] = student.working_budget
                            student.working_budget = 0 # set the student's working budget to 0 since the scholarship met their monetary needs
                        else: # if scholarship does not have enough money to meet the student's needs
                            student.awarded[scholarship.scholarship_id] = scholarship.working_budget # award the student the remaining scholarship money
                            student.working_budget -= scholarship.working_budget # subtract the scholarship's budget from the student's working budget
                            self.awarded[scholarship.scholarship_id][student.student_id] = scholarship.working_budget
                            scholarship.working_budget = 0 # set the scholarship's working budget to 0 since it has been fully awarded
                        
                        #print("Awarded " + str(student.awarded[scholarship.scholarship_id]) + " from scholarship " + str(scholarship.scholarship_id) + " to student " + str(student.student_id))


    # def calculate_priority_score(self, scholarship, student):
    #     # Calculate the priority score for a student
    #     return student.gpa * 100 + scholarship.get_student_score(student.student_id)
    
    # def award_scholarships(self, studentTab, scholarshipTab, h):
    #     # Award scholarships to students
    #     for scholarship in scholarshipTab:
    #         for student in studentTab:
    #             if scholarship.search_criteria("GPA"):
    #                 if student.gpa >= scholarship.criteria["GPA"]:
    #                     if scholarship.num_awards > 0:
    #                         scholarship.num_awards -= 1
    #                         scholarship.award_student(student.student_id)
    #                         student.award_scholarship(scholarship.scholarship_id)
    #                         print("Awarded scholarship to student ", student.student_id, " from scholarship ", scholarship.scholarship_id)
    #                         break
    #                 else:
    #                     print("Student ", student.student_id, " does not meet the criteria for scholarship ", scholarship.scholarship_id)
    #     return True
    
    def get_awards_string(self, scholarship_id):
        # Print the students awarded a scholarship
        string = ""
        if scholarship_id in self.awarded:
            for student_id, amount in self.awarded[scholarship_id].items():
                string += "\tStudent (" + str(student_id) + ") awarded $" + str(amount) + "\n"
        else:
            string += "No students awarded scholarship."
        return string