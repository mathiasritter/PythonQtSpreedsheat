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
            self.data_list.insert(row, {key: "" for key in self.header})
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row+count-1)
        del self.data_list[row:row+count]
        self.endRemoveRows()
        return True

    def insertColumns(self, column, count, parent=QModelIndex()):
        self.beginInsertColumns(parent, column, column+count-1)

        for i in range(count):
            column_count = len(self.header)
            self.header.insert(column, column_count)
            for row in self.data_list:
                row[column_count] = ""
        self.endInsertColumns()

    def removeColumns(self, column, count, parent=QModelIndex()):
        self.beginRemoveColumns(parent, column, column+count-1)
        to_remove = self.header[column:column+count]
        del self.header[column:column+count]
        for row in self.data_list:
            for remove in to_remove:
                del row[remove]
        self.endRemoveColumns()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
        else:
            return None

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return self.data_list[index.row()][self.header[index.column()]]
        else:
            return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.data_list[index.row()][self.header[index.column()]] = value
            return True
        else:
            return False

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        old = self.header[section]
        self.header[section] = value
        for row in self.data_list:
            row[value] = row[old]
            del row[old]
        return True

    def flags(self, *args, **kwargs):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, *args, **kwargs):
        return len(self.data_list)

    def columnCount(self, *args, **kwargs):
        return len(self.header)