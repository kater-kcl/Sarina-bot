import html
import json
import random
from typing import Dict

from utils.message_builder import group_message, private_message

# Every key-value is user_id to gamestatus

user_guess = {}


def cmp_format(s):
    return s.replace('，', ',').replace('：', ':').replace('”', '"').replace('“', '"').replace('（', '(').replace('）',
                                                                                                               ')').replace(
        '＃', '#')


class GameStatus:
    # every score in score board is user_id to score
    def __init__(self, namelist, limit=10):
        self.anslist = []
        self.name_guessed = []
        self.guess_char = []
        self.score_board = {}
        self.guess_limit = 0
        self.limit = limit
        for name in namelist:
            self.anslist.append(name)
            self.name_guessed.append(False)
        self.guess_char = []

    def guess_new_char(self, char):
        if (self.guess_limit == self.limit):
            return -1
        if char.lower() in self.guess_char:
            return 0
        if char.upper() in self.guess_char:
            return 0
        self.guess_char.append(char)
        self.guess_limit += 1
        return 1

    def guess_name(self, nameid, name):
        if self.name_guessed[nameid - 1]:
            return -1
        if cmp_format(self.anslist[nameid - 1].upper()) == cmp_format(name.strip().upper()):
            self.name_guessed[nameid - 1] = True
            return 1
        else:
            return 0

    def set_limit(self, limit):
        self.limit = limit

    def get_chars(self):
        return self.guess_char

    def get_times(self):
        return self.guess_limit

    def get_limit(self):
        return self.limit

    def get_length(self):
        return len(self.anslist)

    def get_display(self):
        display_list = []
        for j in range((len(self.anslist))):
            name = self.anslist[j]
            letters = list(name)
            if self.name_guessed[j]:
                pass
            else:
                for i in range(len(letters)):
                    if letters[i].upper() not in self.guess_char and letters[i].lower() not in self.guess_char and \
                            letters[i] != ' ':
                        letters[i] = '*'
                if '*' not in letters:
                    self.name_guessed[j] = True
            display_list.append(''.join(letters))
        return display_list

    def get_ans(self):
        return self.anslist

    def is_end(self):
        for item in self.name_guessed:
            if not item:
                return False
        return True


games: Dict[str, GameStatus] = {}

mug_names = ['phigros', 'arcaea', 'orzmic', 'dancerail3', 'lanota', 'dynamix', 'maimai', 'wacca', 'chunithm', 'lyrica']

mug_alias = {}

def read_mug_list(mug_name: str):
    if mug_name in mug_names:
        with open('../resource/muguess_module/{}_song.txt'.format(mug_name), 'r') as f:
            return f.read().split('\n')
    else:
        return []


def get_random_ten_name(muglist):
    random_name_list = []
    for mug in muglist:
        random_name_list += read_mug_list(mug)
    random_name_list = list(set(random_name_list))
    if len(random_name_list) < 10:
        return random_name_list
    return random.sample(random_name_list, 10)


def game_help(call_back, group_id):
    result = '''帮助列表：
使用“*muguess create 游戏名”指令创建一场音游猜字母游戏，游戏名之间使用空格隔开
目前支持的音游有：maimai，phigros，wacca，orzmic，arcaea，lanota，dynamix，dancerail
如在游戏名中使用user则为用户自定义曲库，其他曲库内容失效\n
使用“*muguess answer”指令查看答案并结算当前猜字母游戏\n
使用“*muguess char 单个字符”指令对单个字符进行猜测\n
字符的范围包括: “英文，符号，数字，中文，日文，罗马字母”，英文不区分大小写
arcaea的曲库以使用非日文语言所显示的歌曲名为准\n
使用“*muguess name 序号 名字”指令对某首曲目进行猜测\n
或直接使用“*muguess 名字”指令对所有曲目进行猜测\n
名称需完全一致，但可以不区分大小写（如输入法无法打出可以前往萌娘百科或游戏wiki等进行复制）\n
私聊使用“*muguess create”可以创建用户题库，用户题库紧跟指令下一行，以换行分割
示例：
*muguess create
666
996
I
II'''
    ret = group_message(group_id, result)
    call_back(json.dumps(ret))


