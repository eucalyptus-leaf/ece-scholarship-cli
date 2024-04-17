
import os
import re
import pandas as pd
from library.student import Student
from library.scholarship import Scholarship

class Headers:
    def __init__(self):
        self.header_fp = "None"
        self.normalized_fp = "None"
        self.overview_header_fp = "None"
        self.headers = []
        self.normalized_headers = []
        self.overview_headers = []
        self.normalized_overview_headers = []
        self.header_map = {}
        self.overview_header_map = {}

    def to_dict(self):
        return {
            "header_fp": self.header_fp,
            "normalized_fp": self.normalized_fp,
            "overview_header_fp": self.overview_header_fp,
            "headers": self.headers,
            "normalized_headers": self.normalized_headers,
            "overview_headers": self.overview_headers,
            "normalized_overview_headers": self.normalized_overview_headers,
            "header_map": self.header_map,
            "overview_header_map": self.overview_header_map
        }
    
    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.header_fp = data['header_fp']
        obj.normalized_fp = data['normalized_fp']
        obj.overview_header_fp = data['overview_header_fp']
        obj.headers = data['headers']
        obj.normalized_headers = data['normalized_headers']
        obj.overview_headers = data['overview_headers']
        obj.normalized_overview_headers = data['normalized_overview_headers']
        obj.header_map = data['header_map']
        obj.overview_header_map = data['overview_header_map']
        return obj

    # Function to normalize headers
    def _normalize_header(self, header):
        return re.sub(r'\s+', '', header).lower()

    # Function to read and normalize headers from user file
    def normalize_and_save_headers(self, input_file, output_file, overview_file = False):
        with open(input_file, 'r') as file:
            headers = [line.strip() for line in file if line.strip()]
        
        normalized_headers = [self._normalize_header(header) for header in headers]

        if overview_file:
            self.overview_headers = headers
            self.normalized_overview_headers = normalized_headers
            self.overview_header_map = {i : header for i, header in enumerate(headers)}
        else:
            self.headers = headers
            self.normalized_headers = normalized_headers
            self.header_map = {i : header for i, header in enumerate(headers)}

        with open(output_file, 'w') as outfile:
            if overview_file:
                for header in self.overview_headers:
                    outfile.write(header + '\n')
            else:
                for header in self.normalized_headers:
                    outfile.write(header + '\n')

    def get_header(self, index):
        return self.header_map.get(index)
    
    def get_overview_header(self, index):
        return self.overview_header_map.get(index)

    def print_headers(self):
        print(self.headers, '\n')

def import_students_from_file(h, budget, folder_path, studentTab):
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
        student = Student(h, budget)

        student.first_name = row[h.get_header(54)] # Line 55 in headers.txt
        student.middle_name = row[h.get_header(55)] # Line 56 in headers.txt
        student.last_name = row[h.get_header(53)] # Line 54 in headers.txt
        student.student_id = row[h.get_header(52)] # Line 53 in headers.txt
        student.application_id = row[h.get_header(1)] # Line 2 in headers.txt
        student.email = row[h.get_header(6)] # Line 7 in headers.txt
        for header in df.columns:
            student.attributes[header] = row[header]

        # studentTab.insert(student.application_id, student) # TO-DO: remove before deployment...used for copying fake student data to excel
        studentTab.insert(student.student_id, student) 

    return True

def _extract_scholarship_id(view_column_data):
    # Using regex to extract the ID from the href link
    match = re.search(r'opportunities/(\d+)/applications', view_column_data)
    if match:
        return int(match.group(1))  # Return the extracted ID
    else:
        return None  # Or some default value or raise an exception
    
