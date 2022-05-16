# Gift in the dream
## 題目

## 解題
`binwalk gift_in_the_dream.gif` 一下發現啥都沒有。

`strings gift_in_the_dream.gif` 一下看到一堆重複出現的奇怪字串，應該是提示。

通靈一下發現應該要用 identify 把每個幀數間的間距時間抓出來應該就是 flag 了。

## Script

``` bash
#!/bin/bash

for a in $(identify -format "%s %T \n" gift_in_the_dream.gif | awk '{print $2}')
do
    printf "%02X" $a | xxd -r -p
done
```

## Flag
`AIS3{5T3gn0gR4pHy_c4N_b3_fUn_s0m37iMe}`