import random
import string

BASE_LIST = [c for c in string.digits + string.ascii_letters]
random.shuffle(BASE_LIST)
BASE_LIST = ''.join(BASE_LIST)

BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))


def base_decode(s, reverse_base=BASE_DICT):
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(s[::-1]):
        ret += (length ** i) * reverse_base[c]

    return ret


def base_encode(integer, base=BASE_LIST):
    if integer == 0:
        return base[0]

    length = len(base)
    ret = ''
    while integer != 0:
        ret = base[integer % length] + ret
        integer = integer // length

    return ret