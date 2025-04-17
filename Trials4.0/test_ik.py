from arm_control import move_servos
from pose import read_current_pose
import json
from scipy.spatial import distance

GRID_FILE = "pose_grid.json"

# Load grid
try:
    with open(GRID_FILE, "r") as f:
        POSE_GRID = json.load(f)
except FileNotFoundError:
    print("[Error] pose_grid.json not found.")
    POSE_GRID = {}

def find_nearest_pixel_pose(x_pixel, y_pixel):
    if not POSE_GRID:
        print("[Error] Pose grid is empty.")
        return None

    target = [x_pixel, y_pixel]
    keys = [eval(k) for k in POSE_GRID.keys()]
    nearest_key = min(keys, key=lambda k: distance.euclidean(k, target))
    print(f"[Grid Match] Closest to ({x_pixel}, {y_pixel}) → {nearest_key}")
    return POSE_GRID[str(nearest_key)]

def test_pixel_based_pick():
    print("[Pixel IK Test Tool] Input X, Y pixel coordinates.")
    while True:
        try:
            x_input = input("Enter X pixel (or 'q' to quit): ").strip()
            if x_input.lower() == 'q':
                print("[Exit] Exiting test tool.")
                break

            y_input = input("Enter Y pixel: ").strip()

            x = int(x_input)
            y = int(y_input)

            joint_angles = find_nearest_pixel_pose(x, y)
            if joint_angles:
                print(f"[Match Angles] {joint_angles}")
                move_servos(joint_angles, duration=1000)
            else:
                print("[Warning] No matching pixel pose found.")

        except ValueError:
            print("[Error] Please enter valid numeric pixel coordinates.")
        except Exception as e:
            print(f"[Error] {e}")

if __name__ == "__main__":
    test_pixel_based_pick()
