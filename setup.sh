#!/bin/bash

echo "Setting up 7th Ave Trains Display..."

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git build-essential python3-dev python3-pillow

# Clone and build rpi-rgb-led-matrix
echo "Setting up RGB LED Matrix library..."
cd ~
if [ ! -d "rpi-rgb-led-matrix" ]; then
    git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
    cd rpi-rgb-led-matrix
    
    # Build with optimizations
    CFLAGS="-O3" make -C lib
    
    # Build Python bindings with specific RPi 4 flags
    cd bindings/python
    make build-python HARDWARE_DESC=2 PYTHON=$(which python3) CFLAGS="-O3"
    sudo make install-python
fi

# Setup virtual environment and install dependencies
echo "Setting up Python environment and dependencies..."
cd ~/7th-ave-trains
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating run script..."
cat > run.sh << EOF
#!/bin/bash

# Check if running as root
if [ "\$(id -u)" != "0" ]; then
   echo "This script must be run as root (use sudo)" 1>&2
   exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Start the API server in the background
echo "Starting API server..."
python3 main.py &
API_PID=\$!

# Wait a moment for the API to start
sleep 2

# Start the LED controller with recommended flags
echo "Starting LED display controller..."
python3 led_matrix_controller.py

# When LED controller exits, kill the API server
kill \$API_PID
EOF

# Make run script executable
chmod +x run.sh

echo "Setup complete! To run the display:"
echo "  cd ~/7th-ave-trains"
echo "  sudo ./run.sh" 