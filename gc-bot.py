import socketio

# Set up SocketIO client
sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to control system.")

@sio.event
def disconnect():
    print("❌ Disconnected from control system.")

@sio.on("robot_command")
def on_robot_command(data):
    command = data.get("command", "")
    print(f"📡 Received command: {command}")
    # Here you will parse and handle the command (next step)

# Connect to the control system server
sio.connect("http://localhost:5000")  # Update with server IP if needed
sio.wait()
