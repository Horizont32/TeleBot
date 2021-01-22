import numpy as np
from time import time, sleep

def eval_to_part(message):
    message = message.replace(' ', '')
    if '/' in message:
        parts = message.split('/')
        part = int(parts[0])/int(parts[1])
        return part
    elif any(symbol in message for symbol in [',', '.']) or message == '1' or message == '0':
        msg = message.replace(',', '.')
        return float(msg)
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
    users_to_delete = []
    while True:
        try:
            print('checking for users to delete', usersData)
            for user, data in usersData.items():
                if time() - data['last_update'] > 600:
                    users_to_delete.append(user)
            for user in users_to_delete:
                del usersData[user]
                users_to_delete.remove(user)
                print(f'deleted {user}')
            sleep(300)
        except:
            print('Exception while polling')

