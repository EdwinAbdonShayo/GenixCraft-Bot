import json
from scipy.spatial import distance

GRID_FILE = "pose_grid.json"

# Load pixel pose grid
try:
    with open(GRID_FILE, "r") as f:
        POSE_GRID = json.load(f)
except FileNotFoundError:
    print("[Error] pose_grid.json not found.")
    POSE_GRID = {}

def get_angles_from_pixel(x_pixel, y_pixel):
    if not POSE_GRID:
        print("[Error] Pose grid is empty.")
        return None

    target = [x_pixel, y_pixel]
    keys = [eval(k) for k in POSE_GRID.keys()]
    nearest_key = min(keys, key=lambda k: distance.euclidean(k, target))
    print(f"[Grid Match] Closest to ({x_pixel}, {y_pixel}) → {nearest_key}")
    return POSE_GRID[str(nearest_key)]
