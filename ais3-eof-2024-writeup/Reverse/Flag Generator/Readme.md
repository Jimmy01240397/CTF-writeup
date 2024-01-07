# Flag Generator
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/3be03d23-4734-4307-b379-b51690a44d1b)

## 解題
一個 windows 執行檔

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/fdfa9179-addf-465f-b358-407aa4e23c28)

執行以後他會生成另一個 `flag.exe` 執行檔，但是不知道為甚麼生成的檔案是空的。

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/b2311bde-983d-4ad6-a2ec-5112cc766946)

IDA 打開來看到他會執行 `writeFile` function 來寫 `flag.exe` 檔案

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/4917b70a-c2d3-41ce-94be-3bf3ab333118)

但是這個 `writeFile` 裡面沒有寫寫檔的程式，只有印一串字串到 stdout。

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/a69d73b7-91b7-41d5-8dba-694a577d6807)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/76eb0156-8f7e-4b83-9e2e-fe9713fb4f61)

所以需要 patch 一下，把一些不需要的拿掉，然後把 `fwrite` 改成對這個檔案作用，而不是 `stdout`

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/a1565aae-96d6-4ca3-9fe7-fa67a538764e)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/aae51b36-d1e1-4e62-9c73-acda4d7f4f49)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/16695a9f-44e0-4359-8d88-f5db9bfac5d0)

成功生成 `flag.exe` 以後執行就拿到 flag 了

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/66292f23-80bf-489c-b735-8c9b7d149017)


### Flag
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/0ef9cb8c-9212-4a25-8a5f-e2e74ed83127)

`AIS3{Us1n9_WINd0w5_I$_suCh_@_p@1N....}`
