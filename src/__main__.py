# Import System Libraries
import sys
from pathlib import Path

def is_pyInstaller_run():
	"""
	Returns True if the application is running as a PyInstaller bundle.
	"""
	return getattr(sys, 'frozen', False)

def get_base_path(frozen):
	""" Determine the base path where the application should store and look for files. """
	if frozen:
		# Running in a bundle
		return Path(sys.executable).parent
	else:
		# Running live
		return Path(__file__).resolve().parent.parent
	
def print_welcome():
    #----------------------------------------------------------
    # Function to print greeting message at the beginning
    #----------------------------------------------------------
    print("|****************************************************************************|")
    print("|                                                                            |")
    print("|            ------------------------------------------------                |")
    print("|                    Welcome to the Scholarship Program                      |")
    print("|            ------------------------------------------------                |")
    print("|                FA23-SP24 ECE-485 Senior Design Project                     |")
    print("|                    North Carolina State University                         |")
    print("|                                                                            |")
    print("|        Copyright:  Gavin Jones, Loevan Bost, Priya Tella, Josh Turki       |")
    print("|                    Contact: copyright@gavinjones.me                        |")
    print("|                                                                            |")
    print("|****************************************************************************|\n")
	
def main():
	print_welcome()

	frozen = is_pyInstaller_run()

	project_path = get_base_path(frozen)
	data_path = project_path / 'data'
	# config_path = project_path / 'config'
	config_path = Path(sys._MEIPASS) if frozen else project_path / 'config'

	if not frozen:
		print("Running directly from Python script, checking dependencies...")
		from src.version_control import version_control as vc
		vc(config_path / 'dependencies.txt') # System Version Control...Check and install dependencies

	# Import Custom Modules
	from src.scholarship_cli import CLI_system
	# Import Custom Functions
	from src.init_fs import init_fs as ifs

	hidden_path = ifs(str(project_path), str(data_path), str(config_path)) # Initialize the project file structure

	system = CLI_system(str(hidden_path), str(data_path), str(config_path))
	system.run_cli()

	# TO-DO: Implement Error System Catches for the CLI System

if __name__ == "__main__":
	main()
