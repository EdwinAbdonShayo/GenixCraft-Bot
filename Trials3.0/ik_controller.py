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

def calculate_ik(x, y, z, current_angles_deg=None):
    """
    Calculate the joint angles to reach a point (x, y, z).
    Returns joint angles in degrees (for servos).
    """

    Z_OFFSET = 0.1
    target_position = [x, y, z + Z_OFFSET]

    if current_angles_deg:
        # Convert from servo space (0-180) to IKPY space (-90 to +90)
        initial_guess = np.radians(np.array(current_angles_deg) - 90)
        initial_guess = np.insert(initial_guess, 0, 0.0)  # add base fixed joint
    else:
        initial_guess = None  # let IKPY guess from scratch

    ik_result = dofbot_chain.inverse_kinematics(
        target_position=target_position,
        initial_position=initial_guess
    )

    joint_angles_deg = np.degrees(ik_result[1:6]) + 90
    joint_angles_deg = np.clip(joint_angles_deg, 0, 180)

    return joint_angles_deg.tolist()

