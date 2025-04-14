#!/bin/bash

# Exit on error
set -e

# Function to check if we're in the right directory
check_project_dir() {
    if [ ! -f "requirements.txt" ]; then
        echo "Error: requirements.txt not found. Make sure you're in the 7th-ave-trains directory."
        echo "Current directory: $(pwd)"
        exit 1
    fi
}

echo "Setting up 7th Ave Trains Display..."

# Store the project directory
PROJECT_DIR="$PWD"
check_project_dir

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-full \
    git \
    build-essential \
    python3-dev \
    python3-pillow \
    gcc \
    make \
    libgraphicsmagick++-dev \
    libwebp-dev \
    libjpeg-dev \
    libpng-dev \
    pkg-config \
    python3-numpy \
    python3-setuptools \
    libatlas-base-dev

# Clone and build rpi-rgb-led-matrix
echo "Setting up RGB LED Matrix library..."
cd ~
if [ -d "rpi-rgb-led-matrix" ]; then
    echo "Removing existing RGB Matrix library..."
    sudo rm -rf rpi-rgb-led-matrix
fi

# Clone with regular user permissions
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd ~/rpi-rgb-led-matrix

# Build with optimizations for Raspberry Pi
echo "Building RGB Matrix C++ library..."
cd ~/rpi-rgb-led-matrix/lib
sudo make clean
export CFLAGS="-O2 -fPIC"
export CXXFLAGS="$CFLAGS"
sudo make -j4 RGB_LIB_DISTRIBUTION=1 HARDWARE_DESC=2

# Build Python bindings
echo "Building Python bindings..."
cd ~/rpi-rgb-led-matrix/bindings/python
sudo make clean
sudo make build-python HARDWARE_DESC=2 PYTHON=$(which python3) CFLAGS="-O2 -fPIC" RGB_LIB_DISTRIBUTION=1

if [ ! -f "build/lib."*"/rgbmatrix/_core."*".so" ]; then
    echo "Error: Failed to build RGB Matrix Python bindings"
    echo "Build directory contents:"
    ls -R build/
    exit 1
fi

# Install project dependencies
echo "Installing project dependencies..."
cd "$PROJECT_DIR"
pip3 install -r requirements.txt

# Install RGB Matrix Python module
echo "Installing RGB Matrix Python module..."
cd ~/rpi-rgb-led-matrix/bindings/python
sudo rm -rf build dist *.egg-info  # Clean any existing build artifacts

# Set specific build flags for aarch64 architecture
export CFLAGS="-O2 -fPIC"
export CXXFLAGS="$CFLAGS"
export LDFLAGS=""

# Install the RGB Matrix module
pip3 install --upgrade numpy wheel
pip3 install -e .

# Return to project directory
cd "$PROJECT_DIR"

echo "Creating run script..."
cat > run.sh << EOF
#!/bin/bash

# Check if running as root
if [ "\$(id -u)" != "0" ]; then
   echo "This script must be run as root (use sudo)" 1>&2
   exit 1
fi

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "Error: Must be run from the 7th-ave-trains directory"
    exit 1
fi

# Start the API server in the background
echo "Starting API server..."
python3 main.py &
API_PID=\$!

# Wait a moment for the API to start
sleep 2

# Start the LED controller
echo "Starting LED display controller..."
python3 led_matrix_controller.py

# When LED controller exits, kill the API server
kill \$API_PID
EOF

# Make run script executable
sudo chmod +x run.sh

# Verify installation
echo -e "\nSetup complete! To run the display:"
echo "  cd $PROJECT_DIR"
echo "  sudo ./run.sh"

# Verify RGB Matrix installation
echo ""
echo "Verifying RGB Matrix installation..."
python3 -c "import rgbmatrix; print('RGB Matrix installed successfully')" 