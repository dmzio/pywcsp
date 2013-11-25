# coding=utf-8
from PySide.QtCore import Slot
from PySide.QtUiTools import QUiLoader
from PySide import QtCore, QtGui, QtUiTools
import cv, cv2, time
from utils.pyside_dynamic import loadUi
from models.cam import Camera


class CamImageView(QtGui.QWidget):
    MIN_WIDTH = 2  # minimal % of active part
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.cam = Camera()
        #box_layout = QtGui.QVBoxLayout(self)
        layout = QtGui.QGridLayout(self)
        #box_layout.addLayout(layout)
        #self.setLayout(layout)
        self.addinfo = QtGui.QLabel(self)
        self.video = QtGui.QLabel(self)
        self.slider_x1 = QtGui.QSlider(orientation=QtCore.Qt.Horizontal, parent=self)
        self.slider_x1.setValue(1)
        self.slider_x2 = QtGui.QSlider(orientation=QtCore.Qt.Horizontal, parent=self)
        self.slider_x2.setValue(99)
        self.slider_y = QtGui.QSlider(self)
        self.slider_y.setInvertedAppearance(True)
        self.slider_y.setValue(50)
        self.pos_y = QtGui.QLineEdit(self)
        self.pos_y.setText(str(self.slider_y.value()))

        layout.addWidget(self.addinfo, 0, 0, columnSpan=2)
        layout.addWidget(self.video, 1, 0)
        layout.addWidget(self.slider_y, 1, 1)
        layout.addWidget(self.pos_y, 2, 1)
        layout.addWidget(self.slider_x1, 2, 0)
        layout.addWidget(self.slider_x2, 3, 0)

        # Change active part of the frame by sliders
        self.slider_x1.valueChanged.connect(self.update_x1)
        self.slider_x2.valueChanged.connect(self.update_x2)
        self.slider_y.valueChanged.connect(self.update_y)
        self.pos_y.returnPressed.connect(self.update_y_t)

    def redraw(self):
        frame = self.cam.get_frame()

        image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.pixmap = QtGui.QPixmap.fromImage(image).scaledToWidth(self.size().width())

        self.draw_select_rect(self.pixmap)

        self.video.setPixmap(self.pixmap)
        txt = 'BRIGHTNESS: {0} \n' \
              'CONTRAST: {1}'.format(self.cam.capture.get(cv.CV_CAP_PROP_BRIGHTNESS),
                                     self.cam.capture.get(cv.CV_CAP_PROP_CONTRAST))
        self.addinfo.setText(txt)

    @Slot(int)
    def update_x1(self, x1):
        if x1 >= self.slider_x2.value() - self.MIN_WIDTH:
            self.slider_x2.setSliderPosition(x1 + self.MIN_WIDTH)
        self.cam.set_active_part(x1=x1)

    @Slot(int)
    def update_x2(self, x2):
        if x2 <= self.slider_x1.value() + self.MIN_WIDTH:
            self.slider_x1.setSliderPosition(x2 - self.MIN_WIDTH)
        self.cam.set_active_part(x2=x2)

    @Slot(int)
    def update_y(self, y):
        self.cam.set_active_part(y=y)
        self.pos_y.setText(str(y))

    def update_y_t(self):
        y = self.pos_y.text()
        self.cam.set_active_part(y=int(y))
        self.slider_y.setValue(int(y))

    def draw_select_rect(self, pixmap):
        painter = QtGui.QPainter(pixmap)

        h = pixmap.size().height() / 100.0
        w = pixmap.size().width() / 100.0
        x1, x2, y = self.cam.get_active_part_percent()
        rectangle = QtCore.QRectF(w * x1, h * y - 1, w * (x2 - x1), 2)
        painter.drawRect(rectangle)


