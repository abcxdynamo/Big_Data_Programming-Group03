# server info
from init import data_init

SERVER_PORT = 5001
REGISTER_SERVER_NAME = "performa"

SECRET_KEY = "ABCX_PERFORMA"

DB_HOST = '34.130.133.219'
DB_PORT = 3306
DB_USER = 'performa'
DB_PASSWORD = 'QWER1234'
DB_NAME = 'performa'
DB_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'

# DB_HOST = '34.130.150.27'
# DB_PORT = 1433
# DB_USER = 'sqlserver'
# DB_PASSWORD = 'nnEZ+}pGg+nSXz6@'
# DB_NAME = 'performa'
# DB_URI = f'mssql+pyodbc://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=no'

SQLALCHEMY_TRACK_MODIFICATIONS = True

# don't submit next line when set to True
FIRST_RUN = False


def init_database(_app):
    data_init.init_database(_app)
    pass