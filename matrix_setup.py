import platform
import sys
import os
from typing import Dict, Any

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Constants for layout
PANEL_WIDTH = 64  # Width of a single panel
MATRIX_WIDTH = PANEL_WIDTH * 2  # Two panels chained
MATRIX_HEIGHT = 32
PADDING_X = 2
PADDING_Y = 2  # Reduced from 4 to move top circle up
CENTER_GAP = 6  # Increased from 4 to create more separation between rows
ROW_HEIGHT = 10

# Row component measurements
CIRCLE_WIDTH = 13  # Updated circle diameter
FIRST_GAP = 3
LINE_NAME_WIDTH = 72  # Exact width for line name
SECOND_GAP = 5  # Previously updated
MINUTES_WIDTH = 34  # Previously updated

# Get the base directory of the project
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Font path relative to project root - using 5x8 font for narrower spacing
FONT_PATH = os.path.join(PROJECT_ROOT, "assets", "fonts", "6x10.bdf")

def initialize_matrix() -> Dict[str, Any]:
    """Initialize and return the matrix and related objects based on platform.
    
    Returns:
        Dictionary containing matrix, font, graphics objects and is_mock flag.
        If not running on Linux (Raspberry Pi), returns mock objects.
    """
    if platform.system() == "Linux":
        options = RGBMatrixOptions()
        options.rows = 32  # Each panel is 16 rows high
        options.cols = 64  # Each panel is 64 columns wide
        options.chain_length = 2  # Two panels chained horizontally
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat'
        
        # Additional recommended options for better performance
        options.gpio_slowdown = 2  # Slow down GPIO for stability
        options.brightness = 30    # Mid brightness to prevent overheating
        options.pwm_bits = 5      # Lower PWM bits for better refresh
        options.pwm_lsb_nanoseconds = 180  # Tune PWM timing
        options.limit_refresh_rate_hz = 60  # Cap refresh for stability


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

def draw_circle(matrix, graphics, x: int, y: int, radius: int, color):
    """Draw a filled circle with improved radius check to prevent single-pixel protrusions"""
    radius_squared = radius * radius
    for i in range(-radius, radius + 1):
        for j in range(-(radius-1), radius):  # Reduced vertical range by 1
            # Use a tighter radius check near the cardinal points
            # This creates a slightly squashed but more visually balanced circle
            dist = i*i + j*j
            if dist <= radius_squared - (max(abs(i), abs(j)) + 1):
                graphics.SetPixel(matrix, x + i, y + j, color)

def draw_diamond(matrix, graphics, x: int, y: int, radius: int, color):
    """Draw a filled diamond"""
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if abs(i) + abs(j) <= radius:
                graphics.SetPixel(matrix, x + i, y + j, color)
