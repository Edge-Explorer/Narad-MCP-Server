# backend/agents/base_agent.py

class BaseAgent:
    """Base class for all agents in the system."""
    def __init__(self, name: str):
        self.name = name

    def run(self, command: str) -> str:
        """Processes the given command and returns a response.
        This should be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")
