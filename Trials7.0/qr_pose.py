import cv2
from pyzbar.pyzbar import decode

def initialize_camera(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise IOError(f"Could not open camera with ID {camera_id}")
    print("[Camera] Initialized.")
    return cap

def main():
    cap = initialize_camera()

    print("[Test] Starting QR position tracker. Press 'q' to quit.")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[Error] Failed to capture frame.")
                continue

            height, width = frame.shape[:2]
            print(f"[Frame Size] Width: {width}, Height: {height}")

            decoded_objects = decode(frame)
            if decoded_objects:
                for obj in decoded_objects:
                    (x, y, w, h) = obj.rect
                    center_x = x + w // 2
                    center_y = y + h // 2
                    print(f"[QR Found] Center Position: ({center_x}, {center_y})")

                    # Visual feedback
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                    cv2.putText(frame, "QR", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            else:
                print("[QR] No QR code detected.")

            cv2.imshow("QR Position Tracker", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[Exit] Test ended.")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
