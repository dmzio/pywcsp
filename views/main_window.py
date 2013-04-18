# coding=utf-8
from PySide import QtCore, QtGui
import cv, cv2, time, ImageQt


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle(u'Web-Cam Spectrometer System')
        self.setWindowIcon(QtGui.QIcon.fromTheme('face-devilish'))
        self.setMinimumSize(QtCore.QSize(600, 400))

        self.camcapture = cv2.VideoCapture(0)
        self.camcapture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 2280)
        self.camcapture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 720)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.redraw)
        timer.start()

        self.addinfo = QtGui.QLabel("sdfhwsldkjhgklajshgfkafgkjfgkashy", self)

        cwidget = QtGui.QWidget(self)
        self.setCentralWidget(cwidget)

        self.video = QtGui.QLabel(self.centralWidget())
        self.video.setMinimumSize(QtCore.QSize(600, 400))

        self.show()


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

        mt = self.addToolBar('Try')
        mt.addAction(exit)
        mt.setFloatable(True)

    def redraw(self):
        _, frame = self.camcapture.read()

        image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap.fromImage(image).scaledToWidth(600)
        self.video.setPixmap(pixmap)
        self.addinfo.setText('Gain is {0}'.format(self.camcapture.get(cv.CV_CAP_PROP_GAIN)))



