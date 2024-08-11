from collections import defaultdict

def build_tree(paths):
    """Builds a tree structure from the list of file paths."""
    tree = lambda: defaultdict(tree)
    root = tree()

    for path in paths:
        parts = path.split('/')
        current = root
        for part in parts:
            current = current[part]

    return root

def format_tree(tree, indent=0):
    """Formats the tree structure into a string with '-' for indentation."""
    result = []
    for key in sorted(tree.keys()):
        if '.' in key and key.count('.') == 1:  # It's a file
            result.append('-' * indent + key)  # Include full file name
        else:  # It's a directory
            result.append('--' * indent + key)
            result.extend(format_tree(tree[key], indent + 1))
    return result

# Reading from the input file
with open("miniData.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Split the text into paths and build the tree
paths = text.strip().splitlines()
tree = build_tree(paths)

# Format the tree into the desired output format
formatted_text = '\n'.join(format_tree(tree))

# Writing the formatted text to the output file
with open("minidump.txt", "w", encoding="utf-8") as file:
    file.write(formatted_text)

# Optionally print the result for verification
print(formatted_text)
