from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
from secret import FLAG
from os import urandom
from base64 import b64encode, b64decode

def XOR (a, b):
    return l2b(b2l(a) ^ b2l(b)).rjust(len(a), b"\x00")
    
def counter_add(iv):
    return l2b(b2l(iv) + 1).rjust(16, b"\x00")

# These modes of Block Cipher are just like Stream Cipher. Do you know them?
AES_enc = AES.new(urandom(16), AES.MODE_ECB).encrypt
def AES_CFB (iv, pt):
    ct = b""
    for i in range(0, len(pt), 16):
        _ct = XOR(AES_enc(iv), pt[i : i + 16])
        iv = _ct
        ct += _ct
    return ct

def AES_OFB (iv, pt):
    ct = b""
    for i in range(0, len(pt), 16):
        iv = AES_enc(iv)
        ct += XOR(iv, pt[i : i + 16])
    return ct

def AES_CTR (iv, pt):
    ct = b""
    for i in range(0, len(pt), 16):
        ct += XOR(AES_enc(iv), pt[i : i + 16])
        iv = counter_add(iv)
    return ct

if __name__ == "__main__":
    counter = urandom(16)
    
    c1 = urandom(32)
    c2 = urandom(32)
    c3 = XOR(XOR(c1, c2), FLAG)
    print( f"c1_CFB: ({b64encode(counter)}, {b64encode(AES_CFB(counter, c1))})" )
    counter = counter_add(counter)
    print( f"c2_OFB: ({b64encode(counter)}, {b64encode(AES_OFB(counter, c2))})" )
    counter = counter_add(counter)
    print( f"c3_CTR: ({b64encode(counter)}, {b64encode(AES_CTR(counter, c3))})" )
    
    for _ in range(5):
        try:
            counter = counter_add(counter)
            mode = input("What operation mode do you want for encryption? ")
            pt = b64decode(input("What message do you want to encrypt (in base64)? "))
            pt = pt.ljust( ((len(pt) - 1) // 16 + 1) * 16, b"\x00")
            if mode == "CFB":
                print( b64encode(counter), b64encode(AES_CFB(counter, pt)) )
            elif mode == "OFB":
                print( b64encode(counter), b64encode(AES_OFB(counter, pt)) )
            elif mode == "CTR":
                print( b64encode(counter), b64encode(AES_CTR(counter, pt)) )
            else:
                print("Sorry, I don't understand.")
        except:
            print("??")
            exit()
    