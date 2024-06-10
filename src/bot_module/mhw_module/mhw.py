from datetime import datetime
from functools import wraps
import json
from typing import List

from utils.message_builder import group_message
from utils.mhw_util.jhm import check_session_code
from utils.onebot.onebot_api import get_group_member_info, get_group_members
import bot_module.mhw_module.jhm as jhm


def recover_from_database():
    jhm.recover_from_database()


def solve(call_back, message, user_id, group_id):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    # 集会码
    if command == "jhm":
        return solve_jhm(call_back, user_id, group_id, args)
    elif command == "help":
        return help(call_back, user_id, group_id, args)


def solve_jhm(call_back, user_id, group_id, args):
    if " " in args:
        command, args = args.split(" ", 1)
    else:
        command = args
        args = ""
    if command == 'create':
        jhm.create(call_back, user_id, group_id, args)
    elif command == 'delete':
        jhm.delete(call_back, user_id, group_id, args)
    elif command == 'check':
        jhm.check(call_back, user_id, group_id, args)
    else:
        result = "未知命令"
        ret = group_message(group_id, result.rstrip())
        call_back(json.dumps(ret))


def set_new_session_code(call_back, user_id, group_id, session_code):
    if check_session_code(session_code):
        jhm.create(call_back, user_id, group_id, session_code)


def help(call_back, user_id, group_id, args):
    msg = "集会码模块（调用前需要加上*mhw）\n" \
          "jhm create [集会码] 创建集会码\n" \
          "也可直接将集会码发至群内可自动识别\n" \
          "jhm delete [序号] 删除集会码\n" \
          "jhm check 查看集会\n" \
          "()内为可选项"
    ret = group_message(group_id, msg)
    return call_back(json.dumps(ret))
