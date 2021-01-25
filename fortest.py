import numpy as np
import threading as th
from time import time, sleep
import re
#
# a = ' 12312.,42'
# res = re.findall(r'\d+', a)
# re2 = re.split(r'[,.]', a)
# print(res)
# print(re.findall(r'\d+', '123//3/3'))
#
# b = '123//3'
# def tt(str):
#     a = re.findall(r'\d+', str)
#     print(a)
#     assert len(a) == 2
#
# print(tt(b))
#
#
# def eval_to_part(message):
#     message = message.replace(' ', '')
#     if '/' in message:
#         parts = message.split('/')
#         assert len(parts) == 2
#         part = int(parts[0])/int(parts[1])
#         return part
#     elif any(symbol in message for symbol in [',', '.']) or message == '1' or message == '0':
#         val = float(message.replace(',', '.'))
#         assert 0 <= val <= 1
#         return val
#     elif message.isdigit():
#         raise ValueError
#     else:
#         raise TypeError
#
# print(eval_to_part('0./1'))


words = ['one','two','three']
step = 2

def getkek(step):
    for cnt, word in enumerate(words):
        print(cnt, word)
        if step == cnt and step != 6:
            return word
        else:
            if word[step] == 'kek':
                return word

a = b =5
c=3
if a == b != c:
    print('lll')
a = getkek(step)
print(a)