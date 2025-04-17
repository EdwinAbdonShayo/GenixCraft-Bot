import cv2
import numpy as np

clicked_points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append((x, y))
        print(f"Point {len(clicked_points)}: ({x}, {y})")

        # Draw the clicked point
        cv2.circle(param, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Click Calibration Points", param)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Error] Could not open camera.")
        return

    print("\n[Instructions]")
    print("Click the 4 corners of your workspace in this order:")
    print("1. Top-Left\n2. Top-Right\n3. Bottom-Left\n4. Bottom-Right")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Error] Failed to read frame.")
            break

        clone = frame.copy()
        cv2.imshow("Click Calibration Points", clone)
        cv2.setMouseCallback("Click Calibration Points", click_event, clone)

        if len(clicked_points) >= 4:
            print("\n[Done] Here’s your PIXEL_POINTS array:\n")
            pixel_array = np.array(clicked_points, dtype=np.float32)
            print("PIXEL_POINTS = np.array([")
            for pt in pixel_array:
                print(f"    [{pt[0]}, {pt[1]}],")
            print("], dtype=np.float32)")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[Exit] Interrupted.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
