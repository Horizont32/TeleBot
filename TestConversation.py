import config
import telebot
from telebot import types
import copy
import nmarray

bot = telebot.TeleBot(config.token, threaded=True)

usersData = {}


def get_user_step(uid):
    if uid in usersData:
        return usersData[uid]['step']
    else:
        usersData[uid] = {'step': 0}
        print("New user detected, who hasn't used \"/add_event\" yet")
        return 0


@bot.message_handler(func=lambda message: message.text == 'отмена')
def cancel_conversation(m):
    cid = m.chat.id
    usersData[cid]['step'] = 0
    bot.send_message(cid, 'Полученные данные сброшены! Чтобы начать'
                          ' заново, введите /add_event')


@bot.message_handler(commands=['help'])
def help_cmd(m):
    bot.send_message(m.chat.id, 'Привет! Я помогу тебе посчитать, кто и кому сколько должен'
                                ' на большой вечеринке с минимальным количеством транзакций!'
                                ' Для того, что начать и создать вечеринку, введи /add_event')


@bot.message_handler(commands=['add_event'])
def add_event(m):
    uid = m.chat.id
    get_user_step(uid)
    usersData[uid]['step'] = 1
    bot.send_message(m.chat.id, 'Событие создано! Давай добавим участников! Перечисли'
                                ' ОБЯЗАТЕЛЬНО через запятую, регистр при этом безразличен.'
                                ' Например: Вася, Юля, Петя')


@bot.message_handler(content_types=['text'])
def main_handler(m):
    print(m.text)
    print('MainHandler_Called')
    print(funcs[get_user_step(m.chat.id)].__name__)
    print(usersData)
    funcs[get_user_step(m.chat.id)](m)


def add_participants(m):
    cid = m.chat.id
    participants = tuple(m.text.lower().replace(' ', '').replace('\n', ',').replace(',,',',').split(','))
    print(participants)
    if nmarray.check_duplicate(participants):
        bot.send_message(m.chat.id, 'Друг, у вас в тусовке есть тезки, это круто, но ты, боюсь, '
                                    'запутаешься, когда я выведу результат. Введи уникальные имена')
    else:
        mes = ''
        for count, elem in enumerate(participants):
            mes += '\n' + str(count + 1) + '. ' + str(elem)
        bot.send_message(cid, 'А вот и все наши участники! ' '\n' + mes)
        usersData[cid]['participants'] = participants
        usersData[cid]['current_data'] = [[0 for rows in range(len(participants))]
                                          for cols in range(len(participants))]
        bot.send_message(cid, 'Пришло время вносить данные по затратам! Введи имя первой закупки, например,'
                              ' "АЛКОГОЛЬ В Ашане".')
        usersData[cid]['step'] = 2


def add_subevent(m):
    cid = m.chat.id
    usersData[cid]['events'] = {m.text: None}
    usersData[cid]['current_event'] = m.text
    # Creating a keyboard
    keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyb.row('На всех', 'В долях', 'На суммы')
    keyb.row('Отмена')
    bot.send_message(m.chat.id, 'Окей, название добавлено. Давай уточним, как делим бабки'
                                ': На всех поровну, у каждого своя доля (например, половина (1/2), '
                                'четверть (1/4), 1 или 0,2), '
                                'или каждый внес определенную СУММУ?', reply_markup=keyb)
    usersData[cid]['step'] = 3


def choose_subevent_type(m):
    cid = m.chat.id
    text = m.text
    usr_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    usr_keyb.add(*usersData[cid]['participants'])
    usr_keyb.row('Отмена')
    subeventSplitType = text.lower().replace(' ', '')
    if subeventSplitType in ['навсех', 'вдолях', 'насуммы']:
        cur_ev = usersData[cid]['current_event']
        usersData[cid]['events'][cur_ev] = {'split_type': subeventSplitType}
        if subeventSplitType == 'навсех':
            bot.send_message(cid, 'Окей, делим на всех поровну. Кто внес деньги?', reply_markup=usr_keyb)
        elif subeventSplitType == 'вдолях':
            bot.send_message(cid, 'Окей, делим в долях. Кто внес деньги?', reply_markup=usr_keyb)
        elif subeventSplitType == 'насуммы':
            bot.send_message(cid, 'Окей, делим индивидуально на конкретные суммы. Кто внес деньги?',
                                   reply_markup=usr_keyb)
        usersData[cid]['step'] += 1
    else:
        keyb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyb.row('Отмена')
        bot.send_message(cid, 'Ошибка, неверный тип. Введи заново', reply_markup=keyb)


def who_credit(m):
    pass

if __name__ == '__main__':
    funcs = [help_cmd, add_participants, add_subevent, choose_subevent_type, who_credit]
    bot.polling(none_stop=True, interval=2)