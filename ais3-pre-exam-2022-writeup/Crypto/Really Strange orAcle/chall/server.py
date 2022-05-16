from Crypto.Util.number import getStrongPrime, getRandomRange, isPrime, bytes_to_long
from pathlib import Path
import json
import os

flag = os.environb[b"FLAG"]

keyfile = Path("./key.json")
if keyfile.is_file():
    key = json.loads(keyfile.read_text())
    n = key["n"]
    e = key["e"]
else:
    p = getStrongPrime(1024)
    n = p * p
    while True:
        e = getRandomRange(2, p) | 1
        if isPrime(e):
            break
    keyfile.write_text(json.dumps({"n": n, "e": e}))

flag += os.urandom(2048 // 8 - len(flag))
c = pow(bytes_to_long(flag), e, n)
print(c)

while True:
    x = int(input())
    if x >= 0:
        print(pow(x, e, n))
