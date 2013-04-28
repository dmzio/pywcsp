from collections import deque
import numpy as np

class DataQueueController(object):

    def __init__(self, camera):
        self.cam = camera
        self.queue = DataQueue()

    def add_frame_to_queue(self):
        self.queue.append_row(self.cam.get_active_row_data())


class DataQueue(object):
    """
    class for the storage of data extracted from the frames (pixel rows)
    """
    def __init__(self):
        self.data = deque([], maxlen=135)  # queue of pixel rows
        self.prev_shape = None  # shape of the previous row

    def reset(self):
        self.data.clear()

    def append_row(self, row_data):
        if row_data.shape != self.prev_shape:
            self.reset()
        self.prev_shape = row_data.shape
        self.data.append(row_data)


    def get_waterfall_data(self):
        return np.array(self.data)