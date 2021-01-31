import numpy as np
from time import time
import threading
import sqlite3

unknown_types = ['audio', 'document', 'photo', 'sticker', 'video', 'video_note',
                                    'voice', 'location', 'contact', 'new_chat_members', 'left_chat_member',
                                    'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
                                    'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
                                    'migrate_from_chat_id', 'pinned_message']


def eval_to_part(message):
    message = message.replace(' ', '')
    if '/' in message:
        parts = message.split('/')
        assert len(parts) == 2
        part = int(parts[0])/int(parts[1])
        return part
    elif any(symbol in message for symbol in [',', '.']) or message == '1' or message == '0':
        val = float(message.replace(',', '.'))
        assert 0 <= val <= 1
        return val
    elif message.isdigit():
        raise ValueError
    else:
        raise TypeError


def count(array2D):
    for rowI in range(len(array2D)):
        for colI in range(len(array2D[rowI])):
            if array2D[rowI][colI] >= array2D[colI][rowI]:
                array2D[rowI][colI] -= array2D[colI][rowI]
                array2D[colI][rowI] = 0
            else:
                array2D[colI][rowI] -= array2D[rowI][colI]
                array2D[rowI][colI] = 0

# bb = [[40, 40, 40, 40, 40], [20, 20, 20, 20, 20], [0, 0, 0, 0, 0], [20, 15, 2, 23, 20], [40, 40, 40, 40, 40]]


def vzaimozachet(a):
    # Функция создает список с индексами должников в формате [кто должен, кому должен]
    list_dolgov = []
    for rowI in range(len(a)):
        for colI in range(len(a[rowI])):
            if a[rowI][colI] != 0:
                list_dolgov.append([rowI, colI])
    return list_dolgov


def lower_transactions_comper(a):
    list_dolgov = vzaimozachet(a)
    # print(list_dolgov)
    for row in list_dolgov:
        # print('IDEM PO ROW %s' % row)
        for row2 in list_dolgov:
            # print('IDEM PO ROW2 %s' % row2)
            if row[1] == row2[0] and row != row2: ##or row2[0] == row[1] ### was right with row2[1] == row[0]
                if a[row[0]][row[1]] >= a[row2[0]][row2[1]]:
                    # print('row %s' % row)
                    # print(a)
                    a[row[0]][row[1]] -= a[row2[0]][row2[1]]
                    # print(a)
                    a[row[0]][row2[1]] += a[row2[0]][row2[1]]
                    # print(a)
                    a[row2[0]][row2[1]] = 0
                    # print(a)
                    list_dolgov.clear()
                    lower_transactions_comper(a)
                else:
                    # print('else row %s' % row)
                    # print(a)
                    a[row2[0]][row2[1]] -= a[row[0]][row[1]]
                    # print(a)
                    a[row[0]][row2[1]] += a[row[0]][row[1]]
                    # print(a)
                    a[row[0]][row[1]] = 0
                    # print(a)
                    list_dolgov.clear()
                    lower_transactions_comper(a)
            else:
                list_dolgov = vzaimozachet(a)


def main_task(checkmate):
    count(checkmate)
    lower_transactions_comper(checkmate)
    return vzaimozachet(checkmate)


def check_duplicate(list):
    for elem in list:
        if list.count(elem) > 1:
            return True


def prepare_events(events):
    summedEvents = sum([np.array(event['eventData']) for event in events])
    np.fill_diagonal(summedEvents, 0)
    return summedEvents.tolist()


def poll_last_update(usersData):
    try:
        print('checking for users to delete', usersData)
        users_to_delete = [user for user, data in usersData.items() if time() - data['last_update'] > 600]
        for user in users_to_delete:
            del usersData[user]
            print(f'deleted {user}')
        threading.Timer(1200, poll_last_update, args=(usersData,)).start()

    except:
        print('Exception while polling')


def write_user_to_db(uid):
    try:
        with sqlite3.connect('bot.db') as conn:
            c = conn.cursor()
            c.execute('INSERT OR IGNORE INTO users VALUES (?,?)', (uid, round(time())))
            conn.commit()
    except:
        print('ERROR WHILE ADDIND USER TO DB')


def read_users_from_db():
    try:
        with sqlite3.connect('bot.db') as conn:
            c = conn.cursor()
            c.row_factory = lambda cursor, row: row[0]
            c.execute('SELECT id FROM users')
            result = set(c.fetchall())
            return result
    except:
        print('ERROR READING FROM DB')
        return None
