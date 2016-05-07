from PySide.QtGui import QStyledItemDelegate, QLineEdit

from tablemodel.command import EditCommand


class ItemDelegate(QStyledItemDelegate):

    def __init__(self, undo_stack):
        super().__init__()
        self.undo_stack = undo_stack
        self.edit = None

    def setModelData(self, editor, model, index):
        self.edit.new_value = editor.text()
        self.undo_stack.push(self.edit)

    def createEditor(self, parent, option, index):
        return QLineEdit(parent)

    def editorEvent(self, event, model, option, index):
        self.edit = EditCommand(model, index)
        return False
