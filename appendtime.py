import os
import time

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

# Run the rename_files function in a loop
while True:
    rename_files("C:\\Users\\adam.riggs\\Documents\\EssaiToolBox\\Data\\tooldott\\")
    # Sleep for 60 seconds before running the loop again
    time.sleep(5)
