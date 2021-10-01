from numpy.random import randint as ri, seed as sd
from numba import njit
@njit
def randint(x, y):
    return ri(x, y)
@njit
def seed(s):
    sd(s)
def shuffle(array, s):
    seed(s)
    l = len(array)
    for i in range(0, l):
        r = randint(0, l)
        temp = array[r]
        array[r] = array[i]
        array[i] = temp
    return array
if __name__ == '__main__':
    print(bytes(shuffle(bytearray(b'12345'), 0)))
