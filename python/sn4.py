def format_directory_structure(paths):
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
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
    
    def build_output(node, indent=""):
        output = ""
        for item in sorted(node.keys()):
            output += f"{indent}{item}\n"
            output += build_output(node[item], indent + "  ")
        return output
    
    return build_output(tree)

# --- Example Usage ---
with open("miniData.txt", "r", encoding="utf-8") as file:
    paths = [line.strip() for line in file if line.strip()]

formatted_output = format_directory_structure(paths)

with open("minidump.txt", "w", encoding="utf-8") as file:
    file.write(formatted_output)

# If you want to print the output as well
print(formatted_output)