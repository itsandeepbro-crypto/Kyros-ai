# KYROS: Android AI Assistant (Termux)

KYROS is a powerful command-line AI assistant designed to run on Android via the **Termux** app. It combines local automation (Intents, system controls) with the intelligence of **Google Gemini**.

## 🛠 Prerequisites

1.  **Termux**: Install it from F-Droid (preferred) or the Github releases.
2.  **Termux:API**: Install the Termux:API app from F-Droid.
3.  **Packages**: Run the following in Termux:
    ```bash
    pkg update && pkg upgrade
    pkg install python termux-api
    pip install requests flask
    ```

## 🚀 Installation

1.  Clone or download the KYROS files into a folder in Termux:
2.  Navigate to the folder: `cd KYROS`
3.  Grant storage permission if you want to use the File Manager:
    ```bash
    termux-setup-storage
    ```
4.  Run KYROS:
    ```bash
    python kyros.py
    ```

## 🧠 Features

-   **YouTube**: `open youtube`, `search python on youtube`, `play https://... on youtube`
-   **WhatsApp**: `send whatsapp to Rahul saying hello` (Requires `contacts.json` setup)
-   **System**: `battery status`, `flashlight on`, `flashlight off`, `clipboard get`, `clipboard set "new text"`
-   **Files**: `create file notes.txt`, `list files`, `read file notes.txt`, `delete file notes.txt`
-   **Browser**: `search machine learning on google`, `open google.com`
-   **AI Fallback**: Ask anything like `what is quantum computing?` (Uses Gemini API)

## 📁 Data Configuration

-   `config.json`: Stores your Gemini API Key.
-   `contacts.json`: Map names to phone numbers (e.g., `{"Rahul": "+919876543210"}`).
-   `shortcuts.json`: Create macros like `"good morning"`.
-   `history.json`: Automatically stores last 100 commands.

## ⚠️ Safety First
KYROS will always ask for confirmation before:
-   Sending WhatsApp messages
-   Deleting files
-   Executing multi-step shortcuts
