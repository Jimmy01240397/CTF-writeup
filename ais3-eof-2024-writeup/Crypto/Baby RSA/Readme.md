# Baby RSA
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/7045274e-382a-4447-bd6b-0890103f4304)

## 解題

進去會給你 N 跟 e 還有用這個 N 跟 e RSA 加密後的 flag 密文

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/ca214c9e-1f44-4961-aa37-7eb8501ecad2)

每次進去的 N 都不一樣，但是 e 都會是 3

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/d3faef7b-6c5d-407a-aa03-c9ff9642b70d)

可以用 [Coppersmith Basic Broadcast Attack](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_coppersmith_attack/)，先收集一定數量的 N 跟 flag 密文，然後用 Broadcast Attack 破解密文就會拿到 flag

## exploit
```python
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
```
```bash
python3 exp.py chal1.eof.ais3.org 10002 20 data.json
python3 exp.py data.json
```


## Flag
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/af4527d1-9682-4ca5-9fd6-9db19a2ba2b3)

`AIS3{c0pPerSMItH$_5hOr7_p@D_a7t4Ck}`
