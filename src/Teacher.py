from PyQt5.QtWidgets import (
    QTableView, QMessageBox, QDialog,
    QLabel, QPushButton, QTextEdit, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import pyqtSlot, Qt

class Model(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable('teachers')
        self.select()

    def add_rec(self, rec, fio, phone, email, comnt):
        rec.setValue('id_teacher', self.rowCount())
        rec.setValue('fio', fio)
        rec.setValue('phone', phone)
        rec.setValue('email', email)
        rec.setValue('comnt', comnt)
        print(rec.value(0), rec.value(1), rec.value(2), rec.value(3), rec.value(4))
        ok = self.insertRecord(-1, rec)
        print(ok, self.lastError().text())
        self.select()

class View(QTableView):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.conn = conn
        model = Model(parent=self)
        self.setModel(model)
        model.setHeaderData(1, Qt.Horizontal, "ФИО")
        model.setHeaderData(2, Qt.Horizontal, "Телефон")
        model.setHeaderData(3, Qt.Horizontal, "Почта")
        model.setHeaderData(4, Qt.Horizontal, "Коментарий")
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        self.setWordWrap(False)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(4, hh.Stretch)

    @pyqtSlot()
    def add(self):
        #self.model().insertRow(self.model().rowCount())
        dialog = Dialog(self)
        if dialog.exec():
            self.model().add_rec(self.conn.record('teachers'),
                                 dialog.fio, dialog.phone, dialog.email, dialog.comnt)


    @pyqtSlot()
    def delete(self):
        ans = QMessageBox.question(self, 'Учитель', 'Вы уверены?')
        if ans == QMessageBox.Yes:
            self.model().removeRow(self.currentIndex().row())
            self.model().select()


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Учитель')

        fio_lbl = QLabel('&Фамилия И. О.', parent=self)
        self.__fio_edit = QLineEdit(parent=self)
        fio_lbl.setBuddy(self.__fio_edit)

        phone_lbl = QLabel('&Телефон', parent=self)
        self.__phone_edit = QLineEdit(parent=self)
        phone_lbl.setBuddy(self.__phone_edit)

        email_lbl = QLabel('&e-mail', parent=self)
        self.__email_edit = QLineEdit(parent=self)
        email_lbl.setBuddy(self.__email_edit)

        comnt_lbl = QLabel('&Примечание', parent=self)
        self.__comnt_edit = QTextEdit(parent=self)
        comnt_lbl.setBuddy(self.__comnt_edit)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)
        lay.addWidget(fio_lbl)
        lay.addWidget(self.__fio_edit)
        lay.addWidget(phone_lbl)
        lay.addWidget(self.__phone_edit)
        lay.addWidget(email_lbl)
        lay.addWidget(self.__email_edit)
        lay.addWidget(comnt_lbl)
        lay.addWidget(self.__comnt_edit)

        hlay = QHBoxLayout()
        hlay.addStretch()
        hlay.addWidget(ok_btn)
        hlay.addWidget(cancel_btn)
        lay.addLayout(hlay)
        self.setLayout(lay)

        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.finish)

    @pyqtSlot()
    def finish(self):
        if self.fio is None:
            return
        self.accept()

    @property
    def fio(self):
        result = self.__fio_edit.text().strip()
        if result == '':
            return None
        return result

    @property
    def phone(self):
        result = self.__phone_edit.text().strip()
        if result == '':
            return None
        return result

    @property
    def email(self):
        result = self.__email_edit.text().strip()
        if result == '':
            return None
        return result

    @property
    def comnt(self):
        result = self.__comnt_edit.toPlainText().strip()
        if result == '':
            return None
        return result
