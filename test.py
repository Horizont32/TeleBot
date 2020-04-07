import config
import telebot
from telebot import types
import copy
import nmarray
from collections import Counter

bot = telebot.TeleBot(config.token)

i = 0
checkmate = []
checkmate_copy = []
full_check_amount = 0
summa = 0
can_fin = ['Отмена', 'Конец']
cancel_fin_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
cancel_fin_keyb.row(*can_fin)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Добро пожаловать в калькулятор тус!\n/add_event - для добавления глобальной тусы"
                          "\nОтмена - если ошибся где-то и хочешь начать все заново или вовсе хочешь закончить"
                          "\nКонец - если закончил с вводом даных и хочешь получить рассчет"
                          "\nРегистр (маленькими или большими буквамы ты введешь текст) абсолютно неважен!")


@bot.message_handler(commands=['add_event'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, "Итак, введи название вашей большой тусовки. Например, НОЧЬ НА РЕЧКЕ")
    bot.register_next_step_handler(msg, add_event)


def begin(message):
    begin_keyb_am = ['/add_event', '/help']
    begin_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    begin_keyb.row(*begin_keyb_am)
    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Ты остановил расчет. Чтобы начать заново, выбери /add_event.'
                                          ' Если нужна помощь, выбери /help', reply_markup=begin_keyb)
    elif message.text.lower() == 'конец':
        bot.send_message(message.chat.id, 'Расчет закончен! Заскринь и перешли! Если хочешь начать заново(например, '
                                          'рассчитать другую тусу), '
                                          'выбери /add_event', reply_markup=begin_keyb)


def add_event(message):
    msg = bot.send_message(message.chat.id, 'Туса создана, перейдем к добавлению участников. Перечисли'
                                            ' ОБЯЗАТЕЛЬНО через запятую, регистр при этом безразличен.'
                                            ' Например: Вася, Юля, Петя')
    bot.register_next_step_handler(msg, add_participants)


def add_participants(message):
    global participants, checkmate
    if check_if_cancel(message, []):
        return
    participants = message.text.lower().replace(' ', '').replace('\n', ',').replace(',,',',').split(',')
    if nmarray.check_duplicate(participants):
        msg = bot.send_message(message.chat.id, 'Друг, у вас в тусовке есть тезки, это круто, но ты, боюсь, '
                                                'запутаешься, когда я выведу результат. Введи уникальные имена')
        bot.register_next_step_handler(msg, add_participants)
    else:
        checkmate = [[0 for rows in range(len(participants))] for cols in range(len(participants))]
        print(checkmate)
        print(participants)
        cancel_only_fin_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        cancel_only_fin_keyb.row('Отмена')
        msg = bot.send_message(message.chat.id, "Окей. Участиники внесены, перейдем к добавлению событий на тусе. "
                                                "Введи имя первого события, например: ОПЛАТА ТАКСИ. Если ошибся, выбери"
                                                " ОТМЕНА", reply_markup=cancel_only_fin_keyb)
        bot.register_next_step_handler(msg, add_subevent_name)


def add_subevent_name(message):
    global checkmate, keyb, can_fin, can_fin_keyb
    if finish(message, checkmate, participants):
        return
    elif check_if_cancel(message, checkmate):
        return
    else:
        keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyb.row('На всех', 'В долях', 'На суммы')
        keyb.row('Отмена')
        msg = bot.send_message(message.chat.id, 'Окей, название добавлено. Давай уточним, как делим бабки'
                                                ': На всех поровну, у каждого своя доля (например, половина (1/2), '
                                                'четверть (1/4), 1 или 0,2), '
                                                'или каждый внес определенную СУММУ?', reply_markup=keyb)
        bot.register_next_step_handler(msg, choose_subevent_type)


def choose_subevent_type(message):
    global subevent_type, participants
    if check_if_cancel(message, checkmate):
        return
    usr_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    usr_keyb.add(*participants)
    usr_keyb.row('Отмена')
    subevent_type = message.text.lower().replace(' ', '')
    if subevent_type == 'навсех':
        msg = bot.send_message(message.chat.id, 'Окей, делим на всех поровну. Кто внес деньги?', reply_markup=usr_keyb)
        bot.register_next_step_handler(msg, fill_subevent_amount)
    elif subevent_type == 'вдолях':
        msg = bot.send_message(message.chat.id, 'Окей, делим в долях. Кто внес деньги?', reply_markup=usr_keyb)
        bot.register_next_step_handler(msg, fill_subevent_amount)
    elif subevent_type == 'насуммы':
        msg = bot.send_message(message.chat.id, 'Окей, делим индивидуально на конкретные суммы. Кто внес деньги?',
                               reply_markup=usr_keyb)
        bot.register_next_step_handler(msg, fill_subevent_amount)
    else:
        msg = bot.send_message(message.chat.id, 'Ошибка, неверный тип. Введи заново', reply_markup=keyb)
        bot.register_next_step_handler(msg, choose_subevent_type)


