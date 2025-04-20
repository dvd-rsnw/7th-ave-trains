#!/bin/bash

# Matrix Display Application Setup Script
# Created: April 18, 2025

# Exit on any error
set -e

echo "======================================================================"
echo "        7th Avenue Trains LED Matrix Display Setup Wizard"
echo "======================================================================"
echo ""
echo "This script will set up the Matrix Display Application on your Raspberry Pi."
echo "It requires internet connectivity and administrator privileges."
echo ""
echo "The setup will:"
echo "  1. Make required scripts executable"
echo "  2. Install Docker and Docker Compose (if not present)"
echo "  3. Create the configuration files"
echo "  4. Set up network connectivity to the train API"
echo "  5. Build and start the application"
echo ""
echo "Press ENTER to continue or CTRL+C to cancel..."
read -r

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Function to check if a command succeeded
check_status() {
    if [ $? -eq 0 ]; then
        echo "✅ Success: $1"
    else
        echo "❌ Error: $1 failed. Please check the output above for errors."
        exit 1
    fi
}

# Step 1: Make scripts executable
echo ""
echo "Step 1/5: Making scripts executable..."
echo "--------------------------------------------------------------------"
chmod +x "$SCRIPT_DIR/run.sh"
chmod +x "$SCRIPT_DIR/setup.sh"
check_status "Scripts are now executable"

# Step 2: Install Docker if needed
echo ""
echo "Step 2/5: Checking Docker installation..."
echo "--------------------------------------------------------------------"
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing Docker (this may take a few minutes)..."
    curl -sSL https://get.docker.com | sh
    check_status "Docker installation"
    
    echo "Installing Docker Compose..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
    sudo pip3 install docker-compose
    check_status "Docker Compose installation"
else
    echo "✅ Docker is already installed ($(docker --version))"
fi

# Make sure Docker is running
if ! sudo systemctl is-active --quiet docker; then
    echo "Starting Docker service..."
    sudo systemctl start docker
    check_status "Docker service started"
else
    echo "✅ Docker service is running"
fi

# Verify Docker works
echo "Verifying Docker functionality..."
sudo docker run --rm hello-world > /dev/null 2>&1
check_status "Docker test container"

# Step 3: Create configuration files
echo ""
echo "Step 3/5: Creating configuration files..."
echo "--------------------------------------------------------------------"
echo "Creating .env file with API settings..."
echo "TRAIN_API_URL=http://server.local:4599/trains/fg-northbound-next" > .env
check_status ".env file creation"

# Step 4: Configure network connectivity
echo ""
echo "Step 4/5: Setting up network connectivity..."
echo "--------------------------------------------------------------------"
echo "Testing connection to API server (server.local)..."

# Try to ping the host first
if ping -c 1 server.local &> /dev/null; then
    echo "✅ Successfully pinged server.local"
    
    # Get the IP address
    IP_ADDRESS=$(ping -c 1 server.local | grep -oP '(\d+\.\d+\.\d+\.\d+)' | head -1)
    echo "   Resolved to IP address: $IP_ADDRESS"
    
    # Test the API endpoint
    if curl --connect-timeout 5 -s -o /dev/null -w "%{http_code}" "http://server.local:4599/trains/fg-northbound-next" | grep -q "200"; then
        echo "✅ Successfully connected to API endpoint"
    else
        echo "⚠️  Warning: Could not connect to API endpoint at http://server.local:4599/trains/fg-northbound-next"
        echo "   The application may not function correctly. Please check if:"
        echo "   - The API server is running"
        echo "   - Port 4599 is open"
        echo "   - The endpoint path is correct"
    fi
