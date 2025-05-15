@echo off
setlocal enabledelayedexpansion

:: Get commit message from user
set /p commit_message=Enter your commit message: 

:: Add all changes
git add .

:: Commit with the provided message
git commit -m "%commit_message%"

:: Push to both repositories
echo Pushing to first repository...
git push origin main

echo Pushing to second repository...
git push github main

echo Git operations completed successfully!
pause