# 7th Avenue Trains LED Display

Real-time LED matrix display showing F/G train arrival times at 7th Avenue station in Brooklyn. Built for Raspberry Pi with RGB LED matrix panels.

## Hardware Requirements

- Raspberry Pi 4
- Two 64x16 LED Matrix panels (chained horizontally)
- Adafruit RGB Matrix HAT/Bonnet
- 5V 4A+ Power Supply

## Display Features

- Shows next two incoming trains
- Displays F and G train information
- Shows line name and arrival time
- Supports express F train indication
- Auto-scrolling for long text
- Real-time updates every 15 seconds

## Installation

1. Clone this repository:
```bash
git clone https://github.com/dvd-rsnw/7th-ave-trains.git
cd 7th-ave-trains
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

## Running the Display

Start the display:
```bash
sudo ./run.sh
```

Stop the display with Ctrl+C.

## Development

The project uses:
- Python 3.7+
- FastAPI for the backend
- [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library
- HTTPX for async HTTP requests

## Project Structure

```
7th-ave-trains/
├── led_matrix_controller.py  # LED display controller
├── main.py                  # FastAPI server
├── train_types.py          # Train data types
├── styles.py               # Color definitions
├── setup.sh               # Installation script
├── run.sh                # Runtime script
└── requirements.txt      # Python dependencies
```

## License

MIT License - See LICENSE file for details 