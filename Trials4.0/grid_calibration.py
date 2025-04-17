import json
from pose import read_current_pose

GRID_FILE = "pose_grid.json"

def save_pose_to_pixel_grid(x_pixel, y_pixel):
    pose = read_current_pose()
    key = f"({int(x_pixel)}, {int(y_pixel)})"
    
    try:
        with open(GRID_FILE, "r") as f:
            grid = json.load(f)
    except FileNotFoundError:
        grid = {}

    grid[key] = pose

    with open(GRID_FILE, "w") as f:
        json.dump(grid, f, indent=4)

    print(f"[Saved] Pixel {key} ? {pose}")

if __name__ == "__main__":
    print("[Pixel Grid Calibrator] Move arm to a position manually.")
    while True:
        try:
            x = int(input("Enter X pixel coordinate: ").strip())
            y = int(input("Enter Y pixel coordinate: ").strip())
            save_pose_to_pixel_grid(x, y)

            more = input("Add another? (y/n): ").strip().lower()
            if more != "y":
                break
        except Exception as e:
            print(f"[Error] {e}")
