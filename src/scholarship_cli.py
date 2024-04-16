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
import sys
import os
import pandas as pd 
# Now you can import your modules
from library.hashtab import Hashtab
from library.budget_system import BudgetSystem
from library.import_data import Headers
from library.import_data import import_students_from_file
from library.import_data import import_scholarships_from_file
from library.import_data import import_overview_scholarships_from_file
from library.award_system import AwardSystem

class CLI_system:
    # System Flags
    system_quit = False
    system_initialzied = False

    def __init__(self, hidden_path, data_path, config_path, lib_path, src_path):
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
        self.libPath = lib_path
        self.srcPath = src_path
        
        if os.path.exists(os.path.join(self._hiddenPath, "system_state")):
            print("Prior System State Found\n")
            # TO-DO: Add function calls to restore the system state
            system_initialzied = True
        else:
            print("No Prior System State Found\n")
            system_initialzied = False

        # Create the Data Stuctures
        self.studentTab = Hashtab()
        print("Student Table Structure Created\n")
        self.scholarshipTab = Hashtab()
        print("Scholarship Table Structure Created\n")
        self.budget = BudgetSystem()
        print("Department Budget System Created\n")
        self.awards = AwardSystem()
        print("Awards System Created\n")
        self.headers = Headers()
        print("Header Tracker Created\n")
        return
   
    def run_cli(self):
        #----------------------------------------------------------
        # Function to run the CLI
        #----------------------------------------------------------

        if self.system_initialzied is False:
            self.headers.normalize_and_save_headers(os.path.join(self.configPath, "headers.txt"), os.path.join(self.configPath, "normalized_headers.txt"), False)
            self.headers.normalize_and_save_headers(os.path.join(self.configPath, "overview_headers.txt"), os.path.join(self.configPath, "normalized_overview_headers.txt"), True)
            # Import the data
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
            self.awards.award_scholarships_loevan(self.headers, self.studentTab, self.scholarshipTab, self.budget)
            print("Awarded Scholarships\n")
        else:
            print("Prior System State Restored. Use system menu options to modify scholarship and student data.\n")

        while self.system_quit is False:
            print_main_menu()

            choice = input("Enter option (1/2/3/4/5/6/7/8): ").strip()

            if choice == '1': # Print Scholarship List
                # create an output file named scholarship_awards.txt in the data/output folder and write the awards to the file
                with open(os.path.join(self.dataPath, "output", "scholarship_awards.txt"), "w") as f:
                    for scholarship in self.scholarshipTab:
                        print(scholarship)
                        print(self.awards.get_awards_string(scholarship.scholarship_id))
                        f.write(str(scholarship) + "\n")
                        f.write(self.awards.get_awards_string(scholarship.scholarship_id) + "\n")

            elif choice == '2': # Print Student List
                scholarship_id = int(input("Enter the Scholarship ID: ").strip())
                if scholarship_id not in self.scholarshipTab:
                    print("Invalid scholarship ID. Please enter a valid scholarship ID.")
                    continue
                print("Students qualified for scholarship " + str(scholarship_id) + ":")
                for student in self.scholarshipTab[scholarship_id].students.values():
                    print("\t" + str(student))

            elif choice == '3': # Print Names of Scholarships
                print("Scholarships: ")
                for scholarship in self.scholarshipTab:
                    print("\t" + scholarship.name + "\n")

            elif choice == '4' or choice.lower().strip() == 'sort': # Print Student Awards
                studentID = int(input("Enter the Student ID: ").strip())
                if studentID not in self.studentTab:
                    print("Invalid Student ID. Please enter a valid Student ID.")
                    continue
                print("Student " + str(self.studentTab[studentID]) + " has been awarded the following scholarships:")
                for scholarship in self.studentTab[studentID].awarded.keys():
                    print("\t$" + str(self.studentTab[studentID].awarded[scholarship]) + " from scholarship " + str(scholarship) + " " + self.scholarshipTab[scholarship].name)
                
            elif choice == '5' or choice.lower().strip() == 'budget': # print all student awards
                # create an output file named student_awards.txt in the data/output folder and write the student awards to the file
                with open(os.path.join(self.dataPath, "output", "student_awards.txt"), "w") as f:
                    for student in self.studentTab:
                        if student.awarded.keys():
                            print(str(student) + " has been awarded the following scholarships:")
                            f.write("\n" + str(student) + " has been awarded the following scholarships:\n")
                            for scholarship in student.awarded.keys():
                                print("\t$" + str(student.awarded[scholarship]) + " from scholarship " + str(scholarship) + " " + self.scholarshipTab[scholarship].name + "\n")
                                f.write("\t$" + str(student.awarded[scholarship]) + " from scholarship " + str(scholarship) + " " + self.scholarshipTab[scholarship].name + "\n")
                        else:
                            continue

            elif choice == '6' or choice.lower().strip() == 'match': # Match students with scholarships
                print('Match')

            elif choice == '7' or choice.lower().strip() == 'modify': # Modify scholarship or student data
                print('Modify')

            elif choice.strip() == '8' or choice.lower().strip() == 'q' or choice.lower().strip() == 'quit':
                # TO-DO: Add a confirmation message before quitting
                # TO-DO: Add a function to save the data before quitting
                # TO-DO: Add a function to clean up the data before quitting
                # TO-DO: Add a function to display a summary of the program before quitting
                # TO-DO: Add a function to save program state before quitting
                print("Thank you for using the scholarship program!")
                self.system_quit = True

            elif choice.lower() == 'h' or choice.lower().strip() == 'help':
                print_help_menu()
            else:
                print("Invalid choice. Please enter a valid option.")

