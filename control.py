import sys
from PySide import QtGui
from PySide.QtGui import QApplication, QFileDialog, QUndoStack, QAbstractItemView

from csvio import CSV
from model import Model
from view import Ui_MainWindow
from delegate import ItemDelegate


class Control(QtGui.QMainWindow):

    def __init__(self):

        super().__init__()

        self.file_name = None
        self.undo_stack = QUndoStack()

        self.model = Model(self)

        self.view = Ui_MainWindow()
        self.view.setupUi(self)
        self.view.tableView.setModel(self.model)
        self.view.tableView.setItemDelegate(ItemDelegate(self.undo_stack))

        self.connect_elements()

    def connect_elements(self):
        self.view.actionOpen.triggered.connect(self.open)
        self.view.actionSave.triggered.connect(self.save)

    def open(self):
        filename = QFileDialog.getOpenFileName(self, caption="Open CSV file", filter="CSV file (*.csv)")[0]
        if len(filename) > 0:
            header, lines = CSV.read(filename)
            self.model.set_model_data(header, lines)

    def save(self):
        if self.file_name is None:
            self.save_as()
        else:
            CSV.write(self.filename, self.model.header, self.model.data_list)

    def save_as(self):
        filename = QFileDialog.getSaveFileName(self, caption="Save CSV file", filter="CSV file (*.csv)")[0]
        if len(filename) > 0:
            self.file_name = filename
            self.save()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    control = Control()
    control.show()
    control.raise_()
    sys.exit(app.exec_())
