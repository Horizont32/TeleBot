import config
import telebot
import time

bot = telebot.TeleBot(config.token)

# telebot.apihelper.proxy = {'https': 'socks5://artbryansk9_3109:UjKjdfxtd2@vpnnl01.fornex.org:993'}


# @bot.message_handler(commands=['start'])
# def start(message):
#     sent = bot.send_message(message.chat.id, 'Как тебя зовут?')
#     bot.register_next_step_handler(sent, hello)
#
#
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_msg(message):
#     bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")



if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

