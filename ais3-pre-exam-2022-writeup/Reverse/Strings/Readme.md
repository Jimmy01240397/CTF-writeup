# Strings
## 題目
![image](https://user-images.githubusercontent.com/57281249/168676539-b52b4be4-cace-42f7-89b8-3e88fe25c4c8.png)

## 解題
既然叫 strings 那就先 strings 一次

![image](https://user-images.githubusercontent.com/57281249/168676653-150a2672-4bb4-4bcc-90cc-e87ba30b2295.png)

噴出來的 flag 是假的，但也是提示

把阿姨開起來打開 String view 搜假 flag 點兩下到 IDA View 接著 `.data.rel.ro:000055CBACEDDDB0` 點兩下跳過去，然後再網上一點可以看到 `off_55CBACEDDDA0`(應該是變數名稱ㄅ) 點兩下 `strings::main::h34e687dfba9cc523` 就能直達主程式的地方

![image](https://user-images.githubusercontent.com/57281249/168676850-47fe0177-b77d-481c-b091-6def6c6b60f8.png)

![image](https://user-images.githubusercontent.com/57281249/168676909-3c464331-ab05-446d-9e61-1794a127c2f8.png)

![image](https://user-images.githubusercontent.com/57281249/168676966-ccfc3bb2-4cb5-4dbb-9831-e2fa57dddd4d.png)

![image](https://user-images.githubusercontent.com/57281249/168677209-3291d2fc-a304-4aac-9f5d-7225d8929211.png)

F5 反編譯然後開始跑 Debug

![image](https://user-images.githubusercontent.com/57281249/168677122-fa3f1c6f-b32e-4d8d-9cc0-42978091b2c9.png)

可以看到有一個 `core::str::_$LT$impl$u20$str$GT$::split` 這應該是 Rust 寫的，可以看到有一個 `"_"` 參數，應該是用 `"_"` 去拆分字串

![image](https://user-images.githubusercontent.com/57281249/168677345-1eaed10e-80e6-4aa7-91f2-bbb13ad0a256.png)

而後來在走到這邊時得到確認 `if ( alloc::vec::Vec$LT$T$C$A$GT$::len::hd32fa3309483c80e(v41) == 11 )` 代表 split 後的字串要有 11 個

![image](https://user-images.githubusercontent.com/57281249/168677418-25d50774-255d-4e7d-92fc-c25de01e02fc.png)

`if ( (core::cmp::impls::_$LT$impl$u20$core..cmp..PartialEq$LT$$RF$B$GT$$u20$for$u20$$RF$A$GT$::ne::h0948eadbdbca5c0e( v25, &(&off_55CBACEDDDA0)[2 * v21]) & 1) != 0 )`
這邊的話應該是  `v25 != &(&off_55CBACEDDDA0)[2 * v21]` 的話就算 `incorrect flag` 而 `v21` 則是從上面一個 `dest` array 來的

![image](https://user-images.githubusercontent.com/57281249/168677576-7b5264c9-81f0-4077-8df5-03fa0c17708d.png)

`dest` array 的內容是 `[0x0, 0x4, 0x10, 0xD, 0xA, 0x4, 0x8, 0x7, 0x1, 0x2, 0x12]` 換 10 進的話是 `[0, 4, 16, 13, 10, 4, 8, 7, 1, 2, 18]`

![image](https://user-images.githubusercontent.com/57281249/168678100-55920cd6-2e69-4f9e-8d1f-b1268b11d12a.png)

再找切分依據找了一陣子，最後有注意到 `if ( v21 >= 0x13 )` 符合的話會跑一個程式而且 Array 最後也是 18 而且剛好只有 11 個，我猜應該是最多只有 18 組。

![image](https://user-images.githubusercontent.com/57281249/168678269-458e7911-5b3d-48f6-8b62-5a7bd44b7c1e.png)

回到 `off_55CBACEDDDA0` 的 IDA View 時，又注意到它這邊有分 18 行，每行剛好就前進一個單字，除了第一個 "AIS3{" 跟最後一個 "}" 

![image](https://user-images.githubusercontent.com/57281249/168678438-91012e82-e331-43b6-8ba2-749c4d129a77.png)

於是我認為它的切分應該是長這樣 `AIS3{_good_luck_finding_the_flags_value_using_strings_command_guess_which_substring_is_our_actual_answer_lmaoo_}`

接著就簡單了，按照 dest 一個一個接回來送 ./strings 也回 correct flag 這樣就解掉了

## Flag
`AIS3{_the_answer_is_guess_the_strings_using_good_luck_}`
