def extract_unique_dirs(text):
  """Extracts a sorted list of unique directories from the input text.

  A directory is defined as any word that is followed by a '/'.

  Args:
      text: The input text containing file/directory paths.

  Returns:
      A sorted list of unique directory names.
  """

  dirs = set()
  for line in text.splitlines():
    parts = line.strip().split('/')
    for i, part in enumerate(parts):
      if i < len(parts) - 1:  # Check if it's not the last part (filename)
        dirs.add(part)

  return sorted(list(dirs))

# --- Example Usage (same as before) ---
with open("miniData.txt", "r", encoding="utf-8") as file:
    text = file.read()

unique_dirs = extract_unique_dirs(text)

# Convert the list to a string before writing:
output_text = "\n".join(unique_dirs)  # Join with newlines

with open("minidump.txt", "w", encoding="utf-8") as file:
    file.write(output_text) 