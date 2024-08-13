import re
import mysql.connector
from typing import List, Set
from libs import connect_db, load, save
from mysql.connector import Error

def fetch_types():
    """Fetch all types from the database and return as a dictionary."""
    conn = connect_db()
    global DIR_TYPE_ID 
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            # Fetch the DIR ID first
            cursor.execute("SELECT id FROM types WHERE type = 'dir'")  # Case-sensitive search for 'dir'
            dir_id_result = cursor.fetchone()
            if dir_id_result:
                DIR_TYPE_ID = dir_id_result['id']

            cursor.execute('SELECT id, type FROM types')
            types = cursor.fetchall()

            return {type_data['type'].lower(): type_data['id'] for type_data in types}
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
        #print(f"Inserted {inserted_count} types into the database.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            #print("Database connection closed.")
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
    
    if dir_type == DIR_TYPE_ID:
        formatted_name = name
    else:
        formatted_name = name + '.' + str(dir_type)

    directory_structure.append({
        'ID': new_id,
        'PARENT': parent_id,
        'NAME': formatted_name,
        'TYPE': dir_type
    })
    return new_id

def insert_into_database(items):
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
        
        cursor.executemany(add_directory, [(item['PARENT'], item['NAME'], item['TYPE']) for item in items])

        conn.commit()
        # print("Inserted items into the database.")
    except Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            # print("Database connection closed.")
def load_paths(filepath: str) -> List[str]:
    """Load paths from a file."""
    return load(filepath)
def process_file(file_path):
    """Process the file to extract and insert directory structure."""
    paths = load_paths("Data.txt")
    types = extract_types(paths)
    # insert_types_to_db(types)
    # Load and process data
    input_data = load(file_path)
    file_types = fetch_types()
    directory_structure = []

    for line in input_data:
        parts = line.strip().split('/')
        parent_id = None
        current_id = None

        for part in parts:
            file_name, *extension = part.split('.', 1)
            file_type = file_types.get(''.join(extension).upper(), file_types.get('DIR', 1))

            current_id = get_or_create_directory_id(parent_id, file_name, file_type, directory_structure)
            parent_id = current_id
    
    # Insert all items into the database
    insert_into_database(directory_structure)
    
    # Print results
    print("DIRECTORYSTRUCTURE")
    print("-" * 20)
    print("ID\tPARENT\tNAME\tTYPE")
    for item in directory_structure:
        print(f"{item['ID']}\t{item['PARENT'] or 'NULL'}\t{item['NAME']}\t{item['TYPE']}")

if __name__ == "__main__":
    process_file("Data.txt")
