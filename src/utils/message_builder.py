def group_message(group_id, message):
    return {
        'action': 'send_group_msg',
        'params': {
            'group_id': group_id,
            'message': message,
        }
    }


def make_forward_message(message_list: list):
    date = [
        {
            "type": "node",
            "data": {
                "name": "消息发送者A",
                "uin": "2276363693",
                "content": [
                    {
                        "type": "text",
                        "data": {
                            "text": "测试消息1"
                        }
                    }
                ]
            }
        },
        {
            "type": "node",
            "data": {
                "name": "消息发送者B",
                "uin": "2276363693",
                "content": [
                    {
                        "type": "text",
                        "data": {
                            "text": "测试消息1"
                        }
                    }
                ]
            }
        }
    ]
    return {
        'action': 'send_forward_msg',
        'params': {
            'messages': date,
        }
    }