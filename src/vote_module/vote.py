# 啥比腾讯的逆天投票模块太难用了，遂写此功能
from typing import Callable


vote_info = {}

def create_vote(call_back, user_id, group_id, args):


    pass


def solve_vote(call_back: Callable[[str], str], message: str, user_id: str, group_id: str, res_listener):
    if " " in message:
        command, args = message.split(" ", 1)
    else:
        command = message
        args = ""
    if command == "create":
        return create_vote(call_back, user_id, group_id, args)