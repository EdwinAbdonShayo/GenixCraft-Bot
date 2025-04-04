import cv2
from pyzbar.pyzbar import decode
import numpy as np

# Initialize the cameras
def initialize_cameras():
    # Open the normal camera (index 0 is the default camera)
    normal_camera = cv2.VideoCapture(0)
    
    # Open the depth camera (assuming you're using RealSense, index 1 could be the depth camera)
    depth_camera = cv2.VideoCapture(1)  # Adjust based on your camera setup

    if not normal_camera.isOpened() or not depth_camera.isOpened():
        print("Error: Cameras not detected.")
        return None, None
    
    return normal_camera, depth_camera

# Detect QR/Barcode in the normal camera feed
def detect_qr_barcode(frame):
    # Decode QR codes and barcodes from the frame
    detected_objects = decode(frame)
    for obj in detected_objects:
        # Draw the bounding box around detected object
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
            # Draw the QR code text
            cv2.putText(frame, obj.data.decode('utf-8'), (pts[0][0], pts[0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return frame

# Obtain depth information from the depth camera (assuming RealSense)
def get_depth_coordinates(depth_frame, x, y):
    # Example to extract depth value (real depth sensor might differ)
    depth_value = depth_frame[y, x]  # Depth at pixel (x, y)
    return depth_value

def main():
    normal_camera, depth_camera = initialize_cameras()
    
    while True:
        # Read frames from both cameras
        ret_normal, normal_frame = normal_camera.read()
        ret_depth, depth_frame = depth_camera.read()

        if not ret_normal or not ret_depth:
            print("Error: Could not read frames.")
            break

        # Process normal camera for QR/Barcode detection
        normal_frame = detect_qr_barcode(normal_frame)

        # Show the normal camera output
        cv2.imshow('Normal Camera - Object Identification', normal_frame)

        # Simulate depth information - For this part, you would get real depth data from your depth sensor
        if ret_depth:
            # Example: Take coordinates from a detected object in the normal camera
            # For simplicity, let's use a fixed point (e.g., (200, 150)) as an example object position
            x, y = 200, 150  # Coordinates of object in the normal camera frame
            
            # Get the depth at (x, y)
            depth = get_depth_coordinates(depth_frame, x, y)
            print(f"Depth at ({x},{y}): {depth} mm")

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the cameras and close OpenCV windows
    normal_camera.release()
    depth_camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
