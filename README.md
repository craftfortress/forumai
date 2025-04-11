# ForumAI

## Simplest Agent Chat system for idiots - just add your gemini token

A collaborative AI system that uses multiple AI agents to help achieve your goals through strategic discussions and implementation planning.

## Features

- Multiple specialized AI agents working together
- Real-time discussion monitoring
- Goal tracking and strategy development
- Web-based monitoring interface
- Persistent storage of goals and strategies

## Setup

1. Clone the repository:
```bash
git clone https://github.com/craftfortress/forumai.git
cd forumai
```

2. Create and activate a virtual environment:
```bash
python -m venv agent_village_env
source agent_village_env/bin/activate  # On Windows: agent_village_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Gemini API key:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the project root
   - Add your API key: `GEMINI_API_KEY=your_api_key_here`
   - Note: Gemini API is extremely cost-effective, typically costing less than $0.01 per conversation

5. Run the application:
```bash
python agent_village.py
```

6. Open your browser and navigate to:
```
http://localhost:5001
```

## Usage

1. Enter your goals in the web interface
2. Click "Start Discussion" to begin the AI collaboration
3. Monitor the discussion in real-time
4. Review and implement the suggested strategies

## Project Structure

- `agent_village.py`: Main application file
- `agents.py`: Agent definitions and behaviors
- `templates/`: HTML templates for the web interface
- `goals.txt`: Stores your current goals
- `current_strategy.txt`: Stores the current implementation strategy

## Contributing

Feel free to submit issues and enhancement requests! 