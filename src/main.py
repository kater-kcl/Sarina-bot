import html

from flask import Flask
from flask_sockets import Sockets
import database.db_mgr as db
import config.db_config as db_config
import base_module.base as base
import adventure_module.adventure_connect as adv
import muguess_module.guess as guess
import json
import logging

from utils import message_builder

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
sockets = Sockets(app)
db_config.init_config()
db.init_database()
adv.init_adv()


@sockets.route('/')
def bot_socket(ws):
    while not ws.closed:
        data = ws.receive()
        data = json.loads(data)
        if data.get('message_type') == 'group' and data.get('raw_message'):
            raw_message = html.unescape(data['raw_message'])
            user_id = str(data['user_id'])
            group_id = data['group_id']
            message_id = data['message_id']
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

