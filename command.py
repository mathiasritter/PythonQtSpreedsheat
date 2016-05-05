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