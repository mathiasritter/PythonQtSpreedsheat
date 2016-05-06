import sys

from PySide.QtCore import Qt
from PySide.QtGui import QMainWindow, QApplication, QFileDialog, QTableWidgetItem

from tablewidget.csvio import CSV
from tablewidget.view import Ui_MainWindow


class Control(QMainWindow):

    def __init__(self):
        super().__init__()

        self.file_name = None

        self.view = Ui_MainWindow()
        self.view.setupUi(self)

        self.connect_elements()

    def connect_elements(self):
        self.view.actionOpen.triggered.connect(self.open)

    def open(self):
        file_name = QFileDialog.getOpenFileName(self, caption="Open CSV File", filter="CSV-File (*.csv)")[0]
        if file_name:
            self.file_name = file_name
            header, data_list = CSV.read(file_name)

            #self.view.tableWidget.setColumnCount(3)
            #self.view.tableWidget.setRowCount(5)
            self.view.tableWidget.setHorizontalHeaderLabels(header)

            for row_index, row in enumerate(data_list):
                self.view.tableWidget.insertRow(1)
                for col_index, column in enumerate(row):
                    item = QTableWidgetItem(column)
                    self.view.tableWidget.setItem(row_index, col_index, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    control = Control()
    control.show()
    control.raise_()
    sys.exit(app.exec_())
