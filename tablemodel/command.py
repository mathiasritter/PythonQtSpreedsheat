from PySide.QtGui import QUndoCommand

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


class InsertRowsCommand(QUndoCommand):

    def __init__(self, model, row, count):
        super().__init__()
        self.model = model
        self.row = row
        self.count = count

    def undo(self):
        self.model.removeRows(self.row, self.count)

    def redo(self):
        self.model.insertRows(self.row, self.count)


class RemoveRowsCommand(QUndoCommand):

    def __init__(self, model, row, count):
        super().__init__()
        self.model = model
        self.row = row
        self.count = count
        self.old_list = None
        self.old_header = None

    def undo(self):
        self.model.set_model_data(self.old_header, self.old_list)

    def redo(self):
        self.old_header = list(self.model.header)
        self.old_list = list(self.model.data_list)
        self.model.removeRows(self.row, self.count)


class DuplicateRowCommand(QUndoCommand):

    def __init__(self, model, row):
        super().__init__()
        self.model = model
        self.row = row

    def undo(self):
        self.model.removeRows(self.row, 1)

    def redo(self):
        self.model.duplicateRow(self.row)