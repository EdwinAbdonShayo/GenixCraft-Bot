# ik_controller.py
from ikpy.chain import Chain
from ikpy.link import URDFLink
import numpy as np

# Define the DOFBOT's structure
dofbot_chain = Chain(name='dofbot', links=[
    URDFLink(name="base", translation_vector=[0, 0, 0.05], rotation=[0, 0, 1]),
    URDFLink(name="shoulder", translation_vector=[0, 0, 0.08], rotation=[0, 1, 0]),
    URDFLink(name="elbow", translation_vector=[0.11, 0, 0], rotation=[0, 1, 0]),
    URDFLink(name="wrist", translation_vector=[0.10, 0, 0], rotation=[0, 1, 0]),
    URDFLink(name="wrist_rotation", translation_vector=[0.05, 0, 0], rotation=[1, 0, 0]),
    URDFLink(name="gripper", translation_vector=[0.05, 0, 0], rotation=[0, 0, 0]),  # static
])

def calculate_ik(x, y, z):
    # Create a transformation matrix for the target position
    target_frame = np.eye(4)
    target_frame[:3, 3] = [x, y, z]

    ik_result = dofbot_chain.inverse_kinematics(target_frame)

    # Skip the first link (base), and convert radians to degrees
    joint_angles_deg = np.degrees(ik_result[1:6])
    return joint_angles_deg.tolist()
