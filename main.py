import sys
import os
# Now you can import your modules
from library.hashtab import Hashtab
from library.budget_system import BudgetSystem
from library.import_data import Headers
from library.import_data import import_students_from_file
from library.import_data import import_scholarships_from_file
from library.import_data import import_overview_scholarships_from_file
from library.award_system import AwardSystem


from src.init_fs import init_fs as ifs
from src.version_control import version_control as vc

#from bin.library import indv, input, menu, output, priya, program

def main():

	vc()
	ifs()

	project_path = os.path.dirname(__file__)
	print("Project Directory Path: " + project_path + "\n")

	data_path = os.path.join(os.path.dirname(__file__), "data")
	config_path = os.path.join(os.path.dirname(__file__), "config")
	lib_path = os.path.join(os.path.dirname(__file__), "library")
	src_path = os.path.join(os.path.dirname(__file__), "src")
	
	# Create the Data Stuctures
	studentTab = Hashtab()
	print("Student Table Created\n")
	scholarshipTab = Hashtab()
	print("Scholarship Table Created\n")
	budget = BudgetSystem()
	print("Budget System Created\n")
	award = AwardSystem()
	print("Award System Created\n")
	headers = Headers()
	headers.normalize_and_save_headers(os.path.join(config_path, "headers.txt"), os.path.join(config_path, "normalized_headers.txt"), False)
	headers.normalize_and_save_headers(os.path.join(config_path, "overview_headers.txt"), os.path.join(config_path, "normalized_overview_headers.txt"), True)
	print("Headers Created\n")
	
	# Import the data
	import_students_from_file(headers, budget, os.path.join(data_path, "general_application"), studentTab)
	print("Imported Students\n")
	import_scholarships_from_file(headers, budget, os.path.join(data_path, "scholarships"), scholarshipTab, studentTab)
	print("Imported Scholarships\n")
	import_overview_scholarships_from_file(os.path.join(data_path, "scholarships/overview"), scholarshipTab, headers)
	print("Imported Overview Scholarships\n")

	# Initialize the budget system
	budget.init_budget_system(headers, studentTab, scholarshipTab)
	print("Initialized Budget System\n")
	
	# Award scholarships
	award.award_scholarships_loevan(headers, studentTab, scholarshipTab, budget)
	print("Awarded Scholarships\n")

if __name__ == "__main__":
	main()
