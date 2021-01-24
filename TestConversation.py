import config
import telebot
from telebot import types
import nmarray
from threading import Thread
import messages

bot = telebot.TeleBot(config.token, threaded=True)
bot.worker_pool = telebot.util.ThreadPool(num_threads=3)

usersData = {}
knownUsers = set()


# TODO: add buttons to every reply
def get_user_step(uid):
    if uid in usersData:
        return usersData[uid]['step']
    else:
        knownUsers.add(uid)
        print('users: ', knownUsers)
        nmarray.write_user_to_file(uid)
        usersData[uid] = {'step': 0}
        usersData[uid]['tree'] = funcs
        print(f"New user {uid} detected, who hasn't used \"/add_event\" yet")
        return 0


@bot.message_handler(commands=['send_message'], func=lambda msg: msg.chat.id == config.sender_id)
def send_announcement(m):
    text = m.text
    for user in knownUsers:
        bot.send_message(user, text.replace('/send_message', ''))


@bot.message_handler(commands=['delete_me'])
def delete_user(m):
    knownUsers.remove(m.chat.id)


@bot.message_handler(content_types=nmarray.unknown_types)
def unsupported_message(m):
    bot.send_message(m.chat.id, 'Извини, с таким типом сообщения я не умею работать =) Мне нужен только текст')


@bot.message_handler(content_types=['text'], func=lambda msg: msg.text.lower() == 'отмена' or msg.text.lower() == 'c')
def cancel_conversation(m):
    cid = m.chat.id
    try:
        del usersData[cid]
        bot.send_message(cid, messages.data_cleared)
    except:
        bot.send_message(cid, messages.nothing_to_delete)


@bot.message_handler(commands=['finish'])
def finish(m):
    cid = m.chat.id
    step = get_user_step(cid)
    try:
        if step == 2:
            # Calculate
            usersData[cid]['step'] = 7
            step = usersData[cid]['step']
            usersData[cid]['last_update'] = m.date
            usersData[cid]['tree'][step](m)
        else:
            bot.send_message(cid, messages.finish_before_all_data_recieved)
    except:
        bot.send_message(cid, messages.finish_no_data)


@bot.message_handler(commands=['help'])
def help_cmd(m):
    bot.send_message(m.chat.id, messages.help_msg)


@bot.message_handler(commands=['add_event'])
def add_event(m):
    uid = m.chat.id
    get_user_step(uid)
    usersData[uid]['last_update'] = m.date
    usersData[uid]['step'] = 1
    bot.send_message(uid, messages.addEvent)


@bot.message_handler(commands=['fix_event'], func=lambda msg: msg.chat.id in usersData)
def fix_event(m):
    cid = m.chat.id
    text = m.text
    text_no_cmd = text.replace('/fix_event', '')
    try:
        chosenEvent = text_no_cmd.replace(' ', '').lower()
        if chosenEvent:
            cur_ev = chosenEvent
            usersData[cid]['current_event'] = cur_ev
        cur_ev = usersData[cid]['current_event']
        cur_ev_raw = usersData[cid]['events'][cur_ev]['raw_event_name']
        usersData[cid]['events'][cur_ev].clear()
        usersData[cid]['events'][cur_ev]['raw_event_name'] = cur_ev_raw
        usersData[cid]['step'] = 3
        bot.send_message(cid, f'Я очистил все данные, кроме названия, по событию {cur_ev_raw}')
        keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyb.row('На всех', 'В долях', 'На суммы')
        keyb.row('Отмена')
        bot.send_message(cid, messages.fixEvent_success, reply_markup=keyb)
        print(f'Event {cur_ev} cleared')
    except:
        bot.send_message(cid, messages.fixEvent_error)


@bot.message_handler(content_types=['text'], func=lambda msg: not msg.text.startswith('/fix_event'))
def main_handler(m):
    uid = m.chat.id
    print('MainHandler_Called')
    print('Text :', m.text)
    print('Name :', m.from_user.username)
    step = get_user_step(uid)
    usersData[uid]['last_update'] = m.date
    print(usersData[uid]['tree'][step].__name__)
    usersData[uid]['tree'][step](m)
    print(usersData)