def creat_game(call_back, user_id, group_id, raw_mug_list):
    if mug_alias == {}:
        with open('../resource/muguess_module/mug_alias.json', 'r') as f:
            content = json.loads(f.read())
            for key in content.keys():
                mug_alias[key] = content[key]
    msg = ""
    if group_id in games.keys():
        msg = "正在进行游戏中哦，请完成游戏或者输入*muguess answer查看答案结束游戏"
    else:
        if 'user' in raw_mug_list:
            if user_id in user_guess.keys():
                games[group_id] = GameStatus(user_guess[user_id]['namelist'], user_guess[user_id]['limit'])
                msg = '游戏开始，本次的词库来源为：用户自拟题目\n'
                display = games[group_id].get_display()
                for i in range(len(display)):
                    msg += '{0}、{1}\n'.format(i + 1, display[i])
            else:
                msg = '未找到准备好的user题库'
        else:
            mug_list = []
            for mug in raw_mug_list:
                if mug in mug_alias.keys():
                    mug_list.append(mug_alias[mug])
                else:
                    msg = '未找到{}的曲库'.format(mug)
                    ret = group_message(group_id, msg.strip())
                    call_back(json.dumps(ret))
                    return
            mug_list = list(set(mug_list))
            if 'maimai' in mug_list:
                games[group_id] = GameStatus(get_random_ten_name(mug_list), 50)
            else:
                games[group_id] = GameStatus(get_random_ten_name(mug_list))
            msg = '游戏开始，本次的词库来源为：{}\n'.format(mug_list)
            display = games[group_id].get_display()
            for i in range(len(display)):
                msg += '{0}、{1}\n'.format(i + 1, display[i])
    ret = group_message(group_id, msg.strip())
    call_back(json.dumps(ret))


def show_answer(call_back, group_id):
    msg = ""
    if group_id not in games.keys():
        msg = "本群未开始一个游戏，输入“*muguess create”开始一场刺激的音游猜字母吧！"
    else:
        # msg = games[group_id].getscore()
        msg = '本局答案为：\n'
        ans = games[group_id].get_ans()
        for i in range(len(ans)):
            msg += '{0}、{1}\n'.format(i + 1, ans[i])
        del (games[group_id])
    ret = group_message(group_id, msg.strip())
    call_back(json.dumps(ret))


def guess_char(call_back, msg_id, user_id, group_id, char):
    msg = ""
    if group_id not in games.keys():
        msg = "本群未开始一个游戏，输入“*muguess create”开始一场刺激的音游猜字母吧！"
    elif len(char) != 1:
        msg = '只可以猜测单个字符哦'
    else:
        stu = games[group_id].guess_new_char(char)
        if stu == 1:
            msg = '[CQ:reply,id={0}][CQ:at,qq={1}][CQ:at,qq={1}]\n'.format(msg_id, user_id)
            msg += '已猜测字符有：{}({}/{})\n'.format(
                games[group_id].get_chars(), games[group_id].get_times(), games[group_id].get_limit())
            display = games[group_id].get_display()
            for i in range(len(display)):
                msg += '{0}、{1}\n'.format(i + 1, display[i])
        elif stu == 0:
            msg = '该字母已经被猜过了哦'
        elif stu == -1:
            msg = '猜字母数量已达上限'
    ret = group_message(group_id, msg.strip())
    call_back(json.dumps(ret))
    if games[group_id].is_end():
        msg = '全部曲目已出，本次猜曲结束'
        del (games[group_id])
        ret = group_message(group_id, msg.strip())
        call_back(json.dumps(ret))


