def sort_paths(text):
    """Sorts paths so that files with extensions appear after directories at the same level."""
    # Split the text into a list of paths
    paths = text.strip().splitlines()
    
    # Sort the paths
    sorted_paths = sorted(paths, key=lambda p: (p.count('/'), p.split('/')[-1].count('.'), p))
    
    return '\n'.join(sorted_paths)

# Reading from the input file
with open("miniData.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Applying the function to sort the text
sorted_text = sort_paths(text)

# Writing the sorted text to the output file
with open("minidump.txt", "w", encoding="utf-8") as file:
    file.write(sorted_text)
