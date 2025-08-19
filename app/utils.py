from datetime import datetime
import os

def get_shift_name():
    """
    Determine the shift name based on the current time.
    Returns:
        str: The name of the shift ("First", "Second", or "Third").
    """
    current_hour = datetime.now().hour
    print(current_hour) 
    if 6 <= current_hour < 14: # First shift is from 6 AM to 2 PM
        return "First"
    elif 14 <= current_hour < 22: # Second shift is from 2 PM to 10 PM
        return "Second"
    else:
        return "Third" # Third shift is from 10 PM to 6 AM


def delete_files(file_paths:list):
    """
    Delete files if they exist.
    Args:
        file_paths (list): List of file paths to delete.
    """
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)