def guess_name(call_back, msg_id, user_id, group_id, content):
    msg = ""
    content = content.split(' ', 1)
    if group_id not in games.keys():
        msg = "本群未开始一个游戏，输入“*muguess create”开始一场刺激的音游猜字母吧！"
    elif not content[0].isdigit():
        msg = '格式错误，请重新输入'
    else:
        stu = games[group_id].guess_name(int(content[0]), content[1])
        if stu == 1:
            msg = '[CQ:reply,id={0}][CQ:at,qq={1}][CQ:at,qq={1}]\n'.format(
                msg_id, user_id)
            msg += '已猜测字符有：{}({}/{})\n'.format(
                games[group_id].get_chars(), games[group_id].get_times(), games[group_id].get_limit())
            msg += '恭喜你，猜中了\n'
            display = games[group_id].get_display()
            for i in range(len(display)):
                msg += '{0}、{1}\n'.format(i + 1, display[i])
        elif stu == 0:
            msg = '猜错了，要不要再猜猜看\n'

        elif stu == -1:
            msg = '这个已经被猜过了哦\n'
    ret = group_message(group_id, msg.strip())
    call_back(json.dumps(ret))
    if games[group_id].is_end():
        msg = '全部曲目已出，本次猜曲结束'
        del (games[group_id])
        ret = group_message(group_id, msg.strip())
        call_back(json.dumps(ret))


def guess_name_anyway(call_back, message_id, user_id, group_id, message):
    msg = ""
    game = games[group_id]
    stu = 0
    for i in range(game.get_length()):
        i_stu = game.guess_name(i + 1, message)
        if i_stu != 0:
            stu = i_stu
    if stu == 1:
        msg = '[CQ:reply,id={0}][CQ:at,qq={1}][CQ:at,qq={1}]\n'.format(message_id, user_id)
        msg += '已猜测字符有：{}({}/{})\n'.format(
            game.get_chars(), game.get_times(), game.get_limit())
        display = game.get_display()
        for i in range(len(display)):
            msg += '{0}、{1}\n'.format(i + 1, display[i])
    elif stu == 0:
        msg = '猜错了，要不要再猜猜看\n'
    elif stu == -1:
        msg = '这个已经被猜过了哦\n'
    ret = group_message(group_id, msg.strip())
    call_back(json.dumps(ret))


def create_user_guess(call_back, user_id, message):
    print('create user guess')
    names = message.split('\n')
    guess_names = []
    reply = '添加题目为：\n'
    for name in names:
        guess_names.append(name.strip())
        reply += name + '\n'
    user_guess[user_id] = {}
    user_guess[user_id]['namelist'] = guess_names
    user_guess[user_id]['limit'] = 10
    ret = private_message(user_id, reply.strip())
    call_back(json.dumps(ret))


def set_user_guess_limit(call_back, user_id, message):
    if user_id not in user_guess.keys():
        ret = private_message(user_id, '未找到用户题库')
        call_back(json.dumps(ret))
        return
    limit = int(message)
    user_guess[user_id]['limit'] = limit
    ret = private_message(user_id, '设置成功')
    call_back(json.dumps(ret))


# this function is called when some action dose not match any of the existing action


def freedom_listening(call_back, user_id, group_id, message: str, message_id):
    if group_id in games.keys():
        guess_name_anyway(call_back, message_id, user_id, group_id, message)
    else:
        ret = group_message(group_id, '未找到指令')
        call_back(json.dumps(ret))


def mug_guess_solve(callback, user_id, group_id, message: str, message_id):
    if " " in message or "\n" in message:
        command, args = message.split(maxsplit=1)
    else:
        command = message
        args = ""
    if group_id:
        if command == 'create':
            creat_game(callback, user_id, group_id, args.split(' '))
        elif command == 'char':
            guess_char(callback, message_id, user_id, group_id, args)
        elif command == 'name':
            guess_name(callback, message_id, user_id, group_id, args)
        elif command == 'answer':
            show_answer(callback, group_id)
        elif command == 'help':
            game_help(callback, group_id)
        else:
            freedom_listening(callback, user_id, group_id, message, message_id)
    else:
        print(command)
        if command == 'create':
            print('create user guess')
            create_user_guess(callback, user_id, args)
        elif command == 'limit':
            set_user_guess_limit(callback, user_id, args)


if __name__ == '__main__':
    creat_game(print, 123, 123, ['mai','maimai','asd'])