def fill_subevent_amount(message):
    ## Kto vnes babki
    global indexI, participants
    if check_if_cancel(message, checkmate):
        return
    else:
        if message.text.lower().replace(' ', '') not in participants:
            msg = bot.send_message(message.chat.id, 'Так не пойдет, этот человек не в вашей тусе! Введи имя заново')
            bot.register_next_step_handler(msg, fill_subevent_amount)
        else:
            indexI = participants.index(message.text.lower().replace(' ', ''))
            msg = bot.send_message(message.chat.id, 'Окей, сколько %s внес?' % participants[indexI])
            if subevent_type == 'навсех':
                bot.register_next_step_handler(msg, fill_subevent_equal_values)
            elif subevent_type == 'вдолях':
                bot.register_next_step_handler(msg, fill_subevent_part_values)
            elif subevent_type == 'насуммы':
                bot.register_next_step_handler(msg, fill_subevent_bill_values)


def fill_subevent_equal_values(message):
    global row, col, checkmate
    if check_if_cancel(message, checkmate):
        return
    else:
        if is_digit(message.text):
            ## skolko vnes babok
            for kto_dolzen in range(len(checkmate[indexI])):
                checkmate[indexI][kto_dolzen] = checkmate[indexI][kto_dolzen] + float(message.text)/len(participants)
            print(checkmate)
            msg = bot.send_message(message.chat.id, "Добавляем новое событие, введи название. Если ошибся, выбери ОТМЕНА"
                                                    ", чтобы начать все заново. Если закончил, выбери КОНЕЦ",
                                   reply_markup=cancel_fin_keyb)
            bot.register_next_step_handler(msg, add_subevent_name)
        else:
            msg = bot.send_message(message.chat.id, "АЯЯЙ, это не число! Введи число!")
            bot.register_next_step_handler(msg, fill_subevent_equal_values)


def fill_subevent_bill_values(message):
    global summa, full_check_amount, checkmate_copy, checkmate, i
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyb.row('Отмена')
    if check_if_cancel(message, checkmate, sump=summa):
        return
    else:
        if is_digit(message.text):
            ## skolko vnes babok для перовго вызова, потом уже количество денег на каждого
            if i <= len(participants) - 1 and i == 0:
                full_check_amount = float(message.text)
                checkmate_copy = copy.deepcopy(checkmate) ##that worked
                # print(checkmate_copy)
                # print('KOPIYA')
                msg = bot.send_message(message.chat.id, 'Сколько по этому событию должен %s' % participants[i])  ## имя на кого деим чек
                i += 1
                bot.register_next_step_handler(msg, fill_subevent_bill_values)
                # print('OBNULIL')
            elif len(participants) - 1 >= i > 0:
                summa += float(message.text)
                checkmate[indexI][i-1] += float(message.text)
                msg = bot.send_message(message.chat.id, 'Сколько по этому событию должен %s' % participants[i])  ## имя на кого деим чек
                bot.register_next_step_handler(msg, fill_subevent_bill_values)
                i += 1
            else:
                summa += float(message.text)
                checkmate[indexI][-1] += float(message.text)
                if summa == full_check_amount:
                    msg = bot.send_message(message.chat.id, 'Отлично! Все данные совпадают, я их запомнил!'
                                                            '\nЕсли хочешь добавить новое событие, просто введи'
                                                            ' его название. '
                                                            'Если ввел все данные и хочешь рассчитать долги, выбери'
                                                            ' КОНЕЦ.'
                                                            ' Если где-то ошибся (или не хочешь дальше считать),'
                                                            ' выбери ОТМЕНА', reply_markup=cancel_fin_keyb)
                    bot.register_next_step_handler(msg, add_subevent_name)
                    summa = 0
                    i = 0
                else:
                    bot.send_message(message.chat.id, 'Сумма денег, потраченной каждым из вас не равна общей сумме!'
                                                            ' Введи данные по участникам снова!',
                                     reply_markup=keyb)
                    msg = bot.send_message(message.chat.id, ' Сколько %s внес?' % participants[indexI], reply_markup=keyb)
                    i = 0
                    checkmate = checkmate_copy ##That worked
                    summa = 0
                    bot.register_next_step_handler(msg, fill_subevent_bill_values)
                print(checkmate)
                # i = 0
        else:
            msg = bot.send_message(message.chat.id, "АЯЯЙ, это не число! Введи число!")
            bot.register_next_step_handler(msg, fill_subevent_bill_values)


