# 7th Avenue Trains LED Matrix Display

An application for Raspberry Pi to display NYC subway train information on an RGB LED matrix using Docker.

## Features

- Displays real-time train arrival information for F and G trains
- Shows train lines in their proper MTA colors
- Supports both local and express trains
- Uses environment variables for configuration
- Runs in a Docker container for easy setup and maintenance

## Setup Instructions

### Hardware Requirements

- Raspberry Pi (3B+ or newer recommended)
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

#### 3. Make the Setup Script Executable

```bash
# This step is REQUIRED - make the setup script executable
chmod +x setup.sh
```

#### 4. Run the Setup Script

The setup script will handle everything else automatically:

```bash
# Run the setup script
./setup.sh
```

This script will:
- Make both scripts executable
- Install Docker and Docker Compose if not already installed
- Create and configure the `.env` file with the API URL
- Automatically detect the IP address for "mother.local" (the API server)
- Update the Docker configuration with the correct IP address
- Build and start the Docker container
- Create a systemd service file for auto-starting on boot
- Ask if you want to enable the service to start automatically on boot

#### 5. Verify the Installation

After the setup completes, check that the application is running:

```bash
# Check the status of the application
./run.sh status

# View the application logs to verify it's receiving data
./run.sh logs
```

You should see output showing train data being received from the API.

### Accessing the Train API

The application connects to an API endpoint at `mother.local:4599/trains/fg-northbound-next`. Make sure:

1. The device hosting the API ("mother.local") is accessible on your network
2. Port 4599 is open and the API service is running
3. The correct DNS entry exists for "mother.local" (the setup script attempts to resolve this automatically)

## Daily Usage

Once installed, the application should run automatically. The LED matrix will display the latest train information.

You can manage the application with the following commands:

```bash
# Start the application
./run.sh start

# Stop the application
./run.sh stop

# View the application logs
./run.sh logs

# Check the application status
./run.sh status

# Restart the application
./run.sh restart
```

## Troubleshooting Guide

If you encounter issues:

### 1. Network Connectivity Problems

If the application can't reach the API:

```bash
# Test connectivity to mother.local
ping mother.local

# Check if the API endpoint is accessible
curl -v http://mother.local:4599/trains/fg-northbound-next
```

If mother.local can't be resolved, manually add it to your hosts file:

```bash
sudo nano /etc/hosts
```

Add a line like:
```
192.168.68.68 mother.local
```
(Replace with the actual IP address)

### 2. Docker Issues

If Docker isn't running properly:

```bash
# Check Docker service status
sudo systemctl status docker

# Restart Docker if needed
sudo systemctl restart docker

# Then restart the application
./run.sh restart
```

### 3. Application Not Starting

If the application doesn't start:

```bash
# Check for errors in the logs
./run.sh logs

# Make sure the container was built correctly
sudo docker ps -a

# Try rebuilding the container
sudo docker-compose down
sudo docker-compose up -d
```

### 4. Permission Issues

If you encounter permission issues:

```bash
# Make sure both scripts are executable
chmod +x run.sh setup.sh

# If Docker permission issues persist:
sudo usermod -aG docker $USER
# (Log out and back in for this to take effect)
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

Then update the host in docker-compose.yml:
```bash
nano docker-compose.yml
```

Change the extra_hosts entry to match your custom server:
```yaml
extra_hosts:
  - "your-custom-server:192.168.x.x"
```

Restart the application:
```bash
./run.sh restart
```

## Service Management

### Auto-start on Boot

To configure the application to start automatically when the Raspberry Pi boots:

```bash
sudo cp matrix.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable matrix.service
sudo systemctl start matrix.service
```

To disable auto-start:
```bash
sudo systemctl disable matrix.service
```

## Support & Maintenance

### Updating the Application

To update to a new version:

```bash
# Pull the latest code
cd ~/matrix
git pull

# Rebuild and restart the container
./run.sh restart
```

## Checking System Resources

To monitor system resources:

```bash
# Check disk usage
df -h

# Check memory usage
free -m

# Check CPU usage
top
```