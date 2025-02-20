document.addEventListener("DOMContentLoaded", function () {
    // =============================
    // ✅ Chatbot Elements
    // =============================
    const chatbotBtn = document.getElementById("chatbot-btn");
    const chatContainer = document.getElementById("chat-container");
    const closeChatBtn = document.getElementById("close-chat");
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const chatMessages = document.getElementById("chat-messages");

    // ✅ Toggle Chat Visibility
    chatbotBtn.addEventListener("click", function () {
        chatContainer.classList.toggle("open");

        if (chatContainer.classList.contains("open")) {
            chatbotBtn.style.display = "none"; // Hide chatbot button
        }
    });

    // ✅ Close Chat with Arrow Button
    closeChatBtn.addEventListener("click", function () {
        chatContainer.classList.remove("open");
        setTimeout(() => {
            chatbotBtn.style.display = "block"; // Show chatbot button again
        }, 300);
    });

    // ✅ Function to Send a Chat Message
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

    // ✅ Send Message on Button Click
    sendBtn.addEventListener("click", sendMessage);

    // ✅ Send Message on Enter Key
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    // =============================
    // ✅ Investment Growth Feature
    // =============================

    // Investment Elements
    const investmentInput = document.getElementById("investment-input");
    const investmentBtn = document.getElementById("investment-btn");
    const investmentGraph = document.getElementById("investmentGraph");
    let selectedRisk = null;

    // ✅ Handle Risk Level Selection
    const riskButtons = document.querySelectorAll('input[name="risk-level"]');
    riskButtons.forEach(button => {
        button.addEventListener("change", function () {
            selectedRisk = this.value;
        });
    });

    // ✅ Generate Investment Growth Graph
    investmentBtn.addEventListener("click", function () {
        const principal = investmentInput.value.trim();

        if (!principal || !selectedRisk) {
            alert("Please enter an investment amount and select a risk level.");
            return;
        }

        console.log("✅ Sending Request → Principal:", principal, "Risk:", selectedRisk);

        fetch("/api/plot/investment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ principal: principal, aggro: selectedRisk })
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ API Response:", data);

            if (data.graph_url) {
                investmentGraph.innerHTML = `<iframe src="${data.graph_url}" width="100%" height="600px"></iframe>`;
            } else {
                alert("Error generating investment graph.");
            }
        })
        .catch(error => console.error("❌ API Request Failed:", error));
    });
});
