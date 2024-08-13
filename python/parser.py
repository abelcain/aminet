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

def get_or_create_directory_id(parent_id, name, dir_type):
    conn = connect_db()
    if not conn:
        print("Failed to connect to the database.")
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check if directory exists
        cursor.execute("""
            SELECT id FROM directorystructure
            WHERE parentID = %s AND name = %s
        """, (parent_id, name))
        result = cursor.fetchone()
        
        if result:
            return result['id']
        
        # Insert new directory
        cursor.execute("""
            INSERT INTO directorystructure (parentID, name, type)
            VALUES (%s, %s, %s)
        """, (parent_id, name, dir_type))
        conn.commit()
        
        # Get the new directory ID
        new_id = cursor.lastrowid
        return new_id
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

def process_file(file_path):
    file_types = fetch_types()
    
    if not file_types:
        print("Failed to fetch file types.")
        return
    
    # Load data from file
    lines = load(file_path)
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Assuming the format of each line is "parent_id name file_type"
        parts = line.split()
        if len(parts) < 3:
            print(f"Invalid line format: {line}")
            continue
        
        parent_id = int(parts[0])
        name = parts[1]
        file_type = parts[2].upper()
        
        dir_type = file_types.get(file_type)
        if not dir_type:
            print(f"Unknown file type: {file_type}")
            continue
        
        directory_id = get_or_create_directory_id(parent_id, name, dir_type)
        if directory_id:
            print(f"Processed directory ID: {directory_id}")

if __name__ == "__main__":
    process_file("data.txt")
    # types = fetch_types()
    # lines = load("Data.txt")
    # extensions = extract_types(lines)
    # save("minidump.txt", extensions)
    # print("Available extensions:", extensions)
    # print("Fetched types:", types)
