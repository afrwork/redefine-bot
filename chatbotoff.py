import json
import logging
from flask import Flask, render_template, request, jsonify
from urllib.parse import quote as url_quote
import random

app = Flask(__name__, static_folder='static')

EXIT_COMMAND = 'exit'
TRAINING_FILE = "training_data.json"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_json(file_path):
    try:
        with open(file_path) as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading {file_path}: {e}")
        return []

def save_json(file_path, data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        logging.error(f"Error writing to {file_path}: {e}")

def train_chatbot(training_data_file):
    new_training_data = load_json(training_data_file)
    existing_training_data = load_json(TRAINING_FILE)

    # Combine and remove duplicates
    combined_training_data = {frozenset(item.items()): item for item in existing_training_data + new_training_data}
    combined_training_data = list(combined_training_data.values())
    
    save_json(TRAINING_FILE, combined_training_data)
    logging.info("Chatbot training complete.")

def load_training_data():
    return load_json(TRAINING_FILE)

def simple_chatbot(user_input, training_data):
    responses = [data["response"] for data in training_data if data["input"].lower() in user_input.lower()]

    if responses:
        return {"bot_response": random.choice(responses), "train": False}

    return {
        "bot_response": "I'm sorry, I don't understand that. Would you like to train me with the correct response?",
        "train": True
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json.get('user_input')
    training_data = load_training_data()
    response = simple_chatbot(user_input, training_data)
    
    return jsonify(response)

@app.route('/submit_training', methods=['POST'])
def submit_training():
    data = request.json
    user_input = data.get('user_input')
    user_response = data.get('user_response')

    if user_input and user_response:
        new_data = {
            "input": user_input,
            "response": user_response
        }
        
        # Load existing training data
        training_data = load_training_data()
        
        # Add the new data
        training_data.append(new_data)
        
        # Save the updated training data
        save_json(TRAINING_FILE, training_data)
        
        return jsonify({"status": "success", "message": "Training data submitted successfully."})
    
    return jsonify({"status": "error", "message": "Invalid input."})

@app.route('/some_route')
def some_route():
    quoted_url = url_quote("https://example.com")
    return quoted_url

if __name__ == "__main__":
    logging.info("Welcome to the simple chatbot!")
    training_data_file = "training_data.json"
    train_chatbot(training_data_file)
    app.run(host='0.0.0.0', port=5000)
