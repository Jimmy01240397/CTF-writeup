# Robot
## 題目

![image](https://user-images.githubusercontent.com/57281249/239931354-afd14468-755c-4429-93a4-720e96efa0ac.png)

## 解題
``` python
import pwn
import re

r = pwn.remote('chals1.ais3.org', 12348)

r.recvline()
r.recvline()

while True:
    now = r.recv(timeout=1)
    print(now.decode().strip())
    groups = re.match(b'\s*(\d*)\s*([^\s\d]*)\s*(\d*)', now)
    ans = b''
    if groups.group(2) in b'+-*/':
        ans = str(eval(f'{groups.group(1).decode()}{groups.group(2).decode()}{groups.group(3).decode()}')).encode()
        print(f'ans: {ans.decode()}')
        r.sendline(ans)
    else:
        print('bad')
```
```
chummy@hitcon:~/ais3preexam2023$ python3 robotexp.py                                                                                                                                                      [30/53][+] Opening connection to chals1.ais3.org on port 12348: Done
9  +  8
ans: 17
8+9
ans: 17
8        +        5
ans: 13
1  *  5
ans: 5
9 + 7
ans: 16
2 + 4
ans: 6
3  *  9
ans: 27
10+6
ans: 16
6  +  10
ans: 16
3 * 3
ans: 9
6*9
ans: 54
3 * 8
ans: 24
8*7
ans: 56
8 * 1
ans: 8
6    +    3
ans: 9
9     +     7
ans: 16
1*1
ans: 1
3     *     4
ans: 12
6 + 4
ans: 10
7     *     9
ans: 63
3     +     9
ans: 12
8  +  2
ans: 10
1+1
ans: 2
9     *     3
ans: 27
3  *  2
ans: 6
6*2
ans: 12
6+5
ans: 11
1+2
ans: 3
7  *  2
ans: 14
print('Segmentation fault (core dumped)'), exit(139)
bad
6  *  4
ans: 24
Congratulations! Flag: AIS3{don't_eval_unknown_code_or_pipe_curl_to_sh}
bad
Traceback (most recent call last):
  File "/home/chummy/ais3preexam2023/robotexp.py", line 10, in <module>
    now = r.recv(timeout=1)
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/tube.py", line 104, in recv
    return self._recv(numb, timeout) or b''
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/tube.py", line 174, in _recv
    if not self.buffer and not self._fillbuffer(timeout):
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/tube.py", line 153, in _fillbuffer
    data = self.recv_raw(self.buffer.get_fill_size())
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/sock.py", line 56, in recv_raw
    raise EOFError
EOFError
[*] Closed connection to chals1.ais3.org port 12348
```

## Flag
`AIS3{don't_eval_unknown_code_or_pipe_curl_to_sh}`