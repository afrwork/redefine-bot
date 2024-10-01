function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") {
        return;
    }

    // Display user message
    displayMessage("user", userInput);

    // Send user message to server
    fetch("/send_message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json", // Changed to JSON for better structure
        },
        body: JSON.stringify({ user_input: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        displayMessage("bot", data.bot_response);

        // If training is needed, show the training prompt
        if (data.train) {
            promptForTraining(userInput);
        }

        // Clear user input
        document.getElementById("user-input").value = "";
    })
    .catch(error => {
        console.error("Error sending message:", error);
    });
}

// Attach event listeners for both button click and Enter key press
document.getElementById("send-button").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function displayMessage(sender, message) {
    var chatBox = document.getElementById("chat-box");
    var messageDiv = document.createElement("div");
    messageDiv.className = sender + "-message";

    // Set the speaker's name based on the sender
    var speakerName = (sender === "user") ? "You" : "Bot";
    
    // Add the speaker's name and the message content
    messageDiv.textContent = speakerName + ": " + message;

    // Append the message to the chat box
    chatBox.appendChild(messageDiv);

    // Scroll to the bottom to show the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}

function promptForTraining(userInput) {
    // Ask for the correct response
    var correctAnswer = prompt(`I'm sorry, I don't understand "${userInput}". Please provide the correct response:`);
    if (correctAnswer) {
        sendTrainingData(userInput, correctAnswer); // Send both the unknown input and the correct answer
    }
}

function sendTrainingData(userInput, correctAnswer) {
    // Send the training data to the server
    fetch("/submit_training", {
        method: "POST",
        headers: {
            "Content-Type": "application/json", // Changed to JSON for better structure
        },
        body: JSON.stringify({ user_input: userInput, user_response: correctAnswer }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the training result or any other response from the server
        displayMessage("bot", data.message || "Training data submitted successfully.");
    })
    .catch(error => {
        console.error("Error sending training data:", error);
    });
}
