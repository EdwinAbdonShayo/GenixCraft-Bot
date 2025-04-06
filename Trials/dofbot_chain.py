from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import numpy as np

# Fully compatible with ikpy =4.x
dofbot_chain = Chain(name='dofbot', links=[
    OriginLink(),
    URDFLink(
        name="base_rotation",
        origin_translation=[0, 0, 0.06],
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 1]
    ),
    URDFLink(
        name="shoulder",
        origin_translation=[0, 0, 0.08],
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0]
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
        rotation=[0, 0, 1]
    )
])

