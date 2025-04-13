#!/bin/bash

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$SCRIPT_DIR/matrix.log"

# Function to log messages with timestamps
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Clear the log file if it gets too large (> 10MB)
if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE") -gt 10485760 ]; then
    log_message "Clearing log file due to size..."
    echo "" > "$LOG_FILE"
fi

# Ensure we're in the correct directory
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    log_message "ERROR: Python 3 is not installed. Please install Python 3."
    exit 1
fi

# Check if virtual environment exists, create if it doesn't
if [ ! -d "venv" ]; then
    log_message "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    log_message "Installing required packages..."
    pip install httpx
else
    source venv/bin/activate
fi

# Function to run the matrix controller
run_matrix() {
    while true; do
        log_message "Starting LED Matrix Controller..."
        python3 led_matrix_controller.py
        
        # If the script exits with an error
        EXIT_CODE=$?
        if [ $EXIT_CODE -ne 0 ]; then
            log_message "Script crashed with exit code $EXIT_CODE. Restarting in 5 seconds..."
            sleep 5
        else
            log_message "Script exited normally."
            break
        fi
    done
}

# Trap Ctrl+C and other signals
trap 'log_message "Stopping LED Matrix Controller..."; exit 0' SIGINT SIGTERM

# Start the matrix controller with auto-restart
run_matrix 