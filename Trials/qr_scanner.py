import cv2
from pyzbar.pyzbar import decode

def scan_qr_from_camera(camera_index=1):
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    qr_data = None

    if ret:
        decoded_objs = decode(frame)
        for obj in decoded_objs:
            qr_data = obj.data.decode("utf-8")
            break

    cap.release()
    return qr_data
