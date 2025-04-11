# Agent Village

A collaborative AI agent system that uses multiple specialized agents to discuss and refine strategies for solving complex problems.

## Overview

Agent Village is a web-based monitoring system that allows you to observe and interact with a group of AI agents as they collaborate to solve problems. The system includes:

- A web interface for monitoring agent discussions
- Real-time strategy evolution tracking
- Multiple specialized agents (Researcher, Strategist, Implementer)
- Persistent logging of all agent interactions

## Features

- **Multi-Agent Collaboration**: Three specialized agents work together to analyze and solve problems
- **Strategy Evolution**: Watch as the agents refine their approach over time
- **Real-time Monitoring**: Web interface to observe agent discussions and strategy changes
- **Persistent Logging**: All agent interactions are saved for later review

## Requirements

- Python 3.10+
- OpenAI API key
- Flask
- PyAutoGen
- OpenAI Python client
- Python-dotenv

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd agent-village
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on the provided `.env.example`:
   ```
   cp .env.example .env
   ```

4. Edit the `.env` file to add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the application:
   ```
   python agent_village.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Use the web interface to:
   - Monitor agent discussions in real-time
   - View the evolving strategy
   - Start new discussions on specific topics
   - Clear logs when needed

## Project Structure

- `agent_village.py`: Main application file with agent definitions and Flask routes
- `monitor.html`: Web interface for monitoring agent activities
- `agent_logs.txt`: Persistent log file of all agent interactions
- `current_strategy.txt`: File storing the current strategy
- `requirements.txt`: Python dependencies
- `.env`: Configuration file for API keys (not included in repository)

## Troubleshooting

If you encounter the error `ImportError: cannot import name 'APITimeoutError' from 'openai'`, try:
```
pip install --upgrade openai
```

For the warning about flaml.automl, you can install the additional dependencies:
```
pip install "flaml[automl]"
```

## License

MIT 