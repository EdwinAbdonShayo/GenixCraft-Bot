from ik_controller import calculate_ik
from arm_control import move_servos
from pos_test import read_servo_angles
import time

def test_ik_target():
    print("[IK Test Tool] Input X, Y, Z coordinates (in meters).")
    while True:
        try:
            x_input = input("Enter X coordinate (or 'q' to quit): ").strip()
            if x_input.lower() == 'q':
                print("[Exit] Exiting IK test tool.")
                break

            y_input = input("Enter Y coordinate: ").strip()
            z_input = input("Enter Z coordinate: ").strip()

            x = float(x_input)
            y = float(y_input)
            z = float(z_input)

            current_pose = read_servo_angles()
            if current_pose is None:
                print("[Error] Failed to read servo angles.")
                continue

            print(f"[Target] Position: ({x}, {y}, {z})")
            joint_angles = calculate_ik(x, y, z, current_pose)
            print(f"[IK] Joint Angles: {joint_angles}")

            move_servos(joint_angles, duration=1000)
            print("[Action] Robot moved to target.")

        except ValueError:
            print("[Error] Invalid input. Please enter numeric values.")
        except Exception as e:
            print(f"[Error] {e}")

if __name__ == "__main__":
    test_ik_target()
