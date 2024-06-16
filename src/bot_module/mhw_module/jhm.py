import json
from datetime import datetime
from functools import wraps
from typing import List

from bot_module.mhw_module.mhw_class import SessionCodeInfo
from database.mhw_data_mgr import clear_outdated_session_code_info, add_session_code_info, get_all_session_code_info, \
    del_session_code_info
from utils.message_builder import group_message
from utils.mhw_util.jhm import check_session_code, session_code_2_lobby
from utils.onebot.onebot_api import get_group_members, get_group_member_info

session_code_list: List[SessionCodeInfo] = []


def clear_expired_session_code_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global session_code_list
        session_code_list = [session_code for session_code in session_code_list if
                             session_code.create_date.date() == datetime.now().date()]
        clear_outdated_session_code_info()
        return func(*args, **kwargs)

    return wrapper


def recover_from_database():
    global session_code_list
    session_code_list = get_all_session_code_info()


@clear_expired_session_code_info
def create(call_back, user_id, group_id, args):
    if not check_session_code(args):
        result = f"[CQ:at,qq={user_id}] 集会码无效"
    elif any(session_code.session_code == args and session_code.group_id == group_id for session_code in session_code_list):
        result = f"[CQ:at,qq={user_id}] 此集会码已被创建\n" + "传送门：http://mhw.katerkcl.top/mhw/join?lobby={session_code_2_lobby(session_code.session_code)}\n"
    else:
        session_code_list.append(SessionCodeInfo(user_id, group_id, args))
        add_session_code_info(SessionCodeInfo(user_id, group_id, args))
        result = f"[CQ:at,qq={user_id}] 创建集会码{args}成功"
    ret = group_message(group_id, result.rstrip())
    return call_back(json.dumps(ret))


@clear_expired_session_code_info
def delete(call_back, user_id, group_id, args):
    try:
        index = int(args)
        if 0 <= index < len(session_code_list):
            del_session_code_info(session_code_list[index].user_id, group_id)
            del session_code_list[index]
            result = f"[CQ:at,qq={user_id}] 删除集会码成功"
        else:
            result = f"[CQ:at,qq={user_id}] 序号无效"
    except ValueError:
        result = f"[CQ:at,qq={user_id}] 请输入有效的序号"
    ret = group_message(group_id, result.rstrip())
    return call_back(json.dumps(ret))


@clear_expired_session_code_info
def check(call_back, user_id, group_id, args):
    group_session_code_info_list = [info for info in session_code_list if info.group_id == group_id]
    if len(group_session_code_info_list) == 0:
        result = "没有正在进行的集会码"
    else:
        result = "以下是正在进行的集会码：\n"
        for index, session_code in enumerate(group_session_code_info_list):
            mem_info = get_group_member_info(session_code.group_id, session_code.user_id)
            mem_name = mem_info.card if mem_info.card else mem_info.nickname
            result += (f"{index}: 集会码：{session_code.session_code} "
                       f"创建人：{ mem_name }\n"
                       f"传送门：http://mhw.katerkcl.top/mhw/join?lobby={session_code_2_lobby(session_code.session_code)}\n")
    ret = group_message(group_id, result.rstrip())
    return call_back(json.dumps(ret))
