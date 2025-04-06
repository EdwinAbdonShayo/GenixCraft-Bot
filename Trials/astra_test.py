# astra_test.py

from openni import openni2
import numpy as np

class AstraContext:
    def __init__(self):
        openni2.initialize()
        self.device = openni2.Device.open_any()

    def get_devices(self):
        return [self.device]

class DepthStream:
    def __init__(self, device):
        self.stream = device.create_depth_stream()
        self.stream.set_video_mode(
            openni2.OniVideoMode(pixelFormat=openni2.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM,
                                 resolutionX=640,
                                 resolutionY=480,
                                 fps=30)
        )

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()
        openni2.unload()

    def read_frame(self):
        frame = self.stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        depth_array = np.frombuffer(frame_data, dtype=np.uint16).reshape((480, 640))
        return DepthFrame(depth_array)

class DepthFrame:
    def __init__(self, data):
        self.data = data
