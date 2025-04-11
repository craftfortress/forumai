import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Agent definitions with their system messages
AGENT_DEFS = [
    {
        "name": "Explorer",
        "message": """You are the Explorer agent. Your role is to generate bold, unconventional strategies and ideas.
        Think outside the box and don't be afraid to suggest radical approaches.
        Focus on innovation and novel solutions that others might not consider."""
    },
    {
        "name": "Critic",
        "message": """You are the Critic agent. Your role is to find flaws and potential issues in all proposals.
        Be thorough and analytical in your criticism, but maintain a constructive tone.
        Focus on identifying risks, edge cases, and potential failure points."""
    },
    {
        "name": "Synthesizer",
        "message": """You are the Synthesizer agent. Your role is to merge and polish ideas into clear, actionable concepts.
        Take the best elements from different proposals and combine them into coherent strategies.
        Ensure the final output is practical and well-structured."""
    },
    {
        "name": "Refiner",
        "message": """You are the Refiner agent. Your role is to update the strategy document based on the best insights.
        Write clear, concise, and actionable content that builds upon the group's discussion.
        Focus on creating a living document that evolves with each iteration."""
    }
]

# Model configurations
MODELS = {
    "openai": {
        "temperature": 0.7,
        "model": "gpt-4o",
        "api_key": os.getenv("OPENAI_API_KEY")
    },
    "gemini": {
        "temperature": 0.7,
        "model": "gemini-2.5-pro",  # Latest Gemini model
        "api_key": os.getenv("GOOGLE_API_KEY")
    }
}

# Default model to use
DEFAULT_MODEL = "gemini"  # Change this to "openai" to use OpenAI

# File paths
GOALS_FILE = "goals.txt"
STRATEGY_FILE = "strategy.txt"
CHAT_LOGS_DIR = "chat_logs"
SCRATCHPAD_DIR = "scratchpad"

# Loop configuration
LOOP_INTERVAL = 60  # seconds between iterations 