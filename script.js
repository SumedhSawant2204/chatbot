// Get elements from the HTML
const chatLog = document.getElementById("chat-log");
const chatInputBox = document.getElementById("chat-input-box");
const sendBtn = document.getElementById("send-btn");
const resetBtn = document.getElementById("reset-btn");
const logoutBtn = document.getElementById("logout-btn");

// Function to append messages to the chat log
function appendMessage(message, isUser = true) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add(isUser ? "user-message" : "bot-message");
  messageDiv.textContent = message;
  chatLog.appendChild(messageDiv);
}

// Handle sending a message
document.getElementById("send-btn").addEventListener("click", async () => {
    const userMessage = document.getElementById("chat-input-box").value;
    const chatLog = document.getElementById("chat-log");
  
    if (userMessage.trim() === "") return;
  
    // Display user message
    chatLog.innerHTML += `<div class="user-message">${userMessage}</div>`;
  
    // Send message to the backend
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });
  
    const data = await response.json();
  
    // Display bot's response
    const botResponse = data.response;
    chatLog.innerHTML += `<div class="bot-message">${botResponse.replace(/\n/g, "<br>")}</div>`;
    document.getElementById("chat-input-box").value = "";
  
    // Scroll to the bottom to show new messages
    chatLog.scrollTop = chatLog.scrollHeight;
  });
  

// Handle chat reset
resetBtn.addEventListener("click", () => {
  chatLog.innerHTML = "";  // Clear chat log
});

// Handle logout
logoutBtn.addEventListener("click", () => {
  window.location.href = "/login";  // Navigate to the login page (you can adjust as needed)
});
