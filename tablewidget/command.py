import copy

from PySide.QtGui import QUndoCommand, QTableWidgetItem


class EditCommand(QUndoCommand):

    def __init__(self, model, index):
        QUndoCommand.__init__(self)
        self.old_value = None
        self.new_value = None
        self.model = model
        self.index = index

    def undo(self):
        self.new_value = self.model.data(self.index)
        self.model.setData(self.index, self.old_value)

    def redo(self):
        self.old_value = self.model.data(self.index)
        self.model.setData(self.index, self.new_value)


class InsertRowCommand(QUndoCommand):

    def __init__(self, tableWidget, row):
        super().__init__()
        self.tableWidget = tableWidget
        self.row = row

    def undo(self):
        self.tableWidget.removeRow(self.row)

    def redo(self):
        self.tableWidget.insertRow(self.row)


class RemoveRowsCommand(QUndoCommand):

    def __init__(self, tableWidget, row, count):
        super().__init__()
        self.tableWidget = tableWidget
        self.row = row
        self.end_row = row + count
        self.count = count
        self.deleted_rows = []

    def undo(self):
        self.tableWidget.model().insertRows(self.row, self.count)
        for row_no in range(self.row, self.end_row):
            for col_no in range(self.tableWidget.columnCount()):
                item = self.deleted_rows[row_no-self.start_row][col_no]
                self.tableWidget.setItem(row_no, col_no, QTableWidgetItem(item))

    def redo(self):
        for row_no in range(self.row, self.end_row):
            row = []
            for col_no in range(self.tableWidget.columnCount()):
                row.append(self.tableWidget.item(row_no, col_no).text())
            self.deleted_rows.append(row)
        self.tableWidget.model().removeRows(self.row, self.count)


class DuplicateRowCommand(QUndoCommand):

    def __init__(self, tableWidget, row):
        super().__init__()
        if row == tableWidget.rowCount():
            row -= 1
        self.tableWidget = tableWidget
        self.row = row

    def undo(self):
        self.tableWidget.removeRow(self.row)

    def redo(self):
        self.tableWidget.insertRow(self.row+1)
        for col_no in range(self.tableWidget.columnCount()):
            to_duplicate = self.tableWidget.item(self.row, col_no).text()
            self.tableWidget.setItem(self.row+1, col_no, QTableWidgetItem(to_duplicate))