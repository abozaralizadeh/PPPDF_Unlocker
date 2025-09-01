#!/bin/bash

# PDF Unlocker Setup Script
echo "🔧 Setting up PDF Unlocker..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🚀 To use the PDF Unlocker:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the script: python pdf_unlocker.py"
echo ""
echo "📖 For more options, run: python pdf_unlocker.py --help"
echo ""
echo "🔓 The script now uses multiple methods (pikepdf, pdfrw, PyPDF2) for better unlocking success!"
