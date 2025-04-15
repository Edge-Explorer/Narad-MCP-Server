import sys
import os
import logging

# Add the project's root (Narad folder) to the Python path so that backend and its subfolders can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import the necessary modules and agents
from backend.core.model_loader import load_model
from backend.agents.github_agent import GitHubAgent
from backend.agents.email_agent import EmailAgent
from backend.agents.whatsapp_agent import WhatsAppAgent

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("NaradCore")

def route_command(command: str, model) -> str:
    """
    Routes the user command to the appropriate agent based on the prefix.
    Supported commands:
      - github: <command>
      - email: <command>
      - whatsapp: <command>
    If no known prefix is found, it defaults to generating a response using the local LLM.
    """
    lower_command = command.lower().strip()
    
    if lower_command.startswith("github:"):
        gh_command = command[len("github:"):].strip()
        agent = GitHubAgent()
        return agent.run(gh_command)
    elif lower_command.startswith("email:"):
        email_command = command[len("email:"):].strip()
        agent = EmailAgent()
        return agent.run(email_command)
    elif lower_command.startswith("whatsapp:"):
        wa_command = command[len("whatsapp:"):].strip()
        agent = WhatsAppAgent()
        return agent.run(wa_command)
    
    # Fallback to the LLM model's response
    return model.generate(command)

def main():
    """
    Main entry point for Narad core.
    This function loads the LLM model, then enters a loop to accept user commands.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    models_dir = os.path.join(base_dir, "models")
    model_file = "Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf"  # Update if necessary
    model_path = os.path.join(models_dir, model_file)
    
    try:
        model = load_model(model_path)
        logger.info("✅ Narad Core: Model loaded successfully!")
    except Exception as e:
        logger.error("❌ Error loading the model: %s", e)
        return

    logger.info("🟢 Narad is ready. Type your command or 'exit' to quit.")
    
    while True:
        user_input = input("Command: ").strip()
        if not user_input:
            continue  # Ignore blank inputs
        if user_input.lower() in ["exit", "quit"]:
            logger.info("👋 Exiting Narad. Goodbye!")
            break

        try:
            response = route_command(user_input, model)
            print("Narad:", response)
        except Exception as e:
            logger.error("❌ Error generating response: %s", e)
            print("Narad: ⚠️ An error occurred. Please try again.")

if __name__ == "__main__":
    main()


