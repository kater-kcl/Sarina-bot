from typing import List

import requests

import config.onebot_config as onebot_config
from utils.onebot.onebot_class import GroupMemberInfo


def get_group_member_info(group_id, user_id) -> GroupMemberInfo:
    url = f"http://{onebot_config.bot_host}:{onebot_config.bot_port}/get_group_member_info"
    params = {
        "group_id": group_id,
        "user_id": user_id
    }

    content: GroupMemberInfo = requests.get(url, params=params).json()['data']
    return content


def get_group_members(group_id) -> List[GroupMemberInfo]:
    url = f"http://{onebot_config.bot_host}:{onebot_config.bot_port}/get_group_member_list"
    params = {
        "group_id": group_id
    }
    content = requests.get(url, params=params).json()['data']
    res: List[GroupMemberInfo] = [GroupMemberInfo(item) for item in content]
    return res
