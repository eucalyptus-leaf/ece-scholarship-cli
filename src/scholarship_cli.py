# scholarship_cli.py

"""-------------------------------------------------------------------
File name: scholarship_cli.py
Description: This file contains the command-line interface (CLI) for the scholarship program.
Classes:

Functions:


ECE Scholarship Application
Team 32
Jan 2024
-------------------------------------------------------------------"""

# Import necessary libraries
import os
import pandas as pd 
import json
# Now you can import your modules
from src.hashtab import Hashtab
from src.student import Student
from src.scholarship import Scholarship
from src.budget_system import BudgetSystem
from src.import_data import Headers
from src.import_data import import_students_from_file
from src.import_data import import_scholarships_from_file
from src.import_data import import_overview_scholarships_from_file
from src.award_system import AwardSystem

class CLI_system:
    # System Flags
    system_quit = False

    def __init__(self, hidden_path, data_path, config_path):
        #----------------------------------------------------------
        # Function to initialize the CLI system
        #----------------------------------------------------------
        # Initialize the CLI system
        # Args:
        #     data_path: Path to the data folder
        #     config_path: Path to the config folder
        #     lib_path: Path to the library folder
        #     src_path: Path to the src folder
        # Returns:
        #     None
        
        # Set the system flags
        system_quit = False

        # Set the paths
        self._hiddenPath = hidden_path
        self.dataPath = data_path
        self.configPath = config_path
        self.system_initialized = os.path.exists(os.path.join(self._hiddenPath, "system_state.json"))

        # Create the Data Stuctures
        self.studentTab = Hashtab()
        self.scholarshipTab = Hashtab()
        self.budget = BudgetSystem()
        self.awards = AwardSystem()
        self.headers = Headers()

        if self.system_initialized:
            print("Restoring Prior System State...")
            self.load_state()
        return
    
    def save_state(self):
            """ Save the current state of the application to a JSON file in the hidden directory """
            state = {
                "headers": self.headers.to_dict(),
                "students": {student.student_id: student.to_dict() for student in self.studentTab},
                "scholarships": {scholarship.scholarship_id: scholarship.to_dict() for scholarship in self.scholarshipTab},
                "budget": self.budget.to_dict(),
                "awards": self.awards.to_dict()
            }
            with open(os.path.join(self._hiddenPath, "system_state.json"), "w") as file:
                json.dump(state, file, indent = 4)
            print("System state saved!\n")

    def load_state(self):
        """ Load the prior state of the application from the JOSN file in the hidden directory """
        with open(os.path.join(self._hiddenPath, "system_state.json"), "r") as file:
            state = json.load(file)
        self.headers = Headers.from_dict(state["headers"])
        self.budget = BudgetSystem.from_dict(state["budget"])
        self.studentTab = Hashtab()
        self.studentTab.table = {student_id: Student.from_dict(data, self.headers) for student_id, data in state["students"].items()}
        self.scholarshipTab = Hashtab()
        self.scholarshipTab.table = {scholarship_id: Scholarship.from_dict(data, self.headers, self.studentTab) for scholarship_id, data in state["scholarships"].items()}
        self.awards = AwardSystem.from_dict(state["awards"])
        print("Prior System State Restored. Use system menu options to modify scholarship and student data.\n")

   
    def run_cli(self):
        #----------------------------------------------------------
        # Function to run the CLI
        #----------------------------------------------------------

        if self.system_initialized is False:
            #self.headers.normalize_and_save_headers(os.path.join(self.configPath, "headers.txt"), os.path.join(self.configPath, "normalized_headers.txt"), False)
            #self.headers.normalize_and_save_headers(os.path.join(self.configPath, "overview_headers.txt"), os.path.join(self.configPath, "normalized_overview_headers.txt"), True)
            self.headers.normalized_headers = [self.headers._normalize_header(header) for header in self.headers.headers]
            self.headers.header_map = {i : header for i, header in enumerate(self.headers.headers)}
            self.headers.normalized_overview_headers = [self.headers._normalize_header(header) for header in self.headers.overview_headers]
            self.headers.overview_header_map = {i : header for i, header in enumerate(self.headers.overview_headers)}

            # Import the data
            print("Please add the General Scholarship Application excel or csv file to the general_application folder in the data directory.")
            print("Please edit the scholarship_overview_template.xlsx file in the data/scholarships/overview directory.")
            print("Please add all scholarship excels or csvs referenced in the scholarship_overview_template.xlsx to the scholarships folder in the data directory.")
            print()
            response = input("Have you added and edited the files indicated in the instructions above (y/n): ").strip().lower()
            if response == 'n' or response == 'no':
                print("Please add and edit the files as indicated and restart the program.")
                print("Exiting Program. Goodbye!\n")
                return
            import_students_from_file(self.headers, self.budget, os.path.join(self.dataPath, "general_application"), self.studentTab)
            print("Imported Students\n")
            import_scholarships_from_file(self.headers, self.budget, os.path.join(self.dataPath, "scholarships"), self.scholarshipTab, self.studentTab)
            print("Imported Scholarships\n")
            import_overview_scholarships_from_file(self.headers, os.path.join(self.dataPath, "scholarships", "overview"), self.scholarshipTab)
            print("Imported Overview Scholarships\n")

            # Order scholarships
            self.awards.order_scholarships(self.scholarshipTab)

            # Initialize the budget system
            self.budget.init_budget_system(self.headers, self.studentTab, self.scholarshipTab)
            print("Initialized Budget System\n")
            
            # Award scholarships
            self.awards.award_scholarships(self.scholarshipTab, self.studentTab)
            print("Awarded Scholarships\n")

        while self.system_quit is False:
            main_menu_help = False
            if main_menu_help is False:
                print_main_menu()
            else:
                main_menu_help = False

            choice = input("Menu Choice: ").strip().lower()

            if choice == '1' or choice == 'printscholarship' or choice == 'printscholarshipinfo' or choice == 'printscholarshipinformation': # Print Scholarship Information
                print_menu_option1()
                choice = input("Option Choice: ").strip().lower()

                if choice == 'h' or choice == '12' or choice == 'help': # Help
                    print_menu_option1(help=True)
                    choice = input("Option Choice: ").strip().lower()

                if choice == '1': # Scholarship Info (Basic)
                    scholarship_id = input("Enter Scholarship ID: ").strip().lower()
                    scholarship_id = self.process_id_input(scholarship_id, 'scholarship', 3)
                    if scholarship_id == -1:
                        print("Returning to Main Menu...")
                        continue # Return to Main Menu
                    elif scholarship_id == -2:
                        self.system_quit = True
                    else:
                        print()
                        print(str(self.scholarshipTab[scholarship_id]))

                elif choice == '2': # Scholarship Info (Comprehensive)
                    scholarship_id = input("Enter Scholarship ID: ").strip().lower()
                    scholarship_id = self.process_id_input(scholarship_id, 'scholarship', 3)
                    if scholarship_id == -1:
                        print("Returning to Main Menu...")
                        continue # Return to Main Menu
                    elif scholarship_id == -2:
                        self.system_quit = True
                    else:
                        print()
                        print(self.scholarshipTab[scholarship_id].all_info_str())

                elif choice == '3': # Name and ID
                    scholarship_id = input("Enter Scholarship ID: ").strip().lower()
                    scholarship_id = self.process_id_input(scholarship_id, 'scholarship', 3)
                    if scholarship_id == -1:
                        print("Returning to Main Menu...")
                        continue
                    elif scholarship_id == -2:
                        self.system_quit = True
                    else:
                        print()
                        print("(ID#" + str(scholarship_id) + ") " + self.scholarshipTab[scholarship_id].name)

                elif choice == '4': # Qualified Students
                    scholarship_id = input("Enter Scholarship ID: ").strip().lower()
                    scholarship_id = self.process_id_input(scholarship_id, 'scholarship', 3)
                    if scholarship_id == -1:
                        print("Returning to Main Menu...")
                        continue
                    elif scholarship_id == -2:
                        self.system_quit = True
                    else:
                        print("\n" + str(self.scholarshipTab[scholarship_id]) + ":")
                        print("\tQualified students:")
                        print(self.scholarshipTab[scholarship_id].students_str())

                elif choice == '5': # Students Awarded
                    scholarship_id = input("Enter Scholarship ID: ").strip().lower()
                    scholarship_id = self.process_id_input(scholarship_id, 'scholarship', 3)
                    if scholarship_id == -1:
                        print("Returning to Main Menu...")
                        continue
                    elif scholarship_id == -2:
                        self.system_quit = True
                    else:
                        print("\n" + str(self.scholarshipTab[scholarship_id]) + ":")
                        print("\tAwards:")
                        print(self.scholarshipTab[scholarship_id].awards_str())
                    
                elif choice == '6': # Every Scholarship's Info (Basic)
                    print()
                    for scholarship in self.scholarshipTab:
                        print(scholarship)
                    
                elif choice == '7': # Every Scholarship's Info (Comprehensive)
                    print()
                    for scholarship in self.scholarshipTab:
                        print(scholarship.all_info_str())
                    
                elif choice == '8': # Every Scholarship's Name and ID
                    print()
                    for scholarship in self.scholarshipTab:
                        print("(ID#" + str(scholarship.scholarship_id) + ") " + scholarship.name)
                    
                elif choice == '9': # Every Scholarship's Qualified Students
                    print()
                    for scholarship in self.scholarshipTab:
                        print("\n" + str(scholarship) + ":")
                        print("\tQualified students:")
                        print(scholarship.students_str())
                    
                elif choice == '10': # Every Scholarship's Awards
                    print()
                    for scholarship in self.scholarshipTab:
                        print("\n" + str(scholarship) + ":")
                        print("\tAwards:")
                        print(scholarship.awards_str())
                    
                elif choice == 'q' or choice == '11' or choice == 'quit' or choice == 'exit': # Quit
                    self.system_quit = True
                    self.save_state()
                
                else: # Invalid Choice
                    print("Invalid Choice. Returning to Main Menu. Try Again\n")

            elif choice == '2' or choice == 'printstudent' or choice == 'printstudentinfo' or choice == 'printstudentinformation': # Print Student Information
                print_menu_option2()
                choice = input("Option Choice: ").strip().lower()
                if choice == 'h' or choice == '12' or choice == 'help': # Help
                    print_menu_option2(help=True)
                    choice = input("Option Choice: ").strip().lower()
                    
                if choice == '1': # Student Info (Basic)
                    student_id = input("Enter Student ID: ").strip().lower()
                    student_id = self.process_id_input(student_id, 'student', 3)
                    if student_id == -1:
                        print("Returning to Main Menu...")
                        continue # Return to Main Menu
                    elif student_id == -2:
                        self.system_quit = True
                    else:
                        print()
                        print(self.studentTab[student_id].quick_info_str())

                elif choice == '2': # Student Info (Comprehensive)
                    student_id = input("Enter Student ID: ").strip().lower()
                    student_id = self.process_id_input(student_id, 'student', 3)
                    if student_id == -1:
                        print("Returning to Main Menu...")
                        continue # Return to Main Menu
                    elif student_id == -2:
                        self.system_quit = True
                    else:
                        print()
                        print(self.studentTab[student_id].all_info_str())

                elif choice == '3': # Name and IDs
                    student_id = input("Enter Student ID: ").strip().lower()
                    student_id = self.process_id_input(student_id, 'student', 3)
                    if student_id == -1:
                        print("Returning to Main Menu...")
                        continue # Return to Main Menu
                    elif student_id == -2:
                        self.system_quit = True
                    else:
                        print()
                        print(str(self.studentTab[student_id]))

                elif choice == '4': # Qualified Scholarships
                    student_id = input("Enter Student ID: ").strip().lower()
                    student_id = self.process_id_input(student_id, 'student', 3)
                    if student_id == -1:
                        print("Returning to Main Menu...")
                        continue # Return to Main Menu
                    elif student_id == -2:
                        self.system_quit = True
                    else:
                        print("\n" + str(self.studentTab[student_id]) + ":")
                        print("\tQualifies for:")
                        print(self.studentTab[student_id].qualify_str())

                elif choice == '5': # Scholarships Awarded
                    student_id = input("Enter Student ID: ").strip().lower()
                    student_id = self.process_id_input(student_id, 'student', 3)
                    if student_id == -1:
                        print("Returning to Main Menu...")
                        continue # Return to Main Menu
                    elif student_id == -2:
                        self.system_quit = True
                    else:
                        print("\n" + str(self.studentTab[student_id]) + ":")
                        print("\tAwarded:")
                        print(self.studentTab[student_id].awarded_str())

                elif choice == '6': # Every Student's Info (Basic)
                    print()
                    for student in self.studentTab:
                        print(student.quick_info_str())

                elif choice == '7': # Every Student's Info (Comprehensive)
                    print()
                    for student in self.studentTab:
                        print(student.all_info_str())

                elif choice == '8': # Every Student's Name and IDs
                    print()
                    for student in self.studentTab:
                        print(student)

                elif choice == '9': # Every Student's Qualified Scholarships
                    for student in self.studentTab:
                        print("\n" + str(student) + ":")
                        print("\tQualifies for:")
                        print(student.qualify_str())
                    
                elif choice == '10': # Every Student's Awards
                    for student in self.studentTab:
                        print("\n" + str(student) + ":")
                        print("\tAwarded:")
                        print(student.awarded_str())

                elif choice == 'q' or choice == '11' or choice == 'quit' or choice == 'exit': # Quit
                    self.system_quit = True
                    self.save_state()

                else: # Invalid Choice
                    print("Invalid Choice. Returning to Main Menu. Try Again\n")
                
            elif choice == '3' or choice == 'save' or choice == 'saveinfo' or choice == 'saveinformation' or choice == 'saveinformationasafile': # Save Information as a File
                print_menu_option3()
                choice = input("Option Choice: ").strip().lower()
                if choice == 'h' or choice == '4' or choice == 'help': # Help
                    print_menu_option3(help=True)
                    choice = input("Option Choice: ").strip().lower()
                if choice == '1': # Save Scholarship Award Info
                    with open(os.path.join(self.dataPath, "output", "scholarship_awards.txt"), "w") as file:
                        for scholarship in self.scholarshipTab:
                            file.write(str(scholarship) + "\n")
                            file.write("Awards:\n")
                            file.write(scholarship.awards_str() + "\n")

                elif choice == '2': # Save Student Award Info
                    with open(os.path.join(self.dataPath, "output", "student_awards.txt"), "w") as file:
                        for student in self.studentTab:
                            file.write(str(student) + "\n")
                            file.write("Has been Awarded:\n")
                            file.write(student.awarded_str() + "\n")

                elif choice == 'q' or choice == '3' or choice == 'quit' or choice == 'exit': # Quit
                    self.system_quit = True
                    self.save_state()

                else: # Invalid Choice
                    print("Invalid Choice. Returning to Main Menu. Try Again\n")

            elif choice == '4' or choice == 'modify' or choice == 'modifydata': # Modify Data
                print_menu_option4()
                choice = input("Option Choice: ").strip().lower()
                if choice == 'h' or choice == '7' or choice == 'help': # Help
                    print_menu_option4(help=True)
                    choice = input("Option Choice: ").strip().lower()
                if choice == '1': # Award a Student a Scholarship
                    continue
                elif choice == '2': # Remove a Student's Scholarship
                    continue
                elif choice == '3': # Edit a Student's Budget
                    continue
                elif choice == '4': # Edit a Scholarship's Budget
                    continue
                elif choice == '5': # Change Scholarship Priority
                    continue
                elif choice == 'q' or choice == '6' or choice == 'quit' or choice == 'exit': # Quit
                    self.system_quit = True
                    self.save_state()
                else:
                    print("Invalid Choice. Returning to Main Menu. Try Again\n")

            elif choice == 'r' or choice == 'reset' or choice == 'resetsystem': # Reset System
                print("Resetting System State")
                self.system_quit = True
                os.remove(os.path.join(self._hiddenPath, "system_state.json"))
                print("System State Reset. Exiting Program. Goodbye!\n")

            elif choice == 'q' or choice == '5' or choice == 'quit' or choice == 'exit': # Quit
                self.system_quit = True
                self.save_state()

            elif choice == 'h' or choice == '6' or choice == 'help': # Help
                print_main_menu(help=True)
                main_menu_help = True
            
            else:
                print("Invalid Choice. Try Again\n")

        print("\nSaving System State")
        print("Thank you for using the Scholarship Program!")
        print("Exiting Program. Goodbye!\n")

    def process_id_input(self, id, type, count):
        ret = False

        if id == 'q' or id == 'quit' or id == 'exit':
            return -2
        if id == 'return' or id == 'back' or id == 'b' or id == 'r' or id == 'ret':
            return -1
        
        if count > 0:
            if type == 'scholarship':
                try:
                    scholarship_id = int(id)
                    if scholarship_id not in self.scholarshipTab:
                        raise ValueError("Invalid Scholarship ID")
                    else:
                        ret = scholarship_id
                except:
                        print("\nInvalid Scholarship ID. Try Again")
                        new_input = input("Enter Scholarship ID: ").strip().lower()
                        ret = self.process_id_input(new_input, type, count-1)
            elif type == 'student':
                try:
                    student_id = int(id)
                    if student_id not in self.studentTab:
                        raise ValueError("Invalid Student ID")
                    else:
                        ret = student_id
                except:
                    print("\nInvalid Student ID. Try Again")
                    new_input = input("Enter Student ID: ").strip().lower()
                    ret = self.process_id_input(new_input, type, count-1)
            else: # Invalid Type ... should never be reached if program is working correctly
                print("\nInvalid Type. Returning to Main Menu. Try Again\n")
                return -1
        else:
            print("Too many invalid inputs. Returning to Main Menu. Try Again\n")
            return -1
        
        return ret

