import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode
from ultralytics import YOLO
from Tests.astra_test import AstraContext, DepthStream
from Arm_Lib import Arm_Device

# ==== ARM CONTROL SETUP ====
Arm = Arm_Device()
time.sleep(0.1)

def arm_clamp(enable):
    Arm.Arm_serial_servo_write(6, 130 if enable else 60, 400)
    time.sleep(0.5)

def arm_move(p, s_time=500):
    for i in range(5):
        id = i + 1
        duration = int(3 * s_time / 4) if id == 1 else int(s_time)
        if id == 5:
            time.sleep(0.1)
            duration = int(s_time * 1.2)
        Arm.Arm_serial_servo_write(id, p[i], duration)
        time.sleep(0.01)
    time.sleep(s_time / 1000)

p_front = [90, 60, 50, 50, 90]
p_right = [0, 60, 50, 50, 90]
p_left = [180, 60, 50, 50, 90]
p_top = [90, 80, 50, 50, 90]
p_rest = [90, 130, 0, 0, 90]

def move_object(direction):
    arm_clamp(0)
    arm_move(p_front, 1000)
    arm_clamp(1)
    arm_move(p_top, 1000)
    if direction == "left":
        arm_move(p_left, 1000)
    elif direction == "right":
        arm_move(p_right, 1000)
    arm_clamp(0)
    arm_move(p_top, 1000)
    arm_move(p_rest, 1000)

# ==== CAMERA AND YOLO SETUP ====
yolo = YOLO("yolov8n.pt")
normal_cam = cv2.VideoCapture(0)  # RGB camera for YOLO
qr_cam = cv2.VideoCapture(1)      # Second camera for QR reading

# ==== DEPTH CAMERA SETUP ====
context = AstraContext()
device = context.get_devices()[0]
depth_stream = DepthStream(device)
depth_stream.start()

def get_depth(cx, cy, depth_data):
    try:
        return depth_data[cy, cx]
    except:
        return -1

def read_qr_from_second_camera():
    for _ in range(60):  # Try for 2 seconds
        ret, frame = qr_cam.read()
        if not ret:
            continue
        codes = decode(frame)
        if codes:
            for code in codes:
                data = code.data.decode('utf-8')
                print("QR Content:", data)
                return data
        time.sleep(0.03)
    return None

# ==== MAIN LOOP ====
try:
    while True:
        ret, frame = normal_cam.read()
        if not ret:
            break

        results = yolo(frame)
        boxes = results[0].boxes

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            depth_frame = depth_stream.read_frame()
            depth_data = depth_frame.data
            depth = get_depth(cx, cy, depth_data)
            label = yolo.model.names[int(box.cls[0])]
            conf = float(box.conf[0])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
            cv2.putText(frame, f"{label} {conf:.2f} ({depth}mm)", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 2)

            print(f"[INFO] Detected: {label} at depth {depth}mm")

            if depth > 0 and depth < 300:  # Close enough
                print("[INFO] Close enough to scan QR code")
                qr_data = read_qr_from_second_camera()
                if qr_data in ["left", "right"]:
                    print(f"[ACTION] Moving object to {qr_data}")
                    move_object(qr_data)
                else:
                    print("[WARNING] QR code unreadable or invalid")
                break  # Avoid multiple detections at once

        cv2.imshow("Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    print("[INFO] Cleaning up...")
    depth_stream.stop()
    normal_cam.release()
    qr_cam.release()
    cv2.destroyAllWindows()
    del Arm
