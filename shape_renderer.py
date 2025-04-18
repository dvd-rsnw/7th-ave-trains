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
        """Draw a 2px thick F letter (now 9px tall, top line 5px wide, raised 1 row)."""
        if self.is_mock:
            return
        
        r, g, b = self._get_rgb_values(color)
        
        # Vertical line (shifted right by 1, down by 0)
        for i in range(9):  # Height of 9px
            self.matrix.SetPixel(x + 1, y + i, r, g, b)
            self.matrix.SetPixel(x + 2, y + i, r, g, b)
        
        # Top horizontal line (shifted right by 1, down by 0)
        for i in range(5):  # Width of 5px
            self.matrix.SetPixel(x + 1 + i, y, r, g, b)
            self.matrix.SetPixel(x + 1 + i, y + 1, r, g, b)
        
        # Middle horizontal line (move down 1 row)
        for i in range(4):  # Width of 4px
            self.matrix.SetPixel(x + 1 + i, y + 4, r, g, b)
            self.matrix.SetPixel(x + 1 + i, y + 5, r, g, b)

    def draw_thick_G(self, x: int, y: int, color: Any) -> None:
        """Draw a 2px thick G letter (9px tall, with curved bottom left corner, bottom row omits leftmost pixel, and one more row at the top of the inner part)."""
        if self.is_mock:
            return
        
        r, g, b = self._get_rgb_values(color)
        
        # Top row (xooooo)
        for i in range(1, 6):
            self.matrix.SetPixel(x + i, y, r, g, b)
        # Second row (oooooo)
        for i in range(0, 6):
            self.matrix.SetPixel(x + i, y + 1, r, g, b)
        # Third and fourth rows (ooxxxx)
        for j in range(2, 4):
            for i in range(0, 2):
                self.matrix.SetPixel(x + i, y + j, r, g, b)
        # Fifth and sixth rows (ooxooo)
        for j in range(4, 6):
            for i in range(0, 2):
                self.matrix.SetPixel(x + i, y + j, r, g, b)
            for i in range(3, 6):
                self.matrix.SetPixel(x + i, y + j, r, g, b)
        # Seventh row (ooxxoo)
        for i in range(0, 2):
            self.matrix.SetPixel(x + i, y + 6, r, g, b)
        for i in range(4, 6):
            self.matrix.SetPixel(x + i, y + 6, r, g, b)
        # Eighth row (oooooo)
        for i in range(0, 6):
            self.matrix.SetPixel(x + i, y + 7, r, g, b)
        # Ninth row (xooooo)
        for i in range(1, 6):
            self.matrix.SetPixel(x + i, y + 8, r, g, b)