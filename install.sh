#!/bin/bash
set -euo pipefail

echo "======================================================================"
echo "        7th Avenue Trains LED Matrix Display Setup Wizard"
echo "======================================================================"

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    build-essential \
    git \
    python3-dev \
    python3-pip \
    libgraphicsmagick++-dev \
    cython3

# Clean up apt cache
sudo rm -rf /var/lib/apt/lists/*

# Clone and build rpi-rgb-led-matrix
if [ ! -d "/tmp/rpi-rgb-led-matrix" ]; then
    echo "Cloning rpi-rgb-led-matrix..."
    git clone --depth=1 https://github.com/hzeller/rpi-rgb-led-matrix.git /tmp/rpi-rgb-led-matrix
fi

echo "Building Python bindings for matrix..."
(cd /tmp/rpi-rgb-led-matrix && make build-python PYTHON="python3")

# Install Python dependencies
echo "Installing Python dependencies..."
sudo pip3 install --upgrade pip wheel setuptools
sudo pip3 install cython

# Install project dependencies (excluding rgbmatrix)
grep -v '^rgbmatrix' requirements.txt > requirements-nomatrix.txt
sudo pip3 install -r requirements-nomatrix.txt

# Install matrix bindings
(cd /tmp/rpi-rgb-led-matrix/bindings/python && sudo pip3 install .)

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "TRAIN_API_URL=http://server.local:4599/trains/fg-northbound-next" > .env
fi

# Create systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/matrix-display.service > /dev/null << EOL
[Unit]
Description=Matrix Display Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $SCRIPT_DIR/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and enable service
sudo systemctl daemon-reload
echo "Would you like to enable the service to start on boot? (y/N)"
read -r ENABLE_SERVICE
if [[ "$ENABLE_SERVICE" =~ ^[Yy]$ ]]; then
    sudo systemctl enable matrix-display.service
    echo "Service enabled and will start on boot"
fi

echo "======================================================================"
echo "                      Setup Complete! 🎉"
echo "======================================================================"
echo ""
echo "The Matrix Display Application has been installed and configured."
echo ""
echo "To start the application:"
echo "  sudo systemctl start matrix-display"
echo ""
echo "To check status:"
echo "  sudo systemctl status matrix-display"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u matrix-display -f"
echo ""
echo "To stop the application:"
echo "  sudo systemctl stop matrix-display"
echo "======================================================================" 