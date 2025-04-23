import socketio
import time
import sys
import os
import threading

# --- Add child folder to path for imports ---
# sys.path.append(os.path.join(os.path.dirname(__file__), 'child'))

from genix.main import main as visual_pickup  # Visual servoing logic

# --- SocketIO Client Setup ---
sio = socketio.Client()

# --- Global Stop Flag ---
stop_flag = threading.Event()

# --- Utility Functions ---
def send_status_update(message):
    if sio.connected:
        sio.emit("status_update", {"message": message})

def send_error(message):
    if sio.connected:
        sio.emit("error_report", {"error": message})

# --- SocketIO Events ---
@sio.event
def connect():
    print("✅ Connected to control system.")
    send_status_update("GenixCraft is connected and ready.")

@sio.event
def disconnect():
    print("❌ Disconnected from control system.")

@sio.on("robot_command")
def on_robot_command(data):
    command = data.get("command", "").lower()
    payload = data.get("payload", [])  # Expected to be a JSON array
    print(f"--> Received command: {command}, Payload: {payload}")

    try:
        if command == "start":
            if not isinstance(payload, list):
                raise ValueError("Payload for 'start' must be a list of commands.")
            
            stop_flag.clear()
            thread = threading.Thread(target=run_command_sequence, args=(payload,))
            thread.start()

        elif command == "stop":
            print("--> Emergency stop triggered.")
            stop_flag.set()
            send_status_update("--> Emergency stop activated.")
        
        else:
            print(f"⚠️ Unknown command received: {command}")
            send_error(f"Unknown command: {command}")

    except Exception as e:
        print(f"⚠️ Error handling command: {e}")
        send_error(f"Error handling command '{command}': {str(e)}")

# --- Command Execution Logic ---
def run_command_sequence(command_list):
    send_status_update("✅ Executing start sequence.")
    for cmd in command_list:
        if stop_flag.is_set():
            print("--> Sequence interrupted by stop command.")
            return
        print(f"[Executing] --> {cmd}")
        visual_pickup(stop_flag=stop_flag)
    send_status_update("--> All commands completed.")

# --- Connect and Loop ---
try:
    sio.connect("http://192.168.177.74:5000")
except socketio.exceptions.ConnectionError as e:
    print(f"?? Connection failed: {e}")
    sys.exit(1)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n--> Manual shutdown.")
    send_status_update("Client manually shut down.")
    if sio.connected:
        sio.disconnect()
    sys.exit(0)
