# Knock
## 題目

## 解題
原本以為是 Web 題，後來想想又好像不對，request 抓出來改用 curl 跑。
`curl -X POST http://chals1.ais3.org:13337/ -d 'token=<token>'`
回傳的東西都是
`<p>I have knock on the <ip></p>`
於是馬上開 wireguard

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



## Flag
`AIS3{kn0ckKNOCKknock}`