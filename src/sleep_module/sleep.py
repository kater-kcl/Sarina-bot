import json
import datetime
from typing import Callable, Dict, List

from utils.message_builder import group_message
from utils.onebot_api import get_group_member_info

sleep_list: Dict[str, List[str]] = {}

refresh_time_tag = datetime.datetime.now()

random_tips = ['睡在一起的感觉意外不错呢~', '小心随时可能出现的枕头大战哦~', '不要抢别人的被子，但也不要被抢被子！', '暖暖和和的好舒服呢。']
special_tips = ['只有一个人在被窝里啊，好冷清呢。', '一个人睡也许是一种享受呢。']

def refresh_decorator(func):
    def wrapper(*args, **kwargs):
        # 如果进入新的一天并且过了凌晨六点，清空合宿列表
        global refresh_time_tag
        if datetime.datetime.now().date() != refresh_time_tag.date() and datetime.datetime.now().hour >= 6:
            sleep_list.clear()
            refresh_time_tag = datetime.datetime.now()
        return func(*args, **kwargs)

    return wrapper


# 一起睡觉zzzz
def solve_sleep(call_back: Callable[[str], str], message: str, user_id: str, group_id: str, res_listener):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    if command == "":
        return go_sleep(call_back, user_id, group_id)
    elif command == "list":
        return show_sleep_list(call_back, user_id, group_id)
    elif command == "wake":
        return wake_up(call_back, user_id, group_id)
    else:
        result = "[CQ:at,qq={0}] 未知命令".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))


@refresh_decorator
def go_sleep(call_back: Callable[[str], str], user_id: str, group_id: str):
    if group_id not in sleep_list:
        sleep_list[group_id] = []
    if user_id in sleep_list[group_id]:
        result = "[CQ:at,qq={0}] 你已经在合宿中了".format(user_id)
    else:
        result = "[CQ:at,qq={0}] 进入了合宿".format(user_id)
        sleep_list[group_id].append(user_id)
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))


@refresh_decorator
def show_sleep_list(call_back: Callable[[str], str], user_id: str, group_id: str):
    if group_id not in sleep_list:
        result = "[CQ:at,qq={0}] 当前没有人在合宿".format(user_id)
    else:
        result = "[CQ:at,qq={0}] 当前合宿成员：\n\n".format(user_id)
        for index, i in enumerate(sleep_list[group_id], start=1):
            result += str(index) + ". " + get_group_member_info(group_id, i)['nickname'] + "\n"
        if len(sleep_list[group_id]) == 1:
            result += '\n' + special_tips[datetime.datetime.now().second % len(special_tips)]
        else:
            result += '\n' + random_tips[datetime.datetime.now().second % len(random_tips)]
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))


@refresh_decorator
def wake_up(call_back: Callable[[str], str], user_id: str, group_id: str):
    if group_id not in sleep_list:
        result = "[CQ:at,qq={0}] 当前没有人在合宿哦".format(user_id)
    else:
        if user_id in sleep_list[group_id]:
            sleep_list[group_id].remove(user_id)
            result = "[CQ:at,qq={0}] 起床了离开了合宿".format(user_id)
        else:
            result = "[CQ:at,qq={0}] 你不在合宿中哦".format(user_id)
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))
