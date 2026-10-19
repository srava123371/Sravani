
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# Change this if you download a different Ollama model
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My Alexa AI Assistant</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #10152d, #252052, #10152d);
    color: white;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px;
}

.container {
    width: 100%;
    max-width: 750px;
    height: 90vh;
    min-height: 500px;
    background: rgba(15, 20, 45, 0.96);
    border: 1px solid #454b79;
    border-radius: 22px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 15px 50px #0006;
}

header {
    text-align: center;
    padding: 20px 10px;
    border-bottom: 1px solid #343957;
}

.orb {
    width: 65px;
    height: 65px;
    border-radius: 50%;
    margin: auto;
    background: linear-gradient(135deg, #00e5ff, #7662ff);
    box-shadow: 0 0 25px #655cff99;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 30px;
}

h1 { margin: 10px 0 5px; font-size: 25px; }
.subtitle { color: #b9c2e8; font-size: 13px; }

#chat {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}

.message {
    max-width: 85%;
    padding: 13px 16px;
    margin: 12px 0;
    border-radius: 16px;
    line-height: 1.6;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.user {
    background: #635bdf;
    margin-left: auto;
    border-bottom-right-radius: 4px;
}

.bot {
    background: #252d4d;
    border: 1px solid #3d456b;
    margin-right: auto;
    border-bottom-left-radius: 4px;
}

.label {
    font-size: 11px;
    color: #9cecff;
    margin-bottom: 5px;
    font-weight: bold;
}

#status {
    color: #aab4db;
    font-size: 12px;
    padding: 0 18px 8px;
    min-height: 22px;
}

.controls {
    padding: 15px;
    border-top: 1px solid #343957;
}

.input-row {
    display: flex;
    gap: 8px;
}

input {
    flex: 1;
    min-width: 0;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #454b79;
    background: #171d3b;
    color: white;
    outline: none;
    font-size: 15px;
}

button {
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 16px;
    padding: 12px 15px;
    color: white;
    background: #635bdf;
}

button:hover { opacity: 0.85; }
button:disabled { opacity: 0.5; cursor: wait; }

.mic { background: #087fbd; }
.stop { background: #a33a54; }
.speak { background: #315c48; }

.bottom-row {
    display: flex;
    gap: 8px;
    margin-top: 10px;
}

.bottom-row button {
    flex: 1;
    font-size: 13px;
}

footer {
    text-align: center;
    color: #8993bd;
    font-size: 11px;
    padding: 10px;
}

@media(max-width: 500px) {
    .container { height: 94vh; }
    #chat { padding: 12px; }
    .message { max-width: 94%; }
    button { padding: 12px; }
}
</style>
</head>

<body>
<div class="container">

<header>
    <div class="orb">🎙️</div>
    <h1>My Alexa Assistant</h1>
    <div class="subtitle">Ask anything • Type or speak • Listen to answers</div>
</header>

<div id="chat" aria-live="polite">
    <div class="message bot">
        <div class="label">ALEXA</div>
        Hello! 👋 I am your AI assistant.
        Type a question or press the microphone to speak.
    </div>
</div>

<div id="status">Ready to help you!</div>

<div class="controls">
    <div class="input-row">
        <input id="question" type="text"
               placeholder="Type your question here..."
               autocomplete="off">
        <button id="sendBtn" onclick="sendMessage()">➤</button>
    </div>

    <div class="bottom-row">
        <button class="mic" onclick="startListening()">🎤 Speak</button>
        <button class="speak" onclick="toggleVoice()" id="voiceBtn">
            🔊 Voice: ON
        </button>
        <button class="stop" onclick="stopSpeaking()">⏹ Stop</button>
    </div>
</div>

<footer>Python Flask • Ollama AI • HTML • CSS • JavaScript</footer>
</div>

<script>
const chat = document.getElementById("chat");
const input = document.getElementById("question");
const statusText = document.getElementById("status");
const sendBtn = document.getElementById("sendBtn");

let voiceEnabled = true;
let recognition = null;
let busy = false;

function addMessage(text, type) {
    const message = document.createElement("div");
    message.className = "message " + type;

    const label = document.createElement("div");
    label.className = "label";
    label.textContent = type === "user" ? "YOU" : "ALEXA";

    const content = document.createElement("div");
    content.textContent = text;

    message.appendChild(label);
    message.appendChild(content);
    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
}

function speak(text) {
    if (!voiceEnabled || !("speechSynthesis" in window)) return;

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-IN";
    speech.rate = 1;
    speech.pitch = 1;

    window.speechSynthesis.speak(speech);
}

function stopSpeaking() {
    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
    }
    statusText.textContent = "Speech stopped.";
}

function toggleVoice() {
    voiceEnabled = !voiceEnabled;

    document.getElementById("voiceBtn").textContent =
        voiceEnabled ? "🔊 Voice: ON" : "🔇 Voice: OFF";

    if (!voiceEnabled) stopSpeaking();
    else statusText.textContent = "Voice replies enabled.";
}

async function sendMessage() {
    const question = input.value.trim();

    if (!question || busy) return;

    addMessage(question, "user");
    input.value = "";
    busy = true;
    sendBtn.disabled = true;
    statusText.textContent = "Alexa is thinking...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({question: question})
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.answer || "Could not get an answer.");
        }

        addMessage(data.answer, "bot");
        speak(data.answer);
        statusText.textContent = "Answer ready.";

    } catch (error) {
        addMessage("Error: " + error.message, "bot");
        statusText.textContent = "Check that Ollama is running.";
    } finally {
        busy = false;
        sendBtn.disabled = false;
        input.focus();
    }
}

input.addEventListener("keydown", function(event) {
    if (event.key === "Enter") sendMessage();
});

function startListening() {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        statusText.textContent =
            "Speech recognition is not supported in this browser. Try Chrome.";
        return;
    }

    if (recognition) recognition.abort();

    recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = function() {
        statusText.textContent = "Listening... Speak now!";
    };

    recognition.onresult = function(event) {
        input.value = event.results[0][0].transcript;
        statusText.textContent = "You said: " + input.value;
        sendMessage();
    };

    recognition.onerror = function(event) {
        statusText.textContent = "Microphone error: " + event.error;
    };

    recognition.onend = function() {
        if (statusText.textContent === "Listening... Speak now!") {
            statusText.textContent = "Ready to help you!";
        }
    };

    recognition.start();
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question."}), 400

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": question,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        answer = response.json().get("response", "").strip()

        if not answer:
            answer = "Sorry, I could not generate an answer."

        return jsonify({"answer": answer})

    except requests.exceptions.ConnectionError:
        return jsonify({
            "answer": "Ollama is not running. Start Ollama and try again."
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "answer": "The AI took too long to respond. Please try again."
        }), 504

    except Exception as error:
        app.logger.exception("AI request failed")
        return jsonify({
            "answer": "AI error: " + str(error)
        }), 500

if __name__ == "__main__":
    print("Starting My Alexa Assistant...")
    print("Open http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)

