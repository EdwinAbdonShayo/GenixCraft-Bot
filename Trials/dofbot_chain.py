from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import numpy as np

# This is a rough example! You may need to tweak it based on your actual DOFBOT.
dofbot_chain = Chain(name='dofbot', links=[
    OriginLink(),
    URDFLink(
        name="base_rotation",
        translation_vector=[0, 0, 0.06],
        orientation=[0, 0, 0],
        rotation=[0, 0, 1]
    ),
    URDFLink(
        name="shoulder",
        translation_vector=[0, 0, 0.08],
        orientation=[0, 0, 0],
        rotation=[0, 1, 0]
    ),
    URDFLink(
        name="elbow",
        translation_vector=[0.1, 0, 0],
        orientation=[0, 0, 0],
        rotation=[0, 1, 0]
    ),
    URDFLink(
        name="wrist",
        translation_vector=[0.1, 0, 0],
        orientation=[0, 0, 0],
        rotation=[0, 1, 0]
    ),
    URDFLink(
        name="gripper",
        translation_vector=[0.05, 0, 0],
        orientation=[0, 0, 0],
        rotation=[0, 0, 1]
    )
])
