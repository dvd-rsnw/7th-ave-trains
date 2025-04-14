#!/bin/bash

echo "Checking Python environment and RGB Matrix installation..."
echo ""

# Check virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment is active: $VIRTUAL_ENV"
    PYTHON_PATH=$(which python3)
    echo "   Python path: $PYTHON_PATH"
else
    echo "❌ No active virtual environment detected."
fi

echo ""
echo "Testing RGB Matrix module import:"
python3 -c "
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    print(\"✅ Successfully imported rgbmatrix module\")
    
    # Try to create matrix object
    options = RGBMatrixOptions()
    options.rows = 16
    options.cols = 64
    options.chain_length = 2
    
    print(\"   Attempting to initialize RGB Matrix...\")
    try:
        matrix = RGBMatrix(options=options)
        print(\"✅ Successfully initialized RGB Matrix\")
    except Exception as e:
        print(\"❌ Error initializing RGB Matrix: \" + str(e))
        
    # Try to access functions
    print(\"   Module location: \" + RGBMatrix.__module__)
    print(\"   Available attributes: \" + str(dir(RGBMatrix)[:5]) + \"...\")
    
except ImportError as e:
    print(\"❌ Failed to import rgbmatrix module: \" + str(e))
    import sys
    print(\"   Python path: \" + str(sys.path))
    print(\"   Looking for module in installed packages:\")
    import subprocess
    subprocess.call([\"pip\", \"list\", \"| grep\", \"-i\", \"matrix\"])
    
except Exception as e:
    print(\"❌ Unexpected error: \" + str(e))
"

echo ""
echo "System information:"
python3 -c "
import platform
import os
print(f\"Python version: {platform.python_version()}\")
print(f\"Platform: {platform.platform()}\")
print(f\"Architecture: {platform.machine()}\")
"

echo ""
echo "Checking library dependencies:"
if [ -f "/usr/lib/librgbmatrix.so" ] || [ -f "/usr/local/lib/librgbmatrix.so" ]; then
    echo "✅ Found librgbmatrix.so"
else
    echo "❌ librgbmatrix.so not found in standard locations"
fi

echo ""
echo "Check complete." 