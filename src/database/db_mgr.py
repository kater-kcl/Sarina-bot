# 引入数据库
import mysql.connector
import config.db_config as db_config


class DatabaseManager:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.cnx = None
        self.cursor = None

    def connect(self):
        self.cnx = mysql.connector.connect(user=self.user, password=self.password,
                                           host=self.host, database=self.database,
                                           port=self.port, charset='utf8mb4',
                                           collation='utf8mb4_unicode_ci')  # specify collation here
        self.cursor = self.cnx.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()

    def execute_query(self, query, params=None):
        self.connect()
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        self.close()
        return result

    def execute_update(self, query, params=None):
        self.connect()
        self.cursor.execute(query, params)
        self.cnx.commit()
        self.close()


db_mgr: DatabaseManager = None


def init_database():
    global db_mgr
    db_mgr = DatabaseManager(db_config.sql_host, db_config.sql_port, db_config.sql_user, db_config.sql_pass,
                             db_config.sql_database)
