"""
@author: ECE Project Team
ECE 484
Version  
ECE Scholarship Project
    
Description: This program sorts and matches students with scholarships
"""

def print_main_menu():
    print("Main Menu:\n")
    print("1. Print Scholarship List")
    print("2. Print Sorted Student List")
    print("3. Print Matched Scholarships")
    print("4. Save in text file")
    print("5. Quit\n")

def print_scholarship_list():
    print()
    print("Scholarship Name     | Spending Budget | Requirements")
    print("--------------------------------------------------")
    # Replace the following loop with actual scholarship data
    for i in range(1, 4):
        print(f"Scholarship {i}        | $XXXX.XX        | X,Y,Z")

def print_student_list():
    print()
    print("Student Name     | GPA     | Credits taken  | Semesters Remaining | etc..")
    print("-------------------------------------------------------------------------")
    # Replace the following loop with actual scholarship data
    for i in range(1, 4):
        print(f"Student {i}        |  X.XX   | XXX            |  X                  | etc...")

def print_matched_list():
    print()
    print("Scholarship Name              | Student Names (Scholarship Amount)                 ")
    print("-------------------------------------------------------------------------")
    # Replace the following loop with actual scholarship data
    for i in range(1, 4):
        print(f"Scholarship {i}                 |  Student {i} ($XXXX.XX)")

# Prompt the user for input with a clear message
print("|************************************|")
print("| Welcome to the Scholarship Program |")
print("| Please enter the name of the file. |")
print("|************************************|\n")
file_name = input("Scholarships File Name: ")
student_name = input("Students Data File Name: ")
#print("/************************************************************/")

if file_name.strip():
    print(f"\nThank you for selecting '{file_name}' as your file.\n")
else:
    print("Invalid file name. Please provide a valid file name.")

#print_main_menu();

while True:
    print()
    print_main_menu()

    choice = input("Enter option (1/2/3/4/5): ").strip()

    if choice == '1':
        # Add code to print the scholarship list
        print_scholarship_list()
    elif choice == '2':
        # Add code to print the sorted student list
        print_student_list()
    elif choice == '3':
        # Add code to print matched scholarships
        print_matched_list()
    elif choice == '4':
        # Add code to save data to a text file
        print("Saving data to a text file...")

        # Gather scholarship and student information
        header = "ECE Scholarship Project \nECE 484 \nSenior Design Project \nDescription: This program sorts and matches students with scholarships\n\n\n"
        scholarship_info = "Scholarship Name     | Student Name (Budget) \n--------------------------------------------\n"
        # Replace the following loop with actual scholarship data
        for i in range(1, 10):
            scholarship_info += f"Scholarship {i}        | Student {i}  ($XXXX.XX)   \n"

        student_info = "Student Name     | GPA     | Credits taken  | Semesters Remaining | etc..\n---------------------------------------------------------------------\n"
        # Replace the following loop with actual scholarship data
        for i in range(1, 4):
            student_info += f"Student {i}        |  X.XX   | XXX            |  X                  | etc...\n"

        # Write data to a text file
        with open('ScholarshipAndStudent.txt', 'w') as file:
            file.write(header)
            file.write(scholarship_info)
            #file.write(student_info)

        print("Data has been saved to 'ScholarshipAndStudent.txt'")
    elif choice == '5' or choice.lower() == 'q':
        print("Thank you for using the scholarship program!")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
