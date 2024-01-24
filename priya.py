import pandas as pd
import os

def get_top_student(df):
    # Assuming the DataFrame is already sorted, return the first student
    return df.iloc[0]

def main():
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Set the folder path to the 'scholarships' subfolder
    folder_path = os.path.join(script_dir, 'scholarships')
    awarded_students = set()  # To track students who have already been awarded
    awarded_scholarships = []  # List to store scholarship award data

    # Loop through each file in the 'scholarships' directory
    for file in os.listdir(folder_path):
        if file.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_excel(file_path)

                # Check if the top student has already been awarded
                while not df.empty:
                    top_student = get_top_student(df)
                    student_id = top_student['ID']

                    if student_id not in awarded_students:
                        awarded_students.add(student_id)
                        scholarship_name = file.split('_')[0]  # Extract scholarship name from file name
                        print(f"Scholarship: {scholarship_name}, Awarded to: {student_id}")
                        awarded_scholarships.append({'Scholarship': scholarship_name, 'Student ID': student_id})
                        break
                    else:
                        # Remove the top student and check the next one
                        df = df.iloc[1:]
            except FileNotFoundError:
                print(f"File not found: {file}")
            except pd.errors.EmptyDataError:
                print(f"The file is empty: {file}")
            except Exception as e:
                print(f"An error occurred while processing {file}: {e}")

    # Create a DataFrame from the awarded scholarships list
    awards_df = pd.DataFrame(awarded_scholarships)
    # Write the DataFrame to an Excel file in the 'scholarships' folder
    output_path = os.path.join(folder_path, 'awarded_scholarships.xlsx')
    awards_df.to_excel(output_path, index=False)
    print(f"Awarded scholarships have been saved to {output_path}")

if __name__ == "__main__":
    main()
