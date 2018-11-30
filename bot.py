import config
import telebot
import time

bot = telebot.TeleBot(config.token)

# telebot.apihelper.proxy = {'https': 'socks5://artbryansk9_3109:UjKjdfxtd2@vpnnl01.fornex.org:993'}


@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Как тебя зовут?')
    bot.register_next_step_handler(sent, hello)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)

