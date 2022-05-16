from Crypto.Util.number import *
from random import getrandbits
import os

flag = bytes_to_long(os.environb[b"FLAG"])

N_BITS = 1024
PAD_SIZE = 64
p = getPrime(N_BITS // 2 + 1)
q = getPrime(N_BITS // 2 + 1)
n = p * q
e = 11


def generate_padding():
    pad = getrandbits(PAD_SIZE)
    s = 0
    for _ in range(N_BITS // PAD_SIZE):
        s = (s << PAD_SIZE) | pad
    return s


def encrypt(m):
    return pow(m + generate_padding(), e, n)


print(f"{n = }")

while True:
    inp = input("> ")
    if inp == "flag":
        print(encrypt(flag))
    else:
        print(encrypt(int(inp)))
