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

    const investmentInput = document.getElementById("investment-input");
    const investmentBtn = document.getElementById("investment-btn");
    const investmentGraph = document.getElementById("investmentGraph");
    let selectedRisk = null;

    // ✅ Handle Risk Level Selection + Highlighting
    const riskButtons = document.querySelectorAll(".risk-btn");
    riskButtons.forEach(button => {
        button.addEventListener("click", function () {
            selectedRisk = this.getAttribute("data-risk");

            // Remove highlight from all, then highlight the selected one
            riskButtons.forEach(btn => btn.classList.remove("selected"));
            this.classList.add("selected");

            console.log("✅ Selected Risk Level:", selectedRisk);
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
                // ✅ Fix: Make sure the image URL is correctly used
                investmentGraph.innerHTML = `
                    <img src="${data.graph_url}?timestamp=${new Date().getTime()}" 
                         alt="Investment Growth Graph"
                         width="100%" 
                         style="max-width: 800px; display: block; margin: auto; border-radius: 10px; margin-top: 20px;">
                `;
            } else {
                alert("Error generating investment graph.");
            }
        })
        .catch(error => console.error("❌ API Request Failed:", error));
    });

});
