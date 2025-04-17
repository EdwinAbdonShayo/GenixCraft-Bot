# move_single_servo.py
from Arm_Lib import Arm_Device
import time

Arm = Arm_Device()

def move_single_servo():
    while True:
        try:
            print("\n[Servo Move Tool]")
            servo = input("Enter servo number (1–5), or 'q' to quit: ").strip()
            if servo.lower() == 'q':
                print("[Exit] Exiting servo control.")
                break

            servo_num = int(servo)
            if not 1 <= servo_num <= 6:
                print("[Error] Servo number must be between 1 and 5.")
                continue

            angle = int(input(f"Enter angle for Servo {servo_num} (0–180): ").strip())
            if not -50 <= angle <= 180:
                print("[Error] Angle must be between 0 and 180.")
                continue

            duration = 1000  # Move time in milliseconds
            Arm.Arm_serial_servo_write(servo_num, angle, duration)
            time.sleep(duration / 1000)
            print(f"[Moved] Servo {servo_num} set to {angle}°")

        except ValueError:
            print("[Error] Invalid input. Please enter numeric values.")

if __name__ == "__main__":
    print("[Manual Servo Control] Use this tool to move servos individually.")
    move_single_servo()
