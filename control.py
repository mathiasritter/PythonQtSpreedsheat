from PySide import QtGui

from view import Ui_MainWindow


class Control(QtGui.QMainWindow):

    def __init__(self):

        self.view = Ui_MainWindow()


