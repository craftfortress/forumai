import os
from datetime import datetime
from typing import Optional
from config import GOALS_FILE, STRATEGY_FILE, CHAT_LOGS_DIR, SCRATCHPAD_DIR

def ensure_directories():
    """Ensure all required directories exist."""
    os.makedirs(CHAT_LOGS_DIR, exist_ok=True)
    os.makedirs(SCRATCHPAD_DIR, exist_ok=True)

def write_strategy(content: str, append: bool = True):
    """Write content to strategy file, with option to append or overwrite."""
    mode = "a" if append else "w"
    with open(STRATEGY_FILE, mode) as f:
        if append:
            f.write("\n\n" + "="*50 + "\n")
            f.write(f"Update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
        f.write(content)

def log_chat(content: str):
    """Log chat content to a timestamped file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log_{timestamp}.txt"
    filepath = os.path.join(CHAT_LOGS_DIR, filename)
    
    with open(filepath, "w") as f:
        f.write(f"Chat Session: {timestamp}\n")
        f.write("="*50 + "\n\n")
        f.write(content)

def load_goal() -> Optional[str]:
    """Load the current goal from goals.txt."""
    try:
        with open(GOALS_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_to_scratchpad(content: str, prefix: str = "explorer"):
    """Save content to scratchpad with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.txt"
    filepath = os.path.join(SCRATCHPAD_DIR, filename)
    
    with open(filepath, "w") as f:
        f.write(content)

def get_latest_strategy() -> Optional[str]:
    """Read the current strategy file."""
    try:
        with open(STRATEGY_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None 