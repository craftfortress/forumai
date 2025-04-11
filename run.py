#!/usr/bin/env python3
"""
Run script for Agent Village
This script helps with starting the Agent Village application.
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has OpenAI API key."""
    env_file = Path(".env")
    if not env_file.exists():
        print("Error: .env file not found.")
        print("Please run setup.py first or create a .env file manually.")
        sys.exit(1)
    
    with open(env_file, "r") as f:
        content = f.read()
        if "OPENAI_API_KEY" not in content or "your_openai_api_key_here" in content:
            print("Error: OpenAI API key not set in .env file.")
            print("Please edit .env to add your OpenAI API key.")
            sys.exit(1)
    
    print("✓ Environment configuration check passed.")

def start_application():
    """Start the Agent Village application."""
    print("Starting Agent Village...")
    
    try:
        # Start the Flask application
        process = subprocess.Popen([sys.executable, "agent_village.py"])
        
        print("\nAgent Village is running!")
        print("Open your browser and navigate to: http://localhost:5000")
        print("\nPress Ctrl+C to stop the application.")
        
        # Wait for the process to complete or for Ctrl+C
        process.wait()
        
    except KeyboardInterrupt:
        print("\nStopping Agent Village...")
        process.terminate()
        process.wait()
        print("Agent Village stopped.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    """Main run function."""
    check_env_file()
    start_application()

if __name__ == "__main__":
    main() 