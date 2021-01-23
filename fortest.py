import numpy as np
import threading as th
from time import time, sleep

users = {'1424', '214', '1234'}


def known_users_check(users, uid):
    with open('data.txt', mode='r+') as f:
        for line in f:
            users.add(line)
            if not uid == line:
                f.write(uid)

known_users_check(users, '214')
print(users)