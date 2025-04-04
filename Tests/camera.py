import cv2

def test_camera():
    # Open the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Camera not detected.")
        return
    
    # Set the camera resolution (Optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Press 'q' to quit the camera preview.")
    
    # Loop to continuously capture frames from the camera
    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        
        if not ret:
            print("Failed to grab frame.")
            break
        
        # Display the captured frame in a window
        cv2.imshow('Camera Test', frame)
        
        # Wait for the 'q' key to be pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()
