import re
import ee 

from libs import connect_db, load, save
from mysql.connector import Error


def fetch_types():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM types')
            types = cursor.fetchall()
            return types
        finally:
            conn.close()
    return []
def extract_types(lines):
    """Extract types from a list of text lines and update the database."""
    types = set()
    for line in lines:
        for word in line.split():
            if '.' in word:
                type_ = word.split('.')[-1]
                types.add(type_)
    
    conn = connect_db()
    if not conn:
        print("Failed to connect to the database.")
        return []

    try:
        cursor = conn.cursor()
        
        # Insert new types into the database
        for t in types:
            cursor.execute("INSERT IGNORE INTO types (type) VALUES (%s)", (t,))
        
        conn.commit()
        
        # Retrieve all types from the database
        cursor.execute("SELECT type FROM types")
        all_types = [row[0] for row in cursor.fetchall()]
        
        return all_types
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

# Sample data (replace with actual data from a file or input)
with open("Data.txt", "r", encoding="utf-8") as file:
    input_data = file.read()

# Fetch types from the database
types_from_db = fetch_types()

# Create the file_types dictionary
file_types = {}
for type_data in types_from_db:
    type_name = type_data['type'].upper()  # Assuming 'type' is the column name
    type_id = type_data['id']  # Assuming 'id' is the column name for type ID
    file_types[type_name] = type_id

# Initialize tables (you might use a database in a real application)
directory_structure = []
# file_types = {
#     'DIR': 1,
#     'FILE': 2,
#     'INFO': 3,
#     'LIBRARY': 5,
#     'PS':6,
#     'ANIM':7,
#     'PREFS':8,
#     'GADGET':9,
#     'DEVICE':10,
#     'DATATYPE':11
# Add other types as needed
# }

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

def insert_into_database(item):
    cnx = connect_db()
    if not cnx:
        print("Failed to connect to the database.")
        return None
    
    try:
        cursor = cnx.cursor()

        # Insert the item into the directorystructure table
        add_directory = ("INSERT INTO directorystructure "
                       "(parentID, name, type) "
                       "VALUES (%s, %s, %s)")
        data_directory = (item['PARENT'], item['NAME'], item['TYPE'])
        cursor.execute(add_directory, data_directory)

        cnx.commit()
        print(f"Inserted item with ID {item['ID']} into the database.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("Database connection closed.")
for item in directory_structure:
    insert_into_database(item)
print("DIRECTORYSTRUCTURE")
print("-" * 20)
print("ID\tPARENT\tNAME\tTYPE")
for item in directory_structure:
    print(f"{item['ID']}\t{item['PARENT'] or 'NULL'}\t{item['NAME']}\t{item['TYPE']}") 