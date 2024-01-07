#! /usr/bin/python3
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
import os

from secret import FLAG

def encrypt(m, e, n):
    enc = pow(bytes_to_long(m), e, n)
    return enc

def decrypt(c, d, n):
    dec = pow(c, d, n)
    return long_to_bytes(dec)


if __name__ == "__main__":
    
    while True:
        p = getPrime(1024)
        q = getPrime(1024)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 3
        if phi % e != 0 : 
            d = pow(e, -1, phi)
            break
    
    print(f"{n=}, {e=}")
    print("FLAG: ", encrypt(FLAG, e, n))
    
    for _ in range(3):
        try:
            c = int(input("Any message for me?"))
            m = decrypt(c, d, n)
            print("How beautiful the message is, it makes me want to destroy it .w.")
            new_m = long_to_bytes(bytes_to_long(m) ^ bytes_to_long(os.urandom(8)))
            print( "New Message: ", encrypt(new_m, e, n) )
        except:
            print("?")
            exit()
        