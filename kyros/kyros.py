import os
import sys
import json
import subprocess
import time
from datetime import datetime

# Core Modules (Simulated as local imports for the single-folder download)
# Logic is embedded here or imported from core/ if structure allows.

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'

class Kyros:
    def __init__(self):
        self.config_path = "config.json"
        self.contacts_path = "contacts.json"
        self.history_path = "history.json"
        self.shortcuts_path = "shortcuts.json"
        self.load_data()
        
    def load_data(self):
        # Initialize default files if they don't exist
        for path, default in [
            (self.config_path, {"api_key": ""}),
            (self.contacts_path, {}),
            (self.history_path, []),
            (self.shortcuts_path, {"good morning": ["flashlight on", "battery status"]})
        ]:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump(default, f, indent=4)
        
        with open(self.config_path, 'r') as f: self.config = json.load(f)
        with open(self.contacts_path, 'r') as f: self.contacts = json.load(f)
        with open(self.history_path, 'r') as f: self.history = json.load(f)
        with open(self.shortcuts_path, 'r') as f: self.shortcuts = json.load(f)

    def save_history(self, command):
        self.history.insert(0, {"timestamp": str(datetime.now()), "command": command})
        self.history = self.history[:100]
        with open(self.history_path, 'w') as f:
            json.dump(self.history, f, indent=4)

    def log(self, tag, message, color=Colors.GREEN):
        print(f"{color}[{tag}]{Colors.ENDC} {message}")

    def banner(self):
        print(f"""{Colors.CYAN}{Colors.BOLD}
   __  ____     _______  ____  ____ 
  |  |/ /\ \   / / ___ \/  _ \/ ___|
  |  ' /  \ \_/ / |  _  | / \ \___ \\
  |  . \   \   /| |_| | \_/ /  ___| |
  |_|\\_\\   |_|  \_____/\____/|____/ v1.0
        Android AI Automation System
        {Colors.ENDC}""")

    def execute_shell(self, command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output.decode('utf-8').strip()}"

    def ask_confirm(self, message):
        res = input(f"{Colors.WARNING}[CONFIRM]{Colors.ENDC} {message} (y/n): ").lower()
        return res == 'y'

    def parse_intent(self, text):
        text = text.lower().strip()
        
        # Shortcuts
        if text in self.shortcuts:
            return {"type": "shortcut", "commands": self.shortcuts[text]}

        # YouTube
        if "youtube" in text:
            if "search" in text:
                query = text.split("search")[1].split("on youtube")[0].strip()
                return {"type": "youtube_search", "query": query}
            if "play" in text and "http" in text:
                url = text.split("play")[1].split("on youtube")[0].strip()
                return {"type": "youtube_play", "url": url}
            return {"type": "app_open", "package": "com.google.android.youtube"}

        # WhatsApp
        if "whatsapp" in text and "send" in text:
            parts = text.split("to")
            if len(parts) > 1:
                sub_parts = parts[1].split("saying")
                contact_name = sub_parts[0].strip()
                message = sub_parts[1].strip() if len(sub_parts) > 1 else ""
                return {"type": "whatsapp_send", "contact": contact_name, "message": message}

        # System Controls
        if "battery" in text: return {"type": "system", "cmd": "termux-battery-status"}
        if "flashlight" in text:
            state = "on" if "on" in text else "off"
            return {"type": "system", "cmd": f"termux-torch {state}"}
        if "clipboard" in text:
            if "set" in text:
                content = text.split("set")[1].strip().strip('"').strip("'")
                return {"type": "system", "cmd": f"termux-clipboard-set '{content}'"}
            return {"type": "system", "cmd": "termux-clipboard-get"}

        # Google Search / Browser
        if "google" in text and "search" in text:
            query = text.split("search")[1].split("on google")[0].strip()
            return {"type": "google_search", "query": query}
        if "open" in text and ("http" in text or "." in text):
            url = text.split("open")[1].strip()
            if not url.startswith("http"): url = "https://" + url
            return {"type": "browser_open", "url": url}

        # App Management
        if "open" in text:
            app_name = text.replace("open", "").strip()
            return {"type": "app_launch", "app": app_name}
        if "close" in text:
            app_name = text.replace("close", "").strip()
            return {"type": "app_kill", "app": app_name}

        # Files
        if "file" in text:
            if "create" in text:
                filename = text.split("create file")[1].strip()
                return {"type": "file_create", "name": filename}
            if "read" in text:
                filename = text.split("read file")[1].strip()
                return {"type": "file_read", "name": filename}
            if "delete" in text:
                filename = text.split("delete file")[1].strip()
                return {"type": "file_delete", "name": filename}
            if "list" in text:
                return {"type": "file_list"}

        # AI Fallback
        return {"type": "ai_query", "query": text}

    def handle_intent(self, intent):
        self.log("DETECTED", str(intent), Colors.DIM)
        itype = intent["type"]

        if itype == "shortcut":
            for cmd in intent["commands"]:
                self.log("MACRO", f"Executing: {cmd}", Colors.CYAN)
                self.run_command(cmd)

        elif itype == "youtube_search":
            query = intent["query"].replace(" ", "+")
            self.execute_shell(f"am start -a android.intent.action.VIEW 'https://www.youtube.com/results?search_query={query}'")

        elif itype == "youtube_play":
            self.execute_shell(f"am start -a android.intent.action.VIEW '{intent['url']}'")

        elif itype == "app_open" or itype == "app_launch":
            # Simplistic launch for known apps or search by name (requires more logic for package maps)
            pkg = intent.get("package", intent.get("app"))
            self.execute_shell(f"am start -n {pkg}") # Note: requires package name usually

        elif itype == "whatsapp_send":
            contact_name = intent["contact"]
            message = intent["message"]
            number = self.contacts.get(contact_name)
            if not number:
                self.log("ERROR", f"Contact '{contact_name}' not found in contacts.json", Colors.FAIL)
                return
            if not message:
                message = input(f"{Colors.CYAN}Enter message for {contact_name}:{Colors.ENDC} ")
            
            if self.ask_confirm(f"Send WhatsApp to {contact_name} ({number}): '{message}'?"):
                encoded_msg = message.replace(" ", "%20")
                self.execute_shell(f"am start -a android.intent.action.VIEW 'https://wa.me/{number}?text={encoded_msg}'")
                self.log("INFO", "Opening WhatsApp intent...", Colors.GREEN)

        elif itype == "system":
            res = self.execute_shell(intent["cmd"])
            print(f"{Colors.BOLD}{res}{Colors.ENDC}")

        elif itype == "google_search":
            query = intent["query"].replace(" ", "+")
            self.execute_shell(f"am start -a android.intent.action.VIEW 'https://www.google.com/search?q={query}'")

        elif itype == "browser_open":
            self.execute_shell(f"am start -a android.intent.action.VIEW '{intent['url']}'")

        elif itype.startswith("file_"):
            storage_path = os.path.expanduser("~/storage/shared/KYROS/")
            if not os.path.exists(storage_path): os.makedirs(storage_path)
            
            if itype == "file_create":
                path = os.path.join(storage_path, intent["name"])
                with open(path, 'w') as f: f.write("")
                self.log("SUCCESS", f"File created at {path}")
            elif itype == "file_read":
                path = os.path.join(storage_path, intent["name"])
                if os.path.exists(path):
                    with open(path, 'r') as f: print(f.read())
                else: self.log("ERROR", "File not found", Colors.FAIL)
            elif itype == "file_list":
                files = os.listdir(storage_path)
                print("\n".join(files) if files else "No files found.")
            elif itype == "file_delete":
                path = os.path.join(storage_path, intent["name"])
                if self.ask_confirm(f"Delete file {intent['name']}?"):
                    if os.path.exists(path): os.remove(path); self.log("SUCCESS", "Deleted.")
                    else: self.log("ERROR", "Not found", Colors.FAIL)

        elif itype == "ai_query":
            self.call_gemini(intent["query"])

    def call_gemini(self, query):
        api_key = self.config.get("api_key")
        if not api_key:
            self.log("CONFIG", "Gemini API Key missing. Update config.json", Colors.WARNING)
            return
        
        # Simple REST call to Gemini (requires requests)
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts":[{"text": query}]}]}
        
        try:
            self.log("KYROS", "Thinking...", Colors.BLUE)
            response = requests.post(url, headers=headers, json=data)
            res_json = response.json()
            answer = res_json['candidates'][0]['content']['parts'][0]['text']
            print(f"{Colors.BLUE}{Colors.BOLD}KYROS: {Colors.ENDC}{answer}")
        except Exception as e:
            self.log("ERROR", f"AI Brain failed: {str(e)}", Colors.FAIL)

    def run_command(self, cmd):
        intent = self.parse_intent(cmd)
        self.handle_intent(intent)
        self.save_history(cmd)

    def start(self):
        self.banner()
        if not self.config.get("api_key"):
            key = input(f"{Colors.WARNING}No API Key found. Enter Gemini API Key (or press enter to skip AI): {Colors.ENDC}")
            if key:
                self.config["api_key"] = key
                with open(self.config_path, 'w') as f: json.dump(self.config, f, indent=4)

        while True:
            try:
                cmd = input(f"{Colors.CYAN}KYROS > {Colors.ENDC}")
                if cmd.lower() in ['exit', 'quit']: break
                if not cmd: continue
                self.run_command(cmd)
            except KeyboardInterrupt:
                print("\nShutting down KYROS... Goodbye!")
                break

if __name__ == "__main__":
    kyros = Kyros()
    kyros.start()
