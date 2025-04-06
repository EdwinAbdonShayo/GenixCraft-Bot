from astra_test import AstraContext, DepthStream
from depth_utils import image_to_world
from ik_controller import solve_ik_and_move
from qr_scanner import scan_qr_from_camera
from ultralytics import YOLO
from Arm_Lib import Arm_Device
import cv2

model = YOLO("yolov8n.pt")
cam = cv2.VideoCapture(0)
arm = Arm_Device()

context = AstraContext()
depth_stream = DepthStream(context.get_devices()[0])
depth_stream.start()

fx, fy = 525.0, 525.0
cx, cy = 319.5, 239.5

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        results = model(frame)
        boxes = results[0].boxes
        if boxes is None:
            continue

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx_img, cy_img = (x1 + x2) // 2, (y1 + y2) // 2

            depth_data = depth_stream.read_frame().data
            depth = depth_data[cy_img, cx_img]

            if depth > 0:
                x, y, z = image_to_world(cx_img, cy_img, depth, fx, fy, cx, cy)

                if z > 0.15:
                    print("Moving closer...")
                    solve_ik_and_move(x, y, z - 0.05, arm)
                else:
                    print("Close enough. Scanning QR...")
                    qr = scan_qr_from_camera()
                    if qr:
                        print(f"QR: {qr}")
                        # Call appropriate action
                    else:
                        print("QR not found.")
            break

        cv2.imshow("YOLO Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    depth_stream.stop()
    cam.release()
    cv2.destroyAllWindows()
    del arm