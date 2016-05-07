import sys

from PySide import QtGui
from PySide.QtGui import QApplication, QFileDialog, QUndoStack

from csvio import CSV
from delegate import ItemDelegate
from tablemodel.command import RemoveRowsCommand, DuplicateRowCommand, EditCommand, InsertRowCommand
from tablemodel.model import Model
from tablemodel.view import Ui_MainWindow


class Control(QtGui.QMainWindow):
    def __init__(self):

        super().__init__()

        self.file_name = None
        self.undo_stack = QUndoStack()

        self.model = Model(self)

        self.view = Ui_MainWindow()
        self.view.setupUi(self)
        self.view.tableView.setModel(self.model)
        self.view.tableView.setItemDelegate(ItemDelegate(self))

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

    def push_with_text(self, command, text):
        self.undo_stack.beginMacro(text)
        self.undo_stack.push(command)
        self.undo_stack.endMacro()
        self.set_undo_redo_text()

    def set_undo_redo_text(self):
        self.view.actionUndo.setText("Undo " + self.undo_stack.undoText())
        self.view.actionRedo.setText("Redo " + self.undo_stack.redoText())

    def get_selected_rows(self):
        rows = set()
        for index in self.view.tableView.selectionModel().selectedIndexes():
            rows.add(index.row())
        if len(rows) == 0:
            rows.add(self.model.rowCount())
        return rows

    def undo(self):
        self.undo_stack.undo()
        self.set_undo_redo_text()

    def redo(self):
        self.undo_stack.redo()
        self.set_undo_redo_text()

    def copy(self):
        selection = self.view.tableView.selectionModel().selectedIndexes()

        if len(selection) == 1:
            text = self.model.data(selection[0])
            QApplication.clipboard().setText(text)
            return True

    def cut(self):
        if self.copy():
            selection = self.view.tableView.selectionModel().selectedIndexes()
            command = EditCommand(self.model, selection[0])
            self.push_with_text(command, "Cut")

    def paste(self):
        selection = self.view.tableView.selectionModel().selectedIndexes()

        if len(selection) == 1:
            text = QApplication.clipboard().text()
            command = EditCommand(self.model, selection[0])
            command.new_value = text
            self.push_with_text(command, "Paste")

    def add_row(self):
        rows = self.get_selected_rows()
        command = InsertRowCommand(self.model, max(rows))
        self.push_with_text(command, "Insert Row")

    def duplicate_row(self):
        rows = self.get_selected_rows()
        command = DuplicateRowCommand(self.model, max(rows))
        self.push_with_text(command, "Duplicate Row")

    def remove_rows(self):
        rows = self.get_selected_rows()
        command = RemoveRowsCommand(self.model, min(rows), len(rows))
        self.undo_stack.push(command, "Remove Row(s)")

    def open(self):
        file_name = QFileDialog.getOpenFileName(self, aption="Open CSV file", filter="CSV file (*.csv)")[0]
        if len(file_name) > 0:
            self.file_name = file_name
            header, lines = CSV.read(file_name)
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
