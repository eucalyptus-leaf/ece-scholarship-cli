from hashtab import Hashtab
from student import Student

def main():
	studenttab = Hashtab()
	for i in range(3):
		student = Student("Student " + str(i), "Last Name " + str(i), i)
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
