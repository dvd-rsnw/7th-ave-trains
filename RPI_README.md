# 7th Ave Trains LED Display - Raspberry Pi Setup

This guide will help you set up and run the 7th Avenue Trains LED display on your Raspberry Pi 4.

## Hardware Requirements

- Raspberry Pi 4
- Two 64x16 LED Matrix panels (chained)
- Adafruit RGB Matrix HAT/Bonnet
- 5V 4A+ Power Supply

## Panel Configuration

The display uses:
- Two 64x16 panels chained horizontally
- Total resolution: 128x32 pixels
- Panels must be connected via the Adafruit HAT/Bonnet
- Panels should be chained left-to-right

## Installation

1. Clone this repository to your Raspberry Pi:
   ```bash
   cd ~
   git clone https://github.com/yourusername/7th-ave-trains.git
   ```

2. Run the setup script:
   ```bash
   cd ~/7th-ave-trains
   chmod +x setup.sh
   ./setup.sh
   ```

   This will:
   - Install required system packages
   - Set up the RGB LED Matrix library with RPi 4 optimizations
   - Create a Python virtual environment
   - Install Python dependencies
   - Create the run script

## Running the Display

1. Navigate to the project directory:
   ```bash
   cd ~/7th-ave-trains
   ```

2. Start the display:
   ```bash
   sudo ./run.sh
   ```

   This will:
   - Start the FastAPI server (handles train data)
   - Start the LED matrix controller
   - Display train information on the LED panels

3. To stop the display:
   - Press Ctrl+C
   - Both the API server and LED controller will shut down cleanly

## Display Layout

The display shows:
- Two rows of train information (one per panel height)
- Each row contains:
  - Line indicator (circle/diamond) with white F/G letter
  - Line name (72px wide, scrolls if needed)
  - Minutes display (shows arrival time/status)

## Troubleshooting

1. If you see "Must be run as root":
   - Make sure to use `sudo ./run.sh`

2. If panels don't light up:
   - Check power supply connection
   - Verify ribbon cable connections
   - Ensure panels are chained correctly

3. If display is garbled:
   - Check that panels are connected in the correct order
   - Verify the ribbon cable is fully seated

4. If no data appears:
   - Check that the API server started successfully
   - Verify your internet connection
   - Check the API logs for errors

## Logs and Debugging

- The application outputs logs to the console
- API server logs show train data updates
- LED controller logs show display updates
- Both components will show errors if they occur

## Support

If you encounter any issues:
1. Check all physical connections
2. Verify power supply is adequate
3. Ensure all cables are properly seated
4. Check console output for error messages 