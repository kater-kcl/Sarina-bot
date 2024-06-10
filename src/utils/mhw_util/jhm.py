dict = "234678abcdefhijkmnprstuvwxyzABCDEFGHJKLMNPQRTWXYZ!?@&+=$-"


def MUL128H(a, b):
    return (a * b) >> 64


def generate_session_code(lobby):
    temp = lobby
    sum = 0
    while temp:
        sum += temp & 0xFF
        temp >>= 8
    sum &= 0xFF
    mulH = MUL128H(0x2492492492492493, sum)
    sum -= ((((sum - mulH) >> 1) + mulH) >> 5) * 0x38

    temp = lobby
    bytes = 0
    for i in range(8):
        temp ^= (sum + 1) << bytes
        bytes += 0x08

    next = 1
    count = 0
    ans = ""
    while next:
        if count >= 12:
            break
        next = MUL128H(0x8FB823EE08FB823F, temp) >> 5
        num = temp - next * 0x39
        ans = dict[num] + ans
        temp = next
        count += 1
    if count < 11:
        ans = '#' * (11 - count) + ans
    ans = dict[sum + 1] + ans
    return ans


def dict_2_val(c):
    ind = 0
    for ind in range(58):
        if c == dict[ind]:
            return ind
    return -1


def session_code_2_lobby(ans):
    ind = dict_2_val(ans[0])
    sum = ind - 1
    nxt = 0
    for i in range(1, 12):
        if ans[i] == '#':
            continue
        num = dict_2_val(ans[i])
        temp = nxt * 0x39 + num
        nxt = temp
    bytes = 0
    for i in range(8):
        nxt ^= (sum + 1) << bytes
        bytes += 8
    return nxt


def check_session_code(session_code):
    if len(session_code) != 12:
        return False
    for c in session_code:
        if c not in dict and c != '#':
            return False
    lobby = session_code_2_lobby(session_code)
    if (lobby >> 32) != 0x1860000:
        return False
    check_session = generate_session_code(lobby)
    if check_session != session_code:
        return False
    return True

if __name__ == '__main__':
    print(generate_session_code(109775243915699178))
