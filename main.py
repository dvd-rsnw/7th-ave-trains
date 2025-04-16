#!/usr/bin/env python3
import asyncio
import sys
import signal
from typing import Dict, List, Any

import httpx

from rgb_matrix_controller import get_controller

# URL to fetch train data from
API_URL = "http://mother.local:4599/trains/fg-northbound-next"
# Polling interval in seconds
POLLING_INTERVAL = 15

async def poll_and_display(controller: Any, url: str, interval: int) -> None:
    """Poll a URL for train data and display it on the matrix.
    
    Args:
        controller: The matrix controller object
        url: The API URL to poll for train data
        interval: The polling interval in seconds
    """
    while True:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=5.0)
                if resp.status_code == 200:
                    trains = resp.json()
                    controller.display_trains(trains[:2])  # Display first two trains
                else:
                    print(f"Bad response: {resp}")
                    controller.display_trains([
                        {"line": "?", "status": "Bad response", "express": False},
                        {"line": "?", "status": "Bad response", "express": False}
                    ])
        except Exception as e:
            print(f"Error: {e}")
            controller.display_trains([
                {"line": "?", "status": str(e)[:20], "express": False}
            ])
        await asyncio.sleep(interval)

async def main() -> None:
    """Main function to set up and run the train display."""
    # Get the controller instance
    controller = get_controller()
    
    # Register signal handlers for graceful shutdown
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda s, f: sys.exit(0))
    
    # Start polling and displaying trains
    try:
        await poll_and_display(controller, API_URL, POLLING_INTERVAL)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        controller.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
