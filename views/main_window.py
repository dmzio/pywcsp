# coding=utf-8
from PySide import QtCore, QtGui
import cv, cv2, time, ImageQt
from views.camimage import CamImageView


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle(u'Web-Cam Spectrometer System')
        self.setWindowIcon(QtGui.QIcon.fromTheme('face-devilish'))
        self.setMinimumSize(QtCore.QSize(600, 400))

        cwidget = QtGui.QWidget(self)
        self.setCentralWidget(cwidget)

        camimage = CamImageView(cwidget)

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

        self.show()





