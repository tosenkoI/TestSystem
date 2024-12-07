from PyQt5.QtWidgets import (
    QTableView, QMessageBox
)
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtCore import pyqtSlot, Qt


class Model(QSqlRelationalTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable('variants')
        self.setSort(1, Qt.AscendingOrder)
        # id_variant title teacher_id
        self.setRelation(3, QSqlRelation('teachers', 'id_teacher', 'fio'))
        self.select()

    def flags(self, index):
        if (index.column() == 2):
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вариант")
        model = Model(parent=self)
        self.setModel(model)
        self.setItemDelegateForColumn(3, QSqlRelationalDelegate(model))
        model.setHeaderData(1, Qt.Horizontal, "Заголовок")
        model.setHeaderData(2, Qt.Horizontal, "Создан")
        model.setHeaderData(3, Qt.Horizontal, "Автор")
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        #hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(hh.Stretch)

    @pyqtSlot()
    def add(self):
        self.model().insertRow(self.model().rowCount())

    @pyqtSlot()
    def delete(self):
        ans = QMessageBox.question(self, 'Вариант', 'Вы уверены?')
        if ans == QMessageBox.Yes:
            self.model().removeRow(self.currentIndex().row())
            self.model().select()