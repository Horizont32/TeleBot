import telebot

def participants(n):
    names = []
    for i in range(int(n)):
        names.append(input('Имя %s участника ' % str(i+1), ),)
    return names


def make_dict(names):
    d = {}.fromkeys([name for name in names])
    for item in d:
        d.update({item: {'внес': input('%s внес ' % item,), 'Разделить на:': input('Делить сумму на ',), 'Сумма долга общая': 0.}})
    return d


def dolg_calc(names, d):
    for name in names:
        names_dolgi = str(d[name]['Разделить на:']).replace(' ', '').split(',')
        if name not in names_dolgi:
            d[name]['Сумма долга %s' % name] = 0.
        for named in names_dolgi:
            if named != name:
                d[named]['Сумма долга общая'] += int(d[name]['внес']) / len(names_dolgi)
                d[named]['Сумма долга %s' % name] = int(d[name]['внес']) / len(names_dolgi)
            elif named == name:
                d[named]['Сумма долга %s' % name] = 0.
    print(d)
    for user in names:
        for userd in str(d[user]['Разделить на:']).replace(' ', '').split(','):
            for itemd in d[userd]['Разделить на:'].replace(' ', '').split(','):
                if itemd == user:
                    if d[userd]['Сумма долга %s' % user] >= d[user]['Сумма долга %s' % userd]:
                        d[userd]['Сумма долга %s' % user] -= d[user]['Сумма долга %s' % userd]
                        d[userd]['Сумма долга общая'] -= d[user]['Сумма долга %s' % userd]
                        d[user]['Сумма долга общая'] -= d[user]['Сумма долга %s' % userd]
                        d[user]['Сумма долга %s' % userd] = 0.
                    else:
                        d[user]['Сумма долга %s' % userd] -= d[userd]['Сумма долга %s' % user]
                        d[user]['Сумма долга общая'] -= d[userd]['Сумма долга %s' % user]
                        d[userd]['Сумма долга общая'] -= d[userd]['Сумма долга %s' % user]
                        d[userd]['Сумма долга %s' % user] = 0.
    return d


def print_dolg(msg, names, d):
    for name in d:
        for komu_dolgen in names:
            if d[name]['Сумма долга %s' % komu_dolgen] != 0:
                bot.send_message(msg.chat.id, '%s должен ' %name + '%s' %komu_dolgen + str(d[name]['Сумма долга %s' % komu_dolgen]) + ' рублей')




# dolg_calc()
# print(d)
