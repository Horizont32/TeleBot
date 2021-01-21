import numpy as np

finalArray = np.zeros((3,3))
np.fill_diagonal(finalArray, 14)
print(finalArray.tolist())
if not ' ':
    print('empty')

for k in {'kek': 'ch'}:
    print(k)

a = set([11,12])
print(a)
a.add(13)
a.add(11)
print(a)
