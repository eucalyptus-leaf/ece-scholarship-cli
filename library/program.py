'''-------------------------------------------------------------------
File name: project.py
Description: This file contains the main user intertface and options
             for the scholarship application project

ECE Scholarship Application
Team 32
Jan 2024
-------------------------------------------------------------------'''

import os
import pandas as pd 

def print_message():
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
    print("Main Menu:\n")
    print("1. Print Scholarship List            (Prints all Scholarship names with Total Budget and Requirements)")
    print("2. Print Student List                (Prints all the students qualified for a selected scholarship)")
    print("3. Print Names of Scholarships       (Prints the names of all scholarships)")     
    print("4. Sort                              (Sorts all individual and general scholarship files)")
    print("5. Budget                            (Estimates money for each student)")
    print("6. Match                             (Awards scholarship to students)")       
    print("7. Modify                            (User manually awards money to student)")
    print("8. Quit                              (Quit by inputting number '8', 'Q', or 'q')\n")


def read_student_data(folder_path, scholarship_name):
    #----------------------------------------------------------
    # Function to print out info about specific scholarship
    #----------------------------------------------------------
    try:
        # Adjust the scholarship name for ECEGeneral
        if scholarship_name == "ECEGeneral":
            file_path = os.path.join(folder_path, f"{scholarship_name}.xlsx")
        else:
            file_path = os.path.join(folder_path, f"{scholarship_name}_Scholarship_102023.xlsx")


        # Construct the file path for the specific scholarship
        #file_path = os.path.join(folder_path, f"{scholarship_name}_102023.xlsx")

        # Read the student data from the Excel file
        student_data = pd.read_excel(file_path)

        # Print the student data
        print("\nStudent Data:")
        print(student_data)

    except FileNotFoundError:
        print(f"File not found. Please provide a valid file name for scholarship: {scholarship_name}")
    except pd.errors.EmptyDataError:
        print("The file is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_scholarship_data(folder_path, scholarship_name):
    #----------------------------------------------------------
    # Function to print out info from Scholarships folder
    #----------------------------------------------------------
    try:
        # Construct the file path for the scholarship
        file_path = os.path.join(folder_path, f"{scholarship_name}.xlsx")

        # Read the scholarship data from the Excel file
        scholarship_data = pd.read_excel(file_path)

        # Print all columns
        if not scholarship_data.empty:
            print("\nSelected Scholarship Data:")
            print(scholarship_data)
        else:
            print(f"No data found for scholarship: {scholarship_name}")

    except FileNotFoundError:
        print(f"File not found. Please provide a valid file name for scholarship: {scholarship_name}")
    except pd.errors.EmptyDataError:
        print("The file is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_student_and_scholarship_data(folder_path, scholarship_name, output_file):
    #----------------------------------------------------------
    # Function to save information into CSV file
    #----------------------------------------------------------
    try:
        # Construct the file path for the specific scholarship
        file_path = os.path.join(folder_path, f"{scholarship_name}_Scholarship_102023.xlsx")

        # Read student data from the Excel file
        student_data = pd.read_excel(file_path)

        # Read scholarship data from the Excel file
        scholarship_data = pd.read_excel(file_path)

        # Create a text file and write both student and scholarship information
        with open(output_file, 'w') as file:
            file.write("Student Data:\n")
            file.write(student_data.to_string(index=False))
            file.write("\n\nScholarship Data:\n")
            file.write(scholarship_data.to_string(index=False))

        print(f"Data has been saved to '{output_file}'")

    except FileNotFoundError:
        print(f"File not found. Please provide valid file name for scholarship: {scholarship_name}")
    except pd.errors.EmptyDataError:
        print("The file is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_scholarship_names(folder_path):
    #----------------------------------------------------------
    # Function to print all scholarship names
    #----------------------------------------------------------
    scholarship_files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx") and f != "scholarship.xlsx"]
    
    print("\nList of Scholarships (Alphabetical Order):")
    # Sort the scholarship names alphabetically
    scholarship_names = sorted([os.path.splitext(scholarship_file)[0].replace("_", " ").replace("102023", "").replace("scholarships", "") for scholarship_file in scholarship_files])
    
    for scholarship_name in scholarship_names:
        print(scholarship_name)


def process_file(folder_path, input_file_name):
    #----------------------------------------------------------
    # Function to sort students in scholarship files
    #----------------------------------------------------------
    if input_file_name == "scholarships.xlsx":
        print(f"Skipping file '{input_file_name}' as it will not be processed.")
        return
    
    # Start
    #if input_file_name == 'ECEGeneral.xlsx':

    if input_file_name == 'ECEGeneral.xlsx':
        file_path = os.path.join(folder_path, 'ECEGeneral.xlsx')
        #output_file_path = os.path.join(folder_path, 'Sorted', f"sort_{input_file_name}.csv")
        if input_file_name == 'ECEGeneral.xlsx':
            file_path = os.path.join(folder_path, 'ECEGeneral.xlsx')
            output_file_path = os.path.join(folder_path, 'Sorted', f"sort_{input_file_name}")
            grad_column = 'What is your expected graduation date from college? '

            def change_month(date):
                if pd.notnull(date):
                    month_mapping = {6: 5, 4: 5, 7: 8, 9: 8, 10: 12, 11: 12, 1: 5, 2: 5, 3: 5}
                    return date.replace(month=month_mapping.get(date.month, date.month))
                return date

            def format_season(date):
                if pd.notnull(date):
                    season_map = {5: 'Spring', 8: 'Summer', 12: 'Fall'}
                    season = season_map.get(date.month, '')
                    return f' {date.year} {season}' if season else date.strftime('%Y')
                return date

            df = pd.read_excel(file_path)

            df_filter = df[(df['Cumulative GPA'] >= 3.5)].copy()
            df_filter[grad_column] = pd.to_datetime(df_filter[grad_column], format='%Y/%m/%d', errors='coerce')

            df_complete = df_filter.sort_values(by=[grad_column, 'Cumulative GPA'], ascending=[True, False])
            df_complete[grad_column] = df_complete[grad_column].apply(change_month)
            df_complete[grad_column] = df_complete[grad_column].apply(format_season)

            df_complete.to_excel(output_file_path, index=False, engine='openpyxl')  # Specify 'openpyxl' engine
            print(f"Final sorted data for '{input_file_name}' saved to: {output_file_path}")
            return
    

    '''
    input_file_path = os.path.join(folder_path, input_file_name)

    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file '{input_file_name}' not found. Make sure it is present in the specified scholarship folder.")

    correct_headers = ["Name", "Qualification Points", "Encumbered Funds", "ID", "Expected Grad Date", "Acad Level", "Cumulative GPA", "Major Description", "Total Credits Earned", "Major GPA", "Total Credits Remaining "]

    df = pd.read_excel(input_file_path, engine='openpyxl')

    missing_headers = [header for header in correct_headers if header not in df.columns]
    if missing_headers:
        print(f"Warning: Missing headers {missing_headers} in the input file '{input_file_name}'. This file will be skipped.")
        return  # Skip processing this file

    df_filtered = df[correct_headers].copy()

    df_filtered.loc[:, "Expected Grad Date"] = pd.to_datetime(df_filtered["Expected Grad Date"]).dt.to_period('M')

    # Create the Sorted folder if it doesn't exist
    sorted_folder = os.path.join(folder_path, 'Sorted')
    os.makedirs(sorted_folder, exist_ok=True)

    output_file_path = os.path.join(sorted_folder, f"sort_{input_file_name}")

    df_filtered.to_excel(output_file_path, index=False)
    df_sort = pd.read_excel(output_file_path).copy()

    df_filtered_final = df_sort[(df_sort["Cumulative GPA"] >= 3.5) & (df_sort["Acad Level"] != "Freshman") & (df_sort["Major GPA"] != 0)].copy()
    df_filtered_final.loc[:, "Expected Grad Date"] = pd.to_datetime(df_filtered_final["Expected Grad Date"]).dt.to_period('M')

    # Sorting based on Qualification Points, Expected Grad Date, and Cumulative GPA
    df_filtered_final_sorted = df_filtered_final.sort_values(by=["Qualification Points", "Expected Grad Date", "Cumulative GPA"], ascending=[False, True, False])

    # Update the output file path to include "_sort"
    output_file_path = os.path.join(sorted_folder, f"sort_{input_file_name}")

    df_filtered_final_sorted.to_excel(output_file_path, index=False, header=True)

    print(f"Final sorted data for '{input_file_name}' saved to: {output_file_path}")
    '''

    input_file_path = os.path.join(folder_path, input_file_name)

    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file '{input_file_name}' not found. Make sure it is present in the specified scholarship folder.")

    # Read the Excel file
    df = pd.read_excel(input_file_path, engine='openpyxl')

    # Convert 'Expected Grad Date' column to datetime
    df.loc[:, "Expected Grad Date"] = pd.to_datetime(df["Expected Grad Date"]).dt.to_period('M')

    # Create the Sorted folder if it doesn't exist
    sorted_folder = os.path.join(folder_path, 'Sorted')
    os.makedirs(sorted_folder, exist_ok=True)

    # Define the output file path
    output_file_path = os.path.join(sorted_folder, f"sort_{input_file_name}")

    # Sort the DataFrame based on specified criteria
    df_sorted = df[(df["Cumulative GPA"] >= 3.5) & (df["Acad Level"] != "Freshman") & (df["Major GPA"] != 0)].copy()
    df_sorted = df_sorted.sort_values(by=["Qualification Points", "Expected Grad Date", "Cumulative GPA"], ascending=[False, True, False])

    # Write the sorted DataFrame to Excel
    df_sorted.to_excel(output_file_path, index=False, header=True)

    print(f"Final sorted data for '{input_file_name}' saved to: {output_file_path}")


def calculate_budget(folder_path):
    #----------------------------------------------------------
    # Function used to calculate budget for each student
    #----------------------------------------------------------
    '''
    gpa = row['Cumulative GPA']
    grad_date = row['Expected Grad Date']

    if pd.notna(gpa) and pd.notna(grad_date):
        gpa = float(gpa)
        year, month = map(int, grad_date.split('-'))

        if month == 12 and gpa >= 4.0 and year == 2023:  # December graduation with 4.0 GPA
            return 4000  # Half of the maximum allotted amount
        if month == 5 and gpa == 4.0:  # May graduation with 4.0 GPA
            return 2000  # Maximum allotted amount
        if month == 12 and year == 2024 and gpa == 4.0:  # December graduation with GPA decrease in the following academic year
            return 4000
        if month == 5 and year == 2024 and gpa == 4.0:  # May graduation with GPA decrease in the following academic year
            return 3000
        if month == 12 and gpa <= 4.0 and gpa > 3.8 and year == 2023:
            return 3500
        if month == 12 and gpa <= 3.8 and gpa > 3.6 and year == 2023:
            return 3000
        if month == 12 and gpa <= 3.6 and gpa > 3.4 and year == 2023:
            return 2500
        else:
            return 1000  # Default case if none of the conditions are met

    return 0  # Default value if conditions are not met
    '''
    input_file_name = 'sort_ECEGeneral.xlsx'
    input_file_path = os.path.join(folder_path, 'Sorted', input_file_name)

    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_name}' not found.")
        return

    output_file_name = 'budget_ECEGeneral.xlsx'
    output_file_path = os.path.join(folder_path, 'Sorted', output_file_name)

    # Read the input file
    df = pd.read_excel(input_file_path)

    # Select relevant columns
    selected_columns = ['ID', 'What is your expected graduation date from college? ', 'Cumulative GPA']

    # Create a new DataFrame with selected columns
    df_selected = df[selected_columns].copy()

    # Create a new column 'Budget' based on GPA
    df_selected['Budget'] = df_selected['Cumulative GPA'].apply(lambda x: 4000 if x == 4.0 else None)

    # Save the new DataFrame to the output file
    df_selected.to_excel(output_file_path, index=False, engine='openpyxl')

    print(f"Budget calculation completed. File saved to: {output_file_path}")


def duplicate_and_update_excel(input_path, output_path):
    #----------------------------------------------------------
    # Function used to update the scholarship files
    #----------------------------------------------------------
    # Read the original Excel file
    df = pd.read_excel(input_path)

    # Add a new column called "Budget" at the end
    df['Budget'] = df.apply(calculate_budget, axis=1)

    # Write the updated DataFrame to a new Excel file
    df.to_excel(output_path, index=False)


print_message()
print()
print('Program imports os, datetime from datetime, re, and pandas as pd')
print()


while True:
    print('Ensure all required files are downloaded and organized into a designated folder located on the computer desktop. \nFolder should include all downloaded scholarship files and overview of scholarship file\nAccess the folder by specifying its name through input.')
    folder_name = input("Enter Folder Name: ")

    if folder_name.strip():
        folder_path = os.path.join(os.path.expanduser("~"), "Desktop", folder_name)

        if os.path.exists(folder_path):
            print(f"\nThank you for selecting '{folder_name}' as your folder.\n")
            break  # Exit the loop if a valid folder is selected
        else:
            print(f"Folder '{folder_name}' not found on the desktop. Please provide a valid folder name.")
    else:
        print("Invalid folder name. Please provide a valid folder name.")

print('Input "H" for Help')

while True:
    print()
    print_main_menu()

    choice = input("Enter option (1/2/3/4/5/6/7/8): ").strip()

    if choice == '1':
        read_scholarship_data(folder_path, "scholarships")
    elif choice == '2':
        scholarship_name = input("Enter the name of the scholarship: ").strip()
        read_student_data(folder_path, scholarship_name)
    elif choice == '3':
        print_scholarship_names(folder_path)
    #elif choice == '4':
    #    scholarship_name = input("Enter the name of the scholarship: ").strip()
    #    save_student_and_scholarship_data(folder_path, scholarship_name, 'StudentAndScholarship.txt')
    elif choice == '4':
        # Get a list of all files in the folder
        all_files = os.listdir(folder_path)

        # Iterate through the files and process each one
        for file_name in all_files:
            if file_name.endswith(".xlsx"):
                process_file(folder_path, file_name)
        #print("Thank you for using the scholarship program!")
    elif choice == '5':
        calculate_budget(folder_path)
        #base_folder = folder_path
        #input_file = os.path.join(base_folder, 'Sorted', 'sort_ECEGeneral.xlsx')  # Modified file name
        #output_file = os.path.join(base_folder, 'Sorted', 'sort_ECEGeneral_updated.xlsx')
        # Duplicate and update the Excel file
        #duplicate_and_update_excel(input_file, output_file)
    elif choice == '6':
        print('Match')
    elif choice == '7':
        print("Which scholarship would you like to modify: ")
        file_name = "scholarship.xlsx" 
        print("Scholarship 1: XXXX")
        print("Scholarship 2: XXXX")
        print("Scholarship 3: XXXX")
        with open(file_name, 'r') as file:
            # 
            pass 
    elif choice == '8' or choice.lower() == 'q' or choice == 'Q':
        print("Thank you for using the scholarship program!")
        break
    elif choice == 'H':
        print()
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
        
    else:
        print("Invalid choice. Please enter a valid option.")
