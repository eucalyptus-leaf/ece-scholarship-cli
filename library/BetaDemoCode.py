'''-------------------------------------------------------------------
File name: project.py
Description: This file contains the main user intertface and options
             for the scholarship application project

ECE Scholarship Application
Team 32
April 2024
-------------------------------------------------------------------'''

import os
import pandas as pd 
import re
from datetime import datetime

id_total_list = []

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
    print("2. Print Names of Scholarships       (Prints the names of all scholarships)")     
    print("3. Sort                              (Sorts all individual and general scholarship files)")
    print("4. Match                             (Awards scholarship to students)")       
    #print("5. Modify                            (User manually awards money to student)")
    print("5. Quit                              (Quit by inputting number '5', 'Q', or 'q')\n")


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


def compare_student_ids(scholarship_folder_path):
    sorted_folder_path = os.path.join(scholarship_folder_path, "Sorted")

    sorted_files = [file for file in os.listdir(sorted_folder_path) if file.endswith(".xlsx") and file != 'sort_ECEGeneral.xlsx']

    id_files_mapping = {}

    for file_name in sorted_files:
        file_path = os.path.join(sorted_folder_path, file_name)
        try:
            df = pd.read_excel(file_path, usecols=['ID'], engine='openpyxl')
            unique_ids = set(df['ID'])
            for id_num in unique_ids:
                if id_num not in id_files_mapping:
                    id_files_mapping[id_num] = []
                id_files_mapping[id_num].append(file_name)
        except Exception as e:
            print(f"Error occurred while processing file {file_name}: {e}")

    qualified_for_one_scholarship = [id_num for id_num, files in id_files_mapping.items() if len(files) == 1]
    return qualified_for_one_scholarship


def calculate_budget(expected_grad_date, cumulative_gpa):
    #current_year = 2023
    #current_month = 3
    current_year = datetime.now().year
    current_month = datetime.now().month
    grad_year, grad_month = map(int, expected_grad_date.split('-'))
    
    if grad_year == current_year and grad_month >= current_month:
        years_until_graduation = 0
    else:
        years_until_graduation = max(0, (grad_year - current_year) - int(grad_month < current_month))
    
    if years_until_graduation <= 0:
        budget = 2000
    elif years_until_graduation == 1:
        budget = 4000
    elif years_until_graduation == 2:
        budget = 3000
    elif years_until_graduation == 3:
        budget = 2000
    else:
        budget = 0
    
    # Adjust budget based on GPA
    if 3.9 <= cumulative_gpa <= 4.0:
        budget -= 0
    elif 3.8 <= cumulative_gpa < 3.9:
        budget -= 500
    elif 3.7 <= cumulative_gpa < 3.8:
        budget -= 1000
    elif 3.6 <= cumulative_gpa < 3.7:
        budget -= 1500
    elif 3.5 <= cumulative_gpa < 3.6:
        budget -= 2000
    
    # Ensure minimum budget
    if budget < 1000:
        budget = 1000
    
    return budget