def add_participants(m):
    cid = m.chat.id
    try:
        participants = tuple(m.text.lower().replace(' ', '').replace('\n', ',').replace(',,',',').split(','))
        if nmarray.check_duplicate(participants):
            bot.send_message(cid, messages.addPartic_error)
        else:
            mes = ''
            for count, elem in enumerate(participants):
                mes += '\n' + str(count + 1) + '. ' + str(elem)
            bot.send_message(cid, 'А вот и все наши участники! ' '\n' + mes)
            usersData[cid]['participants'] = participants
            bot.send_message(cid, messages.addPartic_success)
            # Creating table for events here, not in add_subevent, because when trying to create new event
            # it is going to make that field default
            usersData[cid]['events'] = {}
            usersData[cid]['step'] = 2
    except:
        bot.send_message(cid, 'Что-то пошло не так, попробуй ввести участников снова!')


def add_subevent(m):
    cid = m.chat.id
    raw_text = m.text
    text = m.text.replace(' ', '').lower()
    try:
        # first check if subevent name already exists in user events
        if text in usersData[cid]['events']:
            raise Exception
        usersData[cid]['events'][text] = {'raw_event_name': raw_text}
        usersData[cid]['current_event'] = text
        # Creating a keyboard
        keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyb.row('На всех', 'В долях', 'На суммы')
        keyb.row('/fix_event')
        bot.send_message(cid, messages.addSubEvent_success, reply_markup=keyb)
        usersData[cid]['step'] = 3
    except:
        bot.send_message(cid, 'Ошибка в имени, введи пожалуйста заново (возможно, такое имя уже есть)')


def choose_subevent_type(m):
    cid = m.chat.id
    text = m.text
    usr_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    usr_keyb.add(*usersData[cid]['participants'])
    usr_keyb.row('/fix_event')
    subeventSplitType = text.lower().replace(' ', '')
    if subeventSplitType in ['навсех', 'вдолях', 'насуммы']:
        cur_ev = usersData[cid]['current_event']
        usersData[cid]['events'][cur_ev]['split_type'] = subeventSplitType
        if subeventSplitType == 'навсех':
            bot.send_message(cid, 'Окей, делим на всех поровну. Кто внес деньги?', reply_markup=usr_keyb)
        elif subeventSplitType == 'вдолях':
            funcs[6] = split_parts
            bot.send_message(cid, 'Окей, делим в долях. Кто внес деньги?', reply_markup=usr_keyb)
        elif subeventSplitType == 'насуммы':
            funcs[6] = split_bill
            bot.send_message(cid, 'Окей, делим индивидуально на конкретные суммы. Кто внес деньги?',
                                   reply_markup=usr_keyb)
        usersData[cid]['step'] += 1
    else:
        keyb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyb.row('/fix_event')
        bot.send_message(cid, 'Ошибка, неверный тип. Введи заново', reply_markup=keyb)


def who_is_sponsor(m):
    cid = m.chat.id
    text = m.text.lower().replace(' ', '')
    partic = usersData[cid]['participants']
    cur_ev = usersData[cid]['current_event']
    cur_ev_raw = usersData[cid]['events'][cur_ev]['raw_event_name']
    if text not in partic:
        usr_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        usr_keyb.add(*usersData[cid]['participants'])
        usr_keyb.row('/fix_event')
        bot.send_message(cid, 'Такого человека нет в туcовке! Укажи действющего участника', reply_markup=usr_keyb)
    else:
        sponsor_idx = partic.index(text)
        usersData[cid]['events'][cur_ev]['sponsor'] = text
        usersData[cid]['events'][cur_ev]['sponsor_idx'] = sponsor_idx
        bot.send_message(cid, f'Окей, сколько денег внес {text.capitalize()} для оплаты события {cur_ev_raw}?',
                         reply_markup=types.ReplyKeyboardRemove())
        usersData[cid]['step'] += 1


