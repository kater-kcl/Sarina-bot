import datetime
import json
import os
import random

from database.adv_save_mgr import get_adv_save, set_adv_save, get_all_adv_save
from utils.utils import DateTimeEncoder, datetime_decoder


from flask import current_app



# 用于记录正在进行的冒险的信息
adv_dict: dict = {}
items = {}
levels_info = {}
event_type_dict = {
    "mine_event": "挖矿",
    "gather_event": "采集",
    "fight_event": "战斗",
    "boss_event": "BOSS战"
}


def init_adv():
    init_items()
    init_levels()
    recover_adv_from_db()


def init_items(file_direct="../resource/adventure_module/"):
    global items
    with open(file_direct + "items/items.json", "r") as f:
        items = json.load(f)
    for item_type in items.keys():
        items[item_type] = dict(zip([item['id'] for item in items[item_type]], items[item_type]))


def init_levels(file_direct="../resource/adventure_module/"):
    global levels_info
    # 遍历文件夹levels下的每个关卡文件并读取
    for file in os.listdir(file_direct + "levels"):
        with open(file_direct + "levels/" + file, "r") as f:
            level_content = json.load(f)
            levels_info[level_content['level_id']] = level_content


def recover_adv_from_db():
    all_adv_save = get_all_adv_save()
    for save in all_adv_save:
        uid = save[0]
        save_json = json.loads(save[1], object_hook=datetime_decoder)
        print(save_json)
        print(save_json["adventure"])
        if "adventure" in save_json and save_json["adventure"] != {}:
            adv_dict[uid] = save_json["adventure"]


def get_level_list():
    result = "关卡列表：\n"
    for level_id in levels_info.keys():
        result += level_id + " : " + levels_info[level_id]['level_name'] + "\n"
    return result.rstrip()



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
    return result.rstrip()



def start_adv(uid: str, level_id: str):
    if uid in adv_dict:
        return None
    else:
        adv_dict[uid] = {
            "level_id": level_id,
            "start_time": datetime.datetime.now(),
            "events": [],
        }
        save = get_adv_save(uid)
        save['adventure'] = adv_dict[uid]
        set_adv_save(uid, save)
        return "踏上了前往{}的冒险之旅".format(levels_info[level_id]['level_name'])


# 未来可能会加入角色属性对于事件的影响
def solve_event_result(event: dict, event_type: str):
    result = {}
    event_result = event['event_result']
    if event_type == "mine_event" or event_type == "gather_event":
        result['get_item'] = {}
        item_result = result['get_item']
        for item in event_result:
            # 根据probability属性随机决定是否获得该物品
            if random.random() < item['probability']:
                item_type = item['item_type']
                item_id = item['item_id']
                amount = random.randint(item['amount']['min'], item['amount']['max'])
                if item_type not in item_result:
                    item_result[item_type] = {}
                if item_id not in item_result[item_type]:
                    item_result[item_type][item_id] = 0
                item_result[item_type][item_id] += amount
    return result


def generate_event(level_event: dict):
    events_type_list = [event_type for event_type in level_event.keys() if
                        len(level_event[event_type]) > 0 and event_type != "boss_event"]
    event_type = random.choice(events_type_list)
    # 从事件列表中以random_weight属性作为权值随机选择一个事件
    event = random.choices(level_event[event_type], [event['random_weight'] for event in level_event[event_type]])[0]
    result = solve_event_result(event, event_type)
    result_event = {
        "event_type": event_type,
        "event_text": event['event_text'],
        "event_id": event['event_id'],
        "event_result": result
    }
    return result_event


# 用于补全事件
def complete_adv(uid: str):
    if uid not in adv_dict:
        return False
    level_info = levels_info[adv_dict[uid]['level_id']]
    second_per_event = level_info['level_time'] / level_info['level_points']
    now = datetime.datetime.now()
    time_passed = now - adv_dict[uid]['start_time']
    event_passed = int(time_passed.total_seconds() / second_per_event)
    event_nums = min(event_passed, level_info['level_points'])
    if event_nums > len(adv_dict[uid]['events']):
        for i in range(event_nums - len(adv_dict[uid]['events'])):
            new_event = generate_event(level_info['level_event'])
            new_event['event_time'] = adv_dict[uid]['start_time'] + datetime.timedelta(seconds=second_per_event * i)
            adv_dict[uid]['events'].append(new_event)
    save = get_adv_save(uid)
    save['adventure'] = adv_dict[uid]
    set_adv_save(uid, save)


def get_adv_progress(uid: str):
    if uid not in adv_dict:
        return None
    complete_adv(uid)
    level_info = levels_info[adv_dict[uid]['level_id']]
    events = adv_dict[uid]['events']
    result = "关卡：" + level_info['level_name'] + "\n"
    result += "已经进行的事件：" + str(len(events)) + "/" + str(level_info['level_points']) + ": \n\n"
    for event in events:
        result += "事件({}/{})".format(events.index(event) + 1, level_info['level_points']) + "\n"
        result += "事件名称：\"" + event['event_text'] + "\"\n"
        result += "事件时间：" + event['event_time'].strftime("%Y-%m-%d %H:%M:%S") + "\n"
        result += "事件结果：\n"
        event_result = event['event_result']
        for item_result in event_result['get_item'].keys():
            item_type = item_result
            result_items = event_result['get_item'][item_result]
            for item_id in result_items.keys():
                item_name = items[item_type][item_id]['chinese_name']
                amount = result_items[item_id]
                result += "获得" + item_name + "：" + str(amount) + "\n"
        result += "\n"

    return result.rstrip()


def finish_adv(uid: str):
    if uid not in adv_dict:
        return None
    result = "冒险结束：\n"
    current_app.logger.info("finish_adv")
    result += get_adv_progress(uid) + "\n"
    current_app.logger.info("after get_adv_progress")
    result += "总计获得奖励：\n"
    result_items = {}
    events = adv_dict[uid]['events']
    for event in events:
        event_result = event['event_result']
        for item_result in event_result['get_item'].keys():
            item_type = item_result
            if item_type not in result_items:
                result_items[item_type] = {}
            result_items[item_type] = event_result['get_item'][item_result]
    current_app.logger.info("after get result_items")
    save = get_adv_save(uid)
    current_app.logger.info(result_items)
    for item_type in result_items.keys():
        current_app.logger.info(item_type)
        if item_type not in save['items']:
            save['items'][item_type] = {}
        for item_id in result_items[item_type].keys():
            current_app.logger.info(item_id)
            if item_id not in save['items'][item_type]:
                save['items'][item_type][item_id] = 0
            save['items'][item_type][item_id] += result_items[item_type][item_id]
    current_app.logger.info("after add items")
    del adv_dict[uid]
    save['adventure'] = {}
    set_adv_save(uid, save)
    current_app.logger.info("end")
    return result.rstrip()


if __name__ == "__main__":
    # init_items("./")
    # init_levels("./")
    # print(get_level_list())
    # print(get_level_info("1-1"))
    print(start_adv("123", "test"))
    while True:
        command = input()
        if command == "p":
            print(get_adv_progress("123"))
