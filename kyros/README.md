# KYROS: Android AI Assistant (Termux)

KYROS is a powerful command-line AI assistant designed to run on Android via the **Termux** app. It combines local automation (Intents, system controls) with the intelligence of **Google Gemini**.

## 🧠 AI Brain & Voice (v1.7)

KYROS now leverages the latest **Gemini 3.1** models:
- **gemini-3.1-pro-preview**: Deep Reasoning & Coding.
- **gemini-3.1-flash-lite-preview**: Fast Logic & Sub-tasks.
- **gemini-3.1-flash-live-preview**: Interactive Brain.
- **gemini-3.1-flash-tts-preview**: Dedicated voice response model.

### 🎙️ Voice Interaction
- **TTS (Talking)**: KYROS automatically speaks through your phone using standard Android TTS via `termux-api`.
- **STT (Listening)**: Type `voice` or `listen` (or tap the Mic button in Web UI) to activate the listener. Note: High-fidelity transcription can be done via Whisper tiny if installed manually.

## 🚀 Installation

1.  **Termux Setup**: Install Termux and Termux:API from F-Droid.
2.  **Packages**: Run the following in Termux:
    ```bash
    pkg update && pkg upgrade
    pkg install python termux-api ffmpeg
    pip install requests flask
    ```
3.  **Run KYROS**: 
    - Terminal mode: `python kyros.py`
    - Web Dashboard: `python server.py` (Localhost:5000)

## 📁 Data Configuration
- `config.json`: Stores your Gemini API Key.
- `contacts.json`: Map names to phone numbers.
- `shortcuts.json`: Custom multi-step macros.

## 🧠 Smart Intent Parsing
- `open youtube`
- `search python tutorials on google`
- `send whatsapp to Rahul saying I am on my way`
- `battery status`
- `flashlight on`
- `create file log.txt`
- `party mode` (Runs pre-configured shortcut)
- `voice` (Activates listening mode)
