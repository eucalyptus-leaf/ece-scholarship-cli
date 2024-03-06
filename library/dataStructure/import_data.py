import re
import os
import glob
import pandas as pd
from library.dataStructure.student import Student


class Headers:
    def __init__(self):
        self.header_fp = "None"
        self.normalized_fp = "None"
        self.headers = []
        self.normalized_headers = []

    # Function to normalize headers
    def _normalize_header(self, header):
        return re.sub(r'\s+', '', header).lower()

    # Function to read and normalize headers from user file
    def normalize_and_save_headers(self, input_file, output_file):
        with open(input_file, 'r') as file:
            self.headers = [line.strip() for line in file if line.strip()]

        self.normalized_headers = [self._normalize_header(header) for header in self.headers]

        file.close()

        with open(output_file, 'w') as outfile:
            for header in self.normalized_headers:
                outfile.write(header + '\n')

        outfile.close()
    
    def print_headers(self):
        print(self.headers, '\n')

def import_students_from_file(folder_path, studentTab, h):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(('.csv', '.xlsx', '.xls')) and os.path.isfile(os.path.join(folder_path, f))]
        if len(files) == 0:
            print("No files found in the specified directory")
            return False
        else:
            print("Files found in the specified directory: ", len(files))
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
            print("Latest file: ", latest_file)
            file_path = os.path.join(folder_path, latest_file)
    except:
        print("Error: Could not find the specified directory")
        return False
    
    # Read the file into a dataframe
    if file_path.endswith('.csv'):
        try:
            df = pd.read_csv(file_path)
        except:
            print(f"Error: Could not read the {file_path}")
            return False
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        try: 
            df = pd.read_excel(file_path)
        except:
            print(f"Error: Could not read the {file_path}")
            return False
    else:
        print("Error: File type not supported")
        return False
    
    #print(df.head()) # DEBUG: Print the first 5 rows of the dataframe
    # Iterate through the rows
    for index, row in df.iterrows():
        student = Student()

        student.first_name = row[h.headers[54]]
        student.middle_name = row[h.headers[55]]
        student.last_name = row[h.headers[53]]
        student.student_id = row[h.headers[52]]
        student.application_id = row[h.headers[1]]
        student.email = row[h.headers[6]]
        for header in df.columns:
            student.attributes[header] = row[header]

        studentTab.insert(student.student_id, student)

    return True



def import_scholarships_from_file(csv_path):
    pass
