#!/usr/bin/env python3
"""
Update script for Agent Village
This script helps with updating dependencies for the Agent Village system.
"""

import os
import sys
import subprocess
import pkg_resources
import json
from pathlib import Path

def get_installed_versions():
    """Get currently installed package versions."""
    installed = {}
    for package in ["flask", "pyautogen", "openai", "python-dotenv"]:
        try:
            installed[package] = pkg_resources.get_distribution(package).version
        except pkg_resources.DistributionNotFound:
            installed[package] = None
    return installed

def get_required_versions():
    """Get required package versions from requirements.txt."""
    required = {}
    try:
        with open("requirements.txt", "r") as f:
            for line in f:
                if "==" in line:
                    package, version = line.strip().split("==")
                    required[package] = version
    except FileNotFoundError:
        print("Error: requirements.txt not found.")
        sys.exit(1)
    return required

def update_packages():
    """Update packages to their required versions."""
    installed = get_installed_versions()
    required = get_required_versions()
    
    print("Current package versions:")
    for package, version in installed.items():
        status = "✓" if version == required.get(package) else "✗"
        print(f"  {status} {package}: {version or 'Not installed'}")
    
    print("\nRequired package versions:")
    for package, version in required.items():
        print(f"  {package}: {version}")
    
    print("\nUpdating packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"])
        print("✓ Packages updated successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to update packages.")
        sys.exit(1)
    
    # Verify updates
    print("\nVerifying updates...")
    updated = get_installed_versions()
    all_updated = True
    
    for package, version in required.items():
        if updated.get(package) != version:
            print(f"✗ {package} is still at version {updated.get(package)}, expected {version}")
            all_updated = False
    
    if all_updated:
        print("✓ All packages are now at their required versions.")
    else:
        print("Some packages could not be updated to their required versions.")
        print("Please try updating manually: pip install -r requirements.txt --upgrade")

def main():
    """Main update function."""
    print("Agent Village Update Tool\n")
    update_packages()
    print("\nUpdate process completed.")

if __name__ == "__main__":
    main() 