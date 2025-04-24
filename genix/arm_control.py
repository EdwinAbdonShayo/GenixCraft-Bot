from genix.pose import read_current_pose
from Arm_Lib import Arm_Device
import time
import json
import os

Arm = Arm_Device()

def move_servos(angles, duration=1000):
    angles = sanitize_pose(angles)
    for i, angle in enumerate(angles, start=1):
        Arm.Arm_serial_servo_write(i, angle, duration)
        time.sleep(0.01)
    time.sleep(duration / 1000)
    print(f"[Pose] Current: {angles}")

def grip(enable):
    angle = 130 if enable else 60
    Arm.Arm_serial_servo_write(6, angle, 400)
    time.sleep(0.5)

def move_and_pick(init_pose, joint_angles):
    print("[Action] Moving to object...")
    move_servos(init_pose, duration=200)
    move_servos(joint_angles, duration=1000)
    grip(1)
    time.sleep(0.5)

    print("[Action] Lifting object slightly...")
    joint_angles[2] = min(180, joint_angles[2] + 40)
    move_servos(joint_angles, duration=800)

def place_object():
    print("[Action] Moving to drop zone...")

    current_pose = read_current_pose()
    if len(current_pose) < 5:
        print("[Error] Cannot read current pose for placement.")
        return

    # Keep servo 1 (base) as-is
    drop_position = current_pose[:]
    drop_position[1] = 70   # Shoulder
    drop_position[2] = 20   # Elbow
    drop_position[3] = 10   # Wrist
    drop_position[4] = 90   # Rotation

    move_servos(drop_position, duration=1000)
    grip(0)
    time.sleep(0.5)
    drop_position[2] = min(180, drop_position[2] + 40)
    move_servos(drop_position, duration=800)

def reset_arm():
    print("[Action] Returning to rest position.")
    rest_position = [90, 90, 0, 10, 90, 50]
    move_servos(rest_position, duration=1000)

# Load angle mappings from JSON
def load_location_map():
    try:
        with open(os.path.join(os.path.dirname(__file__), "locations.json"), "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Error] Failed to load locations.json: {e}")
        return {}

angle_map = load_location_map()


def rotate_to_location(location):

    angle = angle_map.get(location.lower())
    if angle is None:
        print(f"[Error] Unknown location '{location}'")
        return False

    try:
        print(f"[Rotate] Moving base to {angle}� for {location}")
        Arm.Arm_serial_servo_write(1, angle, 800)
        time.sleep(1)
        return True
    except Exception as e:
        print(f"[Error] Failed to rotate to location '{location}': {e}")
        return False


def sanitize_pose(pose):
    pose = [max(0, min(180, p)) for p in pose]
    if pose[1] < 40 and pose[2] < 50:
        print("[Adjust] Elbow too low for shoulder angle. Adjusting elbow to 50.")
        pose[2] = 50
    return pose


def move_and_pick_from_zone(zone, drop_location=None):
    zone_offsets = {
        "center":               [0, -10, 0, 20, 0],
        "center-left":          [13, -15, 0, 30, 15, 0],
        "center-right":         [-7, -15, 0, 30, -10, 0],
        "bottom-left":          [-10, 10, 5, 0, 0],         # not tested
        "bottom-right":         [10, 10, 5, 0, 0],          # not tested
        "bottom-center":        [0, -15, 0, 15, 0, 0],
        "top-center":           [0, -15, 0, 35, 0, 0],
        "top-right":            [5, -15, 0, 35, -10, 0],
        "top-left":             [15, -15, 0, 35, 15, 0],

        "before_pose":          [0, 30, 0, 40, 0, 0]
        
    }

    offsets = zone_offsets.get(zone)
    if offsets is None:
        print(f"[Error] Unknown zone: {zone}")
        return False

    current_pose = read_current_pose()
    if len(current_pose) < 5:
        print("[Error] Couldn't read full pose.")
        return False

    # Generate pickup pose
    new_pose = [current_pose[i] + offsets[i] for i in range(5)]
    new_pose = sanitize_pose(new_pose)

    before_offsets = zone_offsets.get("before_pose", [0, 0, 0, 0, 0, 0])
    init_pose = [current_pose[i] + before_offsets[i] for i in range(5)]
    init_pose = sanitize_pose(init_pose)

    print(f"[Zone] Detected: {zone}")
    print(f"[Pose] Before: {current_pose}")
    print(f"[Offsets] Applied: {offsets}")
    print(f"[Pose] After: {new_pose}")

    try:
        # Move and pick
        move_and_pick(init_pose, new_pose)

        # Rotate to drop-off if specified
        if drop_location:
            if rotate_to_location(drop_location):
                print(f"[Drop] Rotated to {drop_location} for placement.")
            else:
                print(f"[Error] Failed to rotate to drop-off location '{drop_location}'")
                return False

        # Place object
        place_object()
        return True

    except Exception as e:
        print(f"[Failure] Move and pick failed: {e}")
        return False
