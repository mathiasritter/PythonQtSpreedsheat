from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex


class Model(QAbstractTableModel):

    def __init__(self, parent):

        super().__init__(parent)
        self.header = []
        self.data_list = []

    def set_model_data(self, header, data_list):
        self.beginResetModel()
        self.reset()
        self.header = header
        self.data_list = data_list
        self.endResetModel()

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row+count-1)
        for i in range(count):
            self.data_list.insert(row, self.columnCount() * [None])
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row+count-1)
        del self.data_list[row:row+count]
        self.endRemoveRows()
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
        else:
            return None

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return self.data_list[index.row()][index.column()]
        else:
            return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.beginResetModel()
            self.data_list[index.row()][index.column()] = value
            self.endResetModel()
            return True
        else:
            return False

    def duplicateRow(self, row, parent=QModelIndex()):
        if row == self.rowCount():
            row -= 1
        self.beginInsertRows(parent, row, row)
        to_duplicate = self.data_list[row].copy()
        self.data_list.insert(row, to_duplicate)
        self.endInsertRows()
        return True

    def flags(self, *args, **kwargs):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, *args, **kwargs):
        return len(self.data_list)

    def columnCount(self, *args, **kwargs):
        return len(self.header)