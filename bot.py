import config
import telebot
import body
import time

bot = telebot.TeleBot(config.token)

telebot.apihelper.proxy = {'https': 'socks5://80.211.3.175:1295', 'http':'socks5h://80.211.3.175:1295'}


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
    bot.send_message(message.chat.id, message.text)
    bot.register_next_step_handler(message, begin_body)


def begin_body(message):
    names = []
    num = message.text
    for i in range(int(message.text)):
        names.append(input('Имя %s участника ' % str(i + 1), ), )
    return names


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text + ' ну и пососи')


bot.polling(none_stop=True)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=5)

