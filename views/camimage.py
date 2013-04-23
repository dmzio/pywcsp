# coding=utf-8
from PySide import QtCore, QtGui
import cv, cv2, time, ImageQt

class CamImageView(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.camcapture = cv2.VideoCapture(0)
        self.camcapture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 2280)
        self.camcapture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 720)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.redraw)
        timer.start()

        self.addinfo = QtGui.QLabel("sdfhwsldkjhgklajshgfkafgkjfgkashy", self)



        self.video = QtGui.QLabel(parent)
        self.video.setMinimumSize(QtCore.QSize(600, 400))



    def redraw(self):
        _, frame = self.camcapture.read()

        for i in range(50):
            for j in range(i):
                frame[i][j] += [50, 50, 50]


        image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap.fromImage(image).scaledToWidth(600)



        self.video.setPixmap(pixmap)
        self.addinfo.setText('Gain is {0}'.format(self.camcapture.get(cv.CV_CAP_PROP_GAIN)))


    def draw_select_rect(self, x1, y1, x2, y2):
        pass
