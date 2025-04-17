from rgbmatrix import graphics
from typing import Tuple, Any

class ShapeRenderer:
    """Renders shapes on the LED matrix display."""
    
    def __init__(self, matrix: Any, graphics_obj: Any, is_mock: bool = False):
        """Initialize the shape renderer.
        
        Args:
            matrix: The LED matrix instance
            graphics_obj: The graphics object from rgbmatrix
            is_mock: Whether to use mock mode
        """
        self.matrix = matrix
        self.graphics = graphics_obj
        self.is_mock = is_mock

    def _get_rgb_values(self, color: Any) -> Tuple[int, int, int]:
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

    def draw_circle(self, x: int, y: int, radius: int, color: Any) -> None:
        """Draw a filled circle, but remove only the cardinal point pixels for a smoother look."""
        if self.is_mock:
            return
        
        r, g, b = self._get_rgb_values(color)
        radius_squared = radius * radius
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                # Standard filled circle
                if i * i + j * j <= radius_squared:
                    # Remove only the cardinal points (top, bottom, left, right)
                    if (abs(i) == radius and j == 0) or (abs(j) == radius and i == 0):
                        continue
                    self.matrix.SetPixel(x + i, y + j, r, g, b)

    def draw_diamond(self, x: int, y: int, radius: int, color: Any) -> None:
        """Draw a filled diamond."""
        if self.is_mock:
            return
            
        r, g, b = self._get_rgb_values(color)
        radius = 5  # Enforce radius of 5 pixels (10px total width)
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if abs(i) + abs(j) <= radius:
                    self.matrix.SetPixel(x + i, y + j, r, g, b)

    def draw_thick_F(self, x: int, y: int, color: Any) -> None:
        """Draw a 2px thick F letter."""
        if self.is_mock:
            return
            
        r, g, b = self._get_rgb_values(color)
            
        # Vertical line (shifted right by 1, down by 1)
        for i in range(8):  # Height of 8px
            self.matrix.SetPixel(x + 1, y + 1 + i, r, g, b)
            self.matrix.SetPixel(x + 2, y + 1 + i, r, g, b)
        
        # Top horizontal line (shifted right by 1, down by 1)
        for i in range(6):  # Width of 6px
            self.matrix.SetPixel(x + 1 + i, y + 1, r, g, b)
            self.matrix.SetPixel(x + 1 + i, y + 2, r, g, b)
        
        # Middle horizontal line (shifted right by 1, down by 1)
        for i in range(4):  # Width of 4px
            self.matrix.SetPixel(x + 1 + i, y + 4, r, g, b)
            self.matrix.SetPixel(x + 1 + i, y + 5, r, g, b)

    def draw_thick_G(self, x: int, y: int, color: Any) -> None:
        """Draw a 2px thick G letter."""
        if self.is_mock:
            return
            
        r, g, b = self._get_rgb_values(color)
            
        # Top curve
        for i in range(6):  # Width of 6px
            self.matrix.SetPixel(x + i, y, r, g, b)
            self.matrix.SetPixel(x + i, y + 1, r, g, b)
        
        # Left vertical line
        for i in range(8):  # Height of 8px
            self.matrix.SetPixel(x, y + i, r, g, b)
            self.matrix.SetPixel(x + 1, y + i, r, g, b)
        
        # Bottom curve
        for i in range(6):  # Width of 6px
            self.matrix.SetPixel(x + i, y + 6, r, g, b)
            self.matrix.SetPixel(x + i, y + 7, r, g, b)
        
        # Right vertical stub
        for i in range(4):  # Height of 4px
            self.matrix.SetPixel(x + 4, y + 4 + i, r, g, b)
            self.matrix.SetPixel(x + 5, y + 4 + i, r, g, b)
        
        # Middle horizontal line
        self.matrix.SetPixel(x + 3, y + 4, r, g, b)
        self.matrix.SetPixel(x + 3, y + 5, r, g, b)