"""
Alexa-style voice assistant powered by Claude.

HOW IT WORKS
  1. Listens to your microphone
  2. Waits for the wake word ("alexa" by default)
  3. Sends your question to Claude
  4. Speaks the answer out loud

SETUP
  pip install anthropic SpeechRecognition pyttsx3 pyaudio

  Windows: if pyaudio fails ->  pip install pipwin && pipwin install pyaudio
  Mac:     brew install portaudio && pip install pyaudio
  Linux:   sudo apt install portaudio19-dev espeak && pip install pyaudio

  Get an API key at https://console.anthropic.com and set it:
    Windows (cmd):   set ANTHROPIC_API_KEY=your_key_here
    Mac/Linux:       export ANTHROPIC_API_KEY=your_key_here

RUN
  python voice_assistant.py

  Say:  "Alexa, what is the capital of India?"
  Say:  "Alexa, stop"  (to quit)
"""

import os
import anthropic
import pyttsx3
import speech_recognition as sr

WAKE_WORD = "alexa"
MODEL = "claude-sonnet-5-5"
LANGUAGE = "en-IN"  # speech recognition language (en-IN, en-US, hi-IN, kn-IN ...)

SYSTEM_PROMPT = (
    "You are a friendly voice assistant like Alexa. "
    "Your answers are spoken aloud, so keep them short (1-3 sentences), "
    "in plain conversational language, with no markdown, lists or emojis."
)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 175)  # speaking speed

history = []  # remembers the conversation


def speak(text: str) -> None:
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    """Record from the mic and return the recognized text ('' if nothing)."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            return ""
    try:
        text = recognizer.recognize_google(audio, language=LANGUAGE)
        print(f"You: {text}")
        return text.lower()
    except (sr.UnknownValueError, sr.RequestError):
        return ""


def ask_claude(question: str) -> str:
    history.append({"role": "user", "content": question})
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=history[-20:],  # keep last 20 messages as memory
    )
    answer = response.content[0].text
    history.append({"role": "assistant", "content": answer})
    return answer


def main() -> None:
    speak(f"Hello! Say {WAKE_WORD} and then ask me anything.")
    while True:
        heard = listen()
        if WAKE_WORD not in heard:
            continue

        # Everything after the wake word is the question
        question = heard.split(WAKE_WORD, 1)[1].strip(" ,.")

        # If they only said the wake word, ask for the question
        if not question:
            speak("Yes, I'm listening.")
            question = listen()
            if not question:
                speak("Sorry, I didn't catch that.")
                continue

        if question in ("stop", "exit", "quit", "goodbye", "bye"):
            speak("Goodbye!")
            break

        try:
            speak(ask_claude(question))
        except Exception as e:
            print("Error:", e)
            speak("Sorry, I had a problem getting the answer.")


if __name__ == "__main__":
    main()
