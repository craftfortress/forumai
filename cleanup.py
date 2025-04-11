#!/usr/bin/env python3
"""
Cleanup script for Agent Village
This script helps with cleaning up the Agent Village system.
"""

import os
import sys
import shutil
from pathlib import Path

def confirm_action(message):
    """Ask for confirmation before performing an action."""
    response = input(f"{message} (y/n): ").lower()
    return response == 'y' or response == 'yes'

def clean_logs():
    """Clean up log files."""
    log_files = ["agent_logs.txt", "current_strategy.txt"]
    
    for file in log_files:
        path = Path(file)
        if path.exists():
            if confirm_action(f"Delete {file}?"):
                try:
                    path.unlink()
                    print(f"✓ Deleted {file}")
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
        else:
            print(f"  {file} does not exist")

def clean_workspace():
    """Clean up workspace directory."""
    workspace = Path("workspace")
    
    if workspace.exists() and workspace.is_dir():
        if confirm_action("Clean workspace directory?"):
            try:
                for item in workspace.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                print("✓ Workspace directory cleaned")
            except Exception as e:
                print(f"Error cleaning workspace: {e}")
    else:
        print("  Workspace directory does not exist")

def clean_logs_directory():
    """Clean up logs directory."""
    logs_dir = Path("logs")
    
    if logs_dir.exists() and logs_dir.is_dir():
        if confirm_action("Clean logs directory?"):
            try:
                for item in logs_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                print("✓ Logs directory cleaned")
            except Exception as e:
                print(f"Error cleaning logs directory: {e}")
    else:
        print("  Logs directory does not exist")

def reset_strategy():
    """Reset the current strategy to default."""
    strategy_file = Path("current_strategy.txt")
    default_strategy = "Initial strategy: Collaborate to solve complex problems by breaking them down into manageable tasks."
    
    if confirm_action("Reset current strategy to default?"):
        try:
            with open(strategy_file, "w") as f:
                f.write(default_strategy)
            print("✓ Strategy reset to default")
        except Exception as e:
            print(f"Error resetting strategy: {e}")
    else:
        print("  Strategy reset cancelled")

def main():
    """Main cleanup function."""
    print("Agent Village Cleanup Tool\n")
    
    if not confirm_action("This will clean up log files and reset the system. Continue?"):
        print("Cleanup cancelled.")
        sys.exit(0)
    
    clean_logs()
    clean_workspace()
    clean_logs_directory()
    reset_strategy()
    
    print("\nCleanup completed.")

if __name__ == "__main__":
    main() 