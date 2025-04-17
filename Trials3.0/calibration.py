# calibration.py
import numpy as np
import cv2

# You’ll replace these with your actual calibration data
PIXEL_POINTS = np.array([
    [18.0, 18.0],     # Top-left
    [628.0, 18.0],     # Top-right
    [18.0, 468.0],    # Bottom-left
    [628.0, 468.0],    # Bottom-right
], dtype=np.float32)

WORLD_POINTS = np.array([
    [0.00, 0.00],
    [0.09, 0.00],
    [0.00, 0.07],
    [0.09, 0.07],
], dtype=np.float32)

# Create transformation matrix once
transform_matrix = cv2.getPerspectiveTransform(PIXEL_POINTS, WORLD_POINTS)

def pixel_to_world(x_pixel, y_pixel, z_fixed=0.1):
    pixel = np.array([[x_pixel, y_pixel]], dtype=np.float32)
    pixel = np.array([pixel])
    mapped = cv2.perspectiveTransform(pixel, transform_matrix)
    x, y = mapped[0][0]
    return [x, y, z_fixed]  # Assume a fixed z (height from table)
