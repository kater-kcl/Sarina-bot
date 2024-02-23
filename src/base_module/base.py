import datetime
import json
import random
from typing import Callable

import utils.db_mgr as db
from utils.message_builder import group_message


def solve_base(call_back: Callable[[str], str], message: str, user_id: str, group_id: int):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    if command == "sign":
        return sign_in(call_back, user_id, group_id)
    elif command == "coin":
        return get_coins(call_back, user_id, group_id)
    else:
        result = "[CQ:at,qq={0}] 未知命令".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))


def sign_in(call_back: Callable[[str], str], user_id: str, group_id: int):
    last_sign: datetime.datetime = db.get_user_last_sign(user_id)
    if last_sign.date() == datetime.date.today():
        result = "[CQ:at,qq={0}] 今天已经签到过了".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    coins = random.randint(150, 200)
    result = "[CQ:at,qq={0}] 签到成功，获得了{1}个星乐币".format(user_id, coins)
    db.add_user_coins(user_id, coins)
    db.refresh_user_last_sign(user_id)
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))


def get_coins(call_back, user_id, group_id):
    coins = db.get_user_coins(user_id)
    result = "[CQ:at,qq={0}] 你有{1}个星乐币".format(user_id, coins)
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))
