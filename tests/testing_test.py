import sys
sys.path.append('/Users/gavinjones/Library/CloudStorage/OneDrive-Personal/school/college/ncsu/2023-24/ncsu_spring_2024/classes/ece-485/gh/32-ECE-Scholarship-Project')
import os
# Now you can import your modules
from library.hashtab import Hashtab
from library.student import Student
from library.scholarship import Scholarship
from library.test import *
from library.budget_system import BudgetSystem
from library.import_data import Headers
from library.import_data import import_students_from_file
from library.import_data import import_scholarships_from_file
from library.import_data import import_overview_scholarships_from_file

from src.init_fs import init_fs as ifs
from src.version_control import version_control as vc

#from bin.library import indv, input, menu, output, priya, program


def main():
    vc()
    ifs()

    project_path = '/Users/gavinjones/Library/CloudStorage/OneDrive-Personal/school/college/ncsu/2023-24/ncsu_spring_2024/classes/ece-485/gh/32-ECE-Scholarship-Project'
    print("Project Directory Path: " + project_path + "\n")

    data_path = os.path.join(project_path, "data")
    config_path = os.path.join(project_path, "config")
    lib_path = os.path.join(project_path, "library")
    src_path = os.path.join(project_path, "src")

    # Create the Data Stuctures
    studentTab = Hashtab()
    print("Student Table Created\n")
    scholarshipTab = Hashtab()
    print("Scholarship Table Created\n")
    budget = BudgetSystem()
    print("Budget System Created\n")
    headers = Headers()
    headers.normalize_and_save_headers(os.path.join(config_path, "headers.txt"), os.path.join(config_path, "normalized_headers.txt"))
    headers.save_overview_headers(os.path.join(config_path, "overview_headers.txt"))
    print("Headers Created\n")

    # Import the data
    import_students_from_file(os.path.join(data_path, "general_application"), studentTab, headers)
    print("Imported Students\n")
    import_scholarships_from_file(os.path.join(data_path, "scholarships"), scholarshipTab, studentTab, headers)
    print("Imported Scholarships\n")
    #import_overview_scholarships_from_file(os.path.join(data_path, "scholarships/overview"), scholarshipTab, headers)
    #print("Imported Overview Scholarships\n")

    print("starting test")
    get_student_id(studentTab, scholarshipTab, data_path)
            
    # # Initialize the budget system
    # budget.initialize_budget_system(studentTab, scholarshipTab, headers)
    # print("Initialized Budget System\n")
            
    # Award scholarships

if __name__ == "__main__":
	main()