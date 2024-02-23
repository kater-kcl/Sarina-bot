from flask import Flask
from flask_sockets import Sockets
import utils.db_mgr as db
import config.db_config as db_config
import base_module.base as base
import adventure_module.adventure_connect as adv
import json

app = Flask(__name__)
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
            raw_message = data['raw_message']
            user_id = data['user_id']
            group_id = data['group_id']
            if raw_message[0] == "*":
                command = raw_message[1:]
                command, args = command.split(" ", 1)
                if command == "b":
                    base.solve_base(ws.send, args, user_id, group_id)
                elif command == "adv":
                    adv.solve_adv(ws.send, args, user_id, group_id)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('127.0.0.1', 1717), app, handler_class=WebSocketHandler)
    server.serve_forever()
