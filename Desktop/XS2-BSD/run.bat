@echo off
REM ==============================
REM  Auto Commit & Push Script
REM ==============================

REM ----- Set your project folder here -----
set REPO_FOLDER=C:\Users\Steven\Desktop\XS2-BSD

cd /d "%REPO_FOLDER%"

REM Check if inside a git repository
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo ERROR: This folder is not a Git repository.
    pause
    exit /b
)

echo.
echo =============================
echo   Git Auto Commit & Push
echo =============================
echo.

REM Accept commit message from user (or use a default)
set /p COMMIT_MSG=Enter commit message (leave blank for default): 

if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Auto commit from batch script
)

echo Adding files...
git add .

echo Committing with message: "%COMMIT_MSG%"
git commit -m "%COMMIT_MSG%"

echo Pushing to remote...
git push

echo.
echo Commit and push complete!
pause