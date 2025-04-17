import asyncio
import sys
from typing import List, Dict, Any, Optional

from matrix_setup import (
    initialize_matrix,
    MATRIX_WIDTH, MATRIX_HEIGHT, PANEL_WIDTH,
    PADDING_X, PADDING_Y, CENTER_GAP, ROW_HEIGHT
)
from shape_renderer import ShapeRenderer
from text_renderer import TextRenderer
from train_renderer import TrainRenderer

class RGBMatrixController:
    """Controller for the RGB LED matrix display."""
    
    def __init__(self):
        """Initialize the RGB matrix controller with appropriate renderers."""
        # Initialize hardware components
        matrix_components = initialize_matrix()
        self.matrix = matrix_components["matrix"]
        self.is_mock = matrix_components["is_mock"]
        
        # Initialize renderers
        if not self.is_mock:
            self.graphics = matrix_components["graphics"]
            self.font = matrix_components["font"]
            
            self.text_renderer = TextRenderer(
                self.matrix, self.font, self.graphics, is_mock=False
            )
            self.shape_renderer = ShapeRenderer(
                self.matrix, self.graphics, is_mock=False
            )
            self.train_renderer = TrainRenderer(
                self.matrix, self.graphics, self.text_renderer, 
                self.shape_renderer, is_mock=False
            )
        else:
            # Mock versions of renderers
            self.text_renderer = TextRenderer(None, None, None, is_mock=True)
            self.shape_renderer = ShapeRenderer(None, None, is_mock=True)
            self.train_renderer = TrainRenderer(
                None, None, self.text_renderer, self.shape_renderer, is_mock=True
            )
    
    def display_trains(self, trains: List[Dict[str, Any]]) -> None:
        """Display a list of trains on the LED matrix.
        
        Args:
            trains: List of train data dictionaries
        """
        self.train_renderer.render_trains(trains[:2])  # Show at most 2 trains
    
    def clear_display(self) -> None:
        """Clear the LED matrix display."""
        if not self.is_mock and self.matrix:
            self.matrix.Clear()
    
    def shutdown(self) -> None:
        """Clean shutdown of the LED matrix."""
        self.clear_display()

# Singleton instance for easy importing
controller: Optional[RGBMatrixController] = None

def get_controller() -> RGBMatrixController:
    """Get or create the RGBMatrixController singleton.
    
    Returns:
        The singleton RGBMatrixController instance
    """
    global controller
    if controller is None:
        controller = RGBMatrixController()
    return controller

# Start the polling loop when script runs
if __name__ == "__main__":
    try:
        controller = get_controller()
        asyncio.run(controller.poll_and_display())
    except KeyboardInterrupt:
        print("Exiting...")
        controller.shutdown()
        sys.exit(0)