else
    echo "⚠️  Warning: Could not ping server.local"
    IP_ADDRESS=""
    
    # Try to resolve using getent
    GETENT_RESULT=$(getent hosts server.local 2>/dev/null)
    if [ -n "$GETENT_RESULT" ]; then
        IP_ADDRESS=$(echo "$GETENT_RESULT" | awk '{ print $1 }')
        echo "   Resolved using getent to IP: $IP_ADDRESS"
    fi
    
    # Ask user for the IP if we couldn't resolve it
    if [ -z "$IP_ADDRESS" ]; then
        echo "   Could not automatically resolve server.local to an IP address."
        echo "   Please enter the IP address of the API server (default: 192.168.68.68):"
        read -r USER_IP
        
        if [ -z "$USER_IP" ]; then
            IP_ADDRESS="192.168.68.68"
        else
            IP_ADDRESS="$USER_IP"
        fi
        
        echo "   Using IP address: $IP_ADDRESS"
        
        # Ask if the user wants to add an entry to /etc/hosts
        echo "   Would you like to add server.local to your /etc/hosts file? (y/n, default: y)"
        read -r ADD_HOST
        
        if [[ -z "$ADD_HOST" || "$ADD_HOST" =~ ^[Yy]$ ]]; then
            echo "$IP_ADDRESS server.local" | sudo tee -a /etc/hosts > /dev/null
            check_status "Added server.local to /etc/hosts"
        fi
    fi
fi

# Update docker-compose.yml with the correct IP
if [ -n "$IP_ADDRESS" ]; then
    echo "Updating docker-compose.yml with IP: $IP_ADDRESS"
    sed -i "s/server.local:[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+/server.local:$IP_ADDRESS/g" docker-compose.yml
    check_status "docker-compose.yml update"
else
    echo "⚠️  Warning: Could not update docker-compose.yml with IP address"
    echo "   Please edit docker-compose.yml manually with the correct IP address."
fi

# Create systemd service file
echo "Creating systemd service file..."
cat > matrix.service << EOL
[Unit]
Description=Matrix Display Application (Docker)
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
User=root
WorkingDirectory=$SCRIPT_DIR
ExecStart=$SCRIPT_DIR/run.sh start
ExecStop=$SCRIPT_DIR/run.sh stop
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOL
check_status "Service file creation"

# Step 5: Build and start the application
echo ""
echo "Step 5/5: Building and starting the application..."
echo "--------------------------------------------------------------------"
echo "Building and starting the Docker container (this may take a few minutes)..."
sudo docker-compose up -d --build
check_status "Application startup"

# Verify the container is running
if sudo docker ps | grep -q matrix-app; then
    echo "✅ Container is running successfully"
else
    echo "⚠️  Warning: Container is not running. Checking for errors..."
    sudo docker-compose logs
    echo "Please check the logs above for any errors."
fi

# Ask if user wants to enable service at boot
echo ""
echo "Final step: Auto-start configuration"
echo "--------------------------------------------------------------------"
echo "Would you like the application to start automatically on boot? (y/n, default: y)"
read -r ENABLE_SERVICE

if [[ -z "$ENABLE_SERVICE" || "$ENABLE_SERVICE" =~ ^[Yy]$ ]]; then
    echo "Setting up application to start at boot..."
    sudo cp matrix.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable matrix.service
    check_status "Auto-start configuration"
else
    echo "Skipping automatic startup configuration."
    echo "You can manually start the application with: ./run.sh start"
fi

echo ""
echo "======================================================================"
echo "                      Setup Complete! 🎉"
echo "======================================================================"
echo ""
echo "The Matrix Display Application has been installed and configured."
echo ""
echo "✨ Useful commands:"
echo "  ./run.sh start    - Start the application"
echo "  ./run.sh stop     - Stop the application"
echo "  ./run.sh logs     - View application logs"
echo "  ./run.sh status   - Check application status"
echo "  ./run.sh restart  - Restart the application"
echo ""
echo "To verify the application is working correctly:"
echo "  ./run.sh logs"
echo ""
echo "If you encounter any issues, please refer to the troubleshooting"
echo "section in the README.md file."
echo "======================================================================"
