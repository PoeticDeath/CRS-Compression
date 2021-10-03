import zlib
from os import remove
from time import time
from numba import njit
from sys import argv, exit
from psutil import cpu_count
from numpy.random import randint as ri, seed as sd
from multiprocessing import Process as Thread, Manager
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
        array[r], array[i] = array[i], array[r]
    return array
def CompressMT(Threadsnm, srtstr, Threads, srtstrsorted, ANS, CUR, x):
    try:
        v = 1000
        srtstr = bytearray(srtstr)
        for w in range(int(256**7/Threads*(Threadsnm-1)), int(256**7/Threads*Threadsnm)):
            if shuffle(bytearray(srtstrsorted), w) == srtstr:
                ANS[1] = int(w)
                break
            if w % v == 0:
                CUR[1] += v
    except:
        exit()
def Decompress():
    try:
        Filename = argv[2]
    except IndexError:
        Filename = input('What would you like the file to be called? : ')
    OpenFile = open(Filename, 'rb')
    Data = zlib.decompress(OpenFile.read())
    OpenFile.close()
    z = Data[:7]
    z = int.from_bytes(z, 'big')
    Bytes = Data[7:]
    Data = bytes(shuffle(bytearray(Bytes), z))
    remove(Filename)
    Filename = Filename[:-4]
    OpenFile = open(Filename, 'wb')
    OpenFile.write(Data)
    OpenFile.close()
def Compress():
    manager = Manager()
    try:
        Filename = argv[2]
    except IndexError:
        Filename = input('What file would you like to compress? : ')
    OpenFile = open(Filename, 'rb')
    srtstr = OpenFile.read()
    srtstrsorted = bytes(sorted(srtstr))
    srtstrlen = len(srtstr)
    Threads = cpu_count(logical=True)
    try:
        x = int(argv[3])
    except IndexError:
        x = 0
    Threadsnm = 1
    ANS = manager.dict()
    CUR = manager.dict()
    ANS[1] = ''
    CUR[1] = 0 + x
    Start = time()
    while (Threadsnm <= Threads):
        Thread(target=CompressMT, args=(Threadsnm, srtstr, Threads, srtstrsorted, ANS, CUR, x), daemon=True).start()
        print('Thread ' + str(Threadsnm) + ' started.')
        Threadsnm += 1
    while (ANS[1] == ''):
        CURTIME = time() - Start
        print(str(CUR[1]/256**7*100) + '% Complete,', f'{CUR[1]:,}' + ' Checked, ' + f'{int(int(CUR[1]-x)//CURTIME):,}' + ' Checked per Second.', end='\r')
        if CUR[1] == 256**7:
            print('File not compressible.')
            exit()
        pass
    print()
    z = int(ANS[1])
    OpenFile.close()
    remove(Filename)
    Filename = Filename + '.CRS'
    z = z.to_bytes(7, 'big')
    OpenFile = open(Filename, 'wb')
    OpenFile.write(zlib.compress(z + srtstrsorted, level=9))
    OpenFile.close()
def Main():
    try:
        FileAction = argv[1]
    except IndexError:
        FileAction = 0
    if (FileAction == 0):
        FileAction = input('Would you like to compress or decompress the file? Enter 1 to Compress or 2 to Decompress: ')
    if (FileAction == str('1')):
        print('Compressing')
        Start = time()
        Compress()
        End = time() - Start
        print(str('Compression took ' + str(int(End)) + ' seconds.'))
        print('Compressed')
    if (FileAction == str('2')):
        print('Decompressing')
        Start = time()
        Decompress()
        End = time() - Start
        print(str('Decompression took ' + str(int(End)) + ' seconds.'))
        print('Decompressed')
if __name__ == '__main__':
    Main()
