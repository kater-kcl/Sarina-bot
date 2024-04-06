import config.db_config as db_config
import config.onebot_config as onebot_config
import config.steam_config as steam_config

def init_config():
    db_config.init_config()
    onebot_config.init_config()
    steam_config.init_config()