def sponsor_payment_sum(m):
    cid = m.chat.id
    text = m.text
    cur_ev = usersData[cid]['current_event']
    sp_type = usersData[cid]['events'][cur_ev]['split_type']
    partic = usersData[cid]['participants']
    try:
        payment = float(text)
        usersData[cid]['events'][cur_ev]['sponsor_payment'] = payment
        if sp_type == 'навсех':
            split_equal(m)
            usersData[cid]['step'] = 2
        elif sp_type == 'насуммы':
            usersData[cid]['events'][cur_ev]['curIdx'] = 0
            bot.send_message(cid, f'Готово! Внесение денег учтено! Пришла пора делить расходы!'
                                  f' Какую сумму денег должен {partic[0]}')
            usersData[cid]['events'][cur_ev]['eventData'] = []
            usersData[cid]['events'][cur_ev]['parts'] = []
            usersData[cid]['step'] += 1
        elif sp_type == 'вдолях':
            but_list = messages.buts4parts(partic)
            parts_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=5)
            parts_keyb.add(*but_list)
            parts_keyb.row('/fix_event')
            usersData[cid]['events'][cur_ev]['curIdx'] = 0
            usersData[cid]['events'][cur_ev]['eventData'] = []
            usersData[cid]['events'][cur_ev]['parts'] = []
            bot.send_message(cid, f'Готово! Внесение денег учтено! Пришла пора делить расходы!'
                                  f'\nКакую долю от общей суммы должен {partic[0]}', reply_markup=parts_keyb)
            usersData[cid]['step'] += 1
    except:
        bot.send_message(cid, 'Ошибка, вы ввели не число! Введите еще раз')


def split_equal(m):
    cid = m.chat.id
    cur_ev = usersData[cid]['current_event']
    partic = usersData[cid]['participants']
    sponsor_idx = usersData[cid]['events'][cur_ev]['sponsor_idx']
    sponsor_payment = usersData[cid]['events'][cur_ev]['sponsor_payment']
    event_table = [[sponsor_payment/len(partic) if count == sponsor_idx else 0 for count, _ in enumerate(partic)]
                   for _ in partic]
    usersData[cid]['events'][cur_ev]['eventData'] = event_table
    bot.send_message(cid, messages.split_success)


def split_parts(m):
    cid = m.chat.id
    text = m.text
    cur_ev = usersData[cid]['current_event']
    curIdx = usersData[cid]['events'][cur_ev]['curIdx']
    partic = usersData[cid]['participants']
    sponsor_idx = usersData[cid]['events'][cur_ev]['sponsor_idx']
    sponsor_payment = usersData[cid]['events'][cur_ev]['sponsor_payment']
    but_list = messages.buts4parts(partic)
    parts_keyb = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=5)
    parts_keyb.add(*but_list)
    parts_keyb.row('/fix_event')
    try:
        part = nmarray.eval_to_part(text)
        print(part)
        if curIdx < len(partic) - 1:
            arr = [sponsor_payment * part if count == sponsor_idx else 0 for count, _ in enumerate(partic)]
            usersData[cid]['events'][cur_ev]['parts'].append(part)
            usersData[cid]['events'][cur_ev]['eventData'].append(arr)
            curIdx += 1
            usersData[cid]['events'][cur_ev]['curIdx'] = curIdx
            bot.send_message(cid, f' Какую долю от общей суммы должен {partic[curIdx]}', reply_markup=parts_keyb)
        elif curIdx == len(partic) - 1:
            arr = [sponsor_payment * part if count == sponsor_idx else 0 for count, _ in enumerate(partic)]
            usersData[cid]['events'][cur_ev]['parts'].append(part)
            usersData[cid]['events'][cur_ev]['eventData'].append(arr)
            if round(sum(usersData[cid]['events'][cur_ev]['parts']), 2) == 1:
                usersData[cid]['step'] = 2
                bot.send_message(cid, messages.split_success, reply_markup=types.ReplyKeyboardRemove())
            else:
                usersData[cid]['events'][cur_ev]['curIdx'] = 0
                usersData[cid]['events'][cur_ev]['eventData'].clear()
                usersData[cid]['events'][cur_ev]['parts'].clear()
                bot.send_message(cid, f'Сумма, внесенная {partic[sponsor_idx]}, не совпарадет с введенной '
                                      f'вами суммой. Попробуем заново с момента распределения затрат.'
                                      f'\nКакую долю от общей суммы должен {partic[0]}', reply_markup=parts_keyb)
    except:
        bot.send_message(cid, 'Ошибка ввода, введите долю верно')


