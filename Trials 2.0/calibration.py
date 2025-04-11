# calibration.py
import numpy as np
import cv2

# You’ll replace these with your actual calibration data
PIXEL_POINTS = np.array([
    [120, 80],     # Top-left
    [500, 75],     # Top-right
    [130, 400],    # Bottom-left
    [510, 395],    # Bottom-right
], dtype=np.float32)

WORLD_POINTS = np.array([
    [0.00, 0.00],
    [0.30, 0.00],
    [0.00, 0.20],
    [0.30, 0.20],
], dtype=np.float32)

# Create transformation matrix once
transform_matrix = cv2.getPerspectiveTransform(PIXEL_POINTS, WORLD_POINTS)

def pixel_to_world(x_pixel, y_pixel, z_fixed=0.02):
    pixel = np.array([[x_pixel, y_pixel]], dtype=np.float32)
    pixel = np.array([pixel])
    mapped = cv2.perspectiveTransform(pixel, transform_matrix)
    x, y = mapped[0][0]
    return [x, y, z_fixed]  # Assume a fixed z (height from table)
