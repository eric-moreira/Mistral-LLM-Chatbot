# Mistral LLM Chatbot

This project is a simple chatbot using the Mistral model running locally via Ollama.  
The web interface is built with Flask and Bootstrap, with Markdown support in responses.

---

## Requirements

- Python 3.10 or higher  
- Ollama installed locally

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

```bash
python smol.py
```

Open your browser and go to `http://localhost:5000`.

---

## Project structure

```
├── smol.py              # Main Flask application
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Web interface
├── static/
│   └── style.css        # Custom styles
└── README.md
```

---

## Features

- Chat with message history  
- Responses rendered in Markdown, including code blocks  
- Simple and responsive web interface  

---

## Possible improvements

- Support for multiple Ollama models  
- Streaming responses  
- Persistence of chat history  
- User session management  

---

## Author

Eric Moreira  
Computer engineer and low-level systems developer
