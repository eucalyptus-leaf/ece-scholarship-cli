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

	data_path = os.path.join(os.path.dirname(__file__), "data")


	studenttab = Hashtab()
	budget = BudgetSystem()

	# while(True):
	# 	scholarship_cli()

	# call import_students_from_file using the file in the data/general_application directory using os and allow wildcard names for the file in the directory
	import_students_from_file(os.path.join(data_path, "general_application"), studenttab)
	
	print(studenttab.search(200350644))

	for i in range(3):
		student = Student()
		student.student_id = i
		student.first_name = "student_first_name" + str(i)
		student.last_name = "student_last_name" + str(i)
		student.budget = 4000 + i
		studenttab.insert(student.student_id, student)
		print("inserting student ")
		print(student)
		print("\n")
	
	print(studenttab.search(1))
	print(studenttab.search(2))
	print(studenttab.search(3))
	studenttab.delete(2)

if __name__ == "__main__":
	main()
