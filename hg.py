def get_rec_sum(lst, summ=0):
    if len(lst) > 0:
        summ += lst.pop()
        return get_rec_sum(lst, summ)

    else: return summ

def get_rec_sum2(lst):
    head, *tail = lst
    return head + get_rec_sum2(tail) if tail else head


def fib_rec(n, l=[1,1]):
    if n > 2:
        num = l[-2]+l[-1]
        l.append(num)
        fib_rec(n-1, l)
    return l


d = [1, 2, [True, False], ["Москва", "Уфа", [100, 101], ['True', [-2, -1]]], 7.89]

# здесь продолжайте программу
def get_line_list(inl, defl = []):
    for elem in inl:
        if not isinstance(elem, list):
            defl.append(elem)
        else:
            get_line_list(elem, defl)
    return defl


def merge2lists(l1, l2):
    rslt = []
    i, j = 0, 0
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            rslt.append(l1[i])
            i += 1
        else:
            rslt.append(l2[j])
            j += 1
    while i < len(l1):
        rslt.append(l1[i])
        i += 1
    while j < len(l2):
        rslt.append(l2[j])
        j += 1
    print(f'result is {rslt}')
    return rslt




def mergesort(lst):
    print(f'======sorting {lst}=======')
    if len(lst) > 1:
        mid = int(len(lst) / 2)
        leftpart = lst[:mid]
        rightpart = lst[mid:]
        print(leftpart, rightpart)
        l = mergesort(leftpart)
        r = mergesort(rightpart)
        return merge2lists(l, r)
    else: return lst
    print('========done for that part ============')

# print(mergesort([8, 11, -6, 3, 0, 1, 1]))
# print(merge2lists([1,3,4], [2,4]))
get_div = lambda a, b: (b or None) and a / b

from functools import wraps

# здесь продолжайте программу

def dec_in(fn):
    @wraps
    def wrap(*args):
        return sum(fn(*args))
    return wrap


@dec_in
def get_list(s):
    """Функция для формирования списка целых значений"""
    return list(map(int, s.split()))


def gen():
    num = 1
    while True:
        if isPrime(num):
            yield num
        num += 1


print('--------')


def isPrime(f):
    for i in range(2, int(f ** (1 / 2) + 1)):
        if f % i == 0:
            return False
    return f > 1

a = gen()
for _ in range(10):
    print(next(a))
