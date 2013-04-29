# coding=utf-8
from PySide import QtCore, QtGui
import sys
from views.main_window import MainWindow


def main():
    app = QtGui.QApplication(sys.argv)
    QtCore.QCoreApplication.setOrganizationName("PyScience")
    QtCore.QCoreApplication.setOrganizationDomain("ziolkovskiy.com")
    QtCore.QCoreApplication.setApplicationName("PyWCSp")

    # создаём модель
    #model = CplusDModel()

    # создаём контроллер и передаём ему ссылку на модель
    #controller = CplusDController( model )
    spectrometer_app = MainWindow()

    app.exec_()

if __name__ == '__main__':
    sys.exit(  main() )