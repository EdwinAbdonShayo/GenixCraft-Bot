## 📌 Project Overview
### Hardware Components:
- **DOFBOT Robotic Arm (6 DOF)** with clamp as servo 6.
- **Single RGB Camera** (standard USB or Raspberry Pi camera).

### Software Libraries:
- **Python 3**
- **OpenCV**
- **pyzbar**
- **Arm_Lib** (DOFBOT provided library)

## 🚀 Project Workflow
### High-Level Flow:
1. Define angular ranges for tables/workspaces:

- Table A: `0°–45°`
- Table B: `45°–90°`
- Table C: `90°–135°`
- Table D: `135°–180°`

2. Receive command to pick a specific QR-coded object from a defined table (e.g., "Pick object XYZ from table C").

3. Move camera to target area, capture frames, and decode QR codes.

4. Upon QR code match, use image coordinates to calculate robotic arm angles (servo positions).

5. Execute pick-and-place motion with DOFBOT.



## Prompt

I’m working on a robotic sorting system using a **DOFBOT robotic arm** with **6 degrees of freedom** (with servo 6 controlling the clamp). The robot uses a **single normal camera** (no depth sensing) to visually detect and identify objects via **QR codes**, using **OpenCV** and pyzbar.

The workspace is divided into angular zones, each representing a physical table:

- Table A: 0°–45°

- Table B: 45°–90°

- Table C: 90°–135°

- Table D: 135°–180°

The robot receives commands like:
👉 “*move the water box to table A at 12PM*”

### 💡 Project Workflow:
1. The robot receives the object ID and target table.

2. It turns or faces the correct angular segment based on the predefined table angles.

3. It captures a camera frame and uses pyzbar to detect and decode QR codes.

4. Once the desired object is found by matching the QR content:

- Its pixel position in the image is extracted.

- The pixel position is then converted into real-world coordinates (using a calibrated mapping).

- Inverse Kinematics (IK) is used to compute joint angles that allow the robot arm to reach the object.

5. The robot picks the object using the clamp and moves it to a target location (e.g., another table or drop zone).

The movement code for DOFBOT currently supports servo control through `Arm_Lib`, and I am integrating IK using `ikpy` or another appropriate library. My system does not use a depth camera — only 2D image input with calibrated projection.