def get_student_id():
    awarded_ids = {}
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    scholarship_folder_path = os.path.join(desktop_path, "scholarship")
    scholarships_file_path = os.path.join(scholarship_folder_path, "scholarships.xlsx")

    output_file_path = os.path.join(scholarship_folder_path, "Matched.txt")
    
    try:
        df_project_name = pd.read_excel(scholarships_file_path, skiprows=1)  
    except Exception as e:
        print(f"Error occurred while reading Excel file: {e}")
        return
    
    if 'Project Name' not in df_project_name.columns:
        print("Error: 'Project Name' column not found in the Excel file.")
        return
    
    sorted_folder_path = os.path.join(scholarship_folder_path, "Sorted")
    
    with open(output_file_path, 'w') as output_file:
        output_file.write("Matched Scholarship Applications\n\n")
        print("Matched Scholarship Applications\n\n")
        
        qualified_for_one_scholarship = compare_student_ids(scholarship_folder_path)
        
        for index, row in df_project_name.iterrows():
            x = 1
            first_word = re.split(r'[,\s/]+', str(row["Project Name"]))[0].capitalize()

            matching_files = [file for file in os.listdir(sorted_folder_path) if first_word.lower() in file.lower()]

            if not matching_files:
                print(f"No corresponding file found for '{first_word}'")
                output_file.write(f"No corresponding file found for '{first_word}'\n")
                continue

            corresponding_file_path = os.path.join(sorted_folder_path, matching_files[0])
            try:
                corresponding_df = pd.read_excel(corresponding_file_path, engine='openpyxl')
            except Exception as e:
                print(f"Error occurred while reading Excel file: {e}")
                output_file.write(f"Error occurred while reading Excel file: {e}\n")
                continue

            total_budget = row[" Spending Budget "]

            print(f"Project: {first_word} (Total Budget: ${total_budget})")
            output_file.write(f"Project: {first_word} (Total Budget: ${total_budget})\n")

            try:
                df_gpa_grad_date = pd.read_excel(corresponding_file_path, engine='openpyxl')
            except Exception as e:
                print(f"Error occurred while reading Excel file: {e}")
                output_file.write(f"Error occurred while reading Excel file: {e}\n")
                continue

            remaining_budget = total_budget

            if 'Requirements' in df_project_name.columns:
                requirements = row['Requirements']
                print(f"Requirements for {first_word}: {requirements}")
                output_file.write(f"Requirements for {first_word}: {requirements}\n")
                if "1 student" in str(requirements):
                    for index, row in df_gpa_grad_date.iterrows():
                        student_id = row.get('ID')
                        first_name = row.get('First Name')
                        last_name = row.get('Last Name')
                        id_number = row.get('Student ID')
                        print(f"Project: {first_word} (1 Student, Total Budget: ${total_budget})")
                        output_file.write(f"Project: {first_word} (1 Student, Total Budget: ${total_budget})\n")
                        print(f"   ID: {student_id}, {first_name} {last_name}, Student ID: {id_number} (Awarded: ${total_budget})\n")
                        output_file.write(f"   ID: {student_id}, {first_name} {last_name}, Student ID: {id_number} (Awarded: ${total_budget})\n\n")
                        break
                    continue

            for index, row in df_gpa_grad_date.iterrows():
                student_id = row.get('ID')
                first_name = row.get('First Name')
                last_name = row.get('Last Name')
                id_number = row.get('Student ID')
                if student_id in qualified_for_one_scholarship:
                    spending_budget = calculate_budget(row.get('Expected Grad Date'), row.get('Cumulative GPA'))
                    if spending_budget > remaining_budget:
                        spending_budget = remaining_budget
                        x = 0
                    print(f"   ID: {student_id}, {first_name} {last_name}, Student ID: {id_number} (Awarded: ${spending_budget})")
                    output_file.write(f"   ID: {student_id}, {first_name} {last_name}, Student ID: {id_number} (Awarded: ${spending_budget})\n")
                    awarded_amount = awarded_ids.get(student_id, [0, 0])[0] + spending_budget
                    remaining_amount = calculate_budget(row.get('Expected Grad Date'), row.get('Cumulative GPA')) - awarded_amount
                    awarded_ids[student_id] = [awarded_amount, remaining_amount]
                    remaining_budget -= spending_budget
                    break
                
            if x == 1:
                for index, row in df_gpa_grad_date.iterrows():
                    expected_grad_date = row.get('Expected Grad Date')
                    cumulative_gpa = row.get('Cumulative GPA')

                    if expected_grad_date is None or cumulative_gpa is None:
                        continue

                    student_id = row.get('ID')
                    first_name = row.get('First Name')
                    last_name = row.get('Last Name')
                    id_number = row.get('Student ID')

                    if student_id in awarded_ids:
                        awarded_amount, remaining_amount = awarded_ids[student_id]
                        if remaining_amount <= 0:
                            continue

                    spending_budget = calculate_budget(expected_grad_date, cumulative_gpa)

                    if student_id in awarded_ids:
                        awarded_amount, remaining_amount = awarded_ids[student_id]
                        eligible_amount = spending_budget - awarded_amount
                        if eligible_amount <= 0:
                            continue
                        elif eligible_amount < remaining_budget:
                            spending_budget = eligible_amount

                    if spending_budget <= remaining_budget:
                        # Print student details
                        print(f"   ID: {student_id}, {first_name} {last_name}, Student ID: {id_number} (Awarded: ${spending_budget})")
                        output_file.write(f"   ID: {student_id}, {first_name} {last_name}, Student ID: {id_number} (Awarded: ${spending_budget})\n")

                        # Update awarded and remaining amounts
                        awarded_amount = awarded_ids.get(student_id, [0, 0])[0] + spending_budget
                        remaining_amount = calculate_budget(expected_grad_date, cumulative_gpa) - awarded_amount
                        awarded_ids[student_id] = [awarded_amount, remaining_amount]

                        remaining_budget -= spending_budget
                    else:
                        print(f"   ID: {student_id}, {first_name} {last_name}, Student ID: {id_number} (Awarded: ${remaining_budget})")
                        output_file.write(f"   ID: {student_id}, {first_name} {last_name}, Student ID: {id_number} (Awarded: ${remaining_budget})\n")

                        awarded_amount = awarded_ids.get(student_id, [0, 0])[0] + remaining_budget
                        remaining_amount = calculate_budget(expected_grad_date, cumulative_gpa) - awarded_amount
                        awarded_ids[student_id] = [awarded_amount, remaining_amount]

                        remaining_budget = 0
                        break 

            print()
            output_file.write("\n")

            print()
            output_file.write("\n")




