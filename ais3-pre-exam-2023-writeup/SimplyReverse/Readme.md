# Simply Reverse
## 題目

![image](https://user-images.githubusercontent.com/57281249/239952354-903f8815-c99c-414f-ada7-f5559bcd8636.png)

## 解題
1. IDA 打開
2. 讀 verify
![image](https://user-images.githubusercontent.com/57281249/239953043-467c41c6-7739-4d32-9c1f-723478da6244.png)
3. 看起來是把 encrypted 依照 index 做 rotation 就會得到 flag
4. 找 encrypted 的位置把 hex 複製下來
![image](https://user-images.githubusercontent.com/57281249/239955653-08e2130a-4c36-4935-94eb-f587269729c0.png)
5. 然後寫 code 算回來
``` python
import sys
def rotation(nowbyte, length):
    return (((nowbyte >> length) & 255) | ((nowbyte << (8 - length)) & 255)) & 255

enbytes = bytes.fromhex("8A5092C8063D5B95B6521B35825AEAF8942872DDD45DE329BA5852A8643581AC0A64")

ansbytes = []
for i in range(len(enbytes)):
    usebyte = enbytes[i] - 8
    if usebyte < 0:
        usebyte += 2**8
    ansbytes.append((rotation(usebyte, (i ^ 9) & 3) ^ i) & 255)

sys.stdout.buffer.write(bytes(ansbytes))
#print(bytes(ansbytes))
```

## Flag
`AIS3{0ld_Ch@1_R3V1_fr@m_AIS32016!}`
