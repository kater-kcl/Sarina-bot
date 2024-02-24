import json

from database.db_mgr import db_mgr


def adv_save_exists_decorator(func):
    def wrapper(user_id, *args, **kwargs):
        user_exists = check_adv_save_exists(user_id)
        if not user_exists:
            add_adv_save(user_id)
        return func(user_id, *args, **kwargs)

    return wrapper


def check_adv_save_exists(user_id):
    query = "SELECT * FROM adv_save WHERE uid = %s"
    result = db_mgr.execute_query(query, (user_id,))
    return len(result) > 0


def add_adv_save(user_id):
    query = "INSERT INTO adv_save (uid, save_json) VALUES (%s, %s)"
    data = {}
    # read json from ../resources/adventure_module/saves/default.json
    with open('../resource/adventure_module/saves/default.json', 'r') as f:
        data = json.load(f)

    db_mgr.execute_update(query, (user_id, json.dumps(data)))


@adv_save_exists_decorator
def get_adv_save(user_id: str):
    query = "SELECT save_json FROM adv_save WHERE uid = %s"
    result = db_mgr.execute_query(query, (user_id,))
    if result:
        return json.loads(result[0][0])
    else:
        return None


@adv_save_exists_decorator
def set_adv_save(user_id: str, save_json: dict):
    query = "UPDATE adv_save SET save_json = %s WHERE uid = %s"
    db_mgr.execute_update(query, (json.dumps(save_json), user_id))


