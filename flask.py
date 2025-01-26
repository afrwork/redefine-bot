import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.json.get('user_input')
    response = {
        "bot_response": f"Received: {user_input}",
        "train": False
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
