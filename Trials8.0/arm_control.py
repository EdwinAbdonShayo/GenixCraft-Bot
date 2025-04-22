from pose import read_current_pose
from Arm_Lib import Arm_Device
import time

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

def move_and_pick(joint_angles):
    print("[Action] Moving to object...")
    move_servos(joint_angles, duration=1000)
    grip(1)
    time.sleep(0.5)

    print("[Action] Lifting object slightly...")
    joint_angles[2] = max(0, joint_angles[2] - 10)
    move_servos(joint_angles, duration=800)

def place_object():
    print("[Action] Moving to drop zone...")
    drop_position = [90, 60, 50, 50, 90]
    move_servos(drop_position, duration=1000)
    grip(0)
    time.sleep(0.5)

def reset_arm():
    print("[Action] Returning to rest position.")
    rest_position = [90, 90, 0, 10, 90, 50]
    move_servos(rest_position, duration=1000)

def step_move(direction, delta=2):
    pose = read_current_pose()
    if not pose or len(pose) < 5:
        print("[Error] Invalid pose data.")
        return

    print(f"[Move] Direction: {direction}")
    if direction == "left":
        pose[0] += delta
    elif direction == "right":
        pose[0] -= delta
    elif direction == "up":
        pose[1] -= delta
        pose[2] -= delta // 2
    elif direction == "down":
        pose[1] += delta
        pose[2] += delta // 2
    elif direction == "forward":
        pose[3] += 10
    elif direction == "back":
        pose[3] -= 10

    pose = sanitize_pose(pose)
    move_servos(pose, duration=600)

def sanitize_pose(pose):
    pose = [max(0, min(180, p)) for p in pose]
    if pose[1] < 40 and pose[2] < 50:
        print("[Adjust] Elbow too low for shoulder angle. Adjusting elbow to 50.")
        pose[2] = 50
    return pose

def move_and_pick_from_zone(zone):
    zone_offsets = {
        # "top-left-left":     [-15, -5, -5, 0, -5],
        # "top-left":          [-10, -5, -5, 0, 0],
        # "top-right":         [10, -5, -5, 0, 0],
        # "top-right-right":   [15, -5, -5, 0, 5],
        # "bottom-left-left":  [-15, 10, 5, 0, -5],
        # "bottom-left":       [-10, 10, 5, 0, 0],
        # "bottom-right":      [10, 10, 5, 0, 0],
        # "bottom-right-right":[15, 10, 5, 0, 5],
        # "top-center":        [0, -8, -5, 0, 0],
        # "bottom-center":     [0, 10, 5, 0, 0],
        # "left-left":         [-15, 0, 0, 0, -5],
        # "left":              [-10, 0, 0, 0, -3],
        # "right":             [10, 0, 0, 0, 3],
        # "right-right":       [15, 0, 0, 0, 5],
        "center":               [0, 0, 0, 20, 0],
        "center-left":          [13, -15, 0, 30, 15, 0],
        "center-right":         [-7, -15, 0, 30, -10, 0],
        "bottom-center":        [0, -15, 0, 15, 0, 0],
        "top-center":           [0, -15, 0, 35, 0, 0],
        "top-right":            [5, -15, 0, 35, -10, 0],
        "top-left":             [15, -15, 0, 35, 15, 0],
        
    }

    offsets = zone_offsets.get(zone)
    if offsets is None:
        print(f"[Error] Unknown zone: {zone}")
        return

    current_pose = read_current_pose()
    if len(current_pose) < 5:
        print("[Error] Couldn't read full pose.")
        return

    new_pose = [current_pose[i] + offsets[i] for i in range(5)]
    new_pose = sanitize_pose(new_pose)

    print(f"[Zone] Detected: {zone}")
    print(f"[Pose] Before: {current_pose}")
    print(f"[Offsets] Applied: {offsets}")
    print(f"[Pose] After: {new_pose}")

    move_and_pick(new_pose)
