import numpy as np
import threading as th
from time import time, sleep

def poll_last_update(usersData):
    while True:
        print('im polling1')
        for user in usersData:
            print(user['last_update'])
            if time() - user['last_update'] > 10:
                del usersData[user]
                print(f'User {user} deleted')
        sleep(5)


def poll_last_update2(usersData):
    while True:
        print('im polling2')
        for user in usersData:
            if time() - user['last_update'] > 10:
                del usersData[user]
                print(f'User {user} deleted')
        sleep(5)

thread1 = th.Thread(target=poll_last_update, args=({},))
thread1.start()
thread2 = th.Thread(target=poll_last_update2, args=({},))
thread2.start()
