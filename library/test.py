import os
import pandas as pd
import re
from datetime import datetime

def calculate_budget(expected_grad_date, cumulative_gpa):
    current_year = 2023
    current_month = 3
    #current_year = datetime.now().year
    #current_month = datetime.now().month
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


def get_student_id(scholarshipTab, h):
    awarded_ids = {}
    
    # Path to the folder containing scholarships.xlsx
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    scholarship_folder_path = os.path.join(desktop_path, "scholarship")
    scholarships_file_path = os.path.join(scholarship_folder_path, "scholarships.xlsx")

    output_file_path = os.path.join(scholarship_folder_path, "Matched.txt")
    
    try:
        # Read the Excel file with 'Project Name' column
        df_project_name = pd.read_excel(scholarships_file_path, skiprows=1)  
    except Exception as e:
        print(f"Error occurred while reading Excel file: {e}")
        return
    
    # Check if 'Project Name' column exists
    if 'Project Name' not in df_project_name.columns:
        print("Error: 'Project Name' column not found in the Excel file.")
        return
    
    sorted_folder_path = os.path.join(scholarship_folder_path, "Sorted")
    
    with open(output_file_path, 'w') as output_file:
        output_file.write("Matched Scholarship Applications\n\n")
        print("Matched Scholarship Applications\n\n")
        
        # Iterate over each entry in the 'Project Name' column
        for index, row in df_project_name.iterrows():
            # Get the first word from the 'Project Name' column and capitalize only the first word
            first_word = re.split(r'[,\s/]+', str(row["Project Name"]))[0].capitalize()

            # Search for the scholarship in the hash table
            scholarship = None
            for scholarship_id in scholarshipTab:
                if first_word.lower() in scholarshipTab.get(scholarship_id).name.lower():
                    scholarship = scholarshipTab.get(scholarship_id)
                    break

            if scholarship is None:
                print(f"No corresponding scholarship found for '{first_word}'")
                output_file.write(f"No corresponding scholarship found for '{first_word}'\n")
                continue

            # Find the corresponding budget for this project
            total_budget = scholarship.budget

            # Print project name and total budget
            print(f"Project: {scholarship.name} (Total Budget: ${total_budget})")

            remaining_budget = total_budget

            # Iterate over each student in the scholarship
            for student_id, _ in scholarship.students:
                student = studentTab.get(student_id)
                if student is None:
                    continue
                
                # Find the Expected Grad Date and Cumulative GPA
                expected_grad_date = student.attributes.get('Expected Grad Date')
                cumulative_gpa = student.attributes.get('Cumulative GPA')

                if expected_grad_date is None or cumulative_gpa is None:
                    continue

                spending_budget = calculate_budget(expected_grad_date, cumulative_gpa)

                # Check if student has received any money before
                if student_id in awarded_ids:
                    awarded_amount, remaining_amount = awarded_ids[student_id]
                    eligible_amount = spending_budget - awarded_amount
                    if eligible_amount <= 0:
                        continue
                    elif eligible_amount < remaining_budget:
                        spending_budget = eligible_amount

                # Check if remaining budget is sufficient for this student
                if spending_budget <= remaining_budget:
                    # Print student details
                    print(f"   ID: {student_id} (Awarded: ${spending_budget})")

                    # Update awarded and remaining amounts
                    awarded_amount = awarded_ids.get(student_id, [0, 0])[0] + spending_budget
                    remaining_amount = calculate_budget(expected_grad_date, cumulative_gpa) - awarded_amount
                    awarded_ids[student_id] = [awarded_amount, remaining_amount]

                    remaining_budget -= spending_budget
                else:
                    print(f"   ID: {student_id} (Awarded: ${remaining_budget})")

                    awarded_amount = awarded_ids.get(student_id, [0, 0])[0] + remaining_budget
                    remaining_amount = calculate_budget(expected_grad_date, cumulative_gpa) - awarded_amount
                    awarded_ids[student_id] = [awarded_amount, remaining_amount]

                    remaining_budget = 0
                    break

            print()

# Assuming scholarshipTab and h are available from your previous code
get_student_id(scholarshipTab, h)
