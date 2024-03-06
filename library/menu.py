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
    print("2. Print Student List")
    print("3. Print Matched Scholarships")
    print("4. Save in text file")
    print("5. Quit\n")

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
        read_scholarship_data(file_name)
    elif choice == '2':
        # Add code to print the sorted student list
        read_student_data(student_name)
    elif choice == '3':
        # Add code to print matched scholarships
        print_matched_list()
    elif choice == '4':
        # Add code to save data to a text file
        save_student_and_scholarship_data(student_name, file_name, 'StudentAndScholarship.txt')
        print("Data has been saved to 'ScholarshipAndStudent.txt'")
    elif choice == '5' or choice.lower() == 'q':
        print("Thank you for using the scholarship program!")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
