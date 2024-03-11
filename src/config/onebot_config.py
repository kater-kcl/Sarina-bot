import os

bot_host = ''
bot_port = 0
bot_token = ''


def init_config():
    global bot_host, bot_port, bot_token
    bot_host = os.environ.get('BOT_HOST')
    bot_port = os.environ.get('BOT_PORT')
    bot_token = os.environ.get('BOT_TOKEN')
