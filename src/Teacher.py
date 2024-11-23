from PyQt5.QtWidgets import (
    QTableView, QMessageBox, QDialog,
    QLabel, QPushButton, QTextEdit, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtCore import pyqtSlot, reset


class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        sql = '''
            select id_teacher, fio, phone, email, comnt
                from teachers;
        '''
        self.setQuery(sql)

class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)

    @pyqtSlot()
    def add(self):
        #QMessageBox.information(self, 'Учитель', 'Добавление')
        dialog = Dialog(self)
        dialog.exec()

    @pyqtSlot()
    def update(self):
        QMessageBox.information(self, 'Учитель', 'Редактирование')

    @pyqtSlot()
    def delete(self):
        QMessageBox.information(self, 'Учитель', 'Удаление')

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        else:
            return result

    @property
    def phone(self):
        result = self.__phone_edit.text().strip()
        if result == '':
            return None
        else:
            return result

    @property
    def email(self):
        result = self.__email_edit.text().strip()
        if result == '':
            return None
        else:
            return result

    @property
    def comnt(self):
        result = self.__comnt_edit.toPlainText().strip()
        if result == '':
            return None
        else:
            return result
