import json

from utils.message_builder import group_message

together_list = {}



def solve_together(call_back, message, user_id, group_id, res_listener):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    # if command == "list":
    #     return show_together_list(call_back, user_id, group_id)
    # elif command == "info":
    #     return show_together_info(call_back, user_id, group_id, args)
    # elif command == "start":
    #     return start_together(call_back, user_id, group_id, args)



def start_together(call_back, user_id, group_id, level_id):
    result = "一起来玩吧！"
    ret = group_message(group_id, result)
    call_back(json.dumps(ret))