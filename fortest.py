import numpy as np
import threading as th
from time import time, sleep
import re
import pathlib

# with open('data_meSrul.txt', 'r') as f:
#     lines = [line.rstrip('\n') for line in f]
#
# times = [time() - 86400*(len(lines) - cnt) for cnt in range(len(lines))]
# print(times)
# with open('data_meSrul.txt', 'w') as f:
#     for (line, time) in zip(lines, times):
#         f.write(str(line) + '\t' + str(time) + '\n')
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


import sqlite3
# with sqlite3.connect('bot.db') as conn:
    # conn.row_factory = lambda cursor, row: {'Id': row[0], 'joined': row[1]}
    # c = conn.cursor()
    # c.row_factory = dict_factory

    # Create table
    # c.execute('''CREATE TABLE users
    #             (id int, joined int)''')

    # c.execute('DELETE FROM users')
    # # Insert a row of data
    # data = [(224702274, '1611700212'),
    #         (187060079, str(time()))]
    # c.executemany("INSERT INTO users VALUES (?,?)", data)
    # c.execute('SELECT COUNT(*) FROM users')
    # print(c.fetchone()[0])
    # c.execute('SELECT * FROM users')
    # print(c.description)

    # print(c.fetchone())
    # print({row['id']:row['joined'] for row in c.fetchall()})
    # Save (commit) the changes
    # conn.commit()

def write_user_to_db(uid):
    try:
        with sqlite3.connect('bot.db') as conn:
            c = conn.cursor()
            c.execute('INSERT OR IGNORE INTO users VALUES (?,?)', (uid, round(time(), uid)))
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

read_users_from_db()