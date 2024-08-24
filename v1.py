from flask import Flask, request, jsonify, Response
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def chat_endpoint():
    data = request.json
    user_message = data.get('message', 'hi')

    def generate():
        completion = client.chat.completions.create(
            model="lmstudio-ai/gemma-2b-it-GGUF",
            messages=[
                {"role": "system", "content": "Always answer in rhymes."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            stream=True
        )

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                yield f"data: {json.dumps({'response': chunk.choices[0].delta.content})}\n\n"

    return Response(generate(), content_type='text/event-stream')

# Función para inicializar y configurar la ruta
def setup_chat_route(app):
    app.route('/chat/completions', methods=['POST'])(chat_endpoint)

# Función para iniciar el servidor
def run_server():
    app = Flask(__name__)
    setup_chat_route(app)
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_server()