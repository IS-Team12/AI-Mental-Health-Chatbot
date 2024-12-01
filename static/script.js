document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.querySelector('#dark-mode-toggle');

    // Initialize dark mode from localStorage
    if (localStorage.getItem('darkMode') === 'enabled') {
        enableDarkMode();
        darkModeToggle.checked = true;
    }

    // Toggle dark mode
    darkModeToggle?.addEventListener('change', () => {
        if (darkModeToggle.checked) {
            enableDarkMode();
        } else {
            disableDarkMode();
        }
    });

    function enableDarkMode() {
        document.body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'enabled');
    }

    function disableDarkMode() {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'disabled');
    }

    // Chatbot-specific functionality
    const chatContainer = document.querySelector('.chat-container');
    const messageInput = document.querySelector('#message-input');
    const sendButton = document.querySelector('#send-button');

    const greetings = [
        "Hello! What's on your mind today?",
        "Hi there! How are you feeling today?",
        "Hey! What can I help you with today?",
        "Hello! How's everything going?",
        "Hi! What's been happening lately?",
        "Hey there! What’s on your mind?",
        "Hello! How has your day been so far?",
        "Hi! Let’s talk. How can I assist you?",
        "Hey! Is there anything you'd like to share?",
        "Hello! Let’s dive into your thoughts!"
    ];

    // Display initial greeting
    if (chatContainer) {
        const greetingMessage = document.createElement('div');
        greetingMessage.classList.add('bot-message');
        greetingMessage.textContent = greetings[Math.floor(Math.random() * greetings.length)];
        chatContainer.appendChild(greetingMessage);
    }

    // Handle Send Button Click
    sendButton?.addEventListener('click', () => {
        const userMessage = messageInput.value.trim();

        if (userMessage) {
            displayUserMessage(userMessage);
            processUserMessage(userMessage);
            messageInput.value = '';
        }
    });

    // Display User Message
    function displayUserMessage(message) {
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('user-message');
        userMessageElement.textContent = message;
        chatContainer.appendChild(userMessageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the latest message
    }

    // Process User Message and Simulate Bot Response
    function processUserMessage(message) {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        })
            .then(response => response.json())
            .then(data => {
                displayBotMessage(data.reply);
            })
            .catch(error => {
                console.error('Error:', error);
                displayBotMessage("Oops! Something went wrong. Please try again.");
            });
    }

// Display Bot Message
    function displayBotMessage(message) {
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('bot-message');
        botMessageElement.innerHTML = message; // Render HTML in the message
        chatContainer.appendChild(botMessageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the latest message
}

});
