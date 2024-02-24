import json
import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


def datetime_decoder(in_dict):
    for k, v in in_dict.items():
        if isinstance(v, str):
            try:
                in_dict[k] = datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                pass
    return in_dict
