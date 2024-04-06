import os


steam_api_key = ''


def init_config():
    global steam_api_key
    steam_api_key = os.environ.get('STEAM_API_KEY')

