import sys
sys.setrecursionlimit(10000)


def check_sym(pat, sym):
    if pat == '$':
        if sym:
            return False
        return True
    if not pat:
        return True
    if not sym:
        return False
    if pat in ('.', sym):
        return True
    return False


def check_many(pat, string):
    while req_search(pat[2:], string[1:]) and string and check_sym(pat[0:1], string[0:1]):
        string = string[1:]
    return string


def check_word(pat, string):
    if pat and string:
        if pat[0] == '\\':  # escape symbol
            pat = pat[1:]
        if pat[1:2] and pat[1:2] in '?*+':
            if pat[1:2] == '?':
                if check_sym(pat[0], string[0:1]):
                    string = string[1:]
            elif pat[1:2] == '+':
                if check_sym(pat[0], string[0:1]):
                    string = check_many(pat, string)
                else:
                    return False
            else:  # * case
                string = check_many(pat, string)
            pat = pat[2:]
        if check_sym(pat[0:1], string[0:1]):  # regular case
            return check_word(pat[1:], string[1:])
        return False
    return check_sym(pat[0:1], string[0:1])


def req_search(pat, string):
    if pat[0:1] == '^':
        return check_word(pat[1:], string)
    if check_word(pat, string):
        return True
    if string:  # next step
        return req_search(pat, string[1:])
    return False


print(req_search(*input().split('|')))
