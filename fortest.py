import numpy as np
import threading as th
from time import time, sleep

users = {'1424', '214', '1234'}


def known_users_check(uid):
    with open('data.txt', mode='r+') as f:
        lines = [line.strip('\n') for line in f]
        print(lines)
        if uid not in lines:
            f.write(uid + '\n')


known_users_check('111')
print(users)