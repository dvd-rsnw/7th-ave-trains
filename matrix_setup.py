import platform
import os
from typing import Dict, Any, Optional, Union

# Constants for layout
PANEL_WIDTH = 64  # Width of a single panel
MATRIX_WIDTH = PANEL_WIDTH * 2  # Two panels chained
MATRIX_HEIGHT = 32
PADDING_X = 2
PADDING_Y = 4
CENTER_GAP = 4
ROW_HEIGHT = 10

# Row component measurements
CIRCLE_WIDTH = 10
FIRST_GAP = 3
LINE_NAME_WIDTH = 72  # Exact width for line name
SECOND_GAP = 11
MINUTES_WIDTH = 28  # Remaining space: 128 - (2 + 10 + 3 + 72 + 11 + 2) = 28px

# Scrolling configuration
SCROLL_SPEED = 2  # pixels per second
SCROLL_UPDATE_INTERVAL = 15  # seconds (matches polling interval)

# Get the base directory of the project
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Font path relative to project root
FONT_PATH = os.path.join(PROJECT_ROOT, "assets", "fonts", "6x10.bdf")

def initialize_matrix() -> Dict[str, Any]:
    """Initialize and return the matrix and related objects based on platform.
    
    Returns:
        Dictionary containing matrix, font, graphics objects and is_mock flag.
        If not running on Linux (Raspberry Pi), returns mock objects.
    """
    if platform.system() == "Linux":
        from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

        options = RGBMatrixOptions()
        options.rows = 16  # Each panel is 16 rows high
        options.cols = 64  # Each panel is 64 columns wide
        options.chain_length = 2  # Two panels chained horizontally
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat'
        
        # Additional recommended options for better performance
        options.gpio_slowdown = 4  # Slow down GPIO for stability
        options.brightness = 50    # Mid brightness to prevent overheating
        options.pwm_bits = 7      # Lower PWM bits for better refresh
        options.pwm_lsb_nanoseconds = 130  # Tune PWM timing
        options.limit_refresh_rate_hz = 100  # Cap refresh for stability

        matrix = RGBMatrix(options=options)
        font = graphics.Font()
        
        # Load the font from our assets directory
        font.LoadFont(FONT_PATH)
        
        return {
            "matrix": matrix,
            "font": font,
            "graphics": graphics,
            "is_mock": False
        }
    else:
        # Return mock objects for non-Linux platforms
        return {
            "matrix": None,
            "font": None,
            "graphics": None,
            "is_mock": True
        } 