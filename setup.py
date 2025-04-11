#!/usr/bin/env python3
"""
Setup script for Agent Village
This script helps with installation and configuration of the Agent Village system.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 10):
        print("Error: Python 3.10 or higher is required.")
        sys.exit(1)
    print("✓ Python version check passed.")

def install_dependencies():
    """Install required Python packages."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies.")
        sys.exit(1)

def setup_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("✓ Created .env file from .env.example")
            print("  Please edit .env to add your OpenAI API key.")
        else:
            print("Error: .env.example file not found.")
            sys.exit(1)
    else:
        print("✓ .env file already exists.")

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ["workspace", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✓ Created necessary directories.")

def main():
    """Main setup function."""
    print("Setting up Agent Village...")
    
    check_python_version()
    install_dependencies()
    setup_env_file()
    create_directories()
    
    print("\nSetup completed successfully!")
    print("\nTo start the application, run:")
    print("  python agent_village.py")
    print("\nThen open your browser and navigate to:")
    print("  http://localhost:5000")

if __name__ == "__main__":
    main() 