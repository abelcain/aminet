def extract_extensions(paths):
    """Extracts a set of unique file extensions from a list of paths."""
    extensions = set()
    for path in paths:
        for part in path.split('/'):
            if '.' in part:
                extension = part.split('.')[-1]
                extensions.add(extension)
    return extensions

def format_directory_structure(paths, extensions):
    """Formats a list of file/directory paths into a hierarchical structure.
    
    Args:
      paths: A list of file/directory paths.
      extensions: A set of file extensions to be recognized.
    Returns:
      A formatted string representing the hierarchical directory structure.
    """
    tree = {}
    
    for path in paths:
        parts = path.split('/')
        current_level = tree
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        
        last_part = parts[-1]
        if '.' in last_part:
            base_name, ext = last_part.rsplit('.', 1)
            if ext in extensions:
                if base_name:
                    if base_name not in current_level:
                        current_level[base_name] = {f'.{ext}': {}}
                    elif isinstance(current_level[base_name], dict):
                        current_level[base_name][f'.{ext}'] = {}
                else:
                    current_level[f'.{ext}'] = {}
            else:
                if last_part not in current_level:
                    current_level[last_part] = {}
        else:
            if last_part not in current_level:
                current_level[last_part] = {}
    
    def build_output(node, indent=""):
        output = ""
        for item in sorted(node.keys()):
            output += f"{indent}{item}\n"
            output += build_output(node[item], indent + "  ")
        return output
    
    return build_output(tree)

    """Formats a list of file/directory paths into a hierarchical structure.
    
    Args:
      paths: A list of file/directory paths.
    Returns:
      A formatted string representing the hierarchical directory structure.
    """
    tree = {}
    for path in paths:
        parts = path.split('/')
        current_level = tree
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        
        last_part = parts[-1]
        if last_part.endswith('.info'):
            base_name = last_part[:-5]  # remove '.info'
            if base_name:
                if base_name not in current_level:
                    current_level[base_name] = {'.info': {}}
                elif isinstance(current_level[base_name], dict):
                    current_level[base_name]['.info'] = {}
            else:
                current_level['.info'] = {}
        else:
            if last_part not in current_level:
                current_level[last_part] = {}
    
    def build_output(node, indent=""):
        output = ""
        for item in sorted(node.keys()):
            output += f"{indent}{item}\n"
            output += build_output(node[item], indent + "  ")
        return output
    
    return build_output(tree)

# Extract extensions from paths
with open("miniData.txt", "r", encoding="utf-8") as file:
    paths = [line.strip() for line in file if line.strip()]

extensions = extract_extensions(paths)

# Format directory structure based on the extracted extensions
formatted_output = format_directory_structure(paths, extensions)

# Write the formatted output to a file
with open("minidump.txt", "w", encoding="utf-8") as file:
    file.write(formatted_output)

# Optionally print the output for verification
print(formatted_output)
