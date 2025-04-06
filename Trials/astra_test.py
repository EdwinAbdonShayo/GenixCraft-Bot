# astra_test.py

import openni
import numpy as np

class AstraContext:
    def __init__(self):
        openni.initialize()
        self.devices = openni.Device.open_all()
        if not self.devices:
            raise RuntimeError("No Astra devices found.")

    def get_devices(self):
        return self.devices

class DepthStream:
    def __init__(self, device):
        self.stream = device.create_depth_stream()

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()
        openni.unload()

    def read_frame(self):
        frame = self.stream.read_frame()
        data = frame.get_buffer_as_uint16()
        depth_array = np.frombuffer(data, dtype=np.uint16).reshape((480, 640))
        return DepthFrame(depth_array)

class DepthFrame:
    def __init__(self, data):
        self.data = data

