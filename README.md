# 7th Avenue Trains LED Matrix Display

An application for Raspberry Pi to display NYC subway train information on an RGB LED matrix.

## Features

- Displays real-time train arrival information for F and G trains
- Shows train lines in their proper MTA colors
- Supports both local and express trains
- Uses environment variables for configuration

## Setup

### Hardware Requirements

- Raspberry Pi (3B+ or newer recommended)
- RGB LED Matrix with HUB75 interface
- Adafruit RGB Matrix Bonnet or compatible hardware

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/7th-ave-trains.git
   cd 7th-ave-trains
   ```

2. Install dependencies:
   ```
   pip3 install -r requirements.txt
   ```

3. Configure the environment:
   ```
   cp .env.example .env
   ```
   
4. Edit the `.env` file to set your API URL:
   ```
   TRAIN_API_URL=http://your-api-server.local:4599/trains/endpoint
   ```

## Usage

Run the application:

```
python3 main.py
```

### Running as a Service

To run the application as a systemd service:

1. Copy the service file to systemd:
   ```
   sudo cp train-display.service /etc/systemd/system/
   ```

2. Enable and start the service:
   ```
   sudo systemctl enable train-display
   sudo systemctl start train-display
   ```

## Development

- For development on non-Raspberry Pi systems, the application runs in mock mode and prints to the console.
- The application uses environment variables from a `.env` file for configuration. 