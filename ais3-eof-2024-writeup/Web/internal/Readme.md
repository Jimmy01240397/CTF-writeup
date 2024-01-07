# Internal
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/f5f445de-3668-4e00-b166-197c29c0f198)

## 解題
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/4f4b8f77-aeb2-4264-86d7-7371e96bd6e8)

看 code ，似乎是 url 帶 `redir` 參數會被 rediract 到後面的 url

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/cec7b2f9-4786-4c07-b5b4-3c24602f507b)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/59104540-6328-463e-a368-52dab72ef472)

path 用 `/flag` 會被 nginx 擋，所以可能要繞過 nginx 取得後端的 `/flag` api

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/8c81a610-7658-40f6-9514-174c9139ecfe)

仔細看，這邊似乎有 CRLF 的問題（regex 遇到換行會無效，只檢查到換行前）

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/58448297-53f1-4488-8e9c-1b21be1f22f7)

所以我們可以任意更改 response 的 header 或 content。

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/8b4b39fd-e7a3-4bc2-9fa8-730c299e3086)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/85ee4998-a99b-4813-9154-df2fd940fa03)

參考這個 [nginx doc internal](https://nginx.org/en/docs/http/ngx_http_core_module.html#internal)，我們可以增加 `X-Accel-Redirect` header 讓 nginx 收到這個 response 時從 nginx 改成回傳 `/flag` api 的內容。

## exploit
```bash
curl -vvv "$1?redir=$(urlencode "https://google.com
X-Accel-Redirect: /flag")"
```

## Flag
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/bdc8499e-b765-4b59-9e68-f5462358f2a8)

`AIS3{jU$T_sOM3_funNy_N91Nx_FEatur3}`
