from pwn import *
import multiprocessing as mp
import threading
import random

def _int32(x):
    return int(0xFFFFFFFF & x)

class MT19937:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        self.mti = 0
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)


    def extract_number(self):
        if self.mti == 0:
            self.twist()
        y = self.mt[self.mti]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        self.mti = (self.mti + 1) % 624
        return _int32(y)


    def twist(self):
        for i in range(0, 624):
            y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = (y >> 1) ^ self.mt[(i + 397) % 624]

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df


def job(i, data, outdata):
    #print("start: " + str(i * 0x100000))
    #rm = MT19937(i)
    rm = random.Random()
    for x in range(i * 0x35000, (i + 1) * 0x35000):
        rm.seed(x)
        good = True
        for a in range(624):
            if rm.getrandbits(32) % 10 != data[a][0]:
                good = False
                break
        if good:
            print("get: " + str(x))
            outdata.put(x)
            break

if __name__=='__main__':
    random
    conn = remote('1337pins.balsnctf.com', 27491)

    cont = int(input("runcont: "))

    for a in range(cont * 624):
        conn.sendline('5'.encode())

    nowdata = conn.recvrepeat(timeout = 0.5).decode().splitlines()
    assert len(nowdata) == cont * 624

    ans = [ [ nowdata[i * 624 + x] for i in range(cont) ] for x in range(624) ]

    ansseed = mp.Queue()

    alljob = []
    for i in range(_int32(0x4D49)):
        p = mp.Process(target=job, args=(i, ans, ansseed))
        #p = threading.Thread(target=job, args=(i, ans, ansseed))
        #p.start()
        #print("now: " + str(i))
        alljob.append(p)
                
    print("start")
    for now in alljob:
        now.start()
        if ansseed.qsize() != 0:
            break

    for now in alljob:
        now.join()
        if ansseed.qsize() != 0:
            break
    print("nowend")
    
    getansseed = [ ansseed.get() for x in range(ansseed.qsize()) ]
    
    print("ans=" + str(getansseed))
    
    if len(getansseed) != 0:
        rm = random.Random()
        rm.seed(getansseed[0])
        for a in range(cont * 624):
            rm.getrandbits(32)
            
        for a in range(1338):
            now = rm.getrandbits(32) % 10
            conn.sendline(str(now).encode())
        
        print(conn.recvrepeat(timeout = 0.5).decode())
    else:
        print("error")