def print_scholarship_names_with_numbers(folder_path):
    """
    Function to print all scholarship names with numbers and handle user selection
    
    Parameters:
        folder_path (str): The path to the folder containing scholarship files
    """
    scholarship_files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx") and f != "scholarship.xlsx" and f != "Matched.txt" and f != "ECEGeneral.xlsx"]
    
    print("\nList of Scholarships:")
    # Sort the scholarship names alphabetically
    scholarship_names = sorted([os.path.splitext(scholarship_file)[0].replace("_", " ").replace("102023", "").replace("scholarships", "") for scholarship_file in scholarship_files if not scholarship_file.endswith(".txt")])
    
    for idx, scholarship_name in enumerate(scholarship_names, start=0):
        if scholarship_name.strip():  # Check if the scholarship name is not empty
            print(f"{idx}. {scholarship_name}")
    
    # Prompt the user to select a scholarship by number
    selected_number = input("Enter the number of the scholarship you want to select: ")
    
    try:
        selected_number = int(selected_number) + 1
        if 1 <= selected_number <= len(scholarship_names):
            selected_scholarship = scholarship_names[selected_number - 1]
            #print(selected_scholarship)
            if selected_scholarship == "JohnSBrown Scholarship ":
                print("Brown")
                first_word = "Brown"
            else:
                first_word = selected_scholarship.split()[0]
                if first_word == "Scholarship":
                    print(" ".join(selected_scholarship.split()[1:]))
                else:
                    print(first_word)
        else:
            print("Invalid selection. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

    selected_id = input("Enter the application ID of the person you want to modify: ")
    #print(selected_id)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    scholarship_folder_path = os.path.join(desktop_path, "scholarship")
    scholarships_file_path = os.path.join(scholarship_folder_path, "scholarships.xlsx")
    sorted_folder_path = os.path.join(scholarship_folder_path, "Sorted")

    matching_files = [file for file in os.listdir(sorted_folder_path) if first_word.lower() in file.lower()]

    if not matching_files:
        print("No corresponding files found.")
    else:
        found = False
        for file in matching_files:
            file_path = os.path.join(sorted_folder_path, file)
            try:
                corresponding_df = pd.read_excel(file_path, engine='openpyxl')
                if 'ID' in corresponding_df.columns:
                    id_column = corresponding_df['ID']
                    for idx, value in id_column.items():
                        if str(value) == selected_id:
                            #print("Match found in file:", file)
                            found = True
                            # Perform further operations if needed
                            total_amount = input("How much would you like to award: ")
                            #print(total_amount)
                            id_total_list.append({'ID': selected_id, 'Total Amount': total_amount})
                            print("Modification Saved")
                            break
            except Exception as e:
                print(f"Error occurred while reading Excel file {file}: {e}")

        if not found:
            print("No match found for the selected ID in file.")


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

    choice = input("Enter option (1/2/3/4/5): ").strip()

    if choice == '1':
        read_scholarship_data(folder_path, "scholarships")
    elif choice == '2':
        print_scholarship_names(folder_path)
    #elif choice == '4':
    #    scholarship_name = input("Enter the name of the scholarship: ").strip()
    #    save_student_and_scholarship_data(folder_path, scholarship_name, 'StudentAndScholarship.txt')
    elif choice == '3':
        # Get a list of all files in the folder
        all_files = os.listdir(folder_path)

        # Iterate through the files and process each one
        for file_name in all_files:
            if file_name.endswith(".xlsx"):
                process_file(folder_path, file_name)
        #print("Thank you for using the scholarship program!")
    elif choice == '4':
        #print('Match')
        get_student_id()
    #elif choice == '5':
    #    print_scholarship_names_with_numbers(folder_path)
        #print(id_total_list)
        #print("Which scholarship would you like to modify: ")
    elif choice == '5' or choice.lower() == 'q' or choice == 'Q':
        print("Thank you for using the scholarship program!")
        break
    elif choice == 'H':
        print()
        print('Help Instructions:')
        print('-------------------------------------------------------------------------------------------------------------')
        print('The program accepts numerical inputs, with each number corresponding to one of the following options.')
        print('1. Option 1 allows for the printing of all scholarship details, including name, budget, and qualifications.')
        print('2. Option 2 displays the names of all available scholarships on the screen.')
        print('3. Option 3 organizes all student based of qualification points within each file.')
        print('4. Option 4 pairs students with their respective eligible scholarships.')
        #print('5. Option 5 allows for user to input awarded money for specific scholarship')
        print('5. Option 5 concludes the program, also triggered by input of "Q" or "q".')
        
    else:
        print("Invalid choice. Please enter a valid option.")
