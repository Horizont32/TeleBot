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
    bot.reply_to(message, "Сколько вас было на пати?")
    bot.register_next_step_handler(message, begin_body)


def begin_body(message):
    users = message.text.split()
    bot.send_message(message.chat.id, str(users))
    dict = body.make_dict(users)
    bot.send_message(message.chat.id, str(dict))

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


def fill_list(message):
    if message.text == 'stop':
        return
    else:
        bot.send_message(message.chat.id, str(names))

        for i in range(len(names)):
            bot.send_message(message.chat.id, str(i))
            names[i] = str(message.text)
            continue


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text + ' ну и пососи')


bot.polling(none_stop=True)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=5)

