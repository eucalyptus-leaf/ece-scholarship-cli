#input.py

def read_student_data(student_file):
    try:
        # Read the student data from the Excel file
        student_data = pd.read_excel(student_file)

        # Print the student data
        print("\nStudent Data:")
        print(student_data)

    except FileNotFoundError:
        print("File not found. Please provide a valid file name.")
    except pd.errors.EmptyDataError:
        print("The file is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_scholarship_data(scholarship_file):
    try:
        # Read the scholarship data from the Excel file
        scholarship_data = pd.read_excel(scholarship_file)

        # Print the scholarship data
        print("\nScholarship Data:")
        print(scholarship_data)

    except FileNotFoundError:
        print("File not found. Please provide a valid file name.")
    except pd.errors.EmptyDataError:
        print("The file is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")
