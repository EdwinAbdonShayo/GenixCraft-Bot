# arm_control.py

from pose import read_current_pose

import time
from Arm_Lib import Arm_Device

Arm = Arm_Device()

def move_servos(angles, duration=1000):
    """
    Send servo angles to DOFBOT (expecting 5 joints: base to wrist).
    Angles list: [servo1, servo2, servo3, servo4, servo5]
    """
    angles = sanitize_pose(angles)
    for i, angle in enumerate(angles, start=1):
        Arm.Arm_serial_servo_write(i, angle, duration)
        time.sleep(0.01)
    time.sleep(duration / 1000)
    print(f"[Pose] Current: {pose}")



def grip(enable):
    """Enable clamp (servo 6)"""
    angle = 130 if enable else 60
    Arm.Arm_serial_servo_write(6, angle, 400)
    time.sleep(0.5)

def move_and_pick(joint_angles):
    """Move to pick location, grip, lift slightly"""
    print("[Action] Moving to object...")
    move_servos(joint_angles, duration=1000)
    grip(1)
    time.sleep(0.5)

    # Slight lift after grip (modify as needed)
    print("[Action] Lifting object slightly...")
    joint_angles[2] -= 10  # Raise elbow a bit
    move_servos(joint_angles, duration=800)

def place_object():
    """Move to fixed drop location and release"""
    print("[Action] Moving to drop zone...")
    drop_position = [90, 60, 50, 50, 90]  # Customize this
    move_servos(drop_position, duration=1000)
    grip(0)
    time.sleep(0.5)

def reset_arm():
    """Return to rest position"""
    print("[Action] Returning to rest position.")
    rest_position = [90, 130, 0, 0, 90]
    move_servos(rest_position, duration=1000)


# #####################################################3


def step_move(direction, delta=2):
    """Small adjustment based on direction keyword."""
    pose = read_current_pose()
    if not pose or len(pose) < 5:
        print("[Error] Invalid pose data.")
        return

    print(f"[Move] Direction: {direction}")
    if direction == "left":
        pose[0] += delta  # base
    elif direction == "right":
        pose[0] -= delta
    elif direction == "up":
        pose[1] -= delta  # shoulder
        pose[2] -= delta // 2  # elbow
    elif direction == "down":
        pose[1] += delta
        pose[2] += delta // 2
    elif direction == "forward":
        pose[3] += 10  # wrist forward (tweak as needed)
    elif direction == "back":
        pose[3] -= 10

    pose = sanitize_pose(pose)
    move_servos(pose, duration=600)



def sanitize_pose(pose):
    # Safety clamp to 0–180 range
    pose = [max(0, min(180, p)) for p in pose]

    # Inter-servo constraints
    if pose[1] < 40 and pose[2] < 50:
        print("[Adjust] Elbow too low for shoulder angle. Adjusting elbow to 50.")
        pose[2] = 50

    # Add more rules here if needed...

    return pose
