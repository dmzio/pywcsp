import cv, cv2, time
from subprocess import call, check_call, check_output
import subprocess


class Camera(object):

    def __init__(self):
        self.active_part = None

        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 2280)
        self.capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 720)




    def get_frame(self):
        """
        returns raw frame data from OpenCV
        """
        _, frame = self.capture.read()
        return frame

    def set_active_part(self, x1=None, x2=None, y=None):
        """
        sets active part of the frame
        :params - int percentage of the frame
        """
        try:
            assert self.active_part
        except AssertionError or AttributeError:
            self.active_part = {'x1': 1, 'x2': 99, 'y': 50}

        self.active_part.update({
            'x1': x1 if x1 is not None else self.active_part['x1'],
            'x2': x2 if x2 is not None else self.active_part['x2'],
            'y': y if y is not None else self.active_part['y'],
        })

    def get_active_part_percent(self):
        try:
            assert self.active_part
        except AssertionError:
            self.set_active_part()

        a = self.active_part
        return a['x1'], a['x2'], a['y']

    def get_active_row_data(self):
        """
        returns row of active pixels for the current frame
        """
        frame = self.get_frame()
        h, w, colors = frame.shape

        x1_pc, x2_pc, y_pc = self.get_active_part_percent()

        return frame[h * y_pc // 100][w * x1_pc // 100:w * x2_pc // 100]

    def try_uvc_control(self):
        """
        tries to find uvcdynctrl and control camera settings with it
        """
        retval = check_call(["uvcdynctrl", '-l'])
        return not bool(retval)

    def switch_autoexposure(self):
        """

        3 - AE enabled
        1 - AE disabled (at least for some cams)
        """
        #TODO control of the devise name

        cur_val = check_output('uvcdynctrl -d "video1"  -g "Exposure, Auto"', stderr=subprocess.STDOUT, shell=True)
        if int(cur_val) == 3:
            new_val = 1
        else:
            new_val = 3

        check_call('uvcdynctrl -d "video0" -s "Exposure, Auto" {0}'.format(new_val), shell=True)

        return check_output('uvcdynctrl -d "video0" -g "Exposure, Auto"', stderr=subprocess.STDOUT, shell=True)

    def get_exposure_value(self):
        return check_output('uvcdynctrl -d "video0" -g "Exposure (Absolute)"', stderr=subprocess.STDOUT, shell=True)



