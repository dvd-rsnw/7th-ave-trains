#!/bin/bash

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$SCRIPT_DIR/matrix.log"

# Define virtual environment path
VENV_PATH="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_PATH" ]; then
    VENV_PATH="$SCRIPT_DIR/venv"
fi

# Function to log messages with timestamps
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Clear the log file if it gets too large (> 10MB)
if [ -f "$LOG_FILE" ]; then
    # Use stat command compatible with both macOS and Linux
    FILE_SIZE=$(stat -c%s "$LOG_FILE" 2>/dev/null || stat -f%z "$LOG_FILE" 2>/dev/null)
    if [ -n "$FILE_SIZE" ] && [ "$FILE_SIZE" -gt 10485760 ]; then
        log_message "Clearing log file due to size..."
        echo "" > "$LOG_FILE"
    fi
fi

# Ensure we're in the correct directory
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    log_message "ERROR: Python 3 is not installed. Please install Python 3."
    exit 1
fi

# Check if the font file exists
FONT_PATH="/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf"
if [ ! -f "$FONT_PATH" ]; then
    log_message "ERROR: Font file not found at $FONT_PATH"
    log_message "Please check the RGB Matrix installation or run install_font.sh."
    exit 1
fi

# Check if we're running as root
SUDO_CMD=""
if [ "$EUID" -ne 0 ]; then
    log_message "This script requires root privileges to access hardware."
    SUDO_CMD="sudo"
fi

# Function to run the matrix controller
run_matrix() {
    while true; do
        log_message "Starting LED Matrix Controller..."
        
        # Use the Python from the virtual environment if it exists
        if [ -f "$VENV_PATH/bin/python3" ]; then
            PYTHON_PATH="$VENV_PATH/bin/python3"
            SITE_PACKAGES=$(find "$VENV_PATH" -name "site-packages" | head -n 1)
            log_message "Using Python from virtual environment: $PYTHON_PATH"
            log_message "Site packages: $SITE_PACKAGES"
            
            # Add site-packages to PYTHONPATH to ensure modules are found
            export PYTHONPATH="$SITE_PACKAGES:$PYTHONPATH"
        else
            PYTHON_PATH=$(which python3)
            log_message "Using system Python: $PYTHON_PATH"
        fi
        
        # Run the controller with root privileges if needed
        $SUDO_CMD $PYTHON_PATH led_matrix_controller.py
        
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
log_message "Running with root privileges for hardware access."
run_matrix 