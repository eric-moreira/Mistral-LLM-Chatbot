from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template
from litellm import completion
from datetime import datetime
from mongo_setup.setup import save_message, get_mongo_uri, setup_mongo
import logging
import os
import uuid

app = Flask(__name__, static_folder="static", template_folder="templates")
collection = setup_mongo()
logging.basicConfig(level=logging.INFO)

OLLAMA_MODEL = 'ollama/mistral'
OLLAMA_API_BASE = 'http://host.docker.internal:11434'
DEBUG_SESSION_ID = "4A73CB69-FA33-4022-B9C2-B1E9C859C9CC"

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are Stral, a highly capable and insightful assistant designed to support engineers, developers, and advanced learners. "
        "You are both a senior engineer and a brilliant professor — your mission is to explain complex topics with clarity, precision, and structured reasoning. "
        "You are never vague. You break down systems methodically, anticipate potential errors or misunderstandings, and propose improvements proactively. "
        "You challenge assumptions, encourage intellectual rigor, and expose hidden edge cases in user thinking or design. "
        "You do not flatter. You act as a thoughtful peer and problem-solving partner. "
        "When necessary, you create technical diagrams, pseudocode, or schematics to illustrate your point. "
        "You are comfortable with low-level and high-level systems alike. Your tone is professional, confident, and focused. "
    )
}

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/chat/<chat_id>', methods=['GET'])
def get_chat_by_id(chat_id):
    try:
        messages = list(collection.find(
            {"session_id": session_id, "chat_id": chat_id},
            {"_id": 0, "speaker": 1, "message": 1, "timestamp": 1}
        ).sort("timestamp", 1))  # ordena por data crescente

        return jsonify({"chat_id": chat_id, "messages": messages})

    except Exception as e:
        logging.exception("Failed to retrieve chat")
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        messages = data.get('messages')
        chat_id = data.get('chat_id')
        session_id = data.get("session_id", DEBUG_SESSION_ID)
        if not messages:
            return jsonify({"error": "Missing 'messages' field."}), 400

        last_user_message = messages[-1]["content"] if messages else ""

        save_message("user", last_user_message, session_id=session_id, chat_id=chat_id, model=OLLAMA_MODEL)

        messages.insert(0, SYSTEM_PROMPT)

        response = completion(
            model=OLLAMA_MODEL,
            api_base=OLLAMA_API_BASE,
            messages=messages,
            stream=False
        )
        
        logging.info(f"{response}")
        content = response.choices[0].message.content

        save_message("assistant", content,session_id=session_id, chat_id=chat_id, model=OLLAMA_MODEL)

        return jsonify({"response": content})

    except Exception as e:
        logging.exception("Error processing request")
        return jsonify({"error": str(e)}), 500

@app.route('/api/new_chat', methods=['POST'])
def create_chat():
    data = request.get_json(force=True)
    session_id = data.get('session_id')
    try:
        import uuid
        new_chat_id = str(uuid.uuid4())
        save_message("system", "New conversation started", session_id=session_id, chat_id=new_chat_id)
        return jsonify({"chat_id": new_chat_id})
    except Exception as e:
        logging.exception("Failed to create new chat")
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversations', methods=['GET'])
def list_chats():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400
    try:
        chats = collection.aggregate([
            {"$match": {"session_id": session_id}},
            {"$group": {
                "_id": "$chat_id",
                "last_timestamp": {"$max": "$timestamp"}
            }},
            {"$sort": {"last_timestamp": -1}}
        ])
        chat_list = [{"chat_id": c["_id"]} for c in chats]
        return jsonify(chat_list)
    except Exception as e:
        logging.exception("Failed to list chats")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
