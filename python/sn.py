import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=r"90'+iopº",
  database="GPT"
)

mycursor = mydb.cursor()

def get_file_type_id(extension):
    select_query = f"SELECT id FROM FileTypes WHERE type = '{extension}';"
    print(select_query)
    # mycursor.execute(select_query)
    # result = mycursor.fetchone()
    # if result:
    #     return result[0]
    # else:
    #     insert_query = f"INSERT INTO FileTypes (type) VALUES ('{extension}');"
    #     print(insert_query)
    #     # mycursor.execute(insert_query)
    #     # mydb.commit()
    #     # return mycursor.lastrowid

def add_to_directory_structure(name, parent_id, type_id):
    insert_query = f"INSERT INTO DirectoryStructure (name, parent_id, type) VALUES ('{name}', {parent_id}, {type_id});"
    print(insert_query)
    # mycursor.execute(insert_query)
    # mydb.commit()

text = """
disk.info
Utilities.info
Utilities
Utilities/MultiView.info
Utilities/MultiView
"""

lines = text.strip().split('\n')

for line in lines:
    if '/' in line:
        directory, file_name = line.split('/')
        extension = file_name.split('.')[-1] if '.' in file_name else None
        type_id = get_file_type_id(extension) if extension else None
        add_to_directory_structure(file_name, directory, type_id)
    else:
        extension = line.split('.')[-1] if '.' in line else None
        type_id = get_file_type_id(extension) if extension else None
        add_to_directory_structure(line, None, type_id)
