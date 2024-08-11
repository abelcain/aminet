import re

# Sample data (replace with actual data from a file or input)
with open("Data.txt", "r", encoding="utf-8") as file:
    input_data = file.read()

# Initialize tables (you might use a database in a real application)
directory_structure = []
file_types = {
    'DIR': 1,
    'FILE': 2,
    'INFO': 3,
    'LIBRARY': 5,
    'PS':6,
    'ANIM':7,
    'PREFS':8,
    'GADGET':9,
    'DEVICE':10,
    'DATATYPE':11
# Add other types as needed
}

# Function to get or create a directory ID
def get_or_create_directory_id(parent_id, name, dir_type):
    for item in directory_structure:
        if item['PARENT'] == parent_id and item['NAME'] == name:
            return item['ID']
    
    new_id = len(directory_structure) + 1
    directory_structure.append({
        'ID': new_id,
        'PARENT': parent_id,
        'NAME': name,
        'TYPE': dir_type
    })
    return new_id

# Process each line of input
for line in input_data.strip().splitlines():
    parts = line.split('/')
    parent_id = None
    current_id = None
    
    for i, part in enumerate(parts):
        file_name, *extension = part.split('.', 1)  # Split filename and extension
        file_type = file_types.get(''.join(extension).upper(), file_types['DIR'])  # Default to DIR if no extension
        
        current_id = get_or_create_directory_id(parent_id, file_name, file_type)
        parent_id = current_id  # Update parent for next iteration

# Print the resulting table (for demonstration)
print("DIRECTORYSTRUCTURE")
print("-" * 20)
print("ID\tPARENT\tNAME\tTYPE")
for item in directory_structure:
    print(f"{item['ID']}\t{item['PARENT'] or 'NULL'}\t{item['NAME']}\t{item['TYPE']}") 