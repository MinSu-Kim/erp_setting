from util.read_config import read_db_config


class Config:
    environ = read_db_config(filename='resources/db_properties.ini')
    # print(environ)
    # Database config
    db_user = environ.get('user')
    db_password = environ.get('password')
    db_host = environ.get('host')
    db_port = environ.get('port')
    db_name = environ.get('database')