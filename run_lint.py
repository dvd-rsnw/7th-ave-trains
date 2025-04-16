#!/usr/bin/env python3
"""
Script to run pylint on all Python files in the project.
Usage: python run_lint.py
"""

import os
import subprocess
import sys
from typing import List


def get_python_files() -> List[str]:
    """Get a list of all Python files in the project directory.
    
    Returns:
        List of Python file paths
    """
    python_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and not root.startswith("./.venv"):
                python_files.append(os.path.join(root, file))
    return python_files


def run_pylint(files: List[str]) -> int:
    """Run pylint on the given files.
    
    Args:
        files: List of file paths to lint
        
    Returns:
        Exit code from pylint
    """
    try:
        cmd = ["pylint"] + files
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print("Error: pylint is not installed. Install it with:")
        print("pip install pylint")
        return 1


def main() -> int:
    """Main entry point.
    
    Returns:
        Exit code
    """
    python_files = get_python_files()
    if not python_files:
        print("No Python files found.")
        return 0
    
    print(f"Found {len(python_files)} Python files to lint")
    return run_pylint(python_files)


if __name__ == "__main__":
    sys.exit(main()) 