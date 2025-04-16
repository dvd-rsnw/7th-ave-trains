#!/bin/bash
# Script to run the LED Matrix Train Display application

# Set environment variables (modify these values as needed)
export TRAIN_API_URL="http://mother.local:4599/trains/fg-northbound-next"
export POLLING_INTERVAL="15"

# Run the application
python3 main.py 