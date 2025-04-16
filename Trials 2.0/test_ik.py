## test_ik_target.py
from ik_controller import calculate_ik
from arm_control import move_servos
import time

def test_ik_target():
    print("[IK Test Tool] Input X, Y coordinates (in meters). Z will be fixed.")
    while True:
        try:
            x_input = input("Enter X coordinate (or 'q' to quit): ").strip()
            if x_input.lower() == 'q':
                print("[Exit] Exiting IK test tool.")
                break

            y_input = input("Enter Y coordinate: ").strip()

            x = float(x_input)
            y = float(y_input)
            z = 0.02  # Fixed height above the table

            print(f"[Target] Position: ({x}, {y}, {z})")
            joint_angles = calculate_ik(x, y, z)
            print(f"[IK] Joint Angles: {joint_angles}")

            move_servos(joint_angles, duration=1000)
            print("[Action] Robot moved to target.")

        except ValueError:
            print("[Error] Invalid input. Please enter numeric values.")
        except Exception as e:
            print(f"[Error] {e}")

if __name__ == "__main__":
    test_ik_target()