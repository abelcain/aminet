def extract_types(paths: List[str]) -> Set[str]:
    """Extract unique file types from a list of paths."""
    types = set()
    
    for path in paths:
        for part in path.split('/'):
            if '.' in part:
                typ = part.rsplit('.', 1)[-1]
                types.add(typ.lower())  # Normalize to lowercase
    
    return types

with open("Data.txt", "r", encoding="utf-8") as file:
    paths = [line.strip() for line in file if line.strip()]

types = set()
    
for path in paths:
    # Process each path and extract types
    parts = path.split('/')
    for part in parts:
        if '.' in part:
            # Extract the type from the last segment after the last '.'
            typ = part.rsplit('.', 1)[-1]
            types.add(typ.lower())  # Use lowercase for consistency

with open("minidump.txt", "w", encoding="utf-8") as file:
    for typ in types:
        file.write(typ + '\n')