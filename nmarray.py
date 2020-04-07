def eval_to_part(message):
    message = message.replace(' ', '')
    if '/' in message:
        parts = message.split('/')
        part = int(parts[0])/int(parts[1])
        return part
    elif any(symbol in message for symbol in [',', '.']) or message == '1' or message == '0':
        msg = message.replace(',', '.')
        return float(msg)
    elif message.isdigit():
        raise ValueError
    else:
        raise TypeError


def count(array2D):
    for rowI in range(len(array2D)):
        for colI in range(len(array2D[rowI])):
            if array2D[rowI][colI] >= array2D[colI][rowI]:
                array2D[rowI][colI] -= array2D[colI][rowI]
                array2D[colI][rowI] = 0
            else:
                array2D[colI][rowI] -= array2D[rowI][colI]
                array2D[rowI][colI] = 0

# bb = [[40, 40, 40, 40, 40], [20, 20, 20, 20, 20], [0, 0, 0, 0, 0], [20, 15, 2, 23, 20], [40, 40, 40, 40, 40]]


def vzaimozachet(a):
    list_dolgov = []
    for rowI in range(len(a)):
        for colI in range(len(a[rowI])):
            if a[rowI][colI] != 0:
                list_dolgov.append([rowI, colI])
                # print([rowI, colI])
    return list_dolgov


def lower_transactions(a, list_dolgov):
    print(list_dolgov)
    for row in list_dolgov:
        print('IDEM PO ROW %s' % row)
        for row2 in list_dolgov:
            print(list_dolgov)
            print('IDEM PO ROW2 %s' % row2)
            if row[1] == row2[0] and row != row2: ##or row2[0] == row[1] ### was right with row2[1] == row[0]
                if a[row[0]][row[1]] >= a[row2[0]][row2[1]]:
                    print('row %s' % row)
                    print(a)
                    a[row[0]][row[1]] -= a[row2[0]][row2[1]]
                    print(a)
                    # a[row2[0]][row[1]] += a[row2[0]][row2[1]]
                    a[row[0]][row2[1]] += a[row2[0]][row2[1]]
                    print(a)
                    a[row2[0]][row2[1]] = 0
                    print(a)
                    list_dolgov.remove(row2)
                    print(list_dolgov)
                    lower_transactions(a, list_dolgov)
                else:
                    print('else')
                    print('row %s' % row)
                    print(a)
                    a[row2[0]][row2[1]] -= a[row[0]][row[1]]
                    print(a)
                    a[row[0]][row2[1]] += a[row[0]][row[1]]
                    if a[row[0]][row2[1]] not in list_dolgov:
                        list_dolgov.append([row[0], row2[1]])
                    print(a)
                    a[row[0]][row[1]] = 0
                    list_dolgov.remove(row)
                    print(list_dolgov)
                    print(a)
                    lower_transactions(a, list_dolgov)
            # else:
            #     print('else')


def lower_transactions_while(a, list_dolgov):
    print(list_dolgov)
    i = 0
    i2 = 0
    while i < len(list_dolgov):
        print('IDEM PO ROW %s' % list_dolgov[i])
        # for list_dolgov[i2] in list_dolgov:
        # i2 = 0
        while i2 < len(list_dolgov):
            print('IDEM PO 2 %s' % list_dolgov[i2])
            if list_dolgov[i][1] == list_dolgov[i2][0] and list_dolgov[i] != list_dolgov[i2]: ##or row2[0] == row[1] ### was right with row2[1] == row[0]
                if a[list_dolgov[i][0]][list_dolgov[i][1]] >= a[list_dolgov[i2][0]][list_dolgov[i2][1]]:
                    print('row %s' % list_dolgov[i])
                    print(a)
                    a[list_dolgov[i][0]][list_dolgov[i][1]] -= a[list_dolgov[i2][0]][list_dolgov[i2][1]]
                    print(a)
                    # a[row2[0]][row[1]] += a[row2[0]][row2[1]]
                    a[list_dolgov[i][0]][list_dolgov[i2][1]] += a[list_dolgov[i2][0]][list_dolgov[i2][1]]
                    print(a)
                    a[list_dolgov[i2][0]][list_dolgov[i2][1]] = 0
                    print(a)
                    list_dolgov.remove(list_dolgov[i2])
                    print(list_dolgov)
                    # lower_transactions(a, list_dolgov)
                    i2 += 1
                else:
                    print('else')
                    print('row %s' % list_dolgov[i])
                    print(a)
                    a[list_dolgov[i2][0]][list_dolgov[i2][1]] -= a[list_dolgov[i][0]][list_dolgov[i][1]]
                    print(a)
                    a[list_dolgov[i][0]][list_dolgov[i2][1]] += a[list_dolgov[i][0]][list_dolgov[i][1]]
                    if a[list_dolgov[i][0]][list_dolgov[i2][1]] not in list_dolgov:
                        list_dolgov.append([list_dolgov[i][0], list_dolgov[i2][1]])
                    print(a)
                    a[list_dolgov[i][0]][list_dolgov[i][1]] = 0
                    list_dolgov.remove(list_dolgov[i])
                    print(list_dolgov)
                    print(a)
                    i2 += 1
                    # lower_transactions(a, list_dolgov)
            i += 1
            # else:
            #     print('else')


def lower_transactions_comper(a):
    list_dolgov = vzaimozachet(a)
    print(list_dolgov)
    for row in list_dolgov:
        print('IDEM PO ROW %s' % row)
        for row2 in list_dolgov:
            print('IDEM PO ROW2 %s' % row2)
            if row[1] == row2[0] and row != row2: ##or row2[0] == row[1] ### was right with row2[1] == row[0]
                if a[row[0]][row[1]] >= a[row2[0]][row2[1]]:
                    print('row %s' % row)
                    print(a)
                    a[row[0]][row[1]] -= a[row2[0]][row2[1]]
                    print(a)
                    # a[row2[0]][row[1]] += a[row2[0]][row2[1]]
                    a[row[0]][row2[1]] += a[row2[0]][row2[1]]
                    print(a)
                    a[row2[0]][row2[1]] = 0
                    print(a)
                    # list_dolgov.remove(row2)
                    list_dolgov.clear()
                    lower_transactions_comper(a)
                else:
                    print('else')
                    print('row %s' % row)
                    print(a)
                    a[row2[0]][row2[1]] -= a[row[0]][row[1]]
                    print(a)
                    a[row[0]][row2[1]] += a[row[0]][row[1]]
                    # if a[row[0]][row2[1]] not in list_dolgov:
                    #     list_dolgov.append([row[0], row2[1]])
                    print(a)
                    a[row[0]][row[1]] = 0
                    # list_dolgov.remove(row)
                    print(a)
                    list_dolgov.clear()
                    lower_transactions_comper(a)
            else:
                list_dolgov = vzaimozachet(a)
    # return list_dolgov
            # else:
            #     print('else')


def main_task(checkmate):
    count(checkmate)
    # print(checkmate)
    lower_transactions_comper(checkmate)
    # list_dolgov = vzaimozachet(checkmate)
    return vzaimozachet(checkmate)
    # lower_transactions(checkmate, list_dolgov)


def check_duplicate(list):
    for elem in list:
        if list.count(elem) > 1:
            return True


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


# try:
#     dolg = eval_to_part('22')
#     print(dolg)
# except:
#     print('Ошибка')

# kek = eval_to_part('2,2')
# print(kek)
# main_task(bb)
# print(bb)