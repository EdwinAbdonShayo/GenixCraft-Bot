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
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    decoded_objects = decode(thresh)

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
    tolerance = 20

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
                last_known_pose = read_current_pose()  # ? Save pose as soon as QR is seen
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
                    missed_frames = 0  # ? Reset missed frame counter

                    if abs(dx) > abs(dy):
                        if dx < -tolerance:
                            step_move("left")
                        elif dx > tolerance:
                            step_move("right")
                    else:
                        if dy < tolerance:
                            step_move("up")
                        elif dy > -tolerance:
                            step_move("down")
            else:
                print("[Status] Target not detected.")
                missed_frames += 1

                if missed_frames >= 5 and last_known_pose:
                    print(f"[Recovery] QR lost. Returning to last known pose: {last_known_pose}")
                    move_servos(last_known_pose, duration=800)
                    missed_frames = 0

            # Visual display
            cv2.circle(frame, frame_center, 5, (255, 0, 0), -1)
            if qr_center:
                cv2.circle(frame, qr_center, 5, (0, 255, 0), -1)

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
        print("[Action] Returning to rest position.")
        reset_arm()

if __name__ == "__main__":
    main()