def split_bill(m):
    cid = m.chat.id
    text = m.text
    cur_ev = usersData[cid]['current_event']
    curIdx = usersData[cid]['events'][cur_ev]['curIdx']
    partic = usersData[cid]['participants']
    sponsor_idx = usersData[cid]['events'][cur_ev]['sponsor_idx']
    sponsor_payment = usersData[cid]['events'][cur_ev]['sponsor_payment']
    try:
        value = float(text)
        if curIdx < len(partic) - 1:
            arr = [value if count == sponsor_idx else 0 for count, _ in enumerate(partic)]
            usersData[cid]['events'][cur_ev]['parts'].append(value)
            usersData[cid]['events'][cur_ev]['eventData'].append(arr)
            curIdx += 1
            usersData[cid]['events'][cur_ev]['curIdx'] = curIdx
            bot.send_message(cid, f' Какую сумму должен {partic[curIdx]}')
        elif curIdx == len(partic) - 1:
            arr = [value if count == sponsor_idx else 0 for count, _ in enumerate(partic)]
            usersData[cid]['events'][cur_ev]['parts'].append(value)
            usersData[cid]['events'][cur_ev]['eventData'].append(arr)
            if round(sum(usersData[cid]['events'][cur_ev]['parts']), 2) == round(sponsor_payment):
                usersData[cid]['step'] = 2
                bot.send_message(cid, messages.split_success)
            else:
                usersData[cid]['events'][cur_ev]['curIdx'] = 0
                usersData[cid]['events'][cur_ev]['eventData'].clear()
                usersData[cid]['events'][cur_ev]['parts'].clear()
                bot.send_message(cid, f'Сумма, внесенная {partic[sponsor_idx]}, не совпарадет с введенной '
                                      f'вами суммой. Попробуем заново с момента распределения затрат.'
                                      f'\nКакую сумму должен {partic[0]}')
    except:
        bot.send_message(cid, 'Ошибка, введи верную сумму!')


def tree_func(m):
    # This function is going to be replaced
    pass


def calculate(m):
    cid = m.chat.id
    events = usersData[cid]['events'].values()
    partic = usersData[cid]['participants']
    try:
        # Sum up all the events data arrays as numpy arrays
        summedArrays = nmarray.prepare_events(events)
        transaction_holders = nmarray.main_task(summedArrays)
        final_message_text = str()
        for dolg in transaction_holders:
            final_message_text += (partic[dolg[0]].capitalize() + ' должен ' + partic[dolg[1]].capitalize() +
                                   ' ' + str(round(summedArrays[dolg[0]][dolg[1]], 2)) + ' монет\n')
        inline_repost = types.InlineKeyboardMarkup()
        inline_repost.add(types.InlineKeyboardButton(text='Переслать результат в чатик',
                                                     switch_inline_query=final_message_text))
        bot.send_message(cid, text=final_message_text, reply_markup=inline_repost)
        del usersData[cid]
    except:
        bot.send_message(cid, 'Проблема с расчетом, что-то пошло не так, попробуйте снова ввести \n /finish')


if __name__ == '__main__':
    funcs = [help_cmd, add_participants, add_subevent, choose_subevent_type, who_is_sponsor, sponsor_payment_sum,
             tree_func, calculate]
    nmarray.fill_knownusers(knownUsers)
    thread1 = Thread(target=nmarray.poll_last_update, args=(usersData,))
    thread1.start()
    bot.polling(none_stop=True, interval=2)


