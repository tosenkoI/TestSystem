import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase
import settings as st

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName(st.db_params['host'])
        db.setPort(st.db_params['port'])
        db.setDatabaseName(st.db_params['dbname'])
        db.setUserName(st.db_params['user'])
        db.setPassword(st.db_params['password'])
        ok = db.open()
        if ok:
            print('Connected to database', file=sys.stderr)
        else:
            print('Connection FAILED', db.lastError().text(), file=sys.stderr)
# для Windows надо дополнить переменную окружения PATH
# добавить путь к интерпретатору питона
# добавить пути к директориям с драйверами для qt от postgres
# c:\путь к установленной postgres\lib
# c:\путь к установленной postgres\bin
# путь к установленной postgres например 'Program Files\PostgreSQL\16'