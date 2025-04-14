from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import numpy as np

# DOFBOT kinematic chain using ikpy 4.x style (working structure)
dofbot_chain = Chain(name='dofbot', links=[
    OriginLink(),  # Always required as the root

    URDFLink(
        name="base_rotation",
        origin_translation=[0, 0, 0.06],
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 1]  # Base rotation (Z axis)
    ),
    URDFLink(
        name="shoulder",
        origin_translation=[0, 0, 0.08],
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0]  # Y axis
    ),
    URDFLink(
        name="elbow",
        origin_translation=[0.1, 0, 0],
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0]
    ),
    URDFLink(
        name="wrist",
        origin_translation=[0.1, 0, 0],
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0]
    ),
    URDFLink(
        name="gripper",
        origin_translation=[0.05, 0, 0],
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 1]  # Optional: wrist rotation or clamp
    )
])

def calculate_ik(x, y, z):
    """
    Calculate the joint angles to reach a point (x, y, z).
    Returns joint angles in degrees (for servos).
    """
    target_frame = np.eye(4)
    target_frame[:3, 3] = [x, y, z]

    ik_result = dofbot_chain.inverse_kinematics(target_frame)
    joint_angles_deg = np.degrees(ik_result[1:6])  # Skip OriginLink
    return joint_angles_deg.tolist()
