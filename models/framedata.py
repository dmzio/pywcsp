from collections import deque
import numpy as np
import sys

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

    def get_component(self, line=-1, component='R'):
        COMPONENTS = {
            'R': 2,
            'G': 1,
            'B': 0,
        }

        try:
            ret_val = self.data[line][:,COMPONENTS[component]]*1.0
        except IndexError:
            ret_val = None
        return ret_val

    def get_data_line(self, lines, component):
        if type(lines) == int:
            return self.get_component(lines, component)
        elif type(lines) == list:
            out = np.empty_like(self.get_component(lines[0], component))
            counter = 1.0
            for l in lines:
                o_l = self.get_component(l, component)
                if o_l is not None:
                    out += o_l
                    counter += 1

            return out / counter
        else:
            print type(lines)
            print "Incorrect parameter"

