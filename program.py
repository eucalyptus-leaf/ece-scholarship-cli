import os
import pandas as pd 

def print_main_menu():
    print("Main Menu:\n")
    print("1. Print Scholarship List")
    print("2. Print Student List")
    print("3. Print Names of Scholarships")
    print("4. Save in text file")
    print("5. Sort")
    print("6. Budget")
    print("7. Quit\n")


def read_student_data(folder_path, scholarship_name):
    try:
        # Adjust the scholarship name for ECEGeneral
        if scholarship_name == "ECEGeneral":
            file_path = os.path.join(folder_path, f"{scholarship_name}.xlsx")
        else:
            file_path = os.path.join(folder_path, f"{scholarship_name}_102023.xlsx")


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
    scholarship_files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx") and f != "scholarship.xlsx"]
    
    print("\nList of Scholarships (Alphabetical Order):")
    # Sort the scholarship names alphabetically
    scholarship_names = sorted([os.path.splitext(scholarship_file)[0].replace("_", " ").replace("102023", "").replace("scholarships", "") for scholarship_file in scholarship_files])
    
    for scholarship_name in scholarship_names:
        print(scholarship_name)


def process_file(folder_path, input_file_name):
    if input_file_name == "schplarship.xlsx":
        print(f"Skipping file '{input_file_name}' as it will not be processed.")
        return

    input_file_path = os.path.join(folder_path, input_file_name)

    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file '{input_file_name}' not found. Make sure it is present in the specified scholarship folder.")

    correct_headers = ["Name", "Qualification Points", "Encumbered Funds", "ID", "Expected Grad Date", "Acad Level", "Cumulative GPA", "Major Description", "Total Credits Earned", "Major GPA", "Total Credits Remaining "] 

    df = pd.read_excel(input_file_path)

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
    df_filtered_final_sorted = df_filtered_final.sort_values(by=["Expected Grad Date", "Cumulative GPA"], ascending=[True, False])
    
    # Update the output file path to include "_sort"
    output_file_path = os.path.join(sorted_folder, f"sort_{input_file_name}")

    df_filtered_final_sorted.to_excel(output_file_path, index=False, header=True)

    print(f"Final sorted data for '{input_file_name}' saved to: {output_file_path}")


def calculate_budget(row):
    gpa = row['Cumulative GPA']
    grad_date = row['Expected Grad Date']

    if pd.notna(gpa) and pd.notna(grad_date):
        gpa = float(gpa)
        year, month = map(int, grad_date.split('-'))

        if month == 12 and gpa >= 4.0 and year == 2023:  # December graduation with 4.0 GPA
            return 2000  # Half of the maximum allotted amount
        elif month == 5 and gpa == 4.0:  # May graduation with 4.0 GPA
            return 4000  # Maximum allotted amount
        elif month == 12 and year == 2024 and gpa == 4.0:  # December graduation with GPA decrease in the following academic year
            return 4000
        elif month == 5 and year == 2024 and gpa == 4.0:  # May graduation with GPA decrease in the following academic year
            return 3000
        elif month == 12 and gpa <= 4.0 and gpa > 3.8 and year == 2023:
            return 3500
        elif month == 12 and gpa <= 3.8 and gpa > 3.6 and year == 2023:
            return 3000
        elif month == 12 and gpa <= 3.6 and gpa > 3.4 and year == 2023:
            return 2500
        else:
            return 1000  # Default case if none of the conditions are met

    return 0  # Default value if conditions are not met

def duplicate_and_update_excel(input_path, output_path):
    # Read the original Excel file
    df = pd.read_excel(input_path)

    # Add a new column called "Budget" at the end
    df['Budget'] = df.apply(calculate_budget, axis=1)

    # Write the updated DataFrame to a new Excel file
    df.to_excel(output_path, index=False)



# Prompt the user for input with a clear message
print("|*************************************|")
print("| Welcome to the Scholarship Program  |")
print("| Please enter the name of the folder.|")
print("|*************************************|\n")
#folder_name = input("Folder Name on Desktop: ")

while True:
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

while True:
    print()
    print_main_menu()

    choice = input("Enter option (1/2/3/4/5/6/7): ").strip()

    if choice == '1':
        read_scholarship_data(folder_path, "scholarships")
    elif choice == '2':
        scholarship_name = input("Enter the name of the scholarship: ").strip()
        read_student_data(folder_path, scholarship_name)
    elif choice == '3':
        print_scholarship_names(folder_path)
    elif choice == '4':
        scholarship_name = input("Enter the name of the scholarship: ").strip()
        save_student_and_scholarship_data(folder_path, scholarship_name, 'StudentAndScholarship.txt')
    elif choice == '5':
        # Get a list of all files in the folder
        all_files = os.listdir(folder_path)

        # Iterate through the files and process each one
        for file_name in all_files:
            if file_name.endswith(".xlsx"):
                process_file(folder_path, file_name)
        #print("Thank you for using the scholarship program!")
    elif choice == '6':
        base_folder = folder_path
        input_file = os.path.join(base_folder, 'Sorted', 'sort_ECEGeneral.xlsx')  # Modified file name
        output_file = os.path.join(base_folder, 'Sorted', 'sort_ECEGeneral_updated.xlsx')
        # Duplicate and update the Excel file
        duplicate_and_update_excel(input_file, output_file)
    elif choice == '7' or choice.lower() == 'q':
        print("Thank you for using the scholarship program!")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
