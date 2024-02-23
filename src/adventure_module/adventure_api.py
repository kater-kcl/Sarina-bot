import json
import os

from utils.message_builder import group_message

# 用于记录正在进行的冒险的信息
adv_dict: dict = {}
items = {}
levels_info = {}


def init_adv():
    init_items()
    init_levels()


def init_items():
    global items
    with open("./items/items.json", "r") as f:
        items = json.load(f)
    for item_type in items.keys():
        items[item_type] = dict(zip([item['id'] for item in items[item_type]], items[item_type]))


def init_levels():
    global levels_info
    # 遍历文件夹levels下的每个关卡文件并读取
    for file in os.listdir("./levels"):
        with open("./levels/" + file, "r") as f:
            level_content = json.load(f)
            levels_info[level_content['level_id']] = level_content


def get_level_list():
    result = "关卡列表：\n"
    for level_id in levels_info.keys():
        result += level_id + " : " + levels_info[level_id]['level_name'] + "\n"
    return result


def get_level_info(level_id: str):
    if level_id not in levels_info:
        return "未找到关卡"
    level_info = levels_info[level_id]
    result = ""
    result += "关卡名\n"
    result += level_info['level_name'] + "\n\n"
    result += "关卡事件点数\n"
    result += str(level_info['level_points']) + "\n\n"
    result += "关卡事件: \n"
    for event_type in level_info['level_event'].keys():
        result += event_type + ":\n"
        if len(level_info['level_event'][event_type]) == 0:
            result += "无\n\n"
        for event in level_info['level_event'][event_type]:
            result += "事件名：\"" + event['event_text'] + "\"\n"
            result += "奖励获得：\n"
            for item in event['event_result']:
                item_type = item['item_type']
                item_id = item['item_id']
                item_name = items[item_type][item_id]['chinese_name']
                result += item_name + ":"
                min_amount = item['amount']['min']
                max_amount = item['amount']['max']
                if min_amount == max_amount:
                    result += str(min_amount) + "\n\n"
                else:
                    result += str(min_amount) + "~" + str(max_amount) + "\n\n"
    return result


def get_map(uid: str, group_id: int, call_back):
    return


def start_adv(uid: str, group_id: int, call_back):
    if uid in adv_dict:
        result = "[CQ:at,qq={0}] 你已经在冒险中了".format(uid)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))
    else:
        adv_dict[uid] = 0
        result = "[CQ:at,qq={0}] 开始冒险".format(uid)
        ret = group_message(group_id, result)
        return call_back(json.dumps(ret))


if __name__ == "__main__":
    init_items()
    init_levels()
    print(get_level_list())
    # print(get_level_info("1-1"))
