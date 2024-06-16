from datetime import datetime
from functools import wraps
import json
from typing import List

from database.steam_data_mgr import get_all_steam_users
from utils.message_builder import group_message
from utils.mhw_util.jhm import check_session_code, generate_session_code, session_code_2_lobby
from utils.onebot.onebot_api import get_group_member_info, get_group_members
import bot_module.mhw_module.jhm as jhm
from utils.steam_util.steam_api import get_players_summaries


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
    elif command == "kknd":
        return kknd(call_back, user_id, group_id, args)
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
          "kknd 广域集会查询（只包括steam模块绑定后的人员）\n"\
          "jhm create [集会码] 创建集会码\n" \
          "也可直接将集会码发至群内可自动识别\n" \
          "jhm delete [序号] 删除集会码\n" \
          "jhm check 查看集会\n" \
          "()内为可选项"
    ret = group_message(group_id, msg)
    return call_back(json.dumps(ret))


def kknd(call_back, user_id, group_id, args):
    users = get_all_steam_users()
    group_list = get_group_members(group_id)
    group_userid_list = {str(user.user_id): user.card if user.card else user.nickname for user in group_list}
    users = {user[1]: group_userid_list[user[0]] for user in users if user[0] in group_userid_list.keys()}
    steam_ids = list(users.keys())
    summaries = get_players_summaries(steam_ids)
    ret = []
    for user in summaries:
        if user.gameid == '582010' and user.lobbysteamid:
            ret.append((users[user.steamid], user.lobbysteamid))
    lobby_dict = {}
    for name, lobby in ret:
        if lobby in lobby_dict.keys():
            lobby_dict[lobby].append(name)
        else:
            lobby_dict[lobby] = [name]
    if len(lobby_dict) == 0:
        result = "没有人在玩"
    else:
        result = "以下是正在玩的人：\n"
        for lobby, names in lobby_dict.items():
            session_code = generate_session_code(int(lobby))
            result += f"集会：{session_code}\n集会成员："
            members = []
            for name in names:
                members.append(name)
            result += "、".join(members) + "\n"
            result += f"传送门：http://mhw.katerkcl.top/mhw/join?lobby={lobby}\n"
    ret = group_message(group_id, result.rstrip())
    return call_back(json.dumps(ret))


