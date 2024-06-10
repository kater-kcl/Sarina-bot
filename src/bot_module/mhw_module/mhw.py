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

dict = "234678abcdefhijkmnprstuvwxyzABCDEFGHJKLMNPQRTWXYZ!?@&+=$-"

def MUL128H(a, b):
    return ((a * b) >> 64)

def generateSessionCode(lobby):
    temp = lobby
    sum = 0
    while temp:
        sum += temp & 0xFF
        temp >>= 8
    sum &= 0xFF
    mulH = MUL128H(0x2492492492492493, sum)
    sum -= ((((sum - mulH) >> 1) + mulH) >> 5) * 0x38

    temp = lobby
    bytes = 0
    count = 0
    for i in range(8):
        temp ^= (sum + 1) << bytes
        bytes += 0x08

    next = 1
    count = 0
    ans = ""
    while next:
        if count >= 12:
            return ""
        next = MUL128H(0x8FB823EE08FB823F, temp) >> 5
        num = temp - next * 0x39
        ans = dict[num] + ans
        temp = next
        count += 1
    if count > 11:
        return ""
    ans = dict[sum + 1] + ans
    return ans

def dict_2_val(c):
    ind = 0
    for ind in range(58):
        if c == dict[ind]:
            return ind
    return -1

def sessionCode2Lobby(ans):
    ind = dict_2_val(ans[0])
    sum = ind - 1
    nxt = 0
    for i in range(1, 12):
        num = dict_2_val(ans[i])
        temp = nxt * 0x39 + num
        nxt = temp
    bytes = 0
    count = 0
    for i in range(8):
        nxt ^= (sum + 1) << bytes
        bytes += 8
    return nxt

def checkSessionCode(SessionCode):
    if len(SessionCode) != 12:
        return False
    for c in message:
        if c not in dict:
            return False
    lobby = sessionCode2Lobby(SessionCode)
    if ((lobby >> 32) != 0x1860000):
        return False
    checkSession = generateSessionCode(lobby)
    if checkSession != SessionCode:
        return False
    return True


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

def set_new_session_code(call_back, user_id, group_id, session_code):
    print(session_code)
    if checkSessionCode(session_code):
        print("test")
        result = "检测到集会码：" + session_code
        print(result)
        ret = group_message(group_id, result.rstrip())
        call_back(json.dumps(ret))

def help(call_back, user_id, group_id, args):
    msg = "集会码模块（调用前需要加上*mhw）\n" \
          "jhm create [集会码] 创建集会码\n" \
          "jhm delete (目标创建人qq号) 删除集会码\n" \
          "jhm check 查看集会\n" \
          "()内为可选项"
    ret = group_message(group_id, msg)
    return call_back(json.dumps(ret))
