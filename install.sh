#!/bin/bash

echo "============================================================"
echo "  Google Instant Indexer - Installation Script"
echo "============================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Error creating virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error installing dependencies"
    exit 1
fi

echo "✓ All dependencies installed"
echo ""

# Create necessary directories
mkdir -p logs
mkdir -p results

echo "✓ Directories created"
echo ""

echo "============================================================"
echo "  Installation Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. For CLI usage:"
echo "   source venv/bin/activate"
echo "   python quick_start.py"
echo ""
echo "2. For Web Interface:"
echo "   source venv/bin/activate"
echo "   python web_app.py"
echo "   Then open: http://localhost:5000"
echo ""
echo "3. For Google API (optional but recommended):"
echo "   - Set up service account in Google Cloud Console"
echo "   - Download JSON key file"
echo "   - Update paths in quick_start.py or web_app.py"
echo ""
echo "See README.md for detailed setup instructions"
echo "============================================================"
