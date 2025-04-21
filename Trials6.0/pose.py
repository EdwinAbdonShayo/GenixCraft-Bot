# read_pose.py
from Arm_Lib import Arm_Device
import time

Arm = Arm_Device()

def read_current_pose():
    angles = []
    for i in range(1, 6):  # Servos 1 to 5
        angle = Arm.Arm_serial_servo_read(i)
        angles.append(angle)
        print(f"Servo {i}: {angle}°")
    return angles

if __name__ == "__main__":
    print("[Pose Reader] Move the arm to desired position manually.")
    input("Press Enter to read servo angles...")

    pose = read_current_pose()
    print("\n[Captured Pose] ", pose)
