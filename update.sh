#!/bin/bash

# Update .gitignore
echo '.DS_Store' >> .gitignore
echo 'python/.venv/' >> .gitignore

# Stage all changes
git add .

# Commit with a message
git commit -m "Add new files from python folder"

# Push changes to the main branch
git push origin main
