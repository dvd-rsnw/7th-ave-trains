#!/bin/bash

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Try to activate the virtual environment
source .venv/bin/activate 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment."
    exit 1
fi

# Check if Python is running from the virtual environment
PYTHON_PATH=$(which python)
if [[ $PYTHON_PATH != *".venv"* ]]; then
    echo "❌ Python is not running from virtual environment."
    echo "Current Python: $PYTHON_PATH"
    exit 1
fi

# Check if pip is from the virtual environment
PIP_PATH=$(which pip)
if [[ $PIP_PATH != *".venv"* ]]; then
    echo "❌ Pip is not running from virtual environment."
    echo "Current pip: $PIP_PATH"
    exit 1
fi

# Print confirmation message
echo "✅ Virtual environment is properly activated."
echo "Python path: $PYTHON_PATH"
echo "Pip path: $PIP_PATH"

# Check for installed packages
echo ""
echo "Installed packages:"
pip list

# Check if rgbmatrix is installed
if pip list | grep -q rgbmatrix; then
    echo ""
    echo "✅ RGB Matrix module is installed."
else
    echo ""
    echo "⚠️ RGB Matrix module not found in the virtual environment."
fi

# Deactivate virtual environment
deactivate 