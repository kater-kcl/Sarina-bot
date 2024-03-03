import json
import random
import urllib
import html

from utils.message_builder import group_message, private_message

games = {}
# Every key-value is user_id to gamestatus

user_guess = {}


# User's owner guesses


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


def read_from_phigros():
    phi_file = open('../resource/muguess_module/phigros_song.txt', 'r')
    return phi_file.read().split('\n')


def read_from_arcaea():
    phi_file = open('../resource/muguess_module/arcaea_song.txt', 'r')
    return phi_file.read().split('\n')


def read_from_orzmic():
    orz_file = open('../resource/muguess_module/orzmic.txt', 'r')
    return orz_file.read().split('\n')


def read_from_dr3():
    dr3_file = open('../resource/muguess_module/dancerail3_song.txt', 'r')
    return dr3_file.read().split('\n')


def read_from_la():
    la_file = open('../resource/muguess_module/lanota_song.txt', 'r')
    return la_file.read().split('\n')


def read_from_dy():
    dy_file = open('../resource/muguess_module/dy_song.txt', 'r')
    return dy_file.read().split('\n')


def read_from_maimai():
    mai_file = open('../resource/muguess_module/mai_song.txt', 'r')
    return mai_file.read().split('\n')


def read_from_wacca():
    wa_file = open('../resource/muguess_module/wacca_song.txt', 'r')
    return wa_file.read().split('\n')


def read_from_chunithm():
    chu_file = open('../resource/muguess_module/chunithm_song.txt', 'r')
    return chu_file.read().split('\n')


def get_random_ten_name(muglist):
    random_name_list = []
    if 'phigros' in muglist or 'phi' in muglist:
        phi_name_list = read_from_phigros()
        for name in phi_name_list:
            random_name_list.append(name.strip())
    if 'arc' in muglist or 'arcaea' in muglist:
        arc_name_list = read_from_arcaea()
        for name in arc_name_list:
            random_name_list.append(name.strip())
    if 'orz' in muglist or 'orzmic' in muglist:
        orz_name_list = read_from_orzmic()
        for name in orz_name_list:
            random_name_list.append(name.strip())
    if 'dr3' in muglist or 'dancerail3' in muglist:
        dr3_name_list = read_from_dr3()
        for name in dr3_name_list:
            random_name_list.append(name.strip())
    if 'la' in muglist or 'lanota' in muglist:
        la_name_list = read_from_la()
        for name in la_name_list:
            random_name_list.append(name.strip())
    if 'dy' in muglist or 'dynamix' in muglist:
        dy_name_list = read_from_dy()
        for name in dy_name_list:
            random_name_list.append(name.strip())
    if 'mai' in muglist or 'maimai' in muglist:
        mai_name_list = read_from_maimai()
        for name in mai_name_list:
            random_name_list.append(name.strip())
    if 'wa' in muglist or 'wacca' in muglist:
        wa_name_list = read_from_wacca()
        for name in wa_name_list:
            random_name_list.append(name.strip())
    if "chu" in muglist or "chunithm" in muglist or "中二节奏" in muglist or "中二" in muglist:
        chu_name_list = read_from_chunithm()
        for name in chu_name_list:
            random_name_list.append(name.strip())
    random_name_list = list(set(random_name_list))
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
使用“*muguess name 序号 名字”指令对某首曲目进行猜测，名称需完全一致，但可以不区分大小写（如输入法无法打出可以前往萌娘百科或游戏wiki等进行复制）
私聊使用“*muguess create”可以创建用户题库，用户题库紧跟指令下一行，以换行分割
示例：
*muguess create
666
996
I
II'''
    ret = group_message(group_id, result)
    call_back(json.dumps(ret))


def creat_game(call_back, user_id, group_id, muglist):
    msg = ""
    if group_id in games.keys():
        msg = "正在进行游戏中哦，请完成游戏或者输入*muguess answer查看答案结束游戏"
    else:
        if 'user' in muglist:
            if user_id in user_guess.keys():
                games[group_id] = GameStatus(user_guess[user_id]['namelist'], user_guess[user_id]['limit'])
                msg = '游戏开始，本次的词库来源为：用户自拟题目\n'
                display = games[group_id].get_display()
                for i in range(len(display)):
                    msg += '{0}、{1}\n'.format(i + 1, display[i])
            else:
                msg = '未找到准备好的user题库'
        else:
            if 'mai' in muglist or 'maimai' in muglist:
                games[group_id] = GameStatus(get_random_ten_name(muglist), 50)
            else:
                games[group_id] = GameStatus(get_random_ten_name(muglist))
            msg = '游戏开始，本次的词库来源为：{}\n'.format(muglist)
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
    elif False == content[0].isdigit():
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
        print(command)
        if command == 'create':
            print('create user guess')
            create_user_guess(callback, user_id, args)
        elif command == 'limit':
            set_user_guess_limit(callback, user_id, args)
