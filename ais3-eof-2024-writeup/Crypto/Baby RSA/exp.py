import sys
from pwn import *

from Crypto.Util.number import bytes_to_long, long_to_bytes
import json
import gmpy2
from functools import reduce

def modinv(a, m):
    return int(gmpy2.invert(a, m))

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * modinv(p, n_i) * p
    return int(sum % prod)

if len(sys.argv) > 3:
    target = sys.argv[1]
    port = int(sys.argv[2])
    N = []
    c = []
    for a in range(int(sys.argv[3])):
        r = remote(target, port)
        key = r.recvline().strip().decode()
        N.append(str(key.split(',')[0].split('=')[1]))
        c.append(str(r.recvline().strip().decode().split(':')[1].strip()))
        r.close()
    with open(sys.argv[4], 'w') as f:
        f.write(json.dumps({'N': N, 'c': c}))
else:
    with open(sys.argv[1], 'r') as f:
        data = json.loads(f.read())
    m = chinese_remainder([int(a) for a in data['N']], [int(a) for a in data['c']])
    m, state = gmpy2.iroot(m, 3)
    print(hex(int(m)))
    print(long_to_bytes(m))

