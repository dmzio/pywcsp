# coding=utf-8
from PySide.QtCore import Slot
from PySide.QtUiTools import QUiLoader
from PySide import QtCore, QtGui, QtUiTools
import cv, cv2, time, ImageQt
from utils.pyside_dynamic import loadUi
from models.cam import Camera


class CamImageView(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.cam = Camera()



        loadUi('views/ui/camview.ui', self)

        # Change active part of the frame by sliders
        self.slider_x1.valueChanged.connect(self.update_x1)
        self.slider_x2.valueChanged.connect(self.update_x2)
        self.slider_y1.valueChanged.connect(self.update_y1)
        self.slider_y2.valueChanged.connect(self.update_y2)



    def redraw(self):
        frame = self.cam.get_frame()

        image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.pixmap = QtGui.QPixmap.fromImage(image).scaledToWidth(self.size().width()-100)

        self.draw_select_rect(self.pixmap)

        self.video.setPixmap(self.pixmap)
        self.addinfo.setText('Gain is {0}'.format(self.cam.capture.get(cv.CV_CAP_PROP_GAIN)))

    @Slot(int)
    def update_x1(self, x1):
        if x1 >= self.slider_x2.value():
            self.slider_x2.setSliderPosition(x1)
        self.cam.set_active_part(x1=x1)


    @Slot(int)
    def update_x2(self, x2):
        if x2 <= self.slider_x1.value():
            self.slider_x1.setSliderPosition(x2)
        self.cam.set_active_part(x2=x2)

    @Slot(int)
    def update_y1(self, y1):
        if y1 >= self.slider_y2.value():
            self.slider_y2.setSliderPosition(y1)
        self.cam.set_active_part(y1=y1)


    @Slot(int)
    def update_y2(self, y2):
        if y2 <= self.slider_y1.value():
            self.slider_y1.setSliderPosition(y2)
        self.cam.set_active_part(y2=y2)


    def draw_select_rect(self, pixmap):
        painter = QtGui.QPainter(pixmap)

        h = pixmap.size().height() / 100.0
        w = pixmap.size().width() / 100.0
        x1, x2, y1, y2 = self.cam.get_active_part_percent()
        rectangle = QtCore.QRectF(w * x1, h * y1, w * (x2 - x1), h * (y2 - y1))
        painter.drawRect(rectangle)


