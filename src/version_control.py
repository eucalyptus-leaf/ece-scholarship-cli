import sys
import os
import pkg_resources
import subprocess

REQUIRED_PYTHON = "3.11"

def read_dependencies(file_path):
    with open(file_path, 'r') as file:
        dependencies = file.readlines()
    return [dependency.strip() for dependency in dependencies]

def generate_required_packages(dependencies):
    required_packages = {}
    for dependency in dependencies:
        package, version = dependency.split('==')
        required_packages[package] = version
    return required_packages

def check_python_version():
    if sys.version_info < tuple(map(int, REQUIRED_PYTHON.split('.'))):
        raise AssertionError(f"Python {REQUIRED_PYTHON} or later is required.")

def check_package_versions(required_packages):
    for package, required_version in required_packages.items():
        installed_version = pkg_resources.get_distribution(package).version
        # if installed package version is less than the required version, raise an error
        # else let is pass
        # if installed_version != required_version:
        #     raise AssertionError(f"Package {package} requires version {required_version}, found version {installed_version}.")

        if installed_version < required_version:
            raise AssertionError(f"{package} version {required_version} or later is required, but {installed_version} is installed.")


        
def find_dependencies_file(start_dir, max_look_back=1, current_look_back=0):
    if current_look_back > max_look_back:
        raise FileNotFoundError("Could not find dependencies.txt file within the maximum look back limit.")
    
    # First, search downwards from the current directory
    for dirpath, dirnames, filenames in os.walk(start_dir):
        if "dependencies.txt" in filenames:
            return os.path.join(dirpath, "dependencies.txt")
    # If not found, search upwards in the directory tree w/ maximum look back limit
    parent_dir = os.path.dirname(start_dir)
    if parent_dir != start_dir:
        return find_dependencies_file(parent_dir, max_look_back, current_look_back + 1)
    raise FileNotFoundError("Could not find dependencies.txt file in the directory tree.")

def version_control():
    try:
        # Get the directory of the current script
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        dependencies_file_path = find_dependencies_file(curr_dir)

        dependencies = read_dependencies(dependencies_file_path)
        required_packages = generate_required_packages(dependencies)

        check_python_version()
        check_package_versions(required_packages)

        print("All version checks passed.")

    except (AssertionError, FileNotFoundError) as e:
        print(f"Version check failed: {e}")
        sys.exit(1)

def main():
    version_control()

if __name__ == "__main__":
    main()
