from typing import Dict, List, Optional

import requests

import config.steam_config as steam_config


class PlayerSummaries(Dict):
    # public info
    steamid: str
    personaname: str
    profileurl: str
    avatar: str
    avatarmedium: str
    avatarfull: str
    personastate: int
    communityvisibilitystate: int
    profilestate: int
    lastlogoff: int
    commentpermission: int

    # private info
    realname: Optional[str] = None
    primaryclanid: Optional[str] = None
    timecreated: Optional[int] = None
    gameid: Optional[int] = None
    gameserverip: Optional[str] = None
    gameextrainfo: Optional[str] = None
    cityid: Optional[int] = None
    loccountrycode: Optional[str] = None
    locstatecode: Optional[str] = None
    loccityid: Optional[int] = None
    lobbysteamid: Optional[str] = None

    # array of attribute names
    attributes = [
        'steamid',
        'personaname',
        'profileurl',
        'avatar',
        'avatarmedium',
        'avatarfull',
        'personastate',
        'communityvisibilitystate',
        'profilestate',
        'lastlogoff',
        'commentpermission',
        'realname',
        'primaryclanid',
        'timecreated',
        'gameid',
        'gameserverip',
        'gameextrainfo',
        'cityid',
        'loccountrycode',
        'locstatecode',
        'loccityid',
        'lobbysteamid'
    ]

    def __getattribute__(self, item):
        if item in PlayerSummaries.attributes:
            return self.get(item, None)
        return super().__getattribute__(item)


def get_player_summaries(id64s: str) -> Optional[PlayerSummaries]:
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_config.steam_api_key}&steamids={id64s}'
    res = requests.get(url)
    res_json = res.json()
    if len(res_json['response']['players']) == 0:
        return None
    player = res_json['response']['players'][0]
    ret = PlayerSummaries(player)
    return ret


def get_players_summaries(id64s: List[str]) -> List[PlayerSummaries]:
    idstr = ','.join(id64s)
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_config.steam_api_key}&steamids={idstr}'
    res = requests.get(url)
    res_json = res.json()
    players = res_json['response']['players']
    ret = [PlayerSummaries(item) for item in players]
    return ret
