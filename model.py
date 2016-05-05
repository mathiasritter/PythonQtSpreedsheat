from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex


class Model(QAbstractTableModel):

    def __init__(self, parent):

        super().__init__(parent)
        self.header = []
        self.data_list = []

    def set_model_data(self, header, data_list):
        self.beginInsertRows(QModelIndex(), 0, len(data_list)-1)
        self.beginInsertColumns(QModelIndex(), 0, len(header)-1)

        self.header = header
        self.data_list = data_list

        self.endInsertColumns()
        self.endInsertRows()

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

    def flags(self, *args, **kwargs):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, *args, **kwargs):
        return len(self.data_list)

    def columnCount(self, *args, **kwargs):
        return len(self.header)