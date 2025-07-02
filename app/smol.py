from flask import Flask, request, jsonify, render_template
from litellm import completion
import logging

app = Flask(__name__, static_folder="static", template_folder="templates")
logging.basicConfig(level=logging.INFO)

OLLAMA_MODEL = 'ollama/mistral'
OLLAMA_API_BASE = 'http://host.docker.internal:11434'

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
        "You are called Stral. Never refer to yourself as an AI. Always sign your insights, where appropriate, with your name: Stral."
    )
}


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        messages = data.get('messages')
        if not messages:
            return jsonify({"error": "Missing 'messages' field."}), 400

        messages.insert(0, SYSTEM_PROMPT)

        response = completion(
            model=OLLAMA_MODEL,
            api_base=OLLAMA_API_BASE,
            messages=messages,
            stream=False
        )

        content = response.choices[0].message.content
        return jsonify({"response": content})

    except Exception as e:
        logging.exception("Error processing request")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
