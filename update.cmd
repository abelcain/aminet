
@echo off
setlocal

REM Change to the directory of your repository
cd /d C:\Users\PC\Documents\GitHub\aminet

REM Append to .gitignore if not already present
findstr /C:.DS_Store .gitignore >nul || echo .DS_Store >> .gitignore
findstr /C:python/.venv/ .gitignore >nul || echo python/.venv/ >> .gitignore

REM Stage all changes
git add .

REM Commit with a message
git commit -m "Add new files from python folder"

REM Push changes to the main branch
git push origin main

echo Changes have been committed and pushed to the remote repository.

endlocal
