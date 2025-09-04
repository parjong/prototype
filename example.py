from sample._core import hello_from_bin
from sample._core import get_array

import numpy as np

print(hello_from_bin())

print('###')
print('### 1st')
print('###')
arr_1 = np.ndarray([1])
print(arr_1)
get_array(arr_1)

print('###')
print('### 2nd')
print('###')
arr_2 = np.asarray([1, 2, 3, 4], dtype=np.int16).reshape(2, 2)
print(arr_2)
get_array(arr_2)

print('###')
print('### 3rd')
print('###')
arr_3 = np.asarray([1, 2, 3, 4], dtype=np.float32).reshape(2, 2)
print(arr_3)
get_array(arr_3)
