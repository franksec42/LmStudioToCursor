from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    completion = client.chat.completions.create(
        model="lmstudio-ai/gemma-2b-it-GGUF",
        messages=[
            {"role": "system", "content": "Always answer in rhymes."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
    )

    response = completion.choices[0].message.content
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)