# coding=utf-8
from PySide import QtCore, QtGui
import cv, cv2, time, ImageQt
import sys


qt_app = QtGui.QApplication(sys.argv)


class SpectrometerApp(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.setWindowTitle(u'Web-Cam Spectrometer System')

        self.camcapture = cv2.VideoCapture(0)
        self.camcapture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
        self.camcapture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 720)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.redraw)
        timer.start()

        self.addinfo = QtGui.QLabel("sdfhwsldkjhgklajshgfkafgkjfgkashy", self)
        self.video = QtGui.QLabel(self)
        self.video.setMinimumSize(QtCore.QSize(600, 400))

    def redraw(self):
        _, frame = self.camcapture.read()

        image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap.fromImage(image).scaledToWidth(600)
        self.video.setPixmap(pixmap)
        self.addinfo.setText('Gain is {0}'.format(self.camcapture.get(cv.CV_CAP_PROP_GAIN)))

    def run(self):
        self.show()
        qt_app.exec_()

# Create an instance of the application and run it
SpectrometerApp().run()