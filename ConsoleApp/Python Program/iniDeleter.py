#This file doesnt do anything anymore and isnt important to the function of the project it was for deleting desktop.ini files
#that were created by the google drive desktop app while it was syncing, these extra files would mess with the code so I had 
# this program deleting them.

import os
import time

dir_path = "C:/Users/chahn/Downloads" 

def search_and_delete_files(path):
    # get list of all files and directories in path
    for file_or_dir in os.listdir(path):
        file_or_dir_path = os.path.join(path, file_or_dir)
        # if file_or_dir is a directory, recursively call function on it
        if os.path.isdir(file_or_dir_path):
            search_and_delete_files(file_or_dir_path)
        # if file_or_dir is a file and named 'desktop.ini', delete it
        elif os.path.isfile(file_or_dir_path) and file_or_dir == "desktop.ini":
            os.remove(file_or_dir_path)
            print(f"Deleted {file_or_dir_path}")

while True:
    search_and_delete_files(dir_path)
    time.sleep(2) # wait for 2 seconds before checking again