import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from backend.agents.base_agent import BaseAgent


# Load environment variables from the .env file.
load_dotenv()

class EmailAgent(BaseAgent):
    """
    Email Agent for Narad that sends emails using SMTP.
    
    Two command modes are supported:
    
    1. Non-interactive mode:
       Command format:
       send "Your message here" [with subject "Subject text"] to 'recipient@example.com'
       
    2. Interactive mode:
       Use: email: compose email
       Narad will then prompt for:
         - Greeting (Title), e.g., "Dear John,"
         - Subject, e.g., "Meeting Reminder"
         - Message body, e.g., "I would like to remind you about..."
         - Closing, e.g., "Yours faithfully,"
         - Recipient email address
    """
    def __init__(self):
        super().__init__("Email Agent")
        self.email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        try:
            self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        except ValueError:
            self.smtp_port = 587

    def send_email(self, to_address: str, subject: str, message: str) -> str:
        """
        Sends an email via SMTP.
        :param to_address: Recipient email address.
        :param subject: Email subject.
        :param message: Email message body.
        :return: Success or error message.
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = to_address
            msg["Subject"] = subject
            msg["Date"] = formatdate(localtime=True)
            # Attach the text message.
            msg.attach(MIMEText(message, "plain"))
            
            # Connect to SMTP server and send the email.
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            return f"✅ Email sent successfully to {to_address}!"
        except Exception as e:
            return f"❌ Error sending email: {e}"

    def interactive_mode(self) -> str:
        """
        Guides the user through step-by-step input to compose an email.
        """
        try:
            print("Enter the greeting (e.g., 'Dear John,'):")
            greeting = input(">> ").strip()
            print("Enter the subject:")
            subject = input(">> ").strip()
            print("Enter the message body:")
            body = input(">> ").strip()
            print("Enter the closing (e.g., 'Yours faithfully,'):")
            closing = input(">> ").strip()
            print("Enter the recipient email (e.g., recipient@example.com):")
            recipient = input(">> ").strip()

            # Construct the full message.
            full_message = f"{greeting}\n\n{body}\n\n{closing}"
            return self.send_email(recipient, subject, full_message)
        except Exception as e:
            return f"Error during interactive email composition: {e}"

    def run(self, command: str) -> str:
        """
        Processes the email command.
        
        If the command is 'compose email' (non-case-sensitive), then it enters interactive mode;
        otherwise, it falls back to parsing a single-line command.
        
        Expected non-interactive command format:
        send "Your message here" [with subject "Subject text"] to 'recipient@example.com'
        """
        try:
            lower_command = command.lower().strip()
            if lower_command == "compose email":
                return self.interactive_mode()
            else:
                # Non-interactive parsing mode.
                parts = command.split('"')
                if len(parts) < 3:
                    return ("Invalid command format. Use: send \"Your message here\" "
                            "[with subject \"Subject text\"] to 'recipient@example.com'")
                
                message_content = parts[1]
                subject = "Narad Email"
                if "with subject" in command:
                    subject_parts = command.split("with subject")
                    sub_part = subject_parts[1].strip()
                    if sub_part.startswith('"'):
                        subject_text = sub_part.split('"')[1]
                        if subject_text:
                            subject = subject_text
                if "to" not in command:
                    return ("Invalid command format: missing recipient. "
                            "Use: send \"Your message here\" [with subject \"Subject text\"] to 'recipient@example.com'")
                after_to = command.split("to", 1)[1]
                recipient = after_to.split("'")[1]
                return self.send_email(recipient, subject, message_content)
        except Exception as e:
            return f"⚠️ Error processing email command: {e}"

# Standalone test mode: Uncomment the following lines for testing.
# if __name__ == "__main__":
#     agent = EmailAgent()
#     # For interactive mode, type: email: compose email
#     print(agent.run("compose email"))
