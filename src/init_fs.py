# init_fs.py is a script that sets up the project structure for a new project
import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f"Directory {path} already exists")

def setup_project_structure(root_dir):
    data_dir = 'data'
    data_directories = ['scholarships', 'general_application', 'output']

    create_directory(os.path.join(root_dir, data_dir))
    print(f"Created {data_dir} directory")

    for dir in data_directories:
        create_directory(os.path.join(root_dir, data_dir, dir))
        print(f"Created {dir} directory")

    print("Project structure created")

def init_fs():
    root_dir = os.getcwd() # Get the current working directory
    print(f"Setting up project structure in: {root_dir}")
    setup_project_structure(root_dir)


def main():
    init_fs()

if __name__ == "__main__":
    main()
