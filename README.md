# Narad MCP Server

Narad MCP Server integrates GitHub, Email, and WhatsApp agents, allowing seamless communication and task automation through HTTP requests. It supports real-time and offline operations, providing a secure, efficient backend solution for managing multiple services with AI-powered workflows.([GitHub][1])

---

## ⚙️ Features

* **Multi-Channel Integration**: Connects with GitHub, Email, and WhatsApp for comprehensive communication management.
* **Task Automation**: Automates tasks across integrated platforms using HTTP requests.
* **Real-Time & Offline Support**: Operates both in real-time and offline modes for flexible usage.
* **Secure Backend**: Ensures secure operations with a robust backend architecture.

---

## 🧠 Tech Stack

* **Backend**: Python (Flask)
* **Communication Protocol**: HTTP
* **Integration Platforms**: GitHub, Email, WhatsApp([MCP][2])

---

## 📁 Modules

* `base_agent.py`: Abstract base class for all agents.
* `email_agent.py`: Handles email-related functionalities.
* `github_agent.py`: Manages interactions with GitHub.
* `mcp_server.py`: Core server handling multi-channel processing.
* `model_loader.py`: Loads and manages models.
* `narad_core.py`: Central logic for orchestrating agent interactions.
* `whatsapp_agent.py`: Facilitates communication through WhatsApp.([MCP][2], [Gist][3])

---

## 🧪 Input

* **User Commands**: Textual inputs provided by the user through the integrated platforms.
* **Platform Events**: Incoming messages or notifications from integrated platforms like GitHub, Email, and WhatsApp.([Natoma][4])

---

## 🚀 Goal

To develop a versatile and private backend server capable of managing multiple communication channels, providing intelligent responses, and enhancing user productivity without compromising data privacy.