def fill_subevent_part_values(message):
    global summa, full_check_amount, checkmate_copy, checkmate, i
    but_list = []
    for num in range(len(participants)):
        if num/len(participants) == 0:
            but_list.append('0')
        elif num/len(participants) == 0.25:
            but_list.append('1/4')
        elif num/len(participants) == 0.5:
            but_list.append('1/2')
        elif num + 1 == len(participants):
            but_list.append(str(num) + '/%s' % len(participants))
            but_list.append('1')
        else:
            but_list.append(str(num) + '/%s' % len(participants))
            # parts_keyb.add(str(num) + '/%s' % len(participants))
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyb.row('Отмена')
    parts_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=5)
    parts_keyb.add(*but_list)
    parts_keyb.row('Отмена')
    if check_if_cancel(message, checkmate, sump=summa):
        return
    else:
        try:
            part = nmarray.eval_to_part(message.text)
        except TypeError:
            msg = bot.send_message(message.chat.id, 'Ошибка, введи долю заново!', reply_markup=keyb)
            bot.register_next_step_handler(msg, fill_subevent_part_values)
        except ValueError:
            if is_digit(message.text) and message.text != '1':
                ## skolko vnes babok для перовго вызова, потом уже количество денег на каждого
                if i <= len(participants) - 1 and i == 0:
                    full_check_amount = float(message.text)
                    checkmate_copy = copy.deepcopy(checkmate)  ##that worked
                    msg = bot.send_message(message.chat.id, 'Какую долю(например, 1/2, 1/4 ) '
                                                            'по этому событию должен %s' % participants[
                        i], reply_markup=parts_keyb)  ## имя на кого деим чек
                    i += 1
                    bot.register_next_step_handler(msg, fill_subevent_part_values)
            else:
                msg = bot.send_message(message.chat.id, "АЯЯЙ, это не число! Введи число!", reply_markup=keyb)
                bot.register_next_step_handler(msg, fill_subevent_part_values)
        else:
            if len(participants) - 1 >= i > 0:
                summa += full_check_amount * part
                checkmate[indexI][i-1] += full_check_amount * part
                msg = bot.send_message(message.chat.id, 'Какую долю(например, 1/2, 1/4 ) '
                                                        ' по этому событию должен %s' % participants[i],
                                       reply_markup=parts_keyb) ## имя на кого деим чек
                bot.register_next_step_handler(msg, fill_subevent_part_values)
                i += 1
            else:
                summa += full_check_amount * part
                checkmate[indexI][-1] += full_check_amount * part
                if round(summa, ndigits=2) == round(full_check_amount):
                    msg = bot.send_message(message.chat.id, 'Отлично! Все данные совпадают, я их запомнил!'
                                                            '\nЕсли хочешь добавить новое событие, просто введи'
                                                            ' его название. '
                                                            'Если ввел все данные и хочешь рассчитать долги, выбери'
                                                            ' КОНЕЦ.'
                                                            ' Если где-то ошибся (или не хочешь дальше считать),'
                                                            ' выбери ОТМЕНА', reply_markup=cancel_fin_keyb)
                    bot.register_next_step_handler(msg, add_subevent_name)
                    summa = 0
                    i = 0
                else:
                    bot.send_message(message.chat.id, 'Сумма денег, потраченной каждым из вас не равна общей сумме!'
                                                            ' Введи данные по участникам снова!',
                                     reply_markup=keyb)
                    msg = bot.send_message(message.chat.id, ' Сколько %s внес?' % participants[indexI], reply_markup=keyb)
                    i = 0
                    checkmate = checkmate_copy ##That worked
                    summa = 0
                    bot.register_next_step_handler(msg, fill_subevent_part_values)
                print(checkmate)
                # i = 0


def check_if_cancel(message, array, sump=0):
    global i, row, col
    if message.text.lower().replace(' ', '') == 'отмена':
        array.clear()
        sump = 0
        i = 0
        begin(message)
        return True
    else:
        return False


def finish(message, array, users):
    if message.text.lower().replace(' ', '') == 'конец':
        dolgi = nmarray.main_task(array)
        print(dolgi)
        final_message_text = str()
        for dolg in dolgi:
            final_message_text += (users[dolg[1]].capitalize() + ' должен ' + users[dolg[0]].capitalize() +
                                   ' ' + str(round(array[dolg[0]][dolg[1]], 2)) + ' монет\n')
            print(final_message_text)
        try:
            inline_repost = types.InlineKeyboardMarkup()
            inline_repost.add(types.InlineKeyboardButton(text='Переслать результат в чатик',
                                                         switch_inline_query=final_message_text))
            bot.send_message(message.chat.id, text=final_message_text, reply_markup=inline_repost)
        except:
            bot.send_message(message.chat.id, 'Как здорово вы потусили, никто никому ничего не должен!')
        finally:
            array.clear()
            begin(message)
            return True
    else:
        return False


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=2)