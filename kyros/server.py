import os
import json
from flask import Flask, render_template, request, jsonify
from kyros import Kyros  # Import the Kyros class from your script

app = Flask(__name__)
kyros = Kyros()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command', '')
    if not command:
        return jsonify({"status": "error", "message": "No command provided"}), 400
    
    # Capture the output or handle logic
    intent = kyros.parse_intent(command)
    
    # We can't easily capture the 'print' output in real-time here without redirecting stdout
    # but we can return the intent details and some status
    try:
        kyros.run_command(command)
        return jsonify({
            "status": "success", 
            "intent": intent,
            "message": f"Executed: {command}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(kyros.history)

if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible from other devices if needed, 
    # but usually localhost (127.0.0.1) is enough for phone browser.
    print("\n[KYROS WEB] Starting server at http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
