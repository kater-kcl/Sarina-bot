def group_message(group_id, message):
    return {
        'action': 'send_group_msg',
        'params': {
            'group_id': group_id,
            'message': message,
        }
    }


def make_forward_message(message_list: list):
    # ret = []
    #
    # for message in message_list:
    #     cot = {
    #         "type": "node",
    #         "data": {
    #             "user_id": "2523375735",
    #             "nickname": "Sarina bot",
    #             "content": message
    #         }
    #     }
    #     ret.append(cot)
    # return ret
    return {
        "type": "node",
        "data": {
            "user_id": "10001000",
            "nickname": "某人",
            "content": [
                {"type": "face", "data": {"id": "123"}},
                {"type": "text", "data": {"text": "哈喽～"}}
            ]
        }
    }
