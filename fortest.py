import numpy as np
import threading as th
from time import time, sleep

users = {'1424':'sd', '214':None, '1234':None}


def poll_last_update(usersData):
    while True:
        users_to_delete = []
        try:
            print('checking for users to delete', usersData)
            users_to_delete = [user for user, data in usersData.items() if data == 'sd']
            # for user, data in usersData.items():
            #     users_to_delete.append(user)
            print(users_to_delete)
            for user in users_to_delete:
                del usersData[user]
                # users_to_delete.remove(user)
                print(f'deleted {user}')
            print(usersData)
            sleep(2)
        except:
            print('Exception while polling')


poll_last_update(users)
print(users)