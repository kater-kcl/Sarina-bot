from enum import Enum
from typing import Dict, Optional


class Sex(Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'


class GroupMemberInfo(Dict):
    group_id: int
    user_id: Optional[int] = None
    nickname: str
    card: str
    sex: Sex
    age: int
    area: str
    join_time: int
    last_sent_time: int
    level: str
    role: str
    unfriendly: bool
    title: str
    title_expire_time: int
    card_changeable: bool

    attributes = [
        'group_id',
        'user_id',
        'nickname',
        'card',
        'sex',
        'age',
        'area',
        'join_time',
        'last_sent_time',
        'level',
        'role',
        'unfriendly',
        'title',
        'title_expire_time',
        'card_changeable'
    ]

    def __getattribute__(self, item):
        if item in GroupMemberInfo.attributes:
            return self.get(item, None)
        else:
            return super().__getattribute__(item)