def print_main_menu(help=False):
    #----------------------------------------------------------
    # Function to print out Main Menu Options and Help
    #----------------------------------------------------------
    if help is False:
        print("\nMain Menu:")
        print("\t1. Print Scholarship Information")
        print("\t2. Print Student Information")
        print("\t3. Save Information as a File")
        print("\t4. Modify Data")
        print("\tR. Reset System")
        print("\tQ. Quit")
        print("\tH. Help")
    else:
        print('Main Menu Help Menu:')
        print('********************')
        print("Option 1 - Print an individual scholarship's or all scholarships' information.")
        print("Option 2 - Print an individual student's or all students' information.")
        print("Option 3 - Save scholarship or student award information to a file in the data/output directory.")
        print("Option 4 - Modify student or scholarship data.")
        print("Option R - Reset the system to the initial state allowing for re-importing of data from the data directory.")
        print("Option Q - Quit the program. Saves the system state before exiting.")

def print_menu_option1(help=False):
    if help is False:
        print("\nPrint Scholarship Information")
        print("-------------------------------------------------------------------------------------------------------------")
        print("Individual Scholarship Options:")
        print("\t1. Scholarship Info (Basic)")
        print("\t2. Scholarship Info (Comprehensive)")
        print("\t3. Name and ID")
        print("\t4. Qualified Students")
        print("\t5. Students Awarded\n")
        print("All Scholarships Options:")
        print("\t6. Every Scholarship's Info (Basic)")
        print("\t7. Every Scholarship's Info (Comprehensive)")
        print("\t8. Every Scholarship's Name and ID")
        print("\t9. Every Scholarship's Qualified Students")
        print("\t10. Every Scholarship's Awards")
        print("\tQ. Quit")
        print('\tH. Help')
    else:
        print('Scholarship Info Help Menu')
        print('**************************')
        print("Option 1 - Print basic information about an individual scholarship.")
        print("Option 2 - Print comprehensive information about an individual scholarship.")
        print("Option 3 - Print the name and ID of an individual scholarship.")
        print("Option 4 - Print the students qualified for an individual scholarship.")
        print("Option 5 - Print the students awarded an individual scholarship.")
        print("Option 6 - Print basic information about all scholarships.")
        print("Option 7 - Print comprehensive information about all scholarships.")
        print("Option 8 - Print the name and ID of all scholarships.")
        print("Option 9 - Print the students qualified for all scholarships.")
        print("Option 10 - Print the students awarded by all scholarships.")
        print("Option Q - Quit the program. Saves the system state before exiting.")

