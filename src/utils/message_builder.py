import json
from typing import Callable


def group_message(group_id, message):
    return {
        'action': 'send_group_msg',
        'params': {
            'group_id': group_id,
            'message': message,
        }
    }


def make_forward_message(call_back: Callable, message_list: list, res_listener):
    date = []
    for message in message_list:
        cot = {
            "type": "node",
            "data": {
                "name": "消息发送者A",
                "uin": "2523375735",
                "content": [
                    {
                        "type": "text",
                        "data": {
                            "text": message
                        }
                    }
                ]
            }
        }
        date.append(cot)

    ret = {
        'action': 'send_forward_msg',
        'params': {
            'messages': date,
        }
    }
    call_back(json.dumps(ret))
    res = res_listener()
    return json.loads(res)['data']


def forward_message(resid: str):
    return {
        "type": "node",
        "data": {
            "id": resid
        }
    }
