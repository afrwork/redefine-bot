import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static')

EXIT_COMMAND = 'exit'
TRAINING_FILE = "training_data.json"

def load_json(file_path):
    try:
        with open(file_path) as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return []

def save_json(file_path, data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")

def train_chatbot(training_data_file):
    new_training_data = load_json(training_data_file)
    existing_training_data = load_json(TRAINING_FILE)

    # Combine and remove duplicates
    combined_training_data = {frozenset(item.items()): item for item in existing_training_data + new_training_data}
    combined_training_data = list(combined_training_data.values())
    
    save_json(TRAINING_FILE, combined_training_data)

    print("Chatbot training complete.")

def load_training_data():
    return load_json(TRAINING_FILE)

def simple_chatbot(user_input, training_data):
    for data in training_data:
        if data["input"].lower() in user_input.lower():
            return {"bot_response": data["response"], "train": False}
    return {"bot_response": "I'm sorry, I don't understand that.", "train": True}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form.get('user_input')
    training_data = load_training_data()
    response = simple_chatbot(user_input, training_data)
    
    if response["train"]:
        response["bot_response"] += " Would you like to train me with the correct response?"

    return jsonify(response)

@app.route('/submit_training', methods=['POST'])
def submit_training():
    user_input = request.form.get('user_input')
    user_response = request.form.get('user_response')

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

if __name__ == "__main__":
    print("Welcome to the simple chatbot!")
    training_data_file = "training_data.json"  # Update with your JSON file
    train_chatbot(training_data_file)
    app.run(host='0.0.0.0', port=5000)
