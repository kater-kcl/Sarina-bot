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
                "uin": "10086",
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
                "uin": "10087",
                "content": "[CQ:image,file=xxxxx]测试消息2"
            }
        }
    ]
    return {
        'action': 'send_forward_msg',
        'params': {
            'messages': date,
        }
    }