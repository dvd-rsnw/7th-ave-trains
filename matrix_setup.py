import platform
import sys
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, TypedDict, Optional, Tuple
import logging
import numpy as np

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MatrixLayout:
    """Configuration for matrix panel layout"""
    PANEL_WIDTH: int = 64  # Width of a single panel
    MATRIX_WIDTH: int = PANEL_WIDTH * 2  # Two panels chained
    MATRIX_HEIGHT: int = 32
    PADDING_X: int = 2
    PADDING_Y: int = 2
    CENTER_GAP: int = 6
    ROW_HEIGHT: int = 10

@dataclass
class RowComponent:
    """Configuration for row component measurements"""
    CIRCLE_WIDTH: int = 13
    FIRST_GAP: int = 3
    LINE_NAME_WIDTH: int = 72
    SECOND_GAP: int = 5
    MINUTES_WIDTH: int = 34

class MatrixConfig:
    """Matrix hardware configuration"""
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.cols = 64
        self.options.chain_length = 2
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat'
        self.options.disable_hardware_pulsing = True
        self.options.gpio_slowdown = 3
        self.options.brightness = 40
        self.options.pwm_bits = 8
        self.options.pwm_lsb_nanoseconds = 130
        self.options.limit_refresh_rate_hz = 120

class MatrixResult(TypedDict):
    """Type definition for matrix initialization result"""
    matrix: Optional[RGBMatrix]
    font: Optional[graphics.Font]
    graphics: Optional[Any]
    is_mock: bool

def get_font_path() -> Path:
    """Get the font path relative to the project root"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    return project_root / "assets" / "fonts" / "6x10.bdf"

def initialize_matrix() -> MatrixResult:
    """Initialize and return the matrix and related objects based on platform.
    
    Returns:
        MatrixResult containing matrix, font, graphics objects and is_mock flag.
        If not running on Linux (Raspberry Pi), returns mock objects.
    
    Raises:
        FileNotFoundError: If the font file cannot be found
        Exception: If matrix initialization fails
    """
    try:
        if platform.system() == "Linux":
            config = MatrixConfig()
            matrix = RGBMatrix(options=config.options)
            font = graphics.Font()
            
            font_path = get_font_path()
            if not font_path.exists():
                raise FileNotFoundError(f"Font file not found at {font_path}")
            
            if not font.LoadFont(str(font_path)):
                raise Exception("Failed to load font")
            
            logger.info("Matrix initialized successfully")
            return MatrixResult(
                matrix=matrix,
                font=font,
                graphics=graphics,
                is_mock=False
            )
        else:
            logger.warning("Not running on Linux, using mock objects")
            return MatrixResult(
                matrix=None,
                font=None,
                graphics=None,
                is_mock=True
            )
    except Exception as e:
        logger.error(f"Failed to initialize matrix: {e}")
        raise

def draw_circle(
    matrix: RGBMatrix,
    graphics: Any,
    x: int,
    y: int,
    radius: int,
    color: Tuple[int, int, int]
) -> None:
    """Draw a filled circle with improved radius check to prevent single-pixel protrusions.
    
    Args:
        matrix: The RGB matrix instance
        graphics: The graphics instance
        x: Center x coordinate
        y: Center y coordinate
        radius: Circle radius
        color: RGB color tuple
    """
    if radius <= 0:
        return

    # Pre-calculate values
    radius_squared = radius * radius
    
    # Use the exact same algorithm as before for shape preservation
    for i in range(-radius, radius + 1):
        for j in range(-(radius-1), radius):  # Reduced vertical range by 1
            # Use a tighter radius check near the cardinal points
            # This creates a slightly squashed but more visually balanced circle
            dist = i*i + j*j
            if dist <= radius_squared - (max(abs(i), abs(j)) + 1):
                px, py = x + i, y + j
                if 0 <= px < matrix.width and 0 <= py < matrix.height:
                    graphics.SetPixel(matrix, px, py, *color)

def draw_diamond(
    matrix: RGBMatrix,
    graphics: Any,
    x: int,
    y: int,
    radius: int,
    color: Tuple[int, int, int]
) -> None:
    """Draw a filled diamond with boundary checking.
    
    Args:
        matrix: The RGB matrix instance
        graphics: The graphics instance
        x: Center x coordinate
        y: Center y coordinate
        radius: Diamond radius
        color: RGB color tuple
    """
    if radius <= 0:
        return

    # Use generator expression for more efficient iteration
    points = ((i, j) 
             for i in range(-radius, radius + 1)
             for j in range(-radius, radius + 1)
             if abs(i) + abs(j) <= radius)
    
    for i, j in points:
        px, py = x + i, y + j
        if 0 <= px < matrix.width and 0 <= py < matrix.height:
            graphics.SetPixel(matrix, px, py, *color)
