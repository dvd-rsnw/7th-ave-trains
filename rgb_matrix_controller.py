"""RGB Matrix Controller for LED display management.

This module provides a controller for managing RGB LED matrix displays,
with support for rendering text, shapes, and train information. It implements
a thread-safe singleton pattern and provides async support for efficient
display updates.
"""

import asyncio
import logging
import sys
import threading
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, AsyncIterator

from matrix_setup import (
    initialize_matrix,
    MATRIX_WIDTH, MATRIX_HEIGHT, PANEL_WIDTH,
    PADDING_X, PADDING_Y, CENTER_GAP, ROW_HEIGHT
)
from shape_renderer import ShapeRenderer
from text_renderer import TextRenderer
from train_renderer import TrainRenderer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MatrixComponents:
    """Data class for matrix components."""
    matrix: Any
    graphics: Optional[Any] = None
    font: Optional[Any] = None
    is_mock: bool = False

class RGBMatrixError(Exception):
    """Base exception for RGB Matrix related errors."""
    pass

class RGBMatrixController:
    """Controller for the RGB LED matrix display."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'RGBMatrixController':
        """Implement thread-safe singleton pattern."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self) -> None:
        """Initialize the RGB matrix controller with appropriate renderers."""
        if self._initialized:
            return
            
        try:
            # Initialize hardware components
            matrix_components = initialize_matrix()
            self.components = MatrixComponents(
                matrix=matrix_components["matrix"],
                graphics=matrix_components.get("graphics"),
                font=matrix_components.get("font"),
                is_mock=matrix_components["is_mock"]
            )
            
            # Initialize renderers
            self._init_renderers()
            
            # Initialize async lock for thread-safe operations
            self._async_lock = asyncio.Lock()
            
            self._initialized = True
            logger.info("RGB Matrix Controller initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RGB Matrix Controller: {e}")
            raise RGBMatrixError(f"Initialization failed: {str(e)}") from e

    def _init_renderers(self) -> None:
        """Initialize the renderer components."""
        if not self.components.is_mock:
            self.text_renderer = TextRenderer(
                self.components.matrix,
                self.components.font,
                self.components.graphics,
                is_mock=False
            )
            self.shape_renderer = ShapeRenderer(
                self.components.matrix,
                self.components.graphics,
                is_mock=False
            )
        else:
            self.text_renderer = TextRenderer(None, None, None, is_mock=True)
            self.shape_renderer = ShapeRenderer(None, None, is_mock=True)

        self.train_renderer = TrainRenderer(
            self.components.matrix if not self.components.is_mock else None,
            self.components.graphics if not self.components.is_mock else None,
            self.text_renderer,
            self.shape_renderer,
            is_mock=self.components.is_mock
        )

    async def display_trains(self, trains: List[Dict[str, Any]]) -> None:
        """Display a list of trains on the LED matrix.
        
        Args:
            trains: List of train data dictionaries
        """
        async with self._async_lock:
            try:
                self.train_renderer.render_trains(trains[:2])  # Show at most 2 trains
                logger.debug(f"Displayed {len(trains[:2])} trains")
            except Exception as e:
                logger.error(f"Error displaying trains: {e}")
                raise RGBMatrixError(f"Display error: {str(e)}") from e

    async def clear_display(self) -> None:
        """Clear the LED matrix display."""
        async with self._async_lock:
            if not self.components.is_mock and self.components.matrix:
                try:
                    self.components.matrix.Clear()
                    logger.debug("Display cleared")
                except Exception as e:
                    logger.error(f"Error clearing display: {e}")
                    raise RGBMatrixError(f"Clear error: {str(e)}") from e

    async def shutdown(self) -> None:
        """Clean shutdown of the LED matrix."""
        try:
            await self.clear_display()
            # Add any additional cleanup here
            logger.info("RGB Matrix Controller shut down successfully")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            raise RGBMatrixError(f"Shutdown error: {str(e)}") from e

    @asynccontextmanager
    async def display_context(self) -> AsyncIterator['RGBMatrixController']:
        """Context manager for safe display operations.
        
        Yields:
            The RGBMatrixController instance
        """
        try:
            yield self
        finally:
            await self.clear_display()

async def get_controller() -> RGBMatrixController:
    """Get or create the RGBMatrixController singleton.
    
    Returns:
        The singleton RGBMatrixController instance
    """
    return RGBMatrixController()

async def main() -> None:
    """Main entry point for the RGB Matrix Controller."""
    try:
        async with (await get_controller()).display_context() as controller:
            while True:
                # Implement your display loop logic here
                await asyncio.sleep(1)  # Prevent CPU spinning
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        if 'controller' in locals():
            await controller.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)