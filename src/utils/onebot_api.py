import requests

import config.onebot_config as onebot_config


def get_group_member_info(group_id, user_id):
    url = f"http://{onebot_config.bot_host}:{onebot_config.bot_port}/get_group_member_info"
    params = {
        "group_id": group_id,
        "user_id": user_id
    }

    content = requests.get(url, params=params).json()
    print(content)
    return content['data']


def get_group_members(group_id):
    url = f"http://{onebot_config.bot_host}:{onebot_config.bot_port}/get_group_member_list"
    params = {
        "group_id": group_id
    }
    content = requests.get(url, params=params).json()
    return content['data']
