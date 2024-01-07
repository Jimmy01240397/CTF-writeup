# Stateful
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/6e785309-6170-49fc-9714-773494905188)

## 解題
他是一個 linux ELF 執行檔

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/3cbe0887-c8f5-4deb-81cd-a9db1934a7d2)

執行後直接噴 `WRONG!!!`

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/45672138-30f9-4aa2-9fdb-1bfc8458ad8d)

似乎執行時要輸入一個長度為 43 的字串參數，應該是 flag，這個字串會經過 `state_machine` function 運算後跟 `k_target` 裡的資料一個一個做比對。

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/ba46bbd0-0178-4bb9-9ada-cd8c3a15d4ea)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/fe1e25b7-1250-4702-8e97-b66f05fa000d)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/fe6d21e3-06f3-4066-a609-ff1ab19b485e)

把 `k_target` 複製出來

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/0f29e032-b311-41a9-844f-fea2b7f80b72)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/99d07b7c-a60d-4e3e-943a-8d80877ec0de)

`state_machine` 裡面會有一坨判斷並且會按照某個特定順序執行裡面的這些 function，設定中斷點做 debug 逐步執行，並且記錄這些 function 的執行過程

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/3e1242d3-c80f-4e09-85b1-760079fdc09e)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/85b6eea0-8d58-460a-804a-502a843ce8f1)

得到：

```
state_3618225054
state_2057902921
state_671274660
state_2357240312
state_1438496410
state_2263885268
state_4260333374
state_3995931083
state_3844354947
state_2421543205
state_416430256
state_2373489361
state_2202680315
state_4026467378
state_1765279360
state_2131447726
state_1132589236
state_3443361864
state_2098792827
state_4237907356
state_269727185
state_1780152111
state_4046605750
state_3544494813
state_4008735947
state_2309210106
state_3908914479
state_2095151013
state_2816834243
state_4165665722
state_3656605789
state_1154341356
state_809393455
state_1093244921
state_1595228866
state_2316743832
state_2907124712
state_3507844042
state_3907553856
state_1929982570
state_4130555047
state_794507810
state_1843624184
state_3901233957
state_126130845
state_71198295
state_557589375
state_3420754995
state_3648003850
state_1978986903
```
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/4d3b76db-9a4d-478d-9864-adf0d9bd9449)

這些 function 的內部都是一個加減法運算，所以我們按照這個順序反過來把 `k_target` 推回去就會拿到 flag 了

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/404e0876-0838-4e42-aa21-6c555933b623)


## exploit
```python
data = bytearray(b'\x9E\x26\xEC\x33\xE6\x03\xF4\x3A\x6B\x62\x85\x75\x5F\xC4\xD1\x81\x3B\xEC\xF8\xB0\xFA\x34\x4C\xF2\x58\x72\x5F\x0D\x54\x34\x7B\x22\xCD\x33\x53\x53\xC3\xFA\x54\x80\x33\xCC\x7D')
data = [int(a) for a in data]

data[5] -= data[37] + data[20]
data[8] -= data[14] + data[16]
data[17] -= data[38] + data[24]
data[15] -= data[40] + data[8]
data[37] -= data[12] + data[16]
data[4] -= data[6] + data[22]
data[10] += data[12] + data[22]
data[18] -= data[26] + data[31]
data[23] -= data[30] + data[39]
data[4] -= data[27] + data[25]
data[37] -= data[27] + data[18]
data[41] += data[3] + data[34]
data[13] -= data[26] + data[8]
data[2] -= data[34] + data[25]
data[0] -= data[28] + data[31]
data[4] -= data[7] + data[25]
data[18] -= data[29] + data[15]
data[21] += data[13] + data[42]
data[21] -= data[34] + data[15]
data[7] -= data[10] + data[0]
data[13] -= data[25] + data[28]
data[32] -= data[5] + data[25]
data[31] -= data[1] + data[16]
data[1] -= data[16] + data[40]
data[30] += data[13] + data[2]
data[1] -= data[15] + data[6]
data[7] -= data[21] + data[0]
data[24] -= data[20] + data[5]
data[36] -= data[11] + data[15]
data[0] -= data[33] + data[16]
data[19] -= data[10] + data[16]
data[1] += data[29] + data[13]
data[30] += data[33] + data[8]
data[15] -= data[22] + data[10]
data[20] -= data[19] + data[24]
data[27] -= data[18] + data[20]
data[39] += data[25] + data[38]
data[23] -= data[7] + data[34]
data[37] += data[29] + data[3]
data[5] -= data[40] + data[4]
data[17] -= data[0] + data[7]
data[9] -= data[11] + data[3]
data[31] -= data[34] + data[16]
data[16] -= data[25] + data[11]
data[14] += data[32] + data[6]
data[6] -= data[10] + data[41]
data[2] -= data[11] + data[8]
data[0] += data[18] + data[31]
data[9] += data[2] + data[22]
data[14] -= data[35] + data[8]

data = [(a + 512) % 256 for a in data]

print(data)

print(bytes(data))
```

## Flag
![image](https://hackmd.io/_uploads/BydqqnUOT.png)
`AIS3{arE_Y0u_@_sTATEfuL_Or_ST4t3L3SS_CTF3R}`
