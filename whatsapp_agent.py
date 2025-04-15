import os
import pywhatkit as kit
from dotenv import load_dotenv
from backend.agents.base_agent import BaseAgent  # Ensure your folder structure is correct

# Load environment variables (assumes .env is in the root directory)
load_dotenv()

class WhatsAppAgent(BaseAgent):
    """
    WhatsApp Agent using pywhatkit to send messages via WhatsApp Web.

    Command format:
    whatsapp: send "Message content" to '+phone_number'
    """

    def __init__(self):
        super().__init__("WhatsApp Agent")
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")  # Not used by pywhatkit but kept for consistency

    def send_message(self, to: str, message: str) -> str:
        try:
            # Send instantly without scheduled delay
            kit.sendwhatmsg_instantly(to, message, wait_time=10, tab_close=True, close_time=3)
            return f"✅ WhatsApp message sent instantly to {to}!"
        except Exception as e:
            return f"❌ Failed to send WhatsApp message: {e}"

    def run(self, command: str) -> str:
        """
        Parse and run the WhatsApp command.
        Example command:
        whatsapp: send "Hello!" to '+919999999999'
        """
        try:
            parts = command.split('"')
            if len(parts) < 3:
                return "⚠️ Invalid format. Use: send \"message\" to '+1234567890'"
            
            message = parts[1]
            to_part = command.split("to")[-1].strip().strip("'").strip('"')
            return self.send_message(to_part, message)
        except Exception as e:
            return f"⚠️ Error processing WhatsApp command: {e}"

if __name__ == "__main__":
    # For testing the agent standalone:
    agent = WhatsAppAgent()
    print(agent.run("send \"Hello from Narad!\" to '+919768817033'"))
