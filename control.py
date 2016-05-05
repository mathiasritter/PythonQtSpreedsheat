import sys
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QFileDialog, QUndoStack

from command import InsertRowsCommand, RemoveRowsCommand, InsertColumnsCommand, RemoveColumnsCommand
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
        self.view.actionSave_As.triggered.connect(self.save_as)
        self.view.actionAdd.triggered.connect(self.add_row)
        self.view.actionRemove.triggered.connect(self.remove_rows)
        self.view.actionAdd_Column.triggered.connect(self.add_column)
        self.view.actionRemove_Column.triggered.connect(self.remove_columns)
        self.view.actionUndo.triggered.connect(self.undo)
        self.view.actionRedo.triggered.connect(self.redo)

    def get_selected_rows(self):
        indexes = self.view.tableView.selectionModel().selectedIndexes()
        if indexes:
            return indexes[0].row(), len(indexes)
        else:
            return len(self.model.data_list), 1

    def get_selected_columns(self):
        indexes = self.view.tableView.selectionModel().selectedIndexes()
        if indexes:
            return indexes[0].column(), len(indexes)
        else:
            return len(self.model.header), 1

    def undo(self):
        self.undo_stack.undo()

    def redo(self):
        self.undo_stack.redo()

    def add_row(self):
        row, count = self.get_selected_rows()
        self.undo_stack.push(InsertRowsCommand(self.model, row, 1))

    def remove_rows(self):
        row, count = self.get_selected_rows()
        self.undo_stack.push(RemoveRowsCommand(self.model, row, count))

    def add_column(self):
        column, count = self.get_selected_columns()
        self.undo_stack.push(InsertColumnsCommand(self.model, column, 1))

    def remove_columns(self):
        column, count = self.get_selected_columns()
        self.undo_stack.push(RemoveColumnsCommand(self.model, column, count))

    def open(self):
        filename = QFileDialog.getOpenFileName(self, aption="Open CSV file", filter="CSV file (*.csv)")[0]
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
