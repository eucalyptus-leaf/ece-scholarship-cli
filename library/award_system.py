# award_system.py


class AwardSystem:
    def __init__(self, bs):
        self.budget_system = bs

    def calculate_priority_score(self, scholarship, student):
        # Calculate the priority score for a student
        return student.gpa * 100 + scholarship.get_student_score(student.student_id)
    
    def award_scholarships(self, studentTab, scholarshipHashTab, h):
        # Award scholarships to students
        for student in studentTab:
            for scholarship in scholarshipHashTab:
                if scholarship.search_criteria("GPA"):
                    if student.gpa >= scholarship.criteria["GPA"]:
                        if scholarship.num_awards > 0:
                            scholarship.num_awards -= 1
                            scholarship.add_student(student.student_id)
                            student.award_scholarship(scholarship.scholarship_id)
                            print("Awarded scholarship to student ", student.student_id, " from scholarship ", scholarship.scholarship_id)
                            break
                    else:
                        print("Student ", student.student_id, " does not meet the criteria for scholarship ", scholarship.scholarship_id)
        return True