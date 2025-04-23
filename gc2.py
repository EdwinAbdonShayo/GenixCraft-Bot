import socketio
import time
import sys
import os

# --- Import child module functions ---
from genix.arm_control import reset_arm
from genix.pose import read_current_pose
from genix.main import main as visual_pickup

# --- Set up SocketIO client ---
sio = socketio.Client()

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
    time.sleep(1)
    send_status_update("GenixCraft is connected and ready.")

@sio.event
def disconnect():
    print("❌ Disconnected from control system.")

@sio.on("robot_command")
def on_robot_command(data):
    command = data.get("command", "").lower()
    print(f"📡 Received command: {command}")

    try:
        if command == "start":
            visual_pickup()
        elif command == "reset":
            reset_arm()
        elif command == "pose":
            pose = read_current_pose()
            print(f"[Pose] Current servo positions: {pose}")
        else:
            print(f"❓ Unknown command: {command}")

        send_status_update(f"✅ Command '{command}' executed successfully.")
    except Exception as e:
        print(f"⚠️ Error executing command: {e}")
        send_error(f"Error executing command '{command}': {str(e)}")

# --- Connect to Server ---
try:
    sio.connect("http://192.168.97.74:5000")
except socketio.exceptions.ConnectionError as e:
    print(f"🚫 Connection failed: {e}")
    sys.exit(1)

# --- Keep the client running ---
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Shutting down GenixCraft client...")
    send_status_update("GenixCraft client manually shut down.")
    if sio.connected:
        sio.disconnect()
    sys.exit(0)
