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
    WHITE = '\033[97m'

class Kyros:
    def __init__(self):
        # Fix paths to be relative to the script location
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_dir, "config.json")
        self.contacts_path = os.path.join(self.base_dir, "contacts.json")
        self.history_path = os.path.join(self.base_dir, "history.json")
        self.shortcuts_path = os.path.join(self.base_dir, "shortcuts.json")
        self.load_data()
        
    def load_data(self):
        # Initialize default files if they don't exist
        for path, default in [
            (self.config_path, {"api_key": ""}),
            (self.contacts_path, {"Rahul": "+919876543210"}),
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
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.DIM}[{time_str}]{Colors.ENDC} {color}{tag.upper()}{Colors.ENDC} {message}")

    def speak(self, text):
        # Remove markdown symbols for cleaner speech
        clean_text = text.replace('*', '').replace('#', '').strip()
        self.log("TTS", f"Speaking...", Colors.BLUE)
        # Run in background (&) so it doesn't block the next command
        self.execute_shell(f'termux-tts-speak -r 1.3 "{clean_text}" &')

    def listen(self):
        self.log("VOICE", "LISTENING...", Colors.CYAN)
        # Check for whisper-tiny local binary first (High Accuracy)
        # Otherwise fallback to termux-speech-to-text (High Speed)
        if os.path.exists("/usr/local/bin/whisper-tiny") or os.path.exists("./whisper-tiny"):
            self.log("SYNC", "Using Whisper-Tiny engine", Colors.DIM)
            self.execute_shell("termux-microphone-record -f voice.wav -l 3")
            res = self.execute_shell("whisper-tiny -m models/tiny.bin -f voice.wav -otxt && cat voice.wav.txt")
        else:
            res = self.execute_shell("termux-speech-to-text")
        
        if res and "Error" not in res:
            res = res.strip()
            self.log("VOICE", f"Detected: {res}")
            return res
        return None

    def banner(self):
        os.system('clear')
        print(f"""{Colors.CYAN}{Colors.BOLD}
   ┌──────────────────────────────────────────┐
   │  {Colors.WHITE}K Y R O S  {Colors.CYAN}v2.1 {Colors.DIM}│  TURBO AUTOMATION │{Colors.ENDC}{Colors.CYAN}{Colors.BOLD}
   └──────────────────────────────────────────┘{Colors.ENDC}
   {Colors.BLUE}ENGINE: {Colors.GREEN}HYBRID-FLASH-v2 {Colors.DIM}│ {Colors.BLUE}VOICE: {Colors.GREEN}TURBO-TTS{Colors.ENDC}
        """)

    def execute_shell(self, command):
        try:
            # Run in background for app launches to avoid blocking KYROS
            if "monkey" in command or "am start" in command:
                subprocess.Popen(command + " > /dev/null 2>&1", shell=True)
                return "Launching in background..."
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output.decode('utf-8').strip()}"

    def ask_confirm(self, message):
        res = input(f"{Colors.WARNING}[CONFIRM]{Colors.ENDC} {message} (y/n): ").lower()
        return res == 'y'

    def parse_intent(self, text):
        text = text.lower().strip()
        
        # Voice Commands
        if text in ["listen", "voice", "hey kyros", "talk to me"]:
            return {"type": "voice_input"}

        # Shortcuts
        if text in self.shortcuts:
            return {"type": "shortcut", "commands": self.shortcuts[text]}

        # App Mapping
        app_map = {
            "youtube": "com.google.android.youtube",
            "whatsapp": "com.whatsapp",
            "facebook": "com.facebook.katana",
            "instagram": "com.instagram.android",
            "chrome": "com.android.chrome",
            "gmail": "com.google.android.gm",
            "maps": "com.google.android.apps.maps",
            "spotify": "com.spotify.music",
            "telegram": "org.telegram.messenger",
            "snapchat": "com.snapchat.android",
            "tiktok": "com.zhiliaoapp.musically",
            "twitter": "com.twitter.android",
            "x": "com.twitter.android",
            "netflix": "com.netflix.mediaclient"
        }

        # Multi-App Launch
        if "open" in text and not ("http" in text or "." in text):
            detected = []
            for name, pkg in app_map.items():
                if name in text: detected.append(pkg)
            if detected: return {"type": "app_multi_launch", "packages": detected}
            
            # Simple app launch fallback
            app_name = text.replace("open", "").strip()
            if app_name: return {"type": "app_launch", "app": app_name}

        # YouTube specific
        if "youtube" in text:
            if "search" in text:
                query = text.split("search")[1].split("on youtube")[0].strip()
                return {"type": "youtube_search", "query": query}
            if "play" in text and "http" in text:
                url = text.split("play")[1].split("on youtube")[0].strip()
                return {"type": "youtube_play", "url": url}

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

        elif itype == "app_multi_launch":
            for pkg in intent["packages"]:
                self.log("LAUNCH", f"Starting {pkg}...")
                self.execute_shell(f"monkey -p {pkg} 1")

        elif itype == "app_launch":
            pkg = intent.get("app")
            self.log("LAUNCH", f"Attempting to launch {pkg}...")
            self.execute_shell(f"monkey -p {pkg} 1")

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

        elif itype == "voice_input":
            voice_text = self.listen()
            if voice_text:
                self.run_command(voice_text)

        elif itype == "ai_query":
            # For complex coding/deep reasoning use Pro, otherwise Flash-Lite
            model_type = "pro" if "code" in intent["query"] or "deep" in intent["query"] else "lite"
            self.call_gemini(intent["query"], model_type=model_type)

    def call_gemini(self, query, model_type="lite"):
        api_key = self.config.get("api_key", "").strip().strip('"').strip("'")
        if not api_key:
            self.log("CONFIG", "Gemini API Key missing.", Colors.WARNING)
            return
        
        # Fallback list for stability
        models_to_try = [
            "gemini-1.5-flash", 
            "gemini-1.5-flash-8b",
            "gemini-pro"
        ]
        
        import requests
        
        last_error = ""
        for model in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
                headers = {'Content-Type': 'application/json'}
                data = {"contents": [{"parts":[{"text": query}]}]}
                
                # Low timeout for 'Turbo' feel
                response = requests.post(url, headers=headers, json=data, timeout=10)
                res_json = response.json()
                
                if "error" in res_json:
                    last_error = res_json["error"].get("message", "Unknown")
                    continue

                if 'candidates' in res_json:
                    answer = res_json['candidates'][0]['content']['parts'][0]['text']
                    print(f"\n{Colors.BLUE}{Colors.BOLD}┌── KYROS ({model}) ──┐{Colors.ENDC}")
                    print(f"{Colors.WHITE}{answer}{Colors.ENDC}")
                    print(f"{Colors.BLUE}└───────────────────┘{Colors.ENDC}")
                    self.speak(answer)
                    return
            except Exception as e:
                last_error = str(e)
                continue
        
        self.log("FAULT", f"All brains failed. Last error: {last_error}", Colors.FAIL)


    def run_command(self, cmd):
        intent = self.parse_intent(cmd)
        self.handle_intent(intent)
        self.save_history(cmd)

    def start(self):
        self.banner()
        if not self.config.get("api_key"):
            key = input(f"{Colors.WARNING}No API Key found. Enter Gemini API Key (or press enter to skip AI): {Colors.ENDC}")
            if key:
                processed_key = key.strip().strip('"').strip("'")
                self.config["api_key"] = processed_key
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
