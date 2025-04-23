#!/usr/bin/env python3
import asyncio
import sys
import signal
import os
from typing import Dict, List, Any
from pathlib import Path
from dotenv import load_dotenv
import logging

import httpx

from rgb_matrix_controller import get_controller

# Load environment variables from .env file
script_dir = Path(__file__).parent.absolute()
env_path = script_dir / '.env'
load_dotenv(dotenv_path=env_path)

POLLING_INTERVAL = 15
API_URL = os.environ.get("TRAIN_API_URL")

try:
    # Set affinity to CPUs 0, 1, 2 (leaving 3 isolated)
    os.sched_setaffinity(0, {0, 1, 2})
    print("Set CPU affinity to cores 0-2")
except Exception as e:
    print(f"Could not set CPU affinity: {e}")

# For non-root users, use a lower priority
try:
    os.nice(-10)  # Use nice instead of real-time priority
    print("Set process priority")
except Exception as e:
    print(f"Could not set process priority: {e}")

async def poll_and_display(controller: Any, url: str, interval: int) -> None:
    """Poll a URL for train data and display it on the matrix.
    
    Args:
        controller: The matrix controller object
        url: The API URL to poll for train data
        interval: The polling interval in seconds
    """
    print(f"Starting application with API URL: {url}")
    print(f"Polling interval: {interval} seconds")
    
    while True:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=5.0)
                if resp.status_code == 200:
                    trains = resp.json()
                    logging.debug(f"Response: {trains}")
                    await controller.display_trains(trains[:2])  # Display first two trains
                else:
                    logging.error(f"Bad response: {resp.status_code} - {resp.text[:100]}")
                    await controller.display_trains([
                        {"line": "?", "status": f"Error {resp.status_code}", "express": False},
                        {"line": "?", "status": "Bad response", "express": False}
                    ])
        except httpx.RequestError as e:
            logging.error(f"Request error: {e}")
            await controller.display_trains([
                {"line": "?", "status": "Network error", "express": False}
            ])
        except Exception as e:
            logging.error(f"Unexpected error: {e}", exc_info=True)
            await controller.display_trains([
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
