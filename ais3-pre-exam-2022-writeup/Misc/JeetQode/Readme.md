# JeetQode
## 題目
![image](https://user-images.githubusercontent.com/57281249/168675294-9bf6383f-02ff-4d65-ba3e-bb02aece6255.png)

## 解題
這題就 judge 而已，只是要用 jq，老實說 jq 我一直都有再用，但用這麼深還是第一次。
到 [JQ 的 document](https://stedolan.github.io/jq/manual/) 找可以用的指令然後實現題目要求這樣而已(code 有點長因為沒規定長度所以沒特別壓)。

## Code
1. `. == (explode | reverse | implode)`
2. `walk(if type == "object" then (setpath(["tmp"]; .left) | setpath(["left"]; .right) | setpath(["right"]; .tmp) | delpaths([["tmp"]])) else . end)`
3. `.body | walk(if type == "object" and (has("value") | not) then (if ([.op] | contains(["Add"])) then setpath(["value"]; (.left.value + .right.value)) else (if ([.op] | contains(["Sub"])) then setpath(["value"]; (.left.value - .right.value)) else (if ([.op] | contains(["Mult"])) then setpath(["value"]; (.left.value * .right.value)) else (if ([.op] | contains(["Div"])) then setpath(["value"]; (.left.value / .right.value)) else . end) end) end) end) else . end) | .value`

![image](https://user-images.githubusercontent.com/57281249/168675477-8291831f-8eef-4fe8-9d54-c206a2e0d4e4.png)

## Flag
`AIS3{pr0gramm1ng_in_a_json_proce55in9_too1}`

