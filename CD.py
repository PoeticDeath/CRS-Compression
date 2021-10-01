from CRS import shuffle
from sys import argv, exit
from multiprocessing import Process as Thread, Manager
from time import time
from os import remove
from psutil import cpu_count
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
    from ast import literal_eval
    try:
        Filename = argv[2]
    except IndexError:
        Filename = input("What would you like the file to be called? : ")
    OpenFile = open(Filename, "r")
    Data = literal_eval(OpenFile.read())
    OpenFile.close()
    z = Data[0]
    z = int(str(z), 16)
    Bytes = Data[1]
    Data = bytes(shuffle(bytearray(Bytes), z))
    remove(Filename)
    Filename = Filename[:-4]
    OpenFile = open(Filename, "wb")
    OpenFile.write(Data)
    OpenFile.close()
def Compress():
    manager = Manager()
    try:
        Filename = argv[2]
    except IndexError:
        Filename = input("What file would you like to compress? : ")
    OpenFile = open(Filename, "rb")
    srtstr = OpenFile.read()
    srtstrsorted = bytes(sorted(srtstr))
    srtstrlen = len(srtstr)
    Threads = cpu_count(logical=False)
    try:
        x = int(argv[3])
    except IndexError:
        x = 0
    Threadsnm = 1
    ANS = manager.dict()
    CUR = manager.dict()
    ANS[1] = ""
    CUR[1] = 0 + x
    Start = time()
    while (Threadsnm <= Threads):
        Thread(target=CompressMT, args=(Threadsnm, srtstr, Threads, srtstrsorted, ANS, CUR, x), daemon=True).start()
        print("Thread " + str(Threadsnm) + " started.")
        Threadsnm += 1
    while (ANS[1] == ""):
        CURTIME = time() - Start
        print(str(CUR[1]/256**7*100) + '% Complete,', f'{CUR[1]:,}' + ' Checked, ' + f'{int(int(CUR[1]-x)//CURTIME):,}' + ' Checked per Second.', end="\r")
        if CUR[1] == 256**7:
            print('File not compressible.')
            exit()
        pass
    print()
    z = int(ANS[1])
    OpenFile.close()
    remove(Filename)
    Filename = Filename + ".CRS"
    z = hex(z)
    OpenFile = open(Filename, "w")
    OpenFile.write(str([z, srtstrsorted]))
    OpenFile.close()
def Main():
    try:
        FileAction = argv[1]
    except IndexError:
        FileAction = 0
    if (FileAction == 0):
        FileAction = input("Would you like to compress or decompress the file? Enter 1 to Compress or 2 to Decompress: ")
    if (FileAction == str("1")):
        print("Compressing")
        Start = time()
        Compress()
        End = time() - Start
        print(str("\n" + "Compression took " + str(int(End)) + " seconds."))
        print("Compressed")
    if (FileAction == str("2")):
        print("Decompressing")
        Start = time()
        Decompress()
        End = time() - Start
        print(str("Decompression took " + str(int(End)) + " seconds."))
        print("Decompressed")
if __name__ == '__main__':
    Main()
