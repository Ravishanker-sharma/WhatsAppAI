# WhatsApp AI Assistant

This project is a Python-based AI assistant that monitors your WhatsApp for new messages and automatically replies to them on your behalf. It uses a conversational AI model to generate human-like responses and can be configured to use your name and a specific persona. The assistant can also perform web searches to answer questions that require external information.

## Features

* **Automated WhatsApp Monitoring**: Continuously watches for new and unread messages in your WhatsApp account.
* **AI-Powered Replies**: Utilizes a powerful language model to generate contextually relevant and natural-sounding replies.
* **Customizable Persona**: You can set the assistant's name and provide examples of your chatting style to match your personality.
* **Web Search Capability**: Can search the web to find answers to questions and include that information in its replies.
* **Persistent Login**: Remembers your WhatsApp session, so you only need to scan the QR code once.
* **Extensible**: The project is built with a modular architecture, making it easy to add new features and capabilities.

## How It Works

The project uses the Playwright library to automate a web browser and interact with WhatsApp Web. It continuously monitors the chat list for any new messages. When a new message is detected, it is passed to a language model, which generates a suitable reply. The reply is then typed into the chatbox and sent.

The AI's behavior is guided by a system prompt that defines its persona, including your name, the assistant's name, and examples of your chat history. This helps the AI learn your communication style and reply in a way that is consistent with your own.

## Project Structure

The project is organized into the following files:

| File                  | Description                                                                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `main.py`               | The main entry point of the application. It initializes the WhatsApp connection, starts the message monitor, and handles new messages.   |
| `login_whatshapp.py`  | Manages the login process for WhatsApp Web, including session persistence.                                                              |
| `whatshapp_monitor.py` | Continuously monitors the WhatsApp chat list for new and unread messages.                                                              |
| `actions.py`            | Contains functions for interacting with the WhatsApp Web interface, such as clicking on chats and sending messages.                       |
| `chat_reply_ai.py`      | Manages the conversational AI, including the language model, tools, and the logic for generating replies.                                 |
| `config.py`             | Configures the language model with the necessary API keys and settings.                                                                  |
| `.env`                  | Stores the API key for the language model.                                                                                               |
| `scraper.py`            | A tool that allows the AI to perform web searches and scrape websites for information.                                                    |
| `yahooseachengine.py`   | A search engine module that uses Yahoo to find relevant web pages.                                                                       |

## Getting Started

### Prerequisites

* Python 3.7+
* A Google Gemini API key
* Langchain
* playwright
* bs4

### Installation

1.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set up your API key:**
    * Rename the `.env.example` file to `.env`.
    * Open the `.env` file and replace `your-gemini-api-key` with your actual Google Gemini API key.

### Usage

1.  **Run the application:**
    ```bash
    python main.py
    ```
2.  **Log in to WhatsApp:**
    * The first time you run the application, a browser window will open, and you will be prompted to scan a QR code to log in to WhatsApp Web.
    * Your session will be saved, so you won't need to log in again unless you manually log out.
3.  **Let the assistant run:**
    * Once you are logged in, the application will start monitoring your chats for new messages.
    * When a new message is detected, the AI will generate a reply and send it automatically.

## Customization

You can customize the AI's persona by editing the `prompt` variable in the `chat_reply_ai.py` file. This will allow you to change the assistant's name, your name, and the examples of your chat history that the AI uses to learn your style.

## Disclaimer

This project is for educational purposes only. The use of automated scripts to interact with WhatsApp may be against their terms of service. Use this project at your own risk.
