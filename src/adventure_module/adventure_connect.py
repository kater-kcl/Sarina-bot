import json
from typing import Callable
import src.adventure_module.adventure_api as adv_api


def init_adv():
    adv_api.init_adv()


def solve_adv(call_back: Callable[[str], str], message: str, user_id: str, group_id: int):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    if command == "list":
        return show_adv_list(call_back, user_id, group_id)
    elif command == "info":
        return show_adv_info(call_back, user_id, group_id, args)


def show_adv_list(call_back: Callable[[str], str], user_id: str, group_id: int):
    adv_list = adv_api.get_level_list()
    result = "{}".format(adv_list)
    ret = adv_api.group_message(group_id, result)
    call_back(json.dumps(ret))


def show_adv_info(call_back: Callable[[str], str], user_id: str, group_id: int, args: str):
    adv_info = adv_api.get_level_info(args)
    result = "{}".format(adv_info)
    ret = adv_api.group_message(group_id, result)
    call_back(json.dumps(ret))
<<<<<<< HEAD

# if __name__ == "__main__":
#     show_adv_list(print,"!23","123")
=======
>>>>>>> origin/main
