import json
from typing import Callable
import adventure_module.adventure_api as adv_api
from utils.message_builder import group_message, make_forward_message


def init_adv():
    adv_api.init_adv()


def solve_adv(call_back: Callable[[str], str], message: str, user_id: str, group_id: int):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    if command == "list":
        return show_adv_list(call_back, user_id, group_id)
    elif command == "info":
        return show_adv_info(call_back, user_id, group_id, args)
    elif command == "start":
        return start_adv(call_back, user_id, group_id, args)
    elif command == "progress":
        return get_adv_progress(call_back, user_id, group_id)
    else:
        result = "[CQ:at,qq={0}] 未知命令".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))


def show_adv_list(call_back: Callable[[str], str], user_id: str, group_id: int):
    adv_list = adv_api.get_level_list()
    result = "{}".format(adv_list)
    ret = group_message(group_id, result)
    call_back(json.dumps(ret))


def show_adv_info(call_back: Callable[[str], str], user_id: str, group_id: int, args: str):
    adv_info = adv_api.get_level_info(args)
    result = "{}".format(adv_info)
    ret = group_message(group_id, result)
    call_back(json.dumps(ret))


def start_adv(call_back: Callable[[str], str], user_id: str, group_id: int, level_id: str):
    print(user_id,type(user_id))
    if level_id == 'test' and user_id != '2276363693':
        result = "关卡仅限管理员测试使用".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    result = adv_api.start_adv(user_id, level_id)
    result = "[CQ:at,qq={0}]".format(user_id) + result
    ret = group_message(group_id, result)
    if result is not None:
        call_back(json.dumps(ret))


def get_adv_progress(call_back: Callable[[str], str], user_id: str, group_id: int):
    result = adv_api.get_adv_progress(user_id)
    result = make_forward_message(result)
    ret = group_message(group_id, result)
    call_back(json.dumps(ret))
