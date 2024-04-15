# Import System Libraries
import sys
import os
# Import Custom Modules
from src.scholarship_cli import CLI_system
from src.scholarship_cli import print_welcome
# Import Custom Functions
from src.init_fs import init_fs as ifs
from src.version_control import version_control as vc

def main():

	print_welcome()

	vc() # System Version Control
	ifs() # Initialize File System Directories
	project_path = os.path.dirname(__file__)
	print("Project Directory Path: " + project_path + "\n")

	_hidden_path = os.path.join(os.path.dirname(__file__), "localAppData")
	data_path = os.path.join(os.path.dirname(__file__), "data")
	config_path = os.path.join(os.path.dirname(__file__), "config")
	lib_path = os.path.join(os.path.dirname(__file__), "library")
	src_path = os.path.join(os.path.dirname(__file__), "src")

	system = CLI_system(_hidden_path, data_path, config_path, lib_path, src_path)
	system.run_cli()

	# TO-DO: Implement Error System Catches for the CLI System

if __name__ == "__main__":
	main()
