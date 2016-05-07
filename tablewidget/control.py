import sys

from PySide.QtCore import Qt
from PySide.QtGui import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QUndoStack

from csvio import CSV
from delegate import ItemDelegate
from tablewidget.command import RemoveRowsCommand, DuplicateRowCommand, InsertRowCommand, EditCommand
from tablewidget.view import Ui_MainWindow


class Control(QMainWindow):

    def __init__(self):
        super().__init__()

        self.file_name = None
        self.undo_stack = QUndoStack()

        self.view = Ui_MainWindow()
        self.view.setupUi(self)
        self.view.tableWidget.setItemDelegate(ItemDelegate(self.undo_stack))

        self.connect_elements()

    def connect_elements(self):
        self.view.actionOpen.triggered.connect(self.open)
        self.view.actionSave.triggered.connect(self.save)
        self.view.actionSave_As.triggered.connect(self.save_as)
        self.view.actionUndo.triggered.connect(self.undo)
        self.view.actionRedo.triggered.connect(self.redo)
        self.view.actionAdd.triggered.connect(self.insert_row)
        self.view.actionRemove.triggered.connect(self.remove_rows)
        self.view.actionDuplicate_Row.triggered.connect(self.duplicate_row)
        self.view.actionCopy.triggered.connect(self.copy)
        self.view.actionPaste.triggered.connect(self.paste)
        self.view.actionCut.triggered.connect(self.cut)

    def save(self):
        if self.file_name is None:
            self.save_as()
        else:
            header = []
            for col in range(self.view.tableWidget.columnCount()):
                header.append(self.view.tableWidget.model().headerData(col, Qt.Horizontal))

            data_list = []
            for row_index in range(self.view.tableWidget.rowCount()):
                row = []
                for col_index in range(self.view.tableWidget.columnCount()):
                    row.append(self.view.tableWidget.item(row_index, col_index).text())
                data_list.append(row)

            CSV.write(self.file_name, header, data_list)

    def save_as(self):
        file_name = QFileDialog.getSaveFileName(self, caption="Save CSV File", filter="CSV File (*.csv)")[0]
        if file_name:
            self.file_name = file_name
            self.save()

    def open(self):
        file_name = QFileDialog.getOpenFileName(self, caption="Open CSV File", filter="CSV File (*.csv)")[0]
        if file_name:
            self.file_name = file_name
            header, data_list = CSV.read(file_name)

            self.view.tableWidget.setColumnCount(len(header))
            self.view.tableWidget.setHorizontalHeaderLabels(header)

            for row_index, row in enumerate(data_list):
                self.view.tableWidget.insertRow(self.view.tableWidget.rowCount())
                for col_index, item in enumerate(row):
                    self.view.tableWidget.setItem(row_index, col_index, QTableWidgetItem(item))

    def undo(self):
        self.undo_stack.undo()

    def redo(self):
        self.undo_stack.redo()

    def get_selected_rows(self):
        rows = set()
        for index in self.view.tableWidget.selectedIndexes():
            rows.add(index.row())
        if len(rows) == 0:
            rows.add(self.view.tableWidget.rowCount())
        return rows

    def insert_row(self):
        rows = self.get_selected_rows()
        self.undo_stack.push(InsertRowCommand(self.view.tableWidget, max(rows)))

    def remove_rows(self):
        rows = self.get_selected_rows()
        self.undo_stack.push(RemoveRowsCommand(self.view.tableWidget, min(rows), len(rows)))

    def duplicate_row(self):
        rows = self.get_selected_rows()
        self.undo_stack.push(DuplicateRowCommand(self.view.tableWidget, max(rows)))

    def copy(self):
        selection = self.view.tableWidget.selectedIndexes()

        if len(selection) == 1:
            text = self.view.tableWidget.model().data(selection[0])
            QApplication.clipboard().setText(text)
            return True

    def cut(self):
        if self.copy():
            selection = self.view.tableWidget.selectedIndexes()
            self.undo_stack.push(EditCommand(self.view.tableWidget.model(), selection[0]))

    def paste(self):
        selection = self.view.tableWidget.selectedIndexes()

        if len(selection) == 1:
            text = QApplication.clipboard().text()
            command = EditCommand(self.view.tableWidget.model(), selection[0])
            command.new_value = text
            self.undo_stack.push(command)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    control = Control()
    control.show()
    control.raise_()
    sys.exit(app.exec_())
