# coding=utf-8
from PySide import QtCore, QtGui
import cv, cv2, time
from models.cam import Camera
from models.framedata import DataQueue, DataQueueController
from views.camimage import CamImageView
from utils.pyside_dynamic import loadUi
import numpy as np
from PySide.QtCore import Slot
from models.spectra import SpectralData
import sys
import matplotlib

## Added for PySide
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import pylab


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        self.settings = None
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle(u'Web-Cam Spectrometer System')
        self.setWindowIcon(QtGui.QIcon.fromTheme('face-devilish'))
        self.setMinimumSize(QtCore.QSize(600, 400))

        tabs = QtGui.QTabWidget()
        self.setCentralWidget(tabs)

        tab_wf = QtGui.QWidget(self)
        tabs.addTab(tab_wf, 'WF')
        tab_wf_l = QtGui.QVBoxLayout(tab_wf)

        self.waterfall = QtGui.QLabel(tab_wf)
        tab_wf_l.addWidget(self.waterfall)
        self.waterfall.setMaximumHeight(200)

        tab_2 = QtGui.QWidget(self)
        tabs.addTab(tab_2, 'CamView')
        tab_2_layout = QtGui.QVBoxLayout(tab_2)
        camimage = CamImageView(tab_2)
        tab_2_layout.addWidget(camimage)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(camimage.redraw)
        timer.start()

        self.statusBar().showMessage('Ready')


        exit = QtGui.QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.setIcon(QtGui.QIcon.fromTheme('window-close'))
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        openFile = QtGui.QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        #self.connect(openFile, QtCore.SIGNAL('triggered()'), self.showDialog)



        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(openFile)
        file.addAction(exit)

        #mt = self.addToolBar('Try')
        #mt.addAction(exit)
        #mt.setFloatable(True)




            # generate the plot
        fig = Figure(figsize=(600, 600), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = fig.add_subplot(111)
        ax.plot([0, 1])
        # generate the canvas to display the plot
        self.canvas = MyDynamicMplCanvas()
        tab_wf_l.addWidget(self.canvas)


        self.wfqueue = DataQueueController(camimage.cam)
        timer.timeout.connect(self.wf_redraw)

        self.spectral_data = SpectralData()
        self.bt_sp = QtGui.QPushButton('&Catch spectrum', tab_wf)
        tab_wf_l.addWidget(self.bt_sp)
        self.bt_sp.clicked.connect(self.catch_spectrum)


        #trying camera settings
        tab_camset = QtGui.QWidget(self)
        tabs.addTab(tab_camset, 'Camera Settings')
        tab_cs_l = QtGui.QVBoxLayout(tab_camset)
        self.l1 = QtGui.QLabel(tab_camset)
        tab_cs_l.addWidget(self.l1)

        self.bt1 = QtGui.QPushButton('&Try uvcdynctrl', tab_camset)
        tab_cs_l.addWidget(self.bt1)
        self.cam = camimage.cam
        self.bt1.clicked.connect(self.check_params)



        self.readSettings()
        self.show()


    def catch_spectrum(self):
        ll = 10
        lf = 0
        d = (self.wfqueue.queue.get_data_line(range(lf-ll, lf), 'G') + self.wfqueue.queue.get_data_line(range(lf-ll, lf), 'B') + self.wfqueue.queue.get_data_line(range(lf-ll, lf), 'R'))/3.0
        self.spectral_data.add_data(d, None)  # TODO Y



    def check_params(self):
        tt = self.cam.try_uvc_control()
        if tt:
            retval = self.cam.switch_autoexposure()
            self.l1.setText("""
        {0}
        3 - AE enabled
        1 - AE disabled (at least for some cams)
        """.format(retval))




    def wf_redraw(self):
        self.wfqueue.add_frame_to_queue()
        fr = self.wfqueue.queue.get_waterfall_data()

        image = QtGui.QImage(fr.data, fr.shape[1], fr.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.pixmap1 = QtGui.QPixmap.fromImage(image).scaledToWidth(self.size().width())

        self.waterfall.setPixmap(self.pixmap1)

        ll = 10
        lf = 0
        self.canvas.data = self.wfqueue.queue.get_data_line(range(lf-ll, lf), 'G')  # gets the G component from the last line
        self.canvas.data2 = self.wfqueue.queue.get_data_line(range(lf-ll, lf), 'R')  # Red component
        self.canvas.data3 = self.wfqueue.queue.get_data_line(range(lf-ll, lf), 'B')  # Blue component from the last line
        self.canvas.data4 = (self.canvas.data3 + self.canvas.data2 + self.canvas.data) / 3



    def writeSettings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.endGroup()
        self.settings.beginGroup("Camera")
        self.settings.setValue("active_part", self.cam.get_active_part_percent())
        self.settings.endGroup()


    def readSettings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size", QtCore.QSize(400, 400)))
        self.move(self.settings.value("pos", QtCore.QPoint(200, 200)))
        self.settings.endGroup()
        self.settings.beginGroup("Camera")
        self.cam.set_active_part(*self.settings.value("active_part"))
        self.settings.endGroup()

    # event : QCloseEvent
    def closeEvent(self, event):
        if True:  # self.userReallyWantsToQuit():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()



class MyDynamicMplCanvas(FigureCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        timer = QtCore.QTimer(self)
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.update_figure)
        timer.start(10)

        self.data = []
        self.data2 = []
        self.data3 = []
        self.data4 = []

    def compute_initial_figure(self):
         self.axes.plot([0, 1, 2, 3], 'r')

    def update_figure(self):
        l = self.data

        self.axes.plot(l, 'g', self.data2, 'r', self.data3, 'b', self.data4, 'y')
        self.draw()




