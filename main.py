import sys
import os
# Now you can import your modules
from library.dataStructure.hashtab import Hashtab
from library.dataStructure.student import Student
from library.dataStructure.scholarship import Scholarship
from library.dataStructure.budget_system import BudgetSystem
from library.dataStructure.import_data import *

from src.init_fs import init_fs as ifs
from src.version_control import version_control as vc

#from bin.library import indv, input, menu, output, priya, program


def main():

	vc()
	ifs()

	project_path = os.path.dirname(__file__)
	print("Project Directory Path: " + project_path + "\n")

	data_path = os.path.join(os.path.dirname(__file__), "data")
	lib_path = os.path.join(os.path.dirname(__file__), "library")
	src_path = os.path.join(os.path.dirname(__file__), "src")
	
	studentTab = Hashtab()
	print("Student Table Created\n")
	scholarshipTab = Hashtab()
	print("Scholarship Table Created\n")
	budget = BudgetSystem()
	print("Budget System Created\n")
	headers = Headers()
	headers.normalize_and_save_headers(os.path.join(lib_path, "dataStructure/headers.txt"), os.path.join(lib_path, "dataStructure/normalized_headers.txt"))
	print("Headers Created\n")

	# while(True):
	# 	scholarship_cli()

	# call import_students_from_file using the file in the data/general_application directory using os and allow wildcard names for the file in the directory
	
	import_students_from_file(os.path.join(data_path, "general_application"), studentTab, headers)
	import_scholarships_from_file(os.path.join(data_path, "scholarships"), scholarshipTab, studentTab, headers)

	print("Imported Students\n")
if __name__ == "__main__":
	main()
