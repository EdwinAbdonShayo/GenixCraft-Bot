import socketio

import time
import sys

# Set up SocketIO client
sio = socketio.Client()

# --- Utility Functions ---

def send_status_update(message):
    """Send a status update to the server, if connected."""
    if sio.connected:
        sio.emit("status_update", {"message": message})


def send_error(message):
    """Send an error report to the server, if connected."""
    if sio.connected:
        sio.emit("error_report", {"error": message})

# --- SocketIO Events ---

@sio.event
def connect():
    print("✅ Connected to control system.")
    time.sleep(2)
    send_status_update("GenixCraft is connected and ready.")

@sio.event
def disconnect():
    print("❌ Disconnected from control system.")

@sio.on("robot_command")
def on_robot_command(data):
    command = data.get("command", "")
    print(f"📡 Received command: {command}")

    try:
        # TODO: Add real command handling logic here
        # For now, we simulate execution:
        print(f"⚙️ Executing command: {command}")
        
        # After execution, notify the server
        send_status_update(f"✅ Command '{command}' executed successfully.")

    except Exception as e:
        print(f"⚠️ Error executing command: {e}")
        send_error(f"Error executing command '{command}': {str(e)}")

# --- Connect to Server ---

try:
    sio.connect("http://192.168.177.74:5000")
    # sio.wait_background()  # Run in background to keep the main thread alive
except socketio.exceptions.ConnectionError as e:
    print(f"🚫 Connection failed: {e}")
    sys.exit(1)

# --- Keep the client running ---
# sio.wait()
try:
    while True:
        time.sleep(1)  # Keeps the main thread alive
except KeyboardInterrupt:
    print("\n👋 Shutting down GenixCraft client...")
    send_status_update("GenixCraft client manually shut down.")  # Now safe
    if sio.connected:
        sio.disconnect()
    sys.exit(0)
