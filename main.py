#!/usr/bin/env python3
"""
Main entry point for running LLM Chat directly.
This allows running the package without installation using `python main.py`
"""

import sys
import os

print(f"Current working directory: {os.getcwd()}")
print(f"Python path before modification: {sys.path}")

# Add src directory to Python path when running directly
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SCRIPT_DIR, "src")
sys.path.append(SRC_DIR)

print(f"Script directory: {SCRIPT_DIR}")
print(f"SRC directory: {SRC_DIR}")
print(f"Python path after modification: {sys.path}")

try:
    from src.llm_chat.cli import main

    print("Successfully imported main from llm_chat.cli")
except ImportError as e:
    print(f"Import error: {e}")
    print("Error: Could not import llm_chat package.")
    print("Make sure you have all dependencies installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def run_main():
    """
    Wrapper function to handle any high-level setup/teardown needed when
    running the application directly.
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_main()
