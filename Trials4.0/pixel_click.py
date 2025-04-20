import cv2
import json
from pose import read_current_pose

GRID_FILE = "pose_grid.json"

# Load existing grid
try:
    with open(GRID_FILE, "r") as f:
        pose_grid = json.load(f)
except FileNotFoundError:
    pose_grid = {}

def save_pose(pixel):
    pose = read_current_pose()
    key = f"({pixel[0]}, {pixel[1]})"
    pose_grid[key] = pose

    with open(GRID_FILE, "w") as f:
        json.dump(pose_grid, f, indent=4)

    print(f"[Saved] {key} ? {pose}")

def main():
    print("[Pixel Grid Builder] Click on the camera feed to capture (x, y) pixel location.")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[Error] Could not open camera.")
        return

    def on_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"\n[Clicked] Pixel: ({x}, {y})")
            input(">> Move arm to this location and press Enter to save...")
            save_pose((x, y))

    cv2.namedWindow("Camera Feed")
    cv2.setMouseCallback("Camera Feed", on_click)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[Exit] Quitting pixel grid capture.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

