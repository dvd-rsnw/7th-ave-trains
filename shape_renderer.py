from rgbmatrix import graphics
from typing import Tuple, Any, Union, Protocol, TypeVar, cast
from functools import lru_cache

# Define protocols for better type safety
class RGBMatrixProtocol(Protocol):
    def SetPixel(self, x: int, y: int, red: int, green: int, blue: int) -> None: ...

class GraphicsProtocol(Protocol):
    def Color(self, red: int, green: int, blue: int) -> Any: ...

ColorType = Union[Tuple[int, int, int], Any]  # graphics.Color or RGB tuple
T = TypeVar('T')

class ShapeRenderer:
    """Renders shapes on the LED matrix display."""
    
    def __init__(self, matrix: RGBMatrixProtocol, graphics_obj: GraphicsProtocol, is_mock: bool = False):
        """Initialize the shape renderer.
        
        Args:
            matrix: The LED matrix instance
            graphics_obj: The graphics object from rgbmatrix
            is_mock: Whether to use mock mode
        """
        self.matrix = matrix
        self.graphics = graphics_obj
        self.is_mock = is_mock
        
        # Pre-calculate common values
        self._radius_5_squared = 25  # 5 * 5, used in diamond
        self._f_height = 9  # Height of F character
        self._f_top_width = 5  # Width of F top line
        self._f_mid_width = 4  # Width of F middle line
        
    @lru_cache(maxsize=32)
    def _get_rgb_values(self, color: ColorType) -> Tuple[int, int, int]:
        """Extract RGB values from either a Color object or RGB tuple.
        
        Args:
            color: Either a graphics.Color object or RGB tuple
            
        Returns:
            Tuple of (r, g, b) values
        """
        if isinstance(color, tuple):
            return color
        # If it's a graphics.Color object, get its RGB values
        return (color.red, color.green, color.blue)

    def _set_pixels_in_range(self, x: int, y: int, width: int, r: int, g: int, b: int) -> None:
        """Helper to set multiple pixels in a horizontal line."""
        if hasattr(self.matrix, 'width') and hasattr(self.matrix, 'height'):
            for i in range(width):
                px = x + i
                if 0 <= px < self.matrix.width and 0 <= y < self.matrix.height:
                    self.matrix.SetPixel(px, y, r, g, b)
        else:
            for i in range(width):
                self.matrix.SetPixel(x + i, y, r, g, b)

    def draw_circle(self, x: int, y: int, radius: int, color: ColorType) -> None:
        """Draw a filled circle with smoothed edges.
        
        Args:
            x: Center x coordinate
            y: Center y coordinate
            radius: Circle radius
            color: Color to draw with
        """
        if self.is_mock:
            return
        
        r, g, b = self._get_rgb_values(color)
        radius_squared = radius * radius
        
        # Use generator expression for more efficient iteration
        points = ((i, j) 
                 for i in range(-radius, radius + 1)
                 for j in range(-radius, radius + 1)
                 if i * i + j * j <= radius_squared 
                 and not ((abs(i) == radius and j == 0) or (abs(j) == radius and i == 0)))
        
        for i, j in points:
            px, py = x + i, y + j
            if hasattr(self.matrix, 'width') and hasattr(self.matrix, 'height'):
                if 0 <= px < self.matrix.width and 0 <= py < self.matrix.height:
                    self.matrix.SetPixel(px, py, r, g, b)
            else:
                self.matrix.SetPixel(px, py, r, g, b)

    def draw_diamond(self, x: int, y: int, radius: int, color: ColorType) -> None:
        """Draw a filled diamond with fixed radius of 5.
        
        Args:
            x: Center x coordinate
            y: Center y coordinate
            radius: Diamond radius (ignored, fixed at 5)
            color: Color to draw with
        """
        if self.is_mock:
            return
            
        r, g, b = self._get_rgb_values(color)
        
        # Fixed radius - this method only supports radius 5
        radius = 5
        
        # Use generator expression for more efficient iteration
        points = ((i, j) 
                 for i in range(-radius, radius + 1)
                 for j in range(-radius, radius + 1)
                 if abs(i) + abs(j) <= radius)
        
        for i, j in points:
            px, py = x + i, y + j
            if hasattr(self.matrix, 'width') and hasattr(self.matrix, 'height'):
                if 0 <= px < self.matrix.width and 0 <= py < self.matrix.height:
                    self.matrix.SetPixel(px, py, r, g, b)
            else:
                self.matrix.SetPixel(px, py, r, g, b)

    def draw_thick_F(self, x: int, y: int, color: ColorType) -> None:
        """Draw a 2px thick F letter.
        
        Args:
            x: Starting x coordinate
            y: Starting y coordinate
            color: Color to draw with
        """
        if self.is_mock:
            return
        
        r, g, b = self._get_rgb_values(color)
        
        # Vertical line (2px thick)
        for i in range(self._f_height):
            self._set_pixels_in_range(x + 1, y + i, 2, r, g, b)
        
        # Top horizontal line (2px thick)
        for i in range(2):
            self._set_pixels_in_range(x + 1, y + i, self._f_top_width, r, g, b)
        
        # Middle horizontal line (2px thick)
        for i in range(2):
            self._set_pixels_in_range(x + 1, y + 4 + i, self._f_mid_width, r, g, b)

    def draw_thick_G(self, x: int, y: int, color: ColorType) -> None:
        """Draw a 2px thick G letter.
        
        Args:
            x: Starting x coordinate
            y: Starting y coordinate
            color: Color to draw with
        
        The G character is 9px tall and 6px wide with the following pattern:
         xooooo  # Row 0
         oooooo  # Row 1
         oo      # Row 2
         oo      # Row 3
         ooxooo  # Row 4
         ooxooo  # Row 5
         ooxxoo  # Row 6
         oooooo  # Row 7
         xooooo  # Row 8
        where 'x' represents empty space and 'o' represents a filled pixel
        """
        if self.is_mock:
            return
        
        r, g, b = self._get_rgb_values(color)
        
        # Define the G shape as a list of ranges for each row
        # Each tuple represents (start, end) or (start1, end1, start2, end2) for split ranges
        g_shape = [
            (1, 6),    # Row 0: Top row (xooooo)
            (0, 6),    # Row 1: Second row (oooooo)
            (0, 2),    # Row 2: Third row left (oo)
            (0, 2),    # Row 3: Fourth row left (oo)
            (0, 2, 3, 6),  # Row 4: Fifth row (ooxooo)
            (0, 2, 3, 6),  # Row 5: Sixth row (ooxooo)
            (0, 2, 4, 6),  # Row 6: Seventh row (ooxxoo)
            (0, 6),    # Row 7: Eighth row (oooooo)
            (1, 6),    # Row 8: Ninth row (xooooo)
        ]
        
        # Validate G dimensions
        if len(g_shape) != 9:
            raise ValueError("G character must be exactly 9 pixels tall")
        
        for row, ranges in enumerate(g_shape):
            if len(ranges) == 2:
                start, end = ranges
                if end > 6:
                    raise ValueError(f"G character width exceeds 6 pixels at row {row}")
                self._set_pixels_in_range(x + start, y + row, end - start, r, g, b)
            else:  # Split ranges for rows with gaps
                start1, end1, start2, end2 = ranges
                if end1 > 6 or end2 > 6:
                    raise ValueError(f"G character width exceeds 6 pixels at row {row}")
                self._set_pixels_in_range(x + start1, y + row, end1 - start1, r, g, b)
                self._set_pixels_in_range(x + start2, y + row, end2 - start2, r, g, b)