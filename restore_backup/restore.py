import csv
import glob
import os

import mysql
from mysql.connector import Error

from connection.pysql_con import Database
from util.singleton_instance import SingleTonInstance


class Restore(SingleTonInstance):

    def restore(self):
        backup_dir = 'backup'

        if os.path.exists(backup_dir):
            backup_list={}
            for filename in [file for file in glob.glob(backup_dir+'/*') if file.endswith(".txt")]:
                if os.path.basename(filename[:-4]) == 'employee':
                    tuples = [tuple(row)[:-1] for row in csv.reader(open(filename, 'r', encoding='utf8'))]
                else:
                    tuples = [tuple(row) for row in csv.reader(open(filename, 'r', encoding='utf8'))]
                backup_list[os.path.basename(filename[:-4])] = tuples
            self.__restore_data(backup_list)

        else:
            raise Exception("backup dir is not exists")

    def __restore_data(self, backup_list):
        dict_sql = {
            'title': 'insert into title values (%s, %s)',
            'department': 'insert into department values (%s, %s, %s)',
            'employee': 'insert into employee(emp_no, emp_name, title, manager, salary, dept, pass, hire_date, '
                        'gender) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        }
        with Database.instance() as con:
            with con.cursor() as cursor:
                cursor.execute('use pyqt_erp_proj')
                cursor.execute('SET foreign_key_checks = false')
                for table in ['title', 'department', 'employee']:
                    # print(dict_sql[table], ' : ', backup_list[table])
                    cursor.executemany(dict_sql[table], backup_list[table])
                    print('{} table restore OK!'.format(table))
                cursor.execute('SET foreign_key_checks = true')
                self.__load_img(con=con)
                print("load Ok")

    def __load_img(self, con=None, data_dir='backup/img', query='update employee set pic=%s where emp_no=%s'):
        if os.path.exists(data_dir):
            for f in os.scandir(data_dir):
                data = self.__read_image(os.path.abspath(f))
                img_file = os.path.basename(f).split('.')[0]
                try:
                    cursor = con.cursor()
                    cursor.execute(query, (data, img_file))
                    con.commit()
                except mysql.connector.Error as err:
                    raise err
                finally:
                    cursor.close()

    def __read_image(self, filename):
        with open(filename, 'rb') as f:
            photo = f.read()
        return photo
