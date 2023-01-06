import os

def rename_files(directory):
    # navigate to the specified directory
    os.chdir(directory)

    # rename the files
    for file in os.listdir():
        if file.startswith("__"):
            # extract the characters you want to keep from the file name
            new_name = file[2:7]
            # rename the file
            os.rename(file, f"{new_name}_TOOL.T")
