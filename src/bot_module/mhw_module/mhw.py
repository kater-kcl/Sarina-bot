from datetime import datetime
from functools import wraps
import json
from typing import List

from database.mhw_data_mgr import clear_outdated_assembly_info, add_assembly_info, get_all_assembly_info, \
    del_assembly_info
from utils.message_builder import group_message
from utils.onebot.onebot_api import get_group_member_info, get_group_members
from bot_module.mhw_module.mhw_class import AssemblyInfo

assembly_code_list: List[AssemblyInfo] = []


def clear_expired_assembly_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global assembly_code_list
        assembly_code_list = [assembly for assembly in assembly_code_list if
                              assembly.create_date.date() == datetime.now().date()]
        clear_outdated_assembly_info()
        return func(*args, **kwargs)

    return wrapper


def recover_from_database():
    global assembly_code_list
    assembly_code_list = get_all_assembly_info()


def solve(call_back, message, user_id, group_id):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    # 集会码
    if command == "jhm":
        return jhm(call_back, user_id, group_id, args)
    elif command == "help":
        return help(call_back, user_id, group_id, args)


@clear_expired_assembly_info
def jhm(call_back, user_id, group_id, args):
    if " " in args:
        command, args = args.split(" ", 1)
    else:
        command = args
        args = ""
    result = ""
    if command == 'create':
        if len([assembly for assembly in assembly_code_list if
                assembly.user_id == user_id and assembly.group_id == group_id]) > 0:
            result = f"[CQ:at,qq={user_id}] 你已经添加过了集会码"
        else:
            assembly_code_list.append(AssemblyInfo(user_id, group_id, args))
            add_assembly_info(AssemblyInfo(user_id, group_id, args))
            result = f"[CQ:at,qq={user_id}] 创建集会码成功"
    elif command == 'delete':
        target_uid = user_id
        if args:
            target_uid = args
        for assembly in assembly_code_list:
            if assembly.user_id == target_uid and assembly.group_id == group_id:
                assembly_code_list.remove(assembly)
                del_assembly_info(target_uid, group_id)
                result = f"[CQ:at,qq={user_id}] 删除集会码成功"
                break
        else:
            result = f"[CQ:at,qq={user_id}] 你没有创建集会码"
    elif command == 'check':
        user_id_list = [user.user_id for user in get_group_members(group_id)]
        group_assembly_info_list = [info for info in assembly_code_list if info.group_id == group_id]
        if len(group_assembly_info_list) == 0:
            result = "没有正在进行的集会码"
        else:
            result = "以下是正在进行的集会码：\n"
            for assembly in group_assembly_info_list:
                result += f"集会码：{assembly.assembly_code} 创建人：{get_group_member_info(assembly.group_id, assembly.user_id).nickname}\n"
    else:
        result = "未知命令"
    ret = group_message(group_id, result.rstrip())
    return call_back(json.dumps(ret))


def help(call_back, user_id, group_id, args):
    msg = "集会码模块（调用前需要加上*mhw）\n" \
          "jhm create [集会码] 创建集会码\n" \
          "jhm delete (目标创建人qq号) 删除集会码\n" \
          "jhm check 查看集会\n" \
          "()内为可选项"
    ret = group_message(group_id, msg)
    return call_back(json.dumps(ret))
