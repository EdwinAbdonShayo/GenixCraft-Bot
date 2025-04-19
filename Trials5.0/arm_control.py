from pose import read_current_pose

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

    move_servos(pose, duration=600)
