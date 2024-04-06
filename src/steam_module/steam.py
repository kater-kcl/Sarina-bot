import json
import re

import requests

from config import config
from utils.message_builder import group_message
import config.steam_config as steam_config
import database.steam_data_mgr as steam_database
import database.db_mgr as database


def solve(call_back, message, user_id, group_id, res_listener):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    if command == "bind":
        return bind(call_back, user_id, group_id, args)
    elif command == "check":
        return check(call_back, user_id, group_id, args)
    else:
        result = "[CQ:at,qq={0}] 未知命令".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))


def bind(call_back, user_id, group_id, args):
    if not args:
        result = "[CQ:at,qq={0}] 请在命令后输入你的steam id".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    steam_id = args
    print(steam_config.steam_api_key)
    print(steam_id)
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_config.steam_api_key}&steamids={steam_id}'
    res = requests.get(url)
    res_json = res.json()
    players = res_json['response']['players']
    if len(players) == 0:
        result = "[CQ:at,qq={0}] 未找到该用户".format(user_id)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    player = players[0]
    player_name = player['personaname']
    steam_database.bind_steam_id(user_id, steam_id, player_name)
    result = "[CQ:at,qq={0}] 绑定成功，你的steam名为{1}".format(user_id, player_name)
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
    result = steam_database.get_steam_user_by_qid(target)
    if not result:
        result = "[CQ:at,qq={0}] 未绑定steam账号".format(user_id)
    else:
        steam_id = result[0][1]
        url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_config.steam_api_key}&steamids={steam_id}'
        res = requests.get(url)
        print(res.text)
        data = res.json()['response']['players'][0]
        if 'gameextrainfo' in data.keys():
            result = f"{data['personaname']}在玩：{data['gameextrainfo']}"
        else:
            result = f"{data['personaname']}没有在玩游戏"
    ret = group_message(group_id, result)
    return call_back(json.dumps(ret))


