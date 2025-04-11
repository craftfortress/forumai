import os
import json
import time
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import autogen
import google.generativeai as genai
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from flask_sock import Sock

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
sock = Sock(app)

# Add Content Security Policy headers
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; connect-src 'self' ws: wss:; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:;"
    return response

# Global variables to store logs and strategy
chat_logs = []
current_strategy = "Initial strategy: Set clear, measurable goals and create actionable steps to achieve them through effective collaboration and continuous progress tracking."
connected_clients = set()
active_discussion = False
discussion_thread = None

# Configure Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# Configure Gemini API
genai.configure(api_key=api_key)

# Create the model configuration
model_config = {
    "config_list": [{
        "model": "gemini-1.5-pro",
        "api_key": api_key,
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "api_type": "google"
    }],
    "timeout": 600,
    "cache_seed": None
}

# Create necessary files if they don't exist
def ensure_files_exist():
    files_to_create = {
        "agent_logs.txt": "",
        "current_strategy.txt": current_strategy,
        "goals.txt": "Personal Goals:\n1. Improve productivity\n2. Learn new skills\n3. Maintain work-life balance"
    }
    for filename, initial_content in files_to_create.items():
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(initial_content)
            logger.info(f"Created {filename}")

# Ensure files exist before creating agents
ensure_files_exist()

# Create agents with the model configuration
researcher = AssistantAgent(
    name="Researcher",
    llm_config=model_config,
    system_message="""You are a research agent. Your role:
    1. Read goals from goals.txt (read-only)
    2. Read strategy from current_strategy.txt (read-only)
    3. Analyze and provide insights
    4. Be extremely concise - use bullet points and short sentences""",
    human_input_mode="NEVER"
)

strategist = AssistantAgent(
    name="Strategist",
    llm_config=model_config,
    system_message="""You are a strategy agent. Your role:
    1. Read goals from goals.txt (read-only)
    2. Read/write strategy in current_strategy.txt
    3. Create actionable steps
    4. Be extremely concise - use bullet points and short sentences""",
    human_input_mode="NEVER"
)

implementer = AssistantAgent(
    name="Implementer",
    llm_config=model_config,
    system_message="""You are an implementation agent. Your role:
    1. Read goals from goals.txt (read-only)
    2. Read strategy from current_strategy.txt (read-only)
    3. Create practical action steps
    4. Be extremely concise - use bullet points and short sentences""",
    human_input_mode="NEVER"
)

user_proxy = UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
    llm_config=model_config,
    system_message="""You are a user interface agent. Your role:
    1. Read goals from goals.txt (read-only)
    2. Guide discussions based on goals
    3. Keep discussions focused
    4. Be extremely concise - use bullet points and short sentences"""
)

# Create the group chat with proper configuration
groupchat = GroupChat(
    agents=[researcher, strategist, implementer, user_proxy],
    messages=[],
    max_round=50,
    speaker_selection_method="round_robin"
)

chat_manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=model_config
)
logger.info("Successfully created all agents and group chat")

