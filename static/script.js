document.addEventListener("DOMContentLoaded", function () {
    const chatbotBtn = document.getElementById("chatbot-btn");
    const chatContainer = document.getElementById("chat-container");
    const closeChatBtn = document.getElementById("close-chat");
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const chatMessages = document.getElementById("chat-messages");

    // Toggle Chat Visibility
    chatbotBtn.addEventListener("click", function () {
        chatContainer.classList.toggle("open");

        if (chatContainer.classList.contains("open")) {
            chatbotBtn.style.display = "none"; // Hide chatbot button
        }
    });

    // Close Chat with Arrow Button
    closeChatBtn.addEventListener("click", function () {
        chatContainer.classList.remove("open");
        setTimeout(() => {
            chatbotBtn.style.display = "block"; // Show chatbot button again
        }, 300);
    });

    // Function to Send a Message
    function sendMessage() {
        const userMessage = chatInput.value.trim();
        if (userMessage === "") return;

        // Display user message
        const userBubble = document.createElement("div");
        userBubble.classList.add("message", "user-message");
        userBubble.textContent = userMessage;
        chatMessages.appendChild(userBubble);

        chatInput.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll

        // Send message to API
        fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage }),
        })
            .then(response => response.json())
            .then(data => {
                const aiMessage = document.createElement("div");
                aiMessage.classList.add("message", "ai-message");
                aiMessage.textContent = data.response;
                chatMessages.appendChild(aiMessage);
                chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }

    // Send Message on Button Click
    sendBtn.addEventListener("click", sendMessage);

    // Send Message on Enter Key
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});
