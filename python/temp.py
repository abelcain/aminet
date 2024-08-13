import re
import mysql.connector
from typing import List, Set
from libs import connect_db, load, save
from mysql.connector import Error
def list_dir(directory_structure):
    """Process the directory structure to return a list of unique base directories."""
    processed_set = set()
    
    for line in directory_structure:
        if "/" in line:  # Consider only lines with a '/'
            parts = line.split("/")  # Split by '/'
            for part in parts[:-1]:  # Add each directory part except the last
                processed_set.add(part)  # Add the directory part to the set (ensures uniqueness)
    
    # Return the sorted list of unique directory names
    return sorted(processed_set)
    # return processed_set

# Example usage with directory_structure loaded from a file:
directory_structure = load("data.txt")  # Assuming the 'load' function is available
unique_directories = list_dir(directory_structure)

# Print the resulting unique directories
print("Unique processed directories (unfolded):")
for directory in unique_directories:
    print(directory)