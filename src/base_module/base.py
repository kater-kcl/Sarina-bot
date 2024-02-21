import json
import random
from typing import Callable
from utils.message_builder import group_message


def solve_base(call_back: Callable[[str], str], message: str, user_id: int, group_id: int):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    if command == "sign":
        return sign_in(call_back, user_id, group_id)
    else:
        result = "[CQ:at,qq={0}] 未知命令".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))


def sign_in(call_back: Callable[[str], str], user_id: int, group_id: int):
    coins = random.randint(150, 200)
    result = "[CQ:at,qq={0}]签到成功，获得了{1}个星乐币".format(user_id, coins)
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))
