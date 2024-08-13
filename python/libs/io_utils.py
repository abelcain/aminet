# libs/io_utils.py

def load(filepath):
    """Load data from a file into a list."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            # Read each line, strip whitespace, and ignore empty lines
            items = [line.strip() for line in file if line.strip()]
        return items
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []
    except IOError as e:
        print(f"Error reading file: {e}")
        return []

def save(filepath, items):
    """Save a list of items to a file."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            for item in items:
                file.write(item + '\n')
    except IOError as e:
        print(f"Error writing to file: {e}")
