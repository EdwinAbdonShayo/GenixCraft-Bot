import cv2
from pyzbar.pyzbar import decode
from arm_control import move_servos, grip, reset_arm, step_move
from pose import read_current_pose
import json

def initialize_camera(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise IOError(f"Could not open camera with ID {camera_id}")
    print("[GenixCraft Bot] Camera initialized successfully.")
    return cap

def detect_target(frame, target_id):
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        try:
            product_info = json.loads(data)
            if product_info.get("product_id") == target_id:
                (x, y, w, h) = obj.rect
                center = (x + w // 2, y + h // 2)
                return center, product_info
        except json.JSONDecodeError:
            continue
    return None, None

def main():
    print("[GenixCraft Bot] Visual Servoing QR Pickup")
    target_id = input("Enter target object ID (e.g. 'Item123'): ").strip()
    cap = initialize_camera()

    last_known_pose = None
    missed_frames = 0
    tolerance = 30  # Adjusted tolerance for testing

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[Error] Camera frame failed.")
                continue

            qr_center, product_info = detect_target(frame, target_id)
            h, w = frame.shape[:2]
            frame_center = (w // 2, h // 2)

            if qr_center:
                print(f"[Target] Found {product_info['product_name']} at {qr_center}")
                print(f"[Frame Center] {frame_center}, [QR Center] {qr_center}")

                dx = qr_center[0] - frame_center[0]
                dy = qr_center[1] - frame_center[1]

                if abs(dx) < tolerance and abs(dy) < tolerance:
                    print("[Status] QR centered. Proceeding to grab.")
                    step_move("forward")
                    grip(True)
                    break
                else:
                    last_known_pose = read_current_pose()
                    missed_frames = 0

                    # Proportional delta for X
                    if abs(dx) > tolerance:
                        delta_x = min(max(abs(dx) // 15, 1), 6)
                        if dx < 0:
                            step_move("left", delta=delta_x)
                        else:
                            step_move("right", delta=delta_x)

                    # Proportional delta for Y
                    if abs(dy) > tolerance:
                        delta_y = min(max(abs(dy) // 15, 1), 6)
                        if dy < 0:
                            step_move("up", delta=delta_y)
                        else:
                            step_move("down", delta=delta_y)

            else:
                print("[Status] Target not detected.")
                missed_frames += 1

                if missed_frames >= 5 and last_known_pose:
                    print("[Recovery] QR lost. Returning to last known pose.")
                    move_servos(last_known_pose, duration=800)
                    missed_frames = 0

            # Display with center & tolerance box
            cv2.circle(frame, frame_center, 5, (255, 0, 0), -1)
            if qr_center:
                cv2.circle(frame, qr_center, 5, (0, 255, 0), -1)

            # Draw tolerance box
            cv2.line(frame, (frame_center[0] - tolerance, frame_center[1]),
                     (frame_center[0] + tolerance, frame_center[1]), (255, 255, 255), 1)
            cv2.line(frame, (frame_center[0], frame_center[1] - tolerance),
                     (frame_center[0], frame_center[1] + tolerance), (255, 255, 255), 1)

            cv2.imshow("Visual Servoing", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[Exit] Manual interrupt.")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        reset_arm()

if __name__ == "__main__":
    main()
