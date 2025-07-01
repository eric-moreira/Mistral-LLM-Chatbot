from flask import Flask, request, jsonify, render_template
from litellm import completion
import logging

app = Flask(__name__, static_folder="static", template_folder="templates")
logging.basicConfig(level=logging.INFO)

OLLAMA_MODEL = 'ollama/mistral'
OLLAMA_API_BASE = 'http://localhost:11434'

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
