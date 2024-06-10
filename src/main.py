import html

from flask import Flask
from flask_sockets import Sockets
import database.db_mgr as db
import config.config as config
import bot_module.base_module.base as base
import bot_module.adventure_module.adventure_connect as adv
import bot_module.muguess_module.guess as guess
import bot_module.sleep_module.sleep as sleep
import bot_module.steam_module.steam as steam
import bot_module.mhw_module.mhw as mhw

import json
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
sockets = Sockets(app)
config.init_config()
db.init_database()
adv.init_adv()
mhw.recover_from_database()


def commonly_solve(call_back, message, user_id, group_id):
    mhw.set_new_session_code(call_back, user_id, group_id, message)
    keyword_1 = ['来','有','无','在','整']
    # 如果字符串中存在keyword，则触发
    if any(keyword in message for keyword in keyword_1) and '集会' in message:
        mhw.jhm(call_back, user_id, group_id, 'check')
        return True
    elif message == '集会码' or message == '集会':
        mhw.jhm(call_back, user_id, group_id, 'check')
        return True
    return False



@sockets.route('/')
def bot_socket(ws):
    while not ws.closed:
        data = ws.receive()
        data = json.loads(data)
        if data.get('message_type') == 'group' and data.get('raw_message'):
            raw_message = html.unescape(data['raw_message'])
            user_id = str(data['user_id'])
            group_id = str(data['group_id'])
            message_id = data['message_id']
            common_check = commonly_solve(ws.send, raw_message, user_id, group_id)
            if common_check:
                continue
            if raw_message[0] == "*":
                print(raw_message[1:])
                command = raw_message[1:]
                if " " in command:
                    command, args = command.split(" ", 1)
                else:
                    args = ""
                if command == "b":
                    base.solve_base(ws.send, args, user_id, group_id)
                elif command == "adv":
                    adv.solve_adv(ws.send, args, user_id, group_id, ws.receive)
                elif command == "muguess":
                    guess.mug_guess_solve(ws.send, user_id, group_id, args, message_id)
                elif command == "sleep":
                    sleep.solve_sleep(ws.send, args, user_id, group_id, ws.receive)
                elif command == "steam":
                    steam.solve(ws.send, args, user_id, group_id)
                elif command == "mhw":
                    mhw.solve(ws.send, args, user_id, group_id)

        elif data.get('message_type') == 'private' and data.get('raw_message'):
            raw_message = data['raw_message']
            user_id = str(data['user_id'])
            if raw_message[0] == "*":
                command = raw_message[1:]
                if " " in command:
                    command, args = command.split(" ", 1)
                else:
                    args = ""
                if command == "muguess":
                    guess.mug_guess_solve(ws.send, user_id, None, args, None)
                # elif command == 'test':
                #     ret = message_builder.make_forward_message([])
                #     ws.send(json.dumps(ret))
                #     temp = ws.receive()
                #     app.logger.info(temp)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('127.0.0.1', 1717), app, handler_class=WebSocketHandler)
    print("Server start")
    server.serve_forever()