def import_scholarships_from_file(h, budget, folder_path, scholarshipTab, studentTab):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(('.csv', '.xlsx', '.xls')) and os.path.isfile(os.path.join(folder_path, f))]
        if len(files) == 0:
            print("No files found in the specified directory")
            return False
        else:
            print("Files found in the specified directory: ", len(files))
            # Process each file
            new_student_counter = 0 # TO-DO: remove before deployment...used for copying fake student data to excel
            for file in files:
                print("Processing file: ", file)
                file_path = os.path.join(folder_path, file)
                
                # Read the file into a DataFrame
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_path)
                else:
                    print("Error: File type not supported")
                    continue  # Skip unsupported file types
                
                scholarship = None

                # Process each row in the DataFrame
                for index, row in df.iterrows():
                    # student_id = row[h.get_header(1)] # TO-DO: remove before deployment...used for copying fake student data to excel
                    student_id = row[h.get_header(52)] # Line 2 in headers.txt
                    student = studentTab.get(student_id)
                    if student is None:
                        # print(f"Error: Student with application ID {student_id} not found")
                        # print(f"Creating a new student for application ID {student_id}")
                        student = Student(h, budget)
                        student.first_name = row[h.get_header(54)] # Line 55 in headers.txt
                        student.middle_name = row[h.get_header(55)] # Line 56 in headers.txt
                        student.last_name = row[h.get_header(53)] # Line 54 in headers.txt
                        student.student_id = row[h.get_header(52)] # Line 53 in headers.txt
                        student.application_id = row[h.get_header(1)] # Line 2 in headers.txt
                        student.email = row[h.get_header(6)] # Line 7 in headers.txt

                        new_student_counter += 1 # TO-DO: remove before deployment...used for copying fake student data to excel
                        generate_new_student_id_for_new_student(student, new_student_counter) # TO-DO: remove before deployment...used for copying fake student data to excel
                        
                        for header in df.columns:
                            student.attributes[header] = row[header]

                        student.attributes['General Application Score'] = 0
                        studentTab.insert(student.student_id, student)
                    
                    # write_to_df(student,index, df) # TO-DO: remove before deployment...used for copying fake student data to excel

                    if index == 0:
                        scholarship = Scholarship(h, budget)

                    if scholarship is None:
                        print("Error: Scholarship object not initialized correctly at creation when reading files.")
                        continue

                    id = _extract_scholarship_id(row[h.get_header(0)]) # Line 1 in headers.txt
                    if id is None:
                        print("Error: Could not extract scholarship ID")
                        continue  # Skip if ID can't be extracted
                    
                    # Create Scholarship object and populate with data
                    scholarship.scholarship_id = id
                    student.priority.append(id)
                    # scholarship.application_id = id # TO-DO: remove before deployment...used for copying fake student data to excel
                    
                    # Add other scholarship attributes as necessary
                    scholarship.add_student(student_id, studentTab[student_id]) # (student_id:Student object)
                    # scholarship.students.update({student.application_id:student}) # TO-DO: remove before implementation...used for copying fake student data to excel

                    # Add each scholarship to the scholarshipTab
                    scholarshipTab.insert(scholarship.scholarship_id, scholarship)

                # # Sort the students in the scholarship 
                # scholarship.sort_students() # TO-DO: remove before deployment...testing sort priority
                
                # df.to_excel(file_path, index=False, engine='openpyxl') # TO-DO: remove before deployment...used for copying fake student data to excel
            for scholarship in scholarshipTab:
                # Sort the students in the scholarship
                scholarship.sort_students()
                # scholarship.find_priority_students() # TO-DO: remove before deployment...testing sort priority

        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def import_overview_scholarships_from_file(h, folder_path, scholarshipTab):
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
    
    for index, row in df.iterrows():
        id = row[h.get_overview_header(1)]
        scholarshipTab[id].priority = row[h.get_overview_header(0)]
        scholarshipTab[id].name = row[h.get_overview_header(2)]
        scholarshipTab[id].budget = row[h.get_overview_header(3)]
        scholarshipTab[id].working_budget = scholarshipTab[id].budget
        #scholarshipTab[id].criteria = row[h.get_overview_header(4)].split('; ') was used for old overview file
        scholarshipTab[id].num_awards = row[h.get_overview_header(4)]

    return True

def generate_new_student_id_for_new_student(student, new_student_counter): # TO-DO: remove before deployment...used for copying fake student data to excel
    new_student_number = 1000 + new_student_counter # TO-DO: remove before deployment...used for copying fake student data to excel
    student.first_name = 'John' + str(new_student_number) # TO-DO: remove before deployment...used for copying fake student data to excel
    student.middle_name = 'Todd' + str(new_student_number) # TO-DO: remove before deployment...used for copying fake student data to excel
    student.last_name = 'Doe' + str(new_student_number) # TO-DO: remove before deployment...used for copying fake student data to excel
    student.student_id = new_student_number # TO-DO: remove before deployment...used for copying fake student data to excel
    student.email = 'jdoe' + str(new_student_number) + '@ncsu.edu' # TO-DO: remove before deployment...used for copying fake student data to excel

def write_to_df(student,index, df): # TO-DO: remove before deployment...used for copying fake student data to excel
    df.loc[index, 'Student ID'] = student.student_id # TO-DO: remove before deployment...used for copying fake student data to excel
    df.loc[index, 'Name'] = f"{student.last_name}, {student.first_name}" # TO-DO: remove before deployment...used for copying fake student data to excel
    df.loc[index, 'Primary Email'] = student.email # TO-DO: remove before deployment...used for copying fake student data to excel
    df.loc[index, 'First Name'] = student.first_name # TO-DO: remove before deployment...used for copying fake student data to excel
    df.loc[index, 'Last Name'] = student.last_name # TO-DO: remove before deployment...used for copying fake student data to excel
    df.loc[index, 'Middle Name'] = student.middle_name # TO-DO: remove before deployment...used for copying fake student data to excel
