document.getElementById("send-btn").addEventListener("click", sendMessage);

// Add event listener for the Enter key on the input field
document.getElementById("user-input").addEventListener("keypress", function(event) {
    // Check if the Enter key is pressed
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent the default action to stop form submission
        sendMessage();
    }
});

function sendMessage() {
    let userInput = document.getElementById("user-input");
    let userText = userInput.value.trim();
    if (userText) {
        displayMessage(userText, 'user');
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userText }),
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(data.message, 'bot');
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        userInput.value = ''; // Clear the input field after sending
    }
}

function displayMessage(message, sender) {
    let chatBox = document.getElementById("chat-box");
    let messageDiv = document.createElement("div");

    // Simple markdown to HTML converter for bold and italics
    let formattedMessage = message
        .replace(/(\*\*)(.*?)\1/g, '<b>$2</b>') // Bold **text**
        .replace(/(\*)(.*?)\1/g, '<i>$2</i>'); // Italics *text*

    messageDiv.innerHTML = formattedMessage; // Use innerHTML to render formatted text
    messageDiv.classList.add(sender);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}



