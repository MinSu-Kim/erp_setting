import pymysql

from connection.config import Config
from util.singleton_instance import SingleTonInstance


class Database(SingleTonInstance):

    def __init__(self):
        self.conn = None
        config = Config()
        try:
            if self.conn is None:
                self.conn = pymysql.connect(config.db_host,
                                     user=config.db_user,
                                     passwd=config.db_password,
                                     db=config.db_name,
                                     connect_timeout=5)
            print('Connection opened Success.')
        except pymysql.MySQLError as e:
            print('Connection opened fail.')
            raise e

    def __enter__(self):
        print('__enter__()')
        if self.conn is None:
            self.__init__()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')
        self.conn.close()
        self.conn = None