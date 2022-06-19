import numpy as np
import threading as th
from time import time, sleep
import re
import pathlib
import sqlite3, telebot, config

a = [1,2,3,4]
abytes = bytearray(a)
print(abytes)
print(list(abytes))



def adapt_array(arr):
    """
        http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
        """
    return bytearray(arr)

def convert_array(text):
    return list(text)

# with sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES) as conn:
#     c = conn.cursor()
#     # Converts np.array to TEXT when inserting
#     # sqlite3.register_adapter(list, adapt_array)
#
#     # Converts TEXT to np.array when selecting
#     c.row_factory = lambda cursor, row: row[0]
#     sqlite3.register_converter("BLOB", convert_array)
#     # c.execute('INSERT INTO testarray VALUES (?)', (a, ))
#     c.execute('SELECT arr FROM testarray')
#     print('fetched: ', c.fetchone())


bot = telebot.TeleBot(config.token, threaded=True)
bot.worker_pool = telebot.util.ThreadPool(num_threads=3)

def send_announcement(m):

    try:
        bot.send_message(config.sender_id, text='rf')
    except:
        print(f'User {config.sender_id} rejected getting messages from bot')

if __name__ == '__main__':
    while True:
        send_announcement(2)
        sleep(10)