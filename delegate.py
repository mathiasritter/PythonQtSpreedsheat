from PySide.QtGui import QStyledItemDelegate, QLineEdit

from tablemodel.command import EditCommand


class ItemDelegate(QStyledItemDelegate):

    def __init__(self, control):
        super().__init__()
        self.control = control
        self.edit = None

    def setModelData(self, editor, model, index):
        self.edit.new_value = editor.text()
        self.control.push_with_text(self.edit, "Edit Cell")

    def createEditor(self, parent, option, index):
        return QLineEdit(parent)

    def editorEvent(self, event, model, option, index):
        self.edit = EditCommand(model, index)
        return False
