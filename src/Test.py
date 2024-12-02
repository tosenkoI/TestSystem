from PyQt5.QtWidgets import (
    QTableView, QMessageBox, QComboBox,
    QDialog, QHBoxLayout, QVBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton,
    QStyledItemDelegate
)
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import Qt, pyqtSlot


class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.refresh()
        self.__authors = {} #it works until fio unique
        self.selectAuthors()

    @property
    def author_id(self, fio):
        return self.__authors[fio]

    def refresh(self):
        sql = '''
            select t.id_test, t.tname, t.tcontent, a.fio from tests as t, teachers as a
                where t.teacher_id = a.id_teacher ;
        '''
        self.setQuery(sql)

    def add(self, tname, tcontent, teacher):
        add_query = QSqlQuery()
        teacher_id = self.author_id(teacher)
        INSERT = '''
            insert into tests ( tname, tcontent, teacher_id )
            values ( :tname, :tcontent, :teacher_id)
        '''
        add_query.prepare(INSERT)
        add_query.bindValue(':tname', tname)
        add_query.bindValue('tcontent', tcontent)
        add_query.bindValue('teacher_id', teacher_id)
        add_query.exec_()
        self.refresh()

    def select_one(self, id_test):
        one_query = QSqlQuery()
        SELECT_ONE = '''
            select tname, tcontent, teacher_id
            from tests
            where id_test = :id_test ;
        '''
        one_query.prepare(SELECT_ONE)
        one_query.bindValue(':id_test', id_test)
        one_query.exec_()
        #TODO

    def update(self, tname, tcontent, teacher, id_test):
        upd_query = QSqlQuery()
        teacher_id = self.author_id(teacher)
        UPDATE = '''
            update tests set 
                tname = :tname, 
                tcontent = :tcontent,
                teacher_id = :teacher_id
            where id_test = :id_test ;
        '''
        upd_query.prepare(UPDATE)
        upd_query.bindValue(':tname', tname)
        upd_query.bindValue(':tcontent', tcontent)
        upd_query.bindValue(':teacher_id', teacher_id)
        upd_query.bindValue(':id_test', id_test)
        upd_query.exec_()
        self.refresh()

    def delete(self, id_test):
        del_query = QSqlQuery()
        DELETE = '''
            delete from tests where id_test = :id_test ;
        '''
        del_query.prepare(DELETE)
        del_query.bindValue(':id_test', id_test)
        del_query.exec_()
        self.refresh()

    def selectAuthors(self):
        sel_query = QSqlQuery()
        SELECT = '''
            select id_teacher, fio
                from teachers ;
        '''
        sel_query.exec_(SELECT)
        if sel_query.isActive():
            sel_query.first()
            while sel_query.isValid():
                self.__authors[sel_query.value('fio')] = sel_query.value('id_teacher')
                sel_query.next()
            print(self.__authors)

class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        model = Model(parent=self)
        self.setModel(model)
        model.setHeaderData(1, Qt.Horizontal, "Название")
        model.setHeaderData(2, Qt.Horizontal, "Содержание")
        model.setHeaderData(3, Qt.Horizontal, "Автор")
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        #self.hideColumn(0)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(2, hh.Stretch)
        self.selectAuthors()
        self.setItemDelegateForColumn(3, ComboBoxDelegate(parent=self))

    def add(self):
        #self.model().insertRow(self.model().rowCount())
        dialog = Dialog(self)
        if dialog.exec():
            rec = self.conn.record('tests')
            rec.setValue('id_test', self.model().rowCount())
            rec.setValue('tname', dialog.tname)
            rec.setValue('tcontent', dialog.tcontent)
            rec.setValue('teacher_id', None if dialog.teacher == "" else self.__authors[dialog.teacher])
            print(rec.value(0), rec.value(1), rec.value(2), rec.value(3))
            print(self.model().insertRecord(-1, rec), self.model().lastError().text())
            self.model().select()

    def delete(self):
        ans = QMessageBox.question(self, 'Задача', 'Вы уверены?')
        if ans == QMessageBox.Yes:
            self.model().removeRow(self.currentIndex().row())
            self.model().select()


    @property
    def authors(self):
        return self.__authors.keys()

class ComboBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QComboBox(parent)
        editor.setFrame(False)
        editor.addItems(View(parent).authors)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setCurrentIndex(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentIndex()
        model.setData(index, value, Qt.EditRole)

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Задача')

        tname_lbl = QLabel('&Название', parent=self)
        self.__tname_edit = QLineEdit(parent=self)
        tname_lbl.setBuddy(self.__tname_edit)

        tcontent_lbl = QLabel('&Содержание', parent=self)
        self.__tcontent_edit = QTextEdit(parent=self)
        tcontent_lbl.setBuddy(self.__tcontent_edit)

        teacher_lbl = QLabel('&Автор', parent=self)
        self.__teacher_cmb = QComboBox(parent=self)
        teacher_lbl.setBuddy(self.__teacher_cmb)
        self.__teacher_cmb.addItem("")#field teacher_id in table tests is null
        self.__teacher_cmb.addItems(parent.authors)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)
        lay.addWidget(tname_lbl)
        lay.addWidget(self.__tname_edit)
        lay.addWidget(tcontent_lbl)
        lay.addWidget(self.__tcontent_edit)
        lay.addWidget(teacher_lbl)
        lay.addWidget(self.__teacher_cmb)

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
        if self.tcontent is None:
            return
        self.accept()

    @property
    def tname(self):
        result = self.__tname_edit.text().strip()
        if result == '':
            return None
        return result

    @property
    def tcontent(self):
        result = self.__tcontent_edit.toPlainText().strip()
        if result == '':
            return None
        return result

    @property
    def teacher(self):
        return self.__teacher_cmb.currentText()


