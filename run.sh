#!/bin/bash

# Matrix Display Application Runner Script
# Created: April 17, 2025

set -e

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Function to display usage information
usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start       - Start the matrix display application"
    echo "  stop        - Stop the matrix display application"
    echo "  restart     - Restart the matrix display application"
    echo "  status      - Check the status of the matrix display application"
    echo "  logs        - View the logs of the application"
    echo "  help        - Display this help message"
    echo ""
    exit 1
}

# Check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Error: Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! sudo docker info &> /dev/null; then
        echo "Error: Docker daemon is not running. Please start Docker first."
        exit 1
    fi
}

# Function to start the application
start_app() {
    echo "Starting Matrix Display Application..."
    sudo docker-compose up -d
    echo "Application started. Use '$0 logs' to view the logs."
}

# Function to stop the application
stop_app() {
    echo "Stopping Matrix Display Application..."
    sudo docker-compose down
    echo "Application stopped."
}

# Function to restart the application
restart_app() {
    echo "Restarting Matrix Display Application..."
    sudo docker-compose down
    sudo docker-compose up -d
    echo "Application restarted. Use '$0 logs' to view the logs."
}

# Function to check the status of the application
check_status() {
    echo "Checking Matrix Display Application status..."
    sudo docker-compose ps
}

# Function to view the logs of the application
view_logs() {
    echo "Viewing Matrix Display Application logs..."
    sudo docker-compose logs -f
}

# Check Docker installation and daemon status
check_docker

# Process command line arguments
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs
        ;;
    help)
        usage
        ;;
    *)
        echo "Unknown command: $1"
        usage
        ;;
esac

exit 0