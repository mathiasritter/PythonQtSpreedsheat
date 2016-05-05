import sys
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QFileDialog, QUndoStack

from command import InsertRowsCommand, RemoveRowsCommand, DuplicateRowCommand, EditCommand
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
        self.view.actionDuplicate_Row.triggered.connect(self.duplicate_row)
        self.view.actionUndo.triggered.connect(self.undo)
        self.view.actionRedo.triggered.connect(self.redo)
        self.view.actionCopy.triggered.connect(self.copy)
        self.view.actionPaste.triggered.connect(self.paste)
        self.view.actionCut.triggered.connect(self.cut)

    def get_selected_rows(self):
        indexes = self.view.tableView.selectionModel().selectedIndexes()
        if indexes:
            return indexes[0].row(), len(indexes)
        else:
            return len(self.model.data_list), 1

    def undo(self):
        self.undo_stack.undo()

    def redo(self):
        self.undo_stack.redo()

    def copy(self):
        selection = self.view.tableView.selectionModel().selectedIndexes()

        if len(selection) == 1:
            text = self.model.data(selection[0])
            QApplication.clipboard().setText(text)
            return True

    def cut(self):
        if self.copy():
            selection = self.view.tableView.selectionModel().selectedIndexes()
            self.undo_stack.push(EditCommand(self.model, selection[0]))

    def paste(self):
        selection = self.view.tableView.selectionModel().selectedIndexes()

        if len(selection) == 1:
            text = QApplication.clipboard().text()
            command = EditCommand(self.model, selection[0])
            command.new_value = text
            self.undo_stack.push(command)

    def add_row(self):
        row, count = self.get_selected_rows()
        self.undo_stack.push(InsertRowsCommand(self.model, row, 1))

    def duplicate_row(self):
        row, count = self.get_selected_rows()
        self.undo_stack.push(DuplicateRowCommand(self.model, row))

    def remove_rows(self):
        row, count = self.get_selected_rows()
        self.undo_stack.push(RemoveRowsCommand(self.model, row, count))

    def open(self):
        filename = QFileDialog.getOpenFileName(self, aption="Open CSV file", filter="CSV file (*.csv)")[0]
        if len(filename) > 0:
            header, lines = CSV.read(filename)
            self.model.set_model_data(header, lines)

    def save(self):
        if self.file_name is None:
            self.save_as()
        else:
            CSV.write(self.file_name, self.model.header, self.model.data_list)

    def save_as(self):
        file_name = QFileDialog.getSaveFileName(self, caption="Save CSV file", filter="CSV file (*.csv)")[0]
        if len(file_name) > 0:
            self.file_name = file_name
            self.save()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    control = Control()
    control.show()
    control.raise_()
    sys.exit(app.exec_())
