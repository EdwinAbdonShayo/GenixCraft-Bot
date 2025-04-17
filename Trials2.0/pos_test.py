# get_current_position.py (with negative angle support)
from Arm_Lib import Arm_Device
from ik_controller import dofbot_chain
import numpy as np

Arm = Arm_Device()

def read_servo_angles():
    """Read servo angles from Servos 1-5, allowing for negative values"""
    angles = []
    for i in range(1, 6):
        angle = Arm.Arm_serial_servo_read(i)
        if angle is None or not (-50 <= angle <= 180):
            print(f"[Error] Servo {i} returned invalid angle: {angle}")
            return None
        angles.append(angle)
        print(f"Servo {i}: {angle}*")
    return angles

def compute_forward_kinematics(joint_angles_deg):
    """Use ikpy to compute (x, y, z) of the end effector"""
    joint_angles_rad = np.radians(joint_angles_deg)
    full_angles = [0.0] + joint_angles_rad.tolist()  # Add root

    end_effector_matrix = dofbot_chain.forward_kinematics(full_angles)
    position = end_effector_matrix[:3, 3]
    return position

if __name__ == "__main__":
    print("[Position Tracker] Reading current servo angles...")

    angles_deg = read_servo_angles()
    if angles_deg is not None:
        position = compute_forward_kinematics(angles_deg)

        print("\n[Current End Effector Position]")
        print(f"X: {position[0]:.4f} m")
        print(f"Y: {position[1]:.4f} m")
        print(f"Z: {position[2]:.4f} m")
    else:
        print("[Error] Could not compute position due to invalid servo data.")
