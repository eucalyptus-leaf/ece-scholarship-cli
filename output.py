#output.py

def print_matched_list():
    print()
    print("Scholarship Name              | Student Names (Scholarship Amount)                 ")
    print("-------------------------------------------------------------------------")
    # Replace the following loop with actual scholarship data
    for i in range(1, 4):
        print(f"Scholarship {i}                 |  Student {i} ($XXXX.XX)")
        
        
def save_student_and_scholarship_data(student_file, scholarship_file, output_file):
    try:
        # Read student data from the Excel file
        student_data = pd.read_excel(student_file)

        # Read scholarship data from the Excel file
        scholarship_data = pd.read_excel(scholarship_file)

        # Create a text file and write both student and scholarship information
        with open(output_file, 'w') as file:
            file.write("Student Data:\n")
            file.write(student_data.to_string(index=False))
            file.write("\n\nScholarship Data:\n")
            file.write(scholarship_data.to_string(index=False))

        print(f"Data has been saved to '{output_file}'")

    except FileNotFoundError:
        print("File not found. Please provide valid file names.")
    except pd.errors.EmptyDataError:
        print("One of the files is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")
