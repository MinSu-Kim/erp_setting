import csv
import imghdr
import os

from pymysql import Error

from connection.pysql_con import Database
from util.read_config import read_db_config
from util.singleton_instance import SingleTonInstance


class Backup(SingleTonInstance):

    def backup_data(self, backup_data_dir='backup', sql_file='resources/backup_sql.ini'):
        self.__check_exists_dir(backup_data_dir)
        sql_info = read_db_config(sql_file)

        with Database.instance() as con:
            with con.cursor() as cursor:
                cursor.execute('use pyqt_erp_proj')
                for table_name, table_sql in sql_info.items():
                    self.__backup_query(backup_data_dir, table_sql, table_name, con)
                    print('backup file {}.txt OK'.format(table_name))
        print("OK")

    def __backup_query(self, data_dir, select_sql, table_name, con):
        try:
            file_name = "{}/{}.txt".format(data_dir, table_name)
            with con.cursor() as cursor:
                cursor.execute(select_sql)
                rows = cursor.fetchall()
                with open(file_name, 'w', newline='\n', encoding='utf-8') as tuple_fp:
                    for row in rows:
                        img_path = data_dir + '/img'
                        if not os.path.exists(img_path):
                            os.mkdir(img_path)
                        filename = "{}/{}".format(img_path, row[0])
                        row_item = []
                        for item in row:
                            if isinstance(item, bytes) or isinstance(item, bytearray):
                                img_path = self.__write_file(item, filename)
                                print('picture backup {} OK'.format(filename))
                                row_item.append(img_path)
                                continue
                            if item is None:
                                row_item.append('null')
                                continue
                            row_item.append(item)
                        csv.writer(tuple_fp).writerow(row_item)
        except Error as e:
            raise e

    def __check_exists_dir(self, data_dir):
        if os.path.exists(data_dir):
            for f in os.scandir(data_dir):
                if os.path.isdir(f):
                    for sub_f in os.scandir(f):
                        os.remove(sub_f.path)
                    os.rmdir(f)
                else:
                    os.remove(f.path)
            os.rmdir(data_dir)
            print('rmdir {} OK!'.format(data_dir))
        os.mkdir(data_dir)
        print('mkdir {} OK!'.format(data_dir))

    def __write_file(self, data, filename):
        with open(filename, 'wb') as f:
            f.write(data)
        file_ext = imghdr.what(filename)
        os.rename(filename, filename + '.' + file_ext)
        return str(filename + '.' + file_ext)
