# this's actually randomized (just to get cool URLs) [a-zA-Z0-9] 62 letters string
BASE_LIST = 'Sp1hBo8kWXRKNQqc4ATdPfvzgFI0ZV7Hen5Yyt63xmraOw9blUCsDJu2MiLGjE'
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