def print_menu_option2(help=False):
    if help is False:
        print("\nPrint Student Information")
        print("-------------------------------------------------------------------------------------------------------------")
        print("Individual Student Options:")
        print("\t1. Student Info (Basic)")
        print("\t2. Student Info (Comprehensive)")
        print("\t3. Name and IDs")
        print("\t4. Qualified Scholarships")
        print("\t5. Scholarships Awarded\n")
        print("All Student Options:")
        print("\t6. Every Student's Info (Basic)")
        print("\t7. Every Student's Info (Comprehensive)")
        print("\t8. Every Student's Name and IDs")
        print("\t9. Every Student's Qualified Scholarships")
        print("\t10. Every Student's Awards")
        print("\tQ. Quit")
        print('\tH. Help')
    else:
        print("Student Info Help Menu")
        print('**********************')
        print("Option 1 - Print basic information about an individual student.")
        print("Option 2 - Print comprehensive information about an individual student.")
        print("Option 3 - Print the name and IDs of an individual student.")
        print("Option 4 - Print the scholarships qualified for by an individual student.")
        print("Option 5 - Print the scholarships awarded to an individual student.")
        print("Option 6 - Print basic information about all students.")
        print("Option 7 - Print comprehensive information about all students.")
        print("Option 8 - Print the name and IDs of all students.")
        print("Option 9 - Print the scholarships qualified for by all students.")
        print("Option 10 - Print the scholarships awarded to all students.")
        print("Option Q - Quit the program. Saves the system state before exiting.")

