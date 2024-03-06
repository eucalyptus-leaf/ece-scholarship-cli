# import.py
import pandas as pd
import os
import glob
import sys

# Append the parent directory (or any other necessary directory) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library.dataStructure.student import Student
from library.dataStructure.scholarship import Scholarship

def import_students_from_file(folder_path, studentTab):
    """
    Using pandas to read the csv file, iterate throught the row and insert the student into the hash table
    studentTab is a hash table with the student ID as the key and the student object as the value
    csv_path is the path to the csv file
    define the Student methods, first_name, last_name, student_id, application_id, and email directly but any other header and value should go in the attributes dictionary of the student object by using the column header as they key and value in the row as the value to assign to that key
    """
    # create a patter for all .xlsx files in the directory
    pattern = os.path.join(folder_path, "*.csv")

    # Find all files matching the pattern
    files = glob.glob(pattern)

    # Iterate through the files
    for file in files:
        print(f"Reading file: {file}") # DEBUG: Print the file name
        # Read the file
        df = pd.read_csv(file)
        print(df.head()) # DEBUG: Print the first 5 rows of the dataframe
        # Iterate through the rows
        for index, row in df.iterrows():
            student = Student()
            student.first_name = row['first_name']
            student.last_name = row['last_name']
            student.student_id = row['student_id']
            student.application_id = row['application_id']
            student.email = row['email']
            print(f"Inserting student: {student}") # DEBUG: Print the student object
            for header in df.columns:
                if header not in ['first_name', 'last_name', 'student_id', 'application_id', 'email']:
                    student.attributes[header] = row[header]
            studentTab.insert(student.student_id, student)

def import_scholarships_from_file(csv_path):
   pass
