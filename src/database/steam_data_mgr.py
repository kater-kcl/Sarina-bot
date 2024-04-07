import database.db_mgr as DB


def get_steam_user_by_qid(user_id):
    query = "SELECT * FROM steam_users WHERE user_id = %s"
    result = DB.db_mgr.execute_query(query, (user_id,))
    return result


def get_steam_user_by_steam_id(steam_id):
    query = "SELECT * FROM steam_users WHERE steam_id = %s"
    result = DB.db_mgr.execute_query(query, (steam_id,))
    return result


def add_steam_user(user_id, steam_id, nick_name):
    query = "INSERT INTO steam_users (user_id, steam_id, nick_name) VALUES (%s, %s, %s)"
    DB.db_mgr.execute_update(query, (user_id, steam_id, nick_name))
    pass


def bind_steam_id(user_id, steam_id, nick_name):
    if get_steam_user_by_qid(user_id):
        query = "UPDATE steam_users SET steam_id = %s, nick_name = %s WHERE user_id = %s"
        DB.db_mgr.execute_update(query, (steam_id, nick_name, user_id))
    else:
        add_steam_user(user_id, steam_id, nick_name)
    pass


def get_all_steam_users():
    query = "SELECT * FROM steam_users"
    result = DB.db_mgr.execute_query(query)
    return result
