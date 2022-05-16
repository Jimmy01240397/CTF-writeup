# Knock
## 題目
![image](https://user-images.githubusercontent.com/57281249/168674246-cecba6af-39e8-43a6-97fe-0017f75890c3.png)

## 解題
原本以為是 Web 題，後來想想又好像不對，request 抓出來改用 curl 跑。
`curl -X POST http://chals1.ais3.org:13337/ -d 'token=<token>'`
回傳的東西都是
`<p>I have knock on the <ip></p>`
於是馬上開 wireshark
![image](https://user-images.githubusercontent.com/57281249/168674437-9b199fe4-bb49-49e0-9cd3-8220e096b498.png)

果然，而且 dest port 明顯很像 ascii，應該接起來就 flag 了。

## Script
### iptables
``` bash
iptables -I INPUT 1 -i ais3pre2022 -p udp -s 10.113.203.111 -j LOG --log-prefix "FORAIS3"
```

### rsyslog
```
if $msg contains "FORAIS3" then {
    ^<script path>
    stop
}
```

### shell script
```
#!/bin/bash

splitinspace()
{
    for a in $(cat $1)
    do
        echo $a
    done
}

port=`echo $1 | splitinspace | grep DPT | cut -c 5- | sed 's/12//g'`

echo "$(cat /tmp/output)$(printf "%02X\n" $(python3 -c "print(int('$port'))") | xxd -r -p)" > /tmp/output
```

### 執行結果
```
root@jimmyGW:~# curl -X POST http://chals1.ais3.org:13337/ -d 'token=<token>'
<p>I have knock on the <ip></p>
root@jimmyGW:~# vi /tmp/output
```
![image](https://user-images.githubusercontent.com/57281249/168674549-123dd8ae-46c0-4073-b4b2-d8d0d080bb79.png)

## Flag
`AIS3{kn0ckKNOCKknock}`
