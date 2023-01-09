import os
import time
import configparser

def get_modified_date(file_path):
    # Get the modified time of the file
    modified_time = time.gmtime(os.path.getmtime(file_path))
    # Format the time as a string in the desired format
    return time.strftime("%m-%d_%H%M", modified_time)

def rename_files(root_dir):
    # Walk through all subdirectories under the root directory
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(root, file)
            # Get the modified date as a string
            modified_date = get_modified_date(file_path)
            # Check if the modified date is already in the file name
            if modified_date not in file:
                # Rename the file by appending the modified date to the end of the file name
                # before the file extension
                base, extension = os.path.splitext(file_path)
                new_file_name = f"{base}_{modified_date}{extension}"
                os.rename(file_path, new_file_name)

# Parse the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the root directory path from the configuration file
root_dir = config['PATHS']['tool_t_path']

# Wait 2 mins before starting the process to allow time for files to be downloaded
time.sleep(120)
# Run the rename_files function in a loop
while True:
    rename_files(root_dir)
    # Sleep for 900 seconds (15 mins) before running the loop again
    time.sleep(900)
