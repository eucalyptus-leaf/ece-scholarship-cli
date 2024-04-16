# award_system.py

class AwardSystem:
    def __init__(self):
        self.awarded = {}
        self.award_order = []

    def order_scholarships(self, scholarshipTab):
        # Order scholarships by priority
        self.award_order = sorted(scholarshipTab, key=lambda x: -x.priority, reverse=True)

    def award_scholarships_loevan(self, h, studentTab, scholarshipTab, budgetSystem):
        # Award scholarships to students based on Loevan's algorithm
        for scholarship in self.award_order:
            if scholarship.scholarship_id not in self.awarded:
                self.awarded[scholarship.scholarship_id] = {}
            for id in scholarship.studentOrder:
                student = studentTab[id]
                if scholarship.working_budget == 0:
                    print("Scholarship " + str(scholarship.scholarship_id) + " has been fully awarded.")
                    break
                elif scholarship.working_budget <= 0:
                    print("Error in scholarship " + str(scholarship.scholarship_id) + " budget. Budget is negative.")
                    break
                else:
                    if student.working_budget > 0:
                        if scholarship.working_budget >= student.working_budget:
                            scholarship.working_budget -= student.working_budget
                            student.awarded[scholarship.scholarship_id] = student.working_budget
                            self.awarded[scholarship.scholarship_id][student.student_id] = student.working_budget
                            student.working_budget = 0
                        else:
                            student.awarded[scholarship.scholarship_id] = scholarship.working_budget
                            student.working_budget -= scholarship.working_budget
                            self.awarded[scholarship.scholarship_id][student.student_id] = scholarship.working_budget
                            scholarship.working_budget = 0
                        print("Awarded " + str(student.awarded[scholarship.scholarship_id]) + " from scholarship " + str(scholarship.scholarship_id) + " to student " + str(student.student_id))
    
    def get_awards_string(self, scholarship_id):
        # Print the students awarded a scholarship
        string = ""
        if scholarship_id in self.awarded:
            for student_id, amount in self.awarded[scholarship_id].items():
                string += "\tStudent (" + str(student_id) + ") awarded $" + str(amount) + "\n"
        else:
            string += "No students awarded scholarship."
        return string