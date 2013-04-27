from collections import deque


class DataQueue(object):
    """
    class for the storage of data extracted from the frames (pixel rows)
    """
    def __init__(self):
        self.data = deque([])  # queue of pixel rows


    def get_waterfall_data(self):
        pass