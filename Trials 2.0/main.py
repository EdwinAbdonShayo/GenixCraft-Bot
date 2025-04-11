# GenixCraft Bot - Stage 2
# Target object detection and matching
import cv2
from pyzbar.pyzbar import decode
from calibration import pixel_to_world
from ik_controller import calculate_ik
from arm_control import move_and_pick, place_object, reset_arm


def initialize_camera(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise IOError(f"Could not open camera with ID {camera_id}")
    print("[GenixCraft Bot] Camera initialized successfully.")
    return cap

def detect_qr_codes(frame):
    decoded_objects = decode(frame)
    qr_data_list = []

    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        (x, y, w, h) = obj.rect
        center = (x + w // 2, y + h // 2)
        qr_data_list.append((data, center))

        # Draw a rectangle and label the QR code
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return qr_data_list, frame

def main():
    print("[GenixCraft Bot] Starting QR detection system...")

    # Set your target object ID here (could be replaced with user input or dynamic command later)
    target_object_id = input("Enter target object ID (e.g., 'Item123'): ").strip()

    cap = initialize_camera()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[GenixCraft Bot] Frame capture failed.")
                continue

            qr_data_list, processed_frame = detect_qr_codes(frame)

            target_found = False
            for data, center in qr_data_list:
                if data == target_object_id:
                    print(f"[MATCH FOUND] Target '{data}' detected at {center}")
                    world_coords = pixel_to_world(center[0], center[1])
                    print(f"[World Coordinates] {world_coords}")

                    joint_angles = calculate_ik(*world_coords)
                    print(f"[IK Angles] {joint_angles}")
                    target_found = True

                    # For now, pause or just highlight
                    cv2.circle(processed_frame, center, 8, (0, 0, 255), -1)

                    # Move & pick object
                    move_and_pick(joint_angles)
                    place_object()
                    reset_arm()

                    break  # End after successful operation

            if not target_found:
                print("[Status] Target not found in this frame.")

            cv2.imshow("GenixCraft Bot - Camera Feed", processed_frame)

            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[GenixCraft Bot] Exiting detection loop.")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
