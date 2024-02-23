def group_message(group_id, message):
    return {
        'action': 'send_group_msg',
        'params': {
            'group_id': group_id,
            'message': message,
        }
    }


def make_forward_message(message_list: list):
    ret = {
        "type": "node",
        "data": {
            "user_id": "2523375735",
            "nickname": "Sarina bot",
            "content": [

            ]
        }
    }
    for message in message_list:
        cot = {
            "type": "text",
            "data": {
                "text": message
            }
        }
        ret['data']['content'].append(cot)
    return ret
