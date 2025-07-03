# Mistral LLM Chatbot

This project is a simple chatbot using the Mistral model running locally via Ollama.  
The web interface is built with Flask and Bootstrap, with Markdown support in responses.

![image](https://github.com/user-attachments/assets/02ec62d7-2d23-4374-ae75-f5b0251319d7)


---

## Requirements

- Docker (for running all required services and images)
- Ollama installed locally (for local LLM inference)

---

## Installation and usage

### 1. Install Ollama

If you don’t have it installed yet, run:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull and run the Mistral model

```bash
ollama pull mistral
ollama run mistral
```

Ollama will start a local server at `http://localhost:11434`.

### 3. Clone this repository and install dependencies

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Run the chatbot server

#### Before running the chatbot server, create the secrets:
```bash
mkdir .secrets
echo "DB ROOT PASSWORD" >> .secrets/mongo_pass
echo "APP-User RW PASSWORD" >> .secrets/mongo_app_pass
```

Run the chatbot server
```bash
docker compose up -d 
```

Open your browser and go to `http://localhost:5001`.

---

## Project structure

```
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Docker Compose setup (MongoDB, secrets, network)
├── Dockerfile               # Docker build for the app
├── app/
│   ├── static/
│   │   ├── style.css        # Custom styles
│   │   └── app.js           # Frontend logic
│   ├── templates/
│   │   └── index.html       # Web interface
│   ├── mongo_setup/
│   │   ├── setup.py         # MongoDB connection and helpers
│   │   └── __init__.py
│   └── smol.py              # Main Application
├── mongo-init-scripts/
│   └── init-mongo.sh        # MongoDB initialization script
└── README.md
```

---

## Features

- Chat with message history and persistent conversations (MongoDB)
- Responsive web interface (Bootstrap 5, Offcanvas sidebar)
- Sidebar with conversation list and new conversation button always at the top
- Automatic chat title generation using LLM
- Markdown rendering in responses, including code blocks
- User and assistant message bubbles
- Button to start a new conversation at any time
- Send button is disabled while waiting for a response
- Only the sidebar and chat history have scrollbars (no global scroll)
- All UI in English
- Docker Compose support with secrets for MongoDB

---

## Possible improvements

- Support for multiple Ollama models
- Streaming responses
- User authentication and session management
- More advanced chat search/filter
- Improved error handling and notifications

---

## Author

Eric Moreira  
Computer engineer and low-level systems developer
