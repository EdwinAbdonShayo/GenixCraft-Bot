import cv2
from pyzbar.pyzbar import decode
from genix.arm_control import move_servos, grip, reset_arm, move_and_pick_from_zone, rotate_to_location
from genix.pose import read_current_pose
import json
import time

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

def get_zone(qr_center, frame_center, frame_size):
    x, y = qr_center
    fw, fh = frame_size

    margin_x = fw // 6
    margin_y = fh // 6

    if x < frame_center[0] - 2 * margin_x:
        horiz = "left-left"
    elif x < frame_center[0] - margin_x:
        horiz = "left"
    elif x > frame_center[0] + 2 * margin_x:
        horiz = "right-right"
    elif x > frame_center[0] + margin_x:
        horiz = "right"
    else:
        horiz = "center"

    if y < frame_center[1] - margin_y:
        vert = "top"
    elif y > frame_center[1] + margin_y:
        vert = "bottom"
    else:
        vert = "center"

    if horiz == "center" and vert == "center":
        return "center"
    return f"{vert}-{horiz}"

def main(product_id=None, stop_flag=None, send_status_update=None, location1=None, location2=None):
    print("[GenixCraft Bot] Visual Servoing QR Pickup")

    if not product_id:
        print("[ERROR] No product_id passed to main().")
        return

    # Determine pickup/drop locations
    pickup_location = location1
    drop_location = location2

    if location1 and not location2:
        if location1.lower() == "table a":
            pickup_location = "table b"
            drop_location = "table a"
        elif location1.lower() == "table b":
            pickup_location = "table a"
            drop_location = "table b"

    # Move arm to rest before anything
    rest_position = [90, 90, 0, 10, 90, 50]
    move_servos(rest_position, duration=1500)

    # Rotate to pickup location before scanning
    if pickup_location:
        success = rotate_to_location(pickup_location)
        if send_status_update:
            msg = f"[Arm] Rotated to pickup from {pickup_location}" if success else f"[Error] Failed to rotate to {pickup_location}"
            send_status_update(msg)
        if not success:
            return

    cap = initialize_camera()
    last_known_pose = None
    missed_frames = 0
    start_time = time.time()

    try:
        while True:
            if stop_flag and stop_flag.is_set():
                print("[STOP] Emergency stop triggered. Exiting main loop.")
                break

            if time.time() - start_time >= 20:
                message = f"❌ Timeout: No Product found within 20 seconds for product_id {product_id}"
                print("[Timeout]", message)
                if send_status_update:
                    send_status_update(message)
                break

            ret, frame = cap.read()
            if not ret:
                print("[Error] Camera frame failed.")
                continue

            qr_center, product_info = detect_target(frame, product_id)
            h, w = frame.shape[:2]
            frame_center = (w // 2, h // 2)

            if qr_center:
                last_known_pose = read_current_pose()
                print(f"[Target] Found {product_info['product_name']} at {qr_center}")
                print(f"[Frame Center] {frame_center}, [QR Center] {qr_center}")

                zone = get_zone(qr_center, frame_center, (w, h))
                print(f"[Zone] Detected zone: {zone}")

                message = f"[Found] {product_info['product_name']}, Moving!"
                if send_status_update:
                    send_status_update(message)

                if stop_flag and stop_flag.is_set():
                    break

                success = move_and_pick_from_zone(zone, drop_location=drop_location)

                if success:
                    message = f"[Success] {product_info['product_name']} moved successfully!"
                    if send_status_update:
                        send_status_update(message)
                else:
                    message = f"[Failure] Could not move {product_info['product_name']}."
                    if send_status_update:
                        send_status_update(message)

                break
            else:
                print("[Status] Target not detected.")
                missed_frames += 1

                if missed_frames >= 5 and last_known_pose:
                    print(f"[Recovery] Returning to last known pose: {last_known_pose}")
                    move_servos(last_known_pose, duration=800)
                    missed_frames = 0

            if stop_flag and stop_flag.is_set():
                break

            cv2.circle(frame, frame_center, 5, (255, 0, 0), -1)
            if qr_center:
                cv2.circle(frame, qr_center, 5, (0, 255, 0), -1)

            cv2.imshow("Visual Servoing", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[Exit] Manual interrupt.")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("[Action] Returning to rest position.")
        reset_arm()