# Function to log messages with timestamp
def log_message(sender, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {sender}: {message}"
    
    # Add to in-memory logs
    chat_logs.append(log_entry)
    
    # Save to file
    with open("agent_logs.txt", "a") as f:
        f.write(log_entry + "\n")
    
    # Broadcast to all connected WebSocket clients
    broadcast_log(log_entry)
    
    return log_entry

# Function to broadcast log to all connected clients
def broadcast_log(log_entry):
    """Broadcast a log message to all connected clients"""
    logger.info(f"Broadcasting log: {log_entry}")
    message = json.dumps({"log": log_entry})
    for client in connected_clients:
        try:
            client.send(message)
        except Exception as e:
            logger.error(f"Error sending to client: {e}")
            connected_clients.remove(client)

# Function to update strategy file
def update_strategy_file(new_strategy):
    try:
        with open("current_strategy.txt", "w") as f:
            f.write(new_strategy)
        global current_strategy
        current_strategy = new_strategy
        log_message("System", "Strategy updated")
        return True
    except Exception as e:
        logger.error(f"Error updating strategy: {e}")
        log_message("System", f"Error updating strategy: {str(e)}")
        return False

# WebSocket route
@sock.route('/ws')
def ws(ws):
    logger.info("WebSocket connection request received")
    connected_clients.add(ws)
    logger.info(f"New WebSocket client connected. Total clients: {len(connected_clients)}")
    
    try:
        # Send initial logs
        with open("agent_logs.txt", "r") as f:
            logs = f.read()
            if logs:
                logger.info(f"Sending initial logs to client: {len(logs)} characters")
                # Send each log entry separately
                for log_line in logs.split('\n'):
                    if log_line.strip():
                        ws.send(json.dumps({"log": log_line}))
            else:
                logger.info("No initial logs to send")
        
        # Send a test message
        test_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - System: WebSocket connection established"
        ws.send(json.dumps({"log": test_message}))
        logger.info(f"Sent test message: {test_message}")
        
        # Keep the connection open
        while True:
            # Wait for messages (we don't expect any from the client)
            data = ws.receive()
            if data:
                logger.info(f"Received WebSocket message from client: {data}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(ws)
        logger.info(f"WebSocket client disconnected. Remaining clients: {len(connected_clients)}")

# Function to start a discussion
def start_discussion(topic):
    """Start a discussion with the agents"""
    global active_discussion
    
    if active_discussion:
        return {"status": "error", "message": "A discussion is already in progress. Please stop it first."}
    
    try:
        active_discussion = True
        broadcast_log(f"System: Starting discussion on topic: {topic}")
        
        # Read goals and strategy files
        try:
            with open("goals.txt", "r") as f:
                goals = f.read()
        except FileNotFoundError:
            goals = "No goals file found."
            broadcast_log("System: Warning - goals.txt not found")
        
        try:
            with open("current_strategy.txt", "r") as f:
                current_strategy = f.read()
        except FileNotFoundError:
            current_strategy = "No strategy file found."
            broadcast_log("System: Warning - current_strategy.txt not found")
        
        # Create the message for the agents
        message = f"""
        Let's discuss the following topic: {topic}
        
        Current goals (from goals.txt):
        {goals}
        
        Current strategy (from current_strategy.txt):
        {current_strategy}
        
        Please provide your thoughts and suggestions. Remember:
        1. Goals are read-only from goals.txt
        2. Strategy can be read/written in current_strategy.txt
        3. Be extremely concise - use bullet points and short sentences
        4. Focus on actionable steps and measurable outcomes
        5. Keep responses brief and to the point
        6. DO NOT ask for the contents of goals.txt or current_strategy.txt - they are provided above
        """
        
        # Start the discussion
        try:
            # Initialize the chat with the message
            response = chat_manager.initiate_chat(
                user_proxy,
                message=message
            )
            
            # Process the response
            if response is not None:
                if hasattr(response, 'summary'):
                    broadcast_log(f"System: Discussion completed with summary: {response.summary}")
                else:
                    broadcast_log("System: Discussion completed")
                
                # Log any messages from the chat
                if hasattr(groupchat, 'messages') and groupchat.messages:
                    for msg in groupchat.messages:
                        if isinstance(msg, dict) and 'content' in msg and 'name' in msg:
                            broadcast_log(f"{msg['name']}: {msg['content']}")
            else:
                broadcast_log("System: No response from chat manager")
            
            active_discussion = False
            return {"status": "success", "message": "Discussion completed successfully"}
            
        except Exception as chat_error:
            logger.error(f"Error in chat: {str(chat_error)}")
            broadcast_log(f"System: Error in chat: {str(chat_error)}")
            active_discussion = False
            return {"status": "error", "message": f"Error in chat: {str(chat_error)}"}
            
    except Exception as e:
        logger.error(f"Error starting discussion: {str(e)}")
        broadcast_log(f"System: Error starting discussion: {str(e)}")
        active_discussion = False
        return {"status": "error", "message": f"Error starting discussion: {str(e)}"}

# Function to stop a discussion
def stop_discussion():
    global active_discussion
    
    if not active_discussion:
        log_message("System", "No active discussion to stop")
        return "No active discussion to stop"
    
    try:
        active_discussion = False
        log_message("System", "Discussion stopped by user request")
        return "Discussion stopped successfully"
    except Exception as e:
        error_msg = f"Error stopping discussion: {str(e)}"
        logger.error(error_msg)
        log_message("System", error_msg)
        return error_msg

# Flask routes
@app.route('/')
def index():
    return render_template('monitor.html')

@app.route('/play_sound', methods=['GET'])
def play_sound():
    try:
        # Play the system sound using afplay
        os.system('afplay /System/Library/Sounds/Tink.aiff')
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_logs')
def get_logs():
    try:
        with open("agent_logs.txt", "r") as f:
            logs = f.read()
        return logs
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return "Error reading logs"

@app.route('/get_strategy')
def get_strategy():
    try:
        with open("current_strategy.txt", "r") as f:
            strategy = f.read()
        return strategy
    except Exception as e:
        logger.error(f"Error reading strategy: {e}")
        return "Error reading strategy"

@app.route('/start_discussion', methods=['POST'])
def api_start_discussion():
    data = request.json
    topic = data.get('topic', 'How can I achieve my goals with cunning and keeping costs low?')
    result = start_discussion(topic)
    return jsonify({"status": "success", "message": result})

@app.route('/stop_discussion', methods=['POST'])
def api_stop_discussion():
    result = stop_discussion()
    return jsonify({"status": "success", "message": result})

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    global chat_logs
    chat_logs = []
    with open("agent_logs.txt", "w") as f:
        f.write("")
    log_message("System", "Logs cleared")
    return jsonify({"status": "success"})

@app.route('/save_strategy', methods=['POST'])
def save_strategy():
    try:
        data = request.get_json()
        strategy = data.get('strategy', '')
        if update_strategy_file(strategy):
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Failed to update strategy"}), 500
    except Exception as e:
        logger.error(f"Error saving strategy: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/save_goals', methods=['POST'])
def save_goals():
    try:
        data = request.get_json()
        goals = data.get('goals', '')
        with open("goals.txt", "w") as f:
            f.write(goals)
        log_message("System", "Goals updated")
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error saving goals: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test')
def test():
    return jsonify({"status": "success", "message": "Server is running"})

@app.route('/get_previous_logs')
def get_previous_logs():
    try:
        with open("agent_logs.txt", "r") as f:
            logs = f.read()
            if logs:
                # Return logs as a JSON array
                log_lines = [line.strip() for line in logs.split('\n') if line.strip()]
                return jsonify({"logs": log_lines})
            else:
                return jsonify({"logs": []})
    except Exception as e:
        logger.error(f"Error reading previous logs: {e}")
        return jsonify({"logs": [], "error": str(e)})

@app.route('/get_goals')
def get_goals():
    try:
        with open("goals.txt", "r") as f:
            goals = f.read()
        return goals
    except Exception as e:
        logger.error(f"Error reading goals: {e}")
        return "Error reading goals"

@app.route('/ws_test')
def ws_test():
    """Test endpoint to check if WebSocket is working"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <div id="status">Connecting...</div>
        <div id="messages"></div>
        <script>
            const ws = new WebSocket('ws://' + window.location.hostname + ':5001/ws');
            const status = document.getElementById('status');
            const messages = document.getElementById('messages');
            
            ws.onopen = function() {
                status.textContent = 'Connected';
                status.style.color = 'green';
            };
            
            ws.onmessage = function(event) {
                const message = document.createElement('div');
                message.textContent = event.data;
                messages.appendChild(message);
            };
            
            ws.onclose = function() {
                status.textContent = 'Disconnected';
                status.style.color = 'red';
            };
            
            ws.onerror = function() {
                status.textContent = 'Error';
                status.style.color = 'red';
            };
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True, port=5001) 