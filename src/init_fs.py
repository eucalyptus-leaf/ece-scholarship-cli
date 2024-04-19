# init_fs.py is a script that sets up the project structure for a new project
import os
import platform
import subprocess
import pandas as pd


def create_hidden_directory(root_dir, folder_name):
    os_name = platform.system()
    # Convert the Path object to a string for compatibility with os.path.join

    if os_name == 'Windows':
        # On Windows, make the directory and set it as hidden
        directory = os.path.join(root_dir, folder_name)
        os.makedirs(directory, exist_ok=True)
        subprocess.run(['attrib', '+H', directory], check=True)
    elif os_name in ['Linux', 'Darwin']:
        # On Unix-like systems, just prepend a dot to make it hidden
        if not folder_name.startswith('.'):
            folder_name = '.' + folder_name
            directory = os.path.join(root_dir, folder_name)
        os.makedirs(directory, exist_ok=True)
    return directory

def setup_project_structure(root_dir, data_dir, config_dir):
    print("Creating project structure...")
    data_directories = ['scholarships', 'general_application', 'output']

    os.makedirs(data_dir, exist_ok=True) # Create the data directory
    #os.makedirs(config_dir, exist_ok=True) # Create the config directory

    for dir in data_directories: # Create the subdirectories in the data directory
        os.makedirs(os.path.join(data_dir, dir), exist_ok=True)

    os.makedirs(os.path.join(data_dir, 'scholarships', 'overview'), exist_ok=True)

    hidden_path = create_hidden_directory(root_dir, 'local')

    print("Project structure created")

    return hidden_path

def initialize_configuration_files(data_path, config_path):
    create_scholarship_template(data_path)
    # TO-DO: Create other configuration files as needed


def init_fs(root_dir, data_path, config_path):
    hidden_path = setup_project_structure(root_dir, data_path, config_path)
    initialize_configuration_files(data_path, config_path)
    return hidden_path

def create_scholarship_template(data_dir):
    """Creates a scholarship overview template excel file in the data/scholarships/overview directory"""
    template_file = os.path.join(data_dir, 'scholarships', 'overview', 'scholarship_overview_template.xlsx')

    if os.path.exists(template_file):
        return
    
    template_headers = ["Award Sequence", "Scholarship ID", "Scholarship Name", "Scholarship Budget", "Maximum Number of Awards Allowed"]
    template_data = pd.DataFrame(columns=template_headers)
    template_data.to_excel(template_file, index=False)
    print(f"Created scholarship overview template at: {template_file}")