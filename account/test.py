import math


def insert_to_k(n):
    m = n
    length = len(str(n))
    if 3 < length < 7:
        n /= 1000
        mod = math.fmod(m, 1000)
        if mod == 0 or mod < 50:
            return str(math.floor(n)) + 'k'
        else:
            return str(round(n, 1)) + 'k'

    if 6 < length < 10:
        n /= 1000000
        mod = math.fmod(m, 1000000)
        if mod == 0 or mod < 50000:
            return str(math.floor(n)) + 'm'
        else:
            return str(round(n, 1)) + 'm'

    if 9 < length < 13:
        n /= 1000000000
        mod = math.fmod(m, 1000000000)
        if mod == 1 or mod < 50000000:
            return str(math.floor(n)) + 'b'
        else:
            return str(round(n, 1)) + 'b'

    else:
        return n


# print(math.fmod(5, 3))

def commalize(n):
    length = len(str(n))
    if length > 3:
        p1 = length - 2
        n = put_comma(n, 1)
        while p1 > 0:
            p1 -= 3
            n = put_comma(n, p1)
    return n


def put_comma(n, index):
    index -= 1
    return n[:index] + ',' + n[index:]


# # commalize(1493045)
# put_comma(1500, 3)
