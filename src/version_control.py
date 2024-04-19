import sys
import subprocess

REQUIRED_PYTHON = "3.11"

def read_dependencies(dependencies_path):
    try:
        with open(dependencies_path, 'r') as file:
            dependencies = [line.strip() for line in file if line.strip()]
        return dependencies
    except FileNotFoundError:
        print(f"Error: The file {dependencies_path} does not exist. Aborting program.")
        sys.exit(1)

def get_installed_packages():
    result = subprocess.run([sys.executable, '-m', 'pip', '--disable-pip-version-check', 'list'], stdout=subprocess.PIPE, text=True)
    installed_packages = {}
    for line in result.stdout.split('\n'):
        if line and 'Package' not in line and '----' not in line:
            parts = line.split()
            if len(parts) == 2:
                package, version = parts
                installed_packages[package.lower()] = version
    return installed_packages

def check_and_install_packages(dependencies):
    installed_packages = get_installed_packages()
    for dependency in dependencies:
        package, required_version = dependency.split('==')
        if package.lower() in installed_packages:
            installed_version = installed_packages[package.lower()]
            if installed_version < required_version:
                print(f"{package} version {installed_version} is installed, but version {required_version} is required.")
                prompt_install(package, required_version)
        else:
            print(f"{package} is not installed.")
            prompt_install(package, required_version)

def prompt_install(package, version):
    response = input(f"Do you want to install/update {package}? (yes/no): ").lower().strip()
    if response== 'yes' or response == 'y':
        response = input(f"Would you like to install the latest version of {package}? (yes/no): ").lower().strip()
        if response == 'yes' or response == 'y':
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check', f"{package}"])
            print(f"Version {version} of {package} has been installed.\n")
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check', f"{package}=={version}"])
            print(f"Version {version} of {package} has been installed.\n")
    else:
        if response == 'no' or response == 'n':
            print(f"{package} was not installed.\n Aborting program.")
            sys.exit(1)
        else:
            print("Invalid response. Please enter 'yes' or 'no'.")
            prompt_install(package, version)

def version_control(dependencies_path):
    dependencies = read_dependencies(dependencies_path)
    check_and_install_packages(dependencies)
    print("All required packages are correctly installed and up to date.")
