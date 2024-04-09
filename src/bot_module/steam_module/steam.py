import json
import re
from typing import List

import requests

from utils.message_builder import group_message
from utils.onebot.onebot_api import get_group_members
from utils.onebot.onebot_class import GroupMemberInfo
from utils.steam_util.steam_api import get_players_summaries, get_player_summaries
from database.steam_data_mgr import bind_steam_id, get_steam_user_by_qid, get_all_steam_users


def solve(call_back, message, user_id, group_id):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    if command == "bind":
        return bind(call_back, user_id, group_id, args)
    elif command == "check":
        return check(call_back, user_id, group_id, args)
    elif command == "mhw":
        return mhw(call_back, user_id, group_id, args)
    elif command == "checkall":
        return checkall(call_back, user_id, group_id, args)
    elif command == "help":
        return steam_help(call_back, user_id, group_id, args)
    else:
        result = "[CQ:at,qq={0}] 未知命令".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))


def steam_help(call_back, user_id, group_id, args):
    result = "bind <steam_id64>/<steam好友码> 绑定steam账号\n" \
             "unbind 解绑steam账号\n" \
             "check <qq_id> 查看绑定的steam账号\n" \
             "mhw 查看群里的成员是否在玩怪猎世界\n" \
             "checkall 查看群里的人在打什么游戏"
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))


# 一键看群里是谁在玩怪猎崛起
def mhw(call_back, user_id, group_id, args):
    users = get_all_steam_users()
    group_list = get_group_members(group_id)
    group_userid_list = [str(user.user_id) for user in group_list]
    users = [user for user in users if str(user[0]) in group_userid_list]
    ret = []
    summaries = get_players_summaries([user[1] for user in users])
    for user in summaries:
        if user.gameextrainfo == 'Monster Hunter: World':
            ret.append(user.personaname)
    if len(ret) == 0:
        result = "没有人在玩怪猎世界"
    else:
        result = "以下调查团团员正在狩猎：\n"
        for name in ret:
            result += f"{name}\n"
    ret = group_message(group_id, result.rstrip())
    return call_back(json.dumps(ret))


def bind(call_back, user_id, group_id, args):
    if not args:
        result = "[CQ:at,qq={0}] 请在命令后输入你的steam id".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    steam_id = args
    if len(steam_id) != 17:
        steam_id = str(int(steam_id) + 76561197960265728)
    player = get_player_summaries(steam_id)
    if not player:
        result = "[CQ:at,qq={0}] 未找到该用户".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    player_name = player.personaname
    bind_steam_id(user_id, steam_id, player_name)
    result = "[CQ:at,qq={0}] 绑定成功，你的steam名为{1}".format(user_id, player_name)
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))


def unbind(call_back, user_id, group_id, args):
    result = get_steam_user_by_qid(user_id)
    if not result:
        result = "[CQ:at,qq={0}] 未绑定steam账号".format(user_id)
    else:
        result = "[CQ:at,qq={0}] 解绑成功".format(user_id)
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))


def check(call_back, user_id, group_id, args):
    target = args
    if not target:
        result = "[CQ:at,qq={0}] 请在命令后输入目标用户的qq号".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    pattern = r'\[CQ:at,qq=(\d+)\]'
    match = re.search(pattern, target)
    if match:
        target = match.group(1)
    if not target.isdigit():
        result = "[CQ:at,qq={0}] 请在命令后输入目标用户的qq号或@此人\n注意复制后需要重新@".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    result = get_steam_user_by_qid(target)
    if not result:
        result = "[CQ:at,qq={0}] 未绑定steam账号".format(user_id)
    else:
        steam_id = result[0][1]
        player = get_player_summaries(steam_id)
        if player.gameextrainfo:
            result = f"{player.personaname}在玩：{player.gameextrainfo}"
        else:
            result = f"{player.personaname}没有在玩游戏"
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))


def checkall(call_back, user_id, group_id, args):
    users = get_all_steam_users()
    group_list = get_group_members(group_id)
    group_userid_list = [str(user.user_id) for user in group_list]
    users = [user for user in users if str(user[0]) in group_userid_list]
    result = ""
    for user in users:
        player = get_player_summaries(user[1])
        if player.gameextrainfo:
            result += f"{player.personaname}在玩：{player.gameextrainfo}\n"
    if result == "":
        result = "没有人在玩游戏"
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))
