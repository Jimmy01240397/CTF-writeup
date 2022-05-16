# Strings
## 題目

## 解題
既然叫 strings 那就先 strings 一次

噴出來的 flag 是假的，但也是提示

把阿姨開起來打開 String view 搜假 flag 點兩下到 IDA View 接著 `.data.rel.ro:000055CBACEDDDB0` 點兩下跳過去，然後再網上一點可以看到 `off_55CBACEDDDA0`(應該是變數名稱ㄅ) 點兩下 `strings::main::h34e687dfba9cc523` 就能直達主程式的地方

F5 反編譯然後開始跑 Debug

可以看到有一個 `core::str::_$LT$impl$u20$str$GT$::split` 這應該是 Rust 寫的，可以看到有一個 `"_"` 參數，應該是用 `"_"` 去拆分字串

而後來在走到這邊時得到確認 `if ( alloc::vec::Vec$LT$T$C$A$GT$::len::hd32fa3309483c80e(v41) == 11 )` 代表 split 後的字串要有 11 個

`if ( (core::cmp::impls::_$LT$impl$u20$core..cmp..PartialEq$LT$$RF$B$GT$$u20$for$u20$$RF$A$GT$::ne::h0948eadbdbca5c0e( v25, &(&off_55CBACEDDDA0)[2 * v21]) & 1) != 0 )`
這邊的話應該是  `v25 != &(&off_55CBACEDDDA0)[2 * v21]` 的話就算 `incorrect flag` 而 `v21` 則是從上面一個 `dest` array 來的

`dest` array 的內容是 `[0x0, 0x4, 0x10, 0xD, 0xA, 0x4, 0x8, 0x7, 0x1, 0x2, 0x12]` 換 10 進的話是 `[0, 4, 16, 13, 10, 4, 8, 7, 1, 2, 18]`

再找切分依據找了一陣子，最後有注意到 `if ( v21 >= 0x13 )` 跑一個程式而且 Array 最後也是 18 而且剛好只有 11 個，我猜應該是最多只有 18 組。

回到 `off_55CBACEDDDA0` 的 IDA View 時，又注意到它這邊有分 11 行，每行剛好就前進一個單字，除了第一個 "AIS3{" 跟最後一個 "}" 
於是我認為它的切分應該是長這樣 `AIS3{_good_luck_finding_the_flags_value_using_strings_command_guess_which_substring_is_our_actual_answer_lmaoo_}`

接著就簡單了，按照 dest 一個一個接回來送 ./strings 也回 correct flag 這樣就解掉了

## Flag
`AIS3{_the_answer_is_guess_the_strings_using_good_luck_}`