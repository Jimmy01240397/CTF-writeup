from pwn import *

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



conn = remote('1337pins.balsnctf.com', 27491)

cont = int(input("runcont: "))

for a in range(cont * 624):
    conn.sendline('5'.encode())

nowdata = conn.recvrepeat(timeout = 0.5).decode().splitlines()
assert len(nowdata) == cont * 624

ans = [ [ nowdata[i * 624 + x] for i in range(cont) ] for x in range(624) ]

ansseed = -1
for i in range(_int32(0xFFFFFFFF)):
    rm = MT19937(i)
    good = True
    for a in range(624):
        if rm.extract_number() % 10 != ans[a][0]:
            good = False
            break
    if good:
        ansseed = i
        break
    if i % 0xFFF == 0:
        print("now: " + str(i))



print("ans=" + str(ansseed))



