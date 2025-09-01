@echo off
REM PDF Unlocker Setup Script for Windows

echo 🔧 Setting up PDF Unlocker...

REM Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is not installed. Please install Python 3.6 or higher.
    pause
    exit /b 1
)

echo ✅ Python 3 found
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo 📥 Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Setup complete!
echo.
echo 🚀 To use the PDF Unlocker:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the script: python pdf_unlocker.py
echo.
echo 📖 For more options, run: python pdf_unlocker.py --help
echo.
echo 🔓 The script now uses multiple methods (pikepdf, pdfrw, PyPDF2) for better unlocking success!
pause