def print_menu_option3(help=False):
    if help is False:
        print("\nSave Information as a File")
        print("-------------------------------------------------------------------------------------------------------------")
        print("Save Options:")
        print("\t1. Save Scholarship Award Info")
        print("\t2. Save Student Award Info")
        print("\tQ. Quit")
        print('\tH. Help')
    else:
        print("Save Information Help Menu")
        print('*************************')
        print ("Option 1 - Save scholarship award information to a file named scholarship_awards.txt in the data/output directory.")
        print ("Option 2 - Save student award information to a file named student_awards.txt in the data/output directory.")
        print ("Option Q - Quit the program. Saves the system state before exiting.")

def print_menu_option4(help=False):
    if help is False:
        print("\nModify Data")
        print("-------------------------------------------------------------------------------------------------------------")
        print("Modify Options:")
        print("\t1. Award a Student a Scholarship")
        print("\t2. Remove a Student's Scholarship")
        print("\t3. Edit a Student's Budget")
        print("\t4. Edit a Scholarship's Budget")
        print("\t5. Change Scholarship Priority")
        print("\tQ. Quit")
        print('\tH. Help')
    else:
        print("Modify Data Help Menu")
        print('*********************')
        print("Option 1 - Award a student a scholarship.")
        print("Option 2 - Remove a student's scholarship.")
        print("Option 3 - Edit a student's budget.")
        print("Option 4 - Edit a scholarship's budget.")
        print("Option 5 - Change a scholarship's priority.")
        print("Option Q - Quit the program. Saves the system state before exiting.")
