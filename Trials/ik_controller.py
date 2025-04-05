import numpy as np
import time
from dofbot_chain import dofbot_chain

def solve_ik_and_move(x, y, z, arm):
    target_position = [x, y, z]
    
    print(f"[IK] Target world coordinates: {target_position}")
    
    # Compute IK
    joint_angles = dofbot_chain.inverse_kinematics(target_position)
    print(f"[IK] Joint angles: {joint_angles}")

    # Convert to servo degrees and move (skip base link)
    for i in range(1, 6):  # DOFBOT has 5 joints
        angle_deg = int(np.degrees(joint_angles[i]))
        angle_deg = max(0, min(180, angle_deg))  # Clamp for safety
        arm.Arm_serial_servo_write(i, angle_deg, 500)
        time.sleep(0.05)

    print("[IK] Arm moved to position.")
