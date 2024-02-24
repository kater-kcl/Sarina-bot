import database.db_mgr as DB


def user_exists_decorator(func):
    def wrapper(user_id, *args, **kwargs):
        user_exists = check_user_exists(user_id)
        if not user_exists:
            add_user(user_id)
        return func(user_id, *args, **kwargs)

    return wrapper


def check_user_exists(user_id):
    query = "SELECT * FROM user_info WHERE uid = %s"
    result = DB.db_mgr.execute_query(query, (user_id,))
    return len(result) > 0


def add_user(user_id):
    query = "INSERT INTO user_info (uid, last_sign) VALUES (%s, %s)"
    default_time = "2000-01-01 00:00:00"
    DB.db_mgr.execute_update(query, (user_id, default_time))


@user_exists_decorator
def get_user_coins(user_id: str):
    query = "SELECT coins FROM user_info WHERE uid = %s"
    result = DB.db_mgr.execute_query(query, (user_id,))
    if result:
        return result[0][0]
    else:
        return 0


@user_exists_decorator
def get_user_last_sign(user_id: str):
    query = "SELECT last_sign FROM user_info WHERE uid = %s"
    result = DB.db_mgr.execute_query(query, (user_id,))
    if result:
        return result[0][0]
    else:
        return 0


@user_exists_decorator
def refresh_user_last_sign(user_id: str):
    query = "UPDATE user_info SET last_sign = NOW() WHERE uid = %s"
    DB.db_mgr.execute_update(query, (user_id,))


@user_exists_decorator
def add_user_coins(user_id: str, coins: int):
    query = "UPDATE user_info SET coins = coins + %s WHERE uid = %s"
    DB.db_mgr.execute_update(query, (coins, user_id))
