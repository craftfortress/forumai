import subprocess
import sys
import time
import os
import signal
import atexit

def start_agents():
    print("Starting Agent Village system...")
    agent_process = subprocess.Popen([sys.executable, "agents.py"], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
    return agent_process

def start_server():
    print("Starting monitoring server...")
    server_process = subprocess.Popen([sys.executable, "server.py"], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
    return server_process

def cleanup(agent_process, server_process):
    print("\nShutting down...")
    if agent_process:
        agent_process.terminate()
    if server_process:
        server_process.terminate()
    print("All processes terminated.")

def main():
    # Start the agent system
    agent_process = start_agents()
    
    # Give the agent system a moment to start
    time.sleep(2)
    
    # Start the monitoring server
    server_process = start_server()
    
    # Register cleanup function
    atexit.register(cleanup, agent_process, server_process)
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\nReceived Ctrl+C. Shutting down...")
        cleanup(agent_process, server_process)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\n" + "="*50)
    print("Agent Village system is running!")
    print("Open your browser and go to: http://localhost:8000")
    print("Press Ctrl+C to stop the system")
    print("="*50 + "\n")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main() 