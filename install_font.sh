#!/bin/bash

# Create directories if they don't exist
sudo mkdir -p /home/pi/rpi-rgb-led-matrix/fonts

# Download the font file
echo 'Downloading font file...'
sudo wget -O /home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf https://raw.githubusercontent.com/hzeller/rpi-rgb-led-matrix/master/fonts/6x10.bdf

# Set permissions
sudo chmod 644 /home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf

echo 'Font file installed at /home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf' 