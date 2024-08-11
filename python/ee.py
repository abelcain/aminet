def extract_extensions(text):
    extensions = set()
    for word in text.split():
        if '.' in word:
            extension = word.split('.')[-1]
            extensions.add(extension)
    return extensions

with open("Data.txt", "r", encoding="utf-8") as file:
    paths = [line.strip() for line in file if line.strip()]

extensions = set()
for path in paths:
    for word in path.split('/'):
        if '.' in word:
            extension = word.split('.')[-1]
            extensions.add(extension)

with open("minidump.txt", "w", encoding="utf-8") as file:
    for extension in extensions:
        file.write(extension + '\n')