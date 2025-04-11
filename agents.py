import time
from typing import List, Dict
import autogen
import google.generativeai as genai
from config import AGENT_DEFS, MODELS, DEFAULT_MODEL, LOOP_INTERVAL
from tools import (
    ensure_directories,
    write_strategy,
    log_chat,
    load_goal,
    save_to_scratchpad,
    get_latest_strategy
)

class AgentVillage:
    def __init__(self):
        ensure_directories()
        self.model_config = MODELS[DEFAULT_MODEL]
        self._setup_model()
        self.agents = self._create_agents()
        self.group_chat = None
        self.chat_manager = None

    def _setup_model(self):
        """Setup the selected model."""
        if DEFAULT_MODEL == "gemini":
            genai.configure(api_key=self.model_config["api_key"])
            # Configure the model for autogen
            self.model_config["base_url"] = "https://generativelanguage.googleapis.com/v1beta"
            self.model_config["api_type"] = "google"

    def _create_agents(self) -> Dict[str, autogen.AssistantAgent]:
        """Create all agents with their respective configurations."""
        agents = {}
        
        for agent_def in AGENT_DEFS:
            agent = autogen.AssistantAgent(
                name=agent_def["name"],
                system_message=agent_def["message"],
                llm_config=self.model_config
            )
            agents[agent_def["name"]] = agent

        # Register tools for specific agents
        agents["Refiner"]._function_map.update({
            "write_strategy": write_strategy
        })
        agents["Explorer"]._function_map.update({
            "save_to_scratchpad": save_to_scratchpad
        })

        return agents

    def _update_agent_context(self, goal: str):
        """Update agent system messages with current goal context."""
        context = f"Current goal: {goal}\n\n"
        if strategy := get_latest_strategy():
            context += f"Current strategy:\n{strategy}\n\n"
        
        for name, agent in self.agents.items():
            for agent_def in AGENT_DEFS:
                if agent_def["name"] == name:
                    agent._system_message = context + agent_def["message"]
                    break

    def run_chat_loop(self):
        """Main chat loop that runs continuously."""
        while True:
            # Load and validate goal
            goal = load_goal()
            if not goal:
                print("No goal found in goals.txt. Waiting...")
                time.sleep(LOOP_INTERVAL)
                continue

            # Update agent context with current goal
            self._update_agent_context(goal)

            # Initialize group chat
            self.group_chat = autogen.GroupChat(
                agents=list(self.agents.values()),
                messages=[],
                max_round=10
            )
            
            self.chat_manager = autogen.GroupChatManager(
                groupchat=self.group_chat,
                llm_config=self.model_config
            )

            # Run the chat session
            try:
                chat_transcript = self.chat_manager.initiate_chat(
                    message=f"Let's discuss and refine our strategy for: {goal}",
                    sender=self.agents["Explorer"]
                )
                
                # Log the chat transcript
                log_chat(str(chat_transcript))
                
            except Exception as e:
                print(f"Error in chat loop: {e}")
                log_chat(f"Error occurred: {str(e)}")

            # Wait before next iteration
            time.sleep(LOOP_INTERVAL)

if __name__ == "__main__":
    village = AgentVillage()
    village.run_chat_loop() 