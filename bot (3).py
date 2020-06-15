import config
import telebot
import body
import time

bot = telebot.TeleBot(config.token)

# telebot.apihelper.proxy = {'https': 'socks5://138.68.161.14:1080', 'http':'socks5h://138.68.161.14:1080'}


# @bot.message_handler(commands=['start'])
# def start(message):
#     sent = bot.send_message(message.chat.id, 'Как тебя зовут?')
#     bot.register_next_step_handler(sent, hello)
#
#
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_msg(message):
#     bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['loans', 'долги'])
def send_welcome(message):
    msg=bot.reply_to(message, "Кто тусил? (Введи по-братски через запятую все имена тусеров) Например: Никита, Гена, Дюша")
    bot.register_next_step_handler(msg, begin_body)


def begin_body(message):
    global users
    global d
    global users2
    users = message.text.replace(' ', '').split(',')
    users2 = message.text.replace(' ', '').split(',')
    d = {}.fromkeys(users)
    # for item in d:
    #     d.update({item: {'внес': None, 'Разделить на:': None,
    #                      'Сумма долга общая': 0.}})
    print(d)
    msg = bot.send_message(message.chat.id, 'Сколько денег внес %s?' %users[0])
    bot.register_next_step_handler(msg, fill_full)


def fill_full(message):
    d.update({users[0]: {'внес': message.text}})
    del users[0]
    print(d)
    if len(users) >0:
        for user in users:
            msg = bot.send_message(message.chat.id, 'Сколько денег внес %s?' % user)
            bot.register_next_step_handler(msg, fill_full)
            return
    else:
        for item in d:
            msg = bot.send_message(message.chat.id, 'На кого делим бабки от %s?' % item)
            bot.register_next_step_handler(msg, full_delim)
            break


def full_delim(message):
    print(users2)
    d[users2[0]].update({'Разделить на:': message.text, 'Сумма долга общая': 0.})
    print(d)
    del users2[0]
    # for item in d:
    #     d[item].update({'Delim na': message.text})
    #     print(d)
    #     msg = bot.send_message(message.chat.id, 'На кого делим сумму от %s?' % item)
    #     bot.register_next_step_handler(msg, full_delim)
    #     continue
    if len(users2) > 0:
        for item in users2:
            print(d)
            msg = bot.send_message(message.chat.id, 'На кого делим сумму от %s?' % item)
            bot.register_next_step_handler(msg, full_delim)
            return
    else:
        bot.send_message(message.chat.id, 'GOTOVO')
        body.dolg_calc(d.keys(), d)
        print(d)
        print_dolg(message, d.keys(), d)


def print_dolg(msg, names, d):
    for name_kk in d:
        for komu_dolgen in names:
            if d[name_kk]['Сумма долга %s' % komu_dolgen] != 0:
                bot.send_message(msg.chat.id, '%s должен ' %name_kk + '%s ' %komu_dolgen + str(d[name_kk]['Сумма долга %s' % komu_dolgen]) + ' рублей')


#
# def fill_vnes(message):
#     bot.send_message(message.chat.id, 'start fill_vnes')
#     if len(users) > 0:
#         msg = bot.send_message(message.chat.id, 'Сколько денег внес %s?' %users[0])
#         d.update({users[0]: {'внес': message.text}})
#         bot.send_message(message.chat.id, '%s' % d)
#         if int(message.text) > 0:
#             mes = bot.send_message(message.chat.id, 'На кого разделить данную сумму?')
#             bot.register_next_step_handler(mes, fill_split)
#             bot.send_message(message.chat.id, 'finish fill_vnes')
#         else:
#             del users[0]
#             bot.register_next_step_handler(msg, fill_vnes)
#     elif len(users) == 0:
#         bot.send_message(message.chat.id, 'SPS')
#
#
# def fill_split(message):
#     bot.send_message(message.chat.id, 'start fill_split')
#     if len(users) > 0:
#         d.update({users[0]: {'Разделить на': message.text}})
#         print(d)
#         msg = bot.send_message(message.chat.id, '%s' % d)
#         del users[0]
#         print(users)
#         bot.register_next_step_handler(msg, recurs)
#         bot.send_message(message.chat.id, 'finish fill_split')
#         # print('kekkekek')s
#         return

#
# def recurs(message):
#     fill_vnes(message)
#     return

    # for name in users:
    #     msg = bot.send_message(message.chat.id, 'Какую сумму внес %s?' % name)
    #     bot.register_next_step_handler(msg, fill_di)
    #     # @bot.message_handler(content_types=['text'])
    #     def fill_di(message):
    #         for item in d:
    #             d.update({name: {'vnes': message}})
    # bot.send_message(message.chat.id, d)




    # bot.send_message(message.chat.id, str(users))
    # # dict = body.make_dict(users)
    # # bot.send_message(message.chat.id, str(dict))
    # d = {}.fromkeys([name for name in users])

    # global names
    # names = []
    # num = message.text
    # # bot.send_message(message.chat.id, 'Tut bilo %s chelovek' % num)
    # for i in range(int(num)):
    #     # bot.get_updates(limit=i)
    #     bot.send_message(message.chat.id, str(i))
    # #     # @bot.message_handler(content_types=['text'])
    # #     # def looping(message):
    # #     #     bot.send_message(message.chat.id, 'Имя %s участника ' % str(i + 1))
    #     names.append(message.text)
    # bot.send_message(message.chat.id, str(names))
    #     # if message:
    #     #     continue
    # bot.send_message(message.chat.id, 'Введите имя первого ')
    # bot.register_next_step_handler(message, fill_list)



@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text + ' ну и пососи')


bot.polling(none_stop=True)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=5)

