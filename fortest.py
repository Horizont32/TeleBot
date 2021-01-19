import numpy as np

finalArray = np.zeros((3,3))
np.fill_diagonal(finalArray, 14)
print(finalArray.tolist())