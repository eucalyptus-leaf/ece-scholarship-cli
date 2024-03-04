from hashtab import Hashtab
from student import Student

def main():
	studenttab = Hashtab()
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
