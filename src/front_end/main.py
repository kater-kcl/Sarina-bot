from flask import Flask, request, Response, redirect
app = Flask('front_end')
@app.route('/mhw/join')
def mhw_join():
    args=request.args
    if "lobby" in args and "user" in args:
        return redirect(f'steam://joinlobby/582010/{args["lobby"]}/76561198330362644')