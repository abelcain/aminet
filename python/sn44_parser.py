import re
import mysql.connector
from typing import List, Set
from libs import connect_db, load, save
from mysql.connector import Error

# Global variable to control NULL handling
USE_ZERO = True  # Set to True to use 0 instead of NULL, False to use NULL

def fetch_lastID():
    global LAST_ID
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT MAX(id) AS max_id FROM aminet.directorystructure")
            result = cursor.fetchone()
            if result and result['max_id'] is not None:
                LAST_ID = result['max_id']
            else:
                LAST_ID = 0  # Or your desired default value
        finally:
            conn.close()

def fetch_types():
    """Fetch all types from the database and return as a dictionary."""
    global DIR_TYPE_ID 
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM types WHERE type = 'dir'")  # Case-sensitive search for 'dir'
            dir_id_result = cursor.fetchone()
            if dir_id_result:
                DIR_TYPE_ID = dir_id_result['id']
        finally:
            conn.close()   
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT id, type FROM types')
            types = cursor.fetchall()
            return {type_data['type'].upper(): type_data['id'] for type_data in types}
        finally:
            conn.close()
    return {}

def extract_types(paths: List[str]) -> Set[str]:
    """Extract unique file types from a list of paths and insert them into the database."""
    conn = connect_db()
    if not conn:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        inserted_count = 0  # Keep track of inserted types

        for path in paths:
            for part in path.split('/'):
                if '.' in part:
                    typ = part.rsplit('.', 1)[-1].lower()  # Normalize to lowercase
                    try:
                        cursor.execute("INSERT IGNORE INTO types (type) VALUES (%s)", (typ,))
                        inserted_count += 1
                    except Error as e:
                        print(f"Error inserting type '{typ}': {e}")

        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def insert_types_to_db(types: Set[str]):
    """Insert extracted types into the database."""
    conn = connect_db()
    if not conn:
        print("Failed to connect to the database.")
        return
    
    try:
        cursor = conn.cursor()
        
        for typ in types:
            cursor.execute("INSERT IGNORE INTO types (type) VALUES (%s)", (typ,))
        
        conn.commit()
        print(f"Inserted {len(types)} types into the database.")
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

def get_or_create_directory_id(parent_id, name, dir_type, directory_structure):
    """Get existing directory ID or create a new directory record."""
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

def insert_into_database(items):
    global LAST_ID
    """Insert multiple directory items into the database."""
    conn = connect_db()
    if not conn:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()

        add_directory = ("INSERT INTO directorystructure "
                         "(parentID, name, type) "
                         "VALUES (%s, %s, %s)")

        data_to_insert = []
        for item in items:
            # Determine values for ID and PARENT
            id_value = int(item['ID']) if item['ID'] is not None else (0 if USE_ZERO else 'NULL')
            parent_value = int(item['PARENT']) if item['PARENT'] not in [None, 'None'] else (0 if USE_ZERO else 'NULL')

            # Add LAST_ID to the values
            id_with_last = id_value + LAST_ID
            parent_with_last = parent_value + LAST_ID if parent_value != 0 else (0 if USE_ZERO else 'NULL')

            data_to_insert.append((parent_with_last, item['NAME'], item['TYPE']))

        cursor.executemany(add_directory, data_to_insert)

        conn.commit()
        print("Inserted items into the database.")
    except Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def load_paths(filepath: str) -> List[str]:
    """Load paths from a file."""
    return load(filepath)

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

def process_file(file_path):
    """Process the file to extract and insert directory structure."""
    global LAST_ID
    paths = load_paths("Data.txt")
    types = extract_types(paths)
    # insert_types_to_db(types)
    # Load and process data
    input_data = load(file_path)
    file_types = fetch_types()
    directory_structure = []
    fetch_lastID()
    for line in input_data:
        parts = line.strip().split('/')
        parent_id = None
        current_id = None

        for part in parts:
            file_name, *extension = part.split('.', 1)
            file_type = file_types.get(''.join(extension).upper(), file_types.get('DIR', DIR_TYPE_ID))
            current_id = get_or_create_directory_id(parent_id, file_name, file_type, directory_structure)
            parent_id = current_id
    
    # Insert all items into the database
    insert_into_database(directory_structure)
    
    # Print results
    print("DIRECTORYSTRUCTURE")
    print("-" * 20)
    print("ID\tPARENT\tNAME\tTYPE")
    
    for item in directory_structure:
        # Ensure ID is not None and can be converted to integer
        id_value = int(item['ID']) if item['ID'] is not None else (0 if USE_ZERO else 'NULL')
        
        # Ensure PARENT is not None and can be converted to integer
        parent_value = int(item['PARENT']) if item['PARENT'] not in [None, 'None'] else (0 if USE_ZERO else 'NULL')

        # Add LAST_ID to the values
        id_with_last = id_value + LAST_ID
        parent_with_last = parent_value + LAST_ID if parent_value != 0 else (0 if USE_ZERO else 'NULL')

        # Print the formatted output
        print(f"{id_with_last}\t{parent_with_last}\t{item['NAME']}\t{item['TYPE']}")

if __name__ == "__main__":
    process_file("Data.txt")