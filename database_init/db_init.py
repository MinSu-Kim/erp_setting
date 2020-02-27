import mysql
import pymysql
from mysql.connector import errorcode
from pymysql.constants import ER

from connection.pysql_con import Database
from util.read_config import read_db_config
from util.singleton_instance import SingleTonInstance


class DbInit(SingleTonInstance):
    def __init__(self, filename='resources/init_sql.ini'):
        self._db = read_db_config(filename)

    def __create_database(self, con):
        with con.cursor() as cursor:
            try:
                cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self._db['database_name']))
                print("CREATE DATABASE {} OK!".format(self._db['database_name']))
            except pymysql.err.ProgrammingError as err:
                if err.args[0] == ER.DB_CREATE_EXISTS:
                    print(err.args)
                    cursor.execute("DROP DATABASE {} ".format(self._db['database_name']))
                    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self._db['database_name']))
                    print("DROP DATABASE and CREATE DATABASE {} OK!".format(self._db['database_name']))
                else:
                    raise err

    def __create_table(self, con):
        with con.cursor() as cursor:
            try:
                cursor.execute("USE {}".format(self._db['database_name']))
                for table_name, table_sql in self._db['sql'].items():
                    cursor.execute(table_sql)
                    print("Creating table {}: OK".format(table_name))
            except pymysql.err.Error as err:
                print(err)#
                if err.args[0] == ER.TABLE_EXISTS_ERROR:
                    raise err
                else:
                    raise err

    def __create_user(self, con):
        with con.cursor() as cursor:
            try:
                print("Creating user: ", end='')
                cursor.execute(self._db['user_drop'])
                cursor.execute(self._db['user_sql'])
                cursor.execute(self._db['user_grant'])
                print("Creating user: OK")
            except pymysql.err.Error as err:
                raise err

    def init(self):
        print("init()-call")
        with Database.instance() as con:
            try:
                self.__create_database(con)
                self.__create_table(con)
                self.__create_user(con)
            except mysql.connector.Error as err:
                print(err)


if __name__ == "__main__":

    db = DbInit(filename='../resources/init_sql.ini')
    # db = DbInit(filename='../resources/db_properties.ini')
    # db.init()

