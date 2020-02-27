import pymysql
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from pymysql import Error

from connection.pysql_con import Database
from database_init.db_init import DbInit
from restore_backup.backup import Backup
from restore_backup.restore import Restore


class ErpSetting(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('ui/erp_setting.ui', self) # ,self를 생략하면 pyqtslot()연결안됨

    @pyqtSlot()
    def exec_init(self):
        print('exec_init')
        DbInit.instance().init()

    @pyqtSlot()
    def exec_load(self):
        print('exec_load')
        try:
            Restore.instance().restore()
        except Exception as err:
            print(err)

    @pyqtSlot()
    def exec_backup(self):
        print('exec_backup')
        Backup.instance().backup_data()


if __name__ == '__main__':
    app = QApplication([])
    w = ErpSetting()
    w.show()
    app.exec()




    """
    DbInit.instance().init()

    with Database.instance() as conn:
        try:
            query = 'select databases()'
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                print(result)
        except pymysql.MySQLError as e:
            print(e)

    app = QApplication([])
    w = ErpSetting()
    w.show()
    app.exec()

    try:
        db = read_db_config(filename='resources/db_properties.ini')
        print('read_db_config : ', db)
    except Exception as err:
        print("error", err)

    with Database.instance() as conn:
        try:
            query = 'select user(), database()'
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                print(result)
        except pymysql.MySQLError as e:
            print(e)

    with Database.instance() as conn:
        try:
            query = 'select user(), database()'
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                print(result)
        except pymysql.MySQLError as e:
            print(e)
"""