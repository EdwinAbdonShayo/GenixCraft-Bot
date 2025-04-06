from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import numpy as np

# Adjusted for compatibility with newer ikpy versions
dofbot_chain = Chain(name='dofbot', links=[
    OriginLink(),
    URDFLink(
        name="base_rotation",
        translation=[0, 0, 0.06],
        rotation=[0, 0, 1]
    ),
    URDFLink(
        name="shoulder",
        translation=[0, 0, 0.08],
        rotation=[0, 1, 0]
    ),
    URDFLink(
        name="elbow",
        translation=[0.1, 0, 0],
        rotation=[0, 1, 0]
    ),
    URDFLink(
        name="wrist",
        translation=[0.1, 0, 0],
        rotation=[0, 1, 0]
    ),
    URDFLink(
        name="gripper",
        translation=[0.05, 0, 0],
        rotation=[0, 0, 1]
    )
])
