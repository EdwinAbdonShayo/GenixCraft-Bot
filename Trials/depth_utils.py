def image_to_world(u, v, depth, fx, fy, cx, cy):
    Z = depth / 1000.0  # mm → meters
    X = (u - cx) * Z / fx
    Y = (v - cy) * Z / fy
    return X, Y, Z

fx, fy = 525.0, 525.0  # Focal lengths (pixels)
cx, cy = 319.5, 239.5  # Optical center (image center)
