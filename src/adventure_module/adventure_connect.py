import json
from typing import Callable

from flask import current_app

import adventure_module.adventure_api as adv_api
from utils.message_builder import group_message, make_forward_message, forward_message


def init_adv():
    adv_api.init_adv()


def solve_adv(call_back: Callable[[str], str], message: str, user_id: str, group_id: int, res_listener):
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
        return get_adv_progress(call_back, user_id, group_id, res_listener)
    elif command == "finish":
        return finish_adv(call_back, user_id, group_id, res_listener)
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
    print(user_id)
    print(type(user_id))
    # if level_id == 'test' and user_id != '2276363693':
    #     result = "关卡仅限管理员测试使用".format(user_id)
    #     ret = group_message(group_id, result)
    #     return call_back(json.dumps(ret))
    result = adv_api.start_adv(user_id, level_id)
    if result is None:
        result = "[CQ:at,qq={0}] 你已经在冒险中了".format(user_id)
    else:
        result = "[CQ:at,qq={0}]".format(user_id) + result
    ret = group_message(group_id, result)
    if result is not None:
        call_back(json.dumps(ret))


def get_adv_progress(call_back: Callable[[str], str], user_id: str, group_id: int, res_listener: Callable[[str], str]):
    result = adv_api.get_adv_progress(user_id)
    if result is None:
        result = "[CQ:at,qq={0}] 你没有在冒险中".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    # result = make_forward_message(call_back, [result], res_listener)
    # result = forward_message(result)
    ret = group_message(group_id, result)
    # print(ret)
    # print(json.dumps(ret))
    call_back(json.dumps(ret))


def finish_adv(call_back: Callable[[str], str], user_id: str, group_id: int, res_listener: Callable[[str], str]):
    current_app.logger.info("in_finish_adv")
    result = adv_api.finish_adv(user_id)
    current_app.logger.info(result)
    if result is None:
        result = "[CQ:at,qq={0}] 你没有在冒险中".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    # result = make_forward_message(call_back, [result], res_listener)
    # result = forward_message(result)
    ret = group_message(group_id, result)
    # print(ret)
    # print(json.dumps(ret))
    call_back(json.dumps(ret))

# if __name__ == "__main__":
#     adv_api.init_items("./")
#     adv_api.init_levels("./")
#     print(adv_api.get_level_list())
#     print(adv_api.get_level_info("1-1"))
#     print(adv_api.start_adv("123", "1-1"))
#     get_adv_progress(print, 123456789,1)