def print_welcome():
    #----------------------------------------------------------
    # Function to print greeting message at the beginning
    #----------------------------------------------------------
    # Prompt the user for input with a clear message

    print("|***************************************************************|")
    print("|            Welcome to the Scholarship Program                 |")
    print("|Please enter the name of the folder to being using the program.|")
    print("|***************************************************************|\n")

    #folder_name = input("Folder Name on Desktop: ")

def print_main_menu():
    #----------------------------------------------------------
    # Function to print out Main Menu Options
    #----------------------------------------------------------
    print("Main Menu:")
    print("1. Print Scholarship List            (Prints all Scholarship names with Total Budget and Requirements)")
    print("2. Print Student List                (Prints all the students qualified for a selected scholarship)")
    print("3. Print Names of Scholarships       (Prints the names of all scholarships)")     
    print("4. Sort                              (Sorts all individual and general scholarship files)")
    print("5. Budget                            (Estimates money for each student)")
    print("6. Match                             (Awards scholarship to students)")       
    print("7. Modify                            (User manually awards money to student)")
    print("8. Quit                              (Quit by inputting number '8', 'Q', or 'q')")
    print("H. Help                              (Prints the Help Menu)")

def print_help_menu():
    #----------------------------------------------------------
    # Function to print out Help Menu Options
    #----------------------------------------------------------
    print('Help Instructions:')
    print('-------------------------------------------------------------------------------------------------------------')
    print('The program accepts numerical inputs, with each number corresponding to one of the following options.')
    print('1. Option 1 allows for the printing of all scholarship details, including name, budget, and qualifications.')
    print('2. Option 2 prints of all students who meet the criteria for a particular scholarship.')
    print('3. Option 3 displays the names of all available scholarships on the screen.')
    print('4. Option 5 organizes all student based of qualification points within each file.')
    print('5. Option 6 computes the budget allocation for each individual student.')
    print('6. Option 7 pairs students with their respective eligible scholarships.')
    print('7. Option 8 allows for user to input awarded money for specific scholarship')
    print('8. Option 9 concludes the program, also triggered by input of "Q" or "q".')