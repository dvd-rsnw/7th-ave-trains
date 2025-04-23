# 7th Avenue Trains LED Matrix Display

An application for Raspberry Pi to display NYC subway train information on an RGB LED matrix using Python virtual environment.

## Features

- Displays real-time train arrival information for F and G trains
- Shows train lines in their proper MTA colors
- Supports both local and express trains
- Uses environment variables for configuration
- Runs in a Python virtual environment for optimal performance

## Setup Instructions

### Hardware Requirements

- Raspberry Pi Zero 2 W (recommended)
- RGB LED Matrix with HUB75 interface
- Adafruit RGB Matrix Bonnet or compatible hardware
- Power supply for both Raspberry Pi and LED Matrix
- Micro SD card (16GB+ recommended)
- Network connection (WiFi or Ethernet)

### Step-by-Step Installation

#### 1. Prepare the Raspberry Pi

Make sure your Raspberry Pi is set up with Raspberry Pi OS (formerly Raspbian) and has internet access.

```bash
# Update your system
sudo apt-get update
sudo apt-get upgrade -y
```

#### 2. Clone the Repository

```bash
# Clone the repository to your home directory
git clone https://github.com/yourusername/7th-ave-trains.git ~/matrix

# Navigate to the project directory
cd ~/matrix
```

#### 3. Run the Installation Script

The installation script will handle everything automatically:

```bash
# Make the install script executable
chmod +x install.sh

# Run the installation script
./install.sh
```

This script will:
- Create a Python virtual environment
- Install system dependencies
- Install the RGB Matrix library and Python bindings
- Create and configure the `.env` file with the API URL
- Set up a systemd service for auto-starting on boot
- Install all Python dependencies in the virtual environment

#### 4. Verify the Installation

After the installation completes, check that the application is running:

```bash
# Check the status of the application
sudo systemctl status matrix-display

# View the application logs
sudo journalctl -u matrix-display -f
```

You should see output showing train data being received from the API.

### Accessing the Train API

The application connects to an API endpoint at `server.local:4599/trains/fg-northbound-next`. Make sure:

1. The device hosting the API ("server.local") is accessible on your network
2. Port 4599 is open and the API service is running
3. The correct DNS entry exists for "server.local"

## Daily Usage

Once installed, the application should run automatically. The LED matrix will display the latest train information.

You can manage the application with the following commands:

```bash
# Start the application
sudo systemctl start matrix-display

# Stop the application
sudo systemctl stop matrix-display

# View the application logs
sudo journalctl -u matrix-display -f

# Check the application status
sudo systemctl status matrix-display

# Restart the application
sudo systemctl restart matrix-display
```

## Troubleshooting Guide

If you encounter issues:

### 1. Network Connectivity Problems

If the application can't reach the API:

```bash
# Test connectivity to server.local
ping server.local

# Check if the API endpoint is accessible
curl -v http://server.local:4599/trains/fg-northbound-next
```

If server.local can't be resolved, manually add it to your hosts file:

```bash
sudo nano /etc/hosts
```

Add a line like:
```
192.168.68.68 server.local
```
(Replace with the actual IP address)

### 2. Application Not Starting

If the application doesn't start:

```bash
# Check the systemd service status
sudo systemctl status matrix-display

# Check the application logs
sudo journalctl -u matrix-display -f

# Verify the virtual environment
source ~/matrix/venv/bin/activate
python3 -c "import rgbmatrix"
```

### 3. Permission Issues

If you encounter permission issues:

```bash
# Check the ownership of the virtual environment
ls -l ~/matrix/venv

# Fix permissions if needed
sudo chown -R $USER:$USER ~/matrix
```

## Advanced Configuration

### Custom API Endpoint

To use a different API endpoint, edit the `.env` file:

```bash
nano .env
```

Update the TRAIN_API_URL variable:
```
TRAIN_API_URL=http://your-custom-server:port/your-endpoint
```

Restart the application:
```bash
sudo systemctl restart matrix-display
```

## Service Management

The application is managed through systemd. The service file is located at `/etc/systemd/system/matrix-display.service`.

### Auto-start on Boot

The installation script will ask if you want to enable auto-start. To manage it manually:

To enable auto-start:
```bash
sudo systemctl enable matrix-display
```

To disable auto-start:
```bash
sudo systemctl disable matrix-display
```

## Support & Maintenance

### Updating the Application

To update to a new version:

```bash
# Pull the latest code
cd ~/matrix
git pull

# Reactivate the virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Restart the service
sudo systemctl restart matrix-display
```

### Rebuilding the Virtual Environment

If you need to rebuild the virtual environment from scratch:

```bash
# Stop the service
sudo systemctl stop matrix-display

# Remove the old virtual environment
rm -rf ~/matrix/venv

# Run the installation script again
./install.sh
```