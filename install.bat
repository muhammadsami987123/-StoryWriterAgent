@echo off
echo ================================================
echo   StoryWriterAgent - One-Click Installation
echo   Day 36 of #100DaysOfAI-Agents
echo ================================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Verifying installation...
python test_installation.py

echo.
echo ================================================
echo   Installation Complete!
echo ================================================
echo.
echo   To start the application:
echo     1. Activate venv: venv\Scripts\activate
echo     2. Run: python main.py --web
echo.
echo   Or run: python main.py --terminal
echo.
pause
