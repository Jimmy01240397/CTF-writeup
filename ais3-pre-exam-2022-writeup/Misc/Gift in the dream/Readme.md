# Gift in the dream
## 題目
![image](https://user-images.githubusercontent.com/57281249/168673698-16d3c232-db1c-4d69-a3c0-9970b5503f32.png)

## 解題
`binwalk gift_in_the_dream.gif` 一下發現啥都沒有。
![image](https://user-images.githubusercontent.com/57281249/168673798-46ea4b75-0057-40ed-84a7-8b8960af17c5.png)

`strings gift_in_the_dream.gif` 一下看到一堆重複出現的奇怪字串，應該是提示。
![image](https://user-images.githubusercontent.com/57281249/168673891-c278d846-63a4-4d04-9323-9f5107eaaf25.png)

通靈一下發現應該要用 identify 把每個幀數間的間距時間抓出來應該就是 flag 了。
![image](https://user-images.githubusercontent.com/57281249/168673950-126f0c6a-39d7-46ad-ac6d-00dc62b475fd.png)

## Script

``` bash
#!/bin/bash

for a in $(identify -format "%s %T \n" gift_in_the_dream.gif | awk '{print $2}')
do
    printf "%02X" $a | xxd -r -p
done
```
![image](https://user-images.githubusercontent.com/57281249/168674150-9425fae5-e7af-4ab2-8de2-65af515d8752.png)

## Flag
`AIS3{5T3gn0gR4pHy_c4N_b3_fUn_s0m37iMe}`
