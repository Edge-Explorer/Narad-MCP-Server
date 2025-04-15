import sys
import os
import logging
from flask import Flask, request, jsonify

# Add the root project directory to the Python path so that backend modules are found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Import your model loader and agents
from backend.core.model_loader import load_model
from backend.agents.github_agent import GitHubAgent
from backend.agents.email_agent import EmailAgent
from backend.agents.whatsapp_agent import WhatsAppAgent

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("MCPServer")

# Create the Flask app
app = Flask(__name__)

# Load your local LLM model on startup
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
models_dir = os.path.join(base_dir, "models")
model_file = "Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf"  # Update if necessary
model_path = os.path.join(models_dir, model_file)

try:
    model = load_model(model_path)
    logger.info("MCP Server: Model loaded successfully!")
except Exception as e:
    logger.error("MCP Server: Error loading model: %s", e)
    model = None

def route_command(command: str, model) -> str:
    """
    Routes the user command to the appropriate agent based on the prefix.
    
    Supported prefixes:
      - github: <command>
      - email: <command>
      - whatsapp: <command>
    Fallbacks to the local LLM model if no agent is specified.
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
    
    if model is not None:
        return model.generate(command)
    else:
        return "LLM model not loaded."

@app.route("/command", methods=["POST"])
def handle_command():
    """
    HTTP endpoint to process commands.
    Expected JSON input:
      { "command": "your command text" }
    Returns a JSON response with the result.
    """
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "No command provided"}), 400
    
    command = data["command"]
    logger.info("Processing command: %s", command)
    response = route_command(command, model)
    return jsonify({"response": response})

if __name__ == "__main__":
    # Run the MCP server on all interfaces at port 5000
    app.run(host="0.0.0.0", port=5000)
