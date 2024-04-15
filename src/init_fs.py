# init_fs.py is a script that sets up the project structure for a new project
import os
import platform
import subprocess

def create_hidden_directory(directory):
    os_name = platform.system()
    if os_name == 'Windows':
        # On Windows, make the directory and set it as hidden
        os.makedirs(directory, exist_ok=True)
        subprocess.run(['attrib', '+H', directory], check=True)
    elif os_name in ['Linux', 'Darwin']:
        # On Unix-like systems, just prepend a dot to make it hidden
        if not directory.startswith('.'):
            directory = '.' + directory
        os.makedirs(directory, exist_ok=True)
    return directory

def setup_project_structure(root_dir):
    data_dir = 'data'
    data_directories = ['scholarships', 'general_application', 'output']

    os.makedirs(os.path.join(root_dir, data_dir), exist_ok=True)

    for dir in data_directories:
        os.makedirs(os.path.join(root_dir, data_dir, dir), exist_ok=True)

    create_hidden_directory(os.path.join(root_dir, 'localAppData'))

    print("Project structure created")

def init_fs():
    root_dir = os.getcwd() # Get the current working directory
    print(f"Setting up project structure in: {root_dir}")
    setup_project_structure(root_dir)


def main():
    init_fs()

if __name__ == "__main__":
    main()
