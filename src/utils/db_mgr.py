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
                                           port=self.port, charset='utf8')
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


def user_exists_decorator(func):
    def wrapper(user_id, *args, **kwargs):
        user_exists = check_user_exists(user_id)
        if not user_exists:
            add_user(user_id)
        return func(user_id, *args, **kwargs)

    return wrapper


def init_database():
    global db_mgr
    db_mgr = DatabaseManager(db_config.sql_host, db_config.sql_port, db_config.sql_user, db_config.sql_pass, db_config.sql_database)


def check_user_exists(user_id):
    query = "SELECT * FROM user_info WHERE uid = %s"
    result = db_mgr.execute_query(query, (user_id,))
    return len(result) > 0


def add_user(user_id):
    query = "INSERT INTO user_info (uid, last_sign) VALUES (%s, %s)"
    default_time = "2000-01-01 00:00:00"
    db_mgr.execute_update(query, (user_id, default_time))


@user_exists_decorator
def get_user_coins(user_id: str):
    query = "SELECT coins FROM user_info WHERE uid = %s"
    result = db_mgr.execute_query(query, (user_id,))
    if result:
        return result[0][0]
    else:
        return 0


@user_exists_decorator
def get_user_last_sign(user_id: str):
    query = "SELECT last_sign FROM user_info WHERE uid = %s"
    result = db_mgr.execute_query(query, (user_id,))
    if result:
        return result[0][0]
    else:
        return 0


@user_exists_decorator
def refresh_user_last_sign(user_id: str):
    query = "UPDATE user_info SET last_sign = NOW() WHERE uid = %s"
    db_mgr.execute_update(query, (user_id,))


@user_exists_decorator
def add_user_coins(user_id: str, coins: int):
    query = "UPDATE user_info SET coins = coins + %s WHERE uid = %s"
    db_mgr.execute_update(query, (coins, user_id))

# init_database()

# if __name__ == '__main__':
#     db_config.init_config()
#     init_database()
#     add_user_coins(123456, 100)
#     print(get_user_coins(123456))
