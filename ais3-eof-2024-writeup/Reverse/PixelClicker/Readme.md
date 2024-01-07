# PixelClicker
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/0728f691-eff5-4ab0-bf26-40d4f319bf19)

(本題是賽後解的)

## 解題
一個充滿了點點的正方形的 windows from，這接點點（pixel）可以點擊

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/70b2aa04-a4ef-4707-b492-3310618aab71)

IDA 打開來看翻一翻，翻到 `sub_7FF7059813B0` function 應該是處理點擊 pixel 的 function

最下面的 switch 是處理計數的，點擊次數是存在 `dword_7FF705985708` 這個 global var 裡

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/72ef7d61-735f-4649-9ca6-dd9e3da2cf97)

上面的 if 是判斷遊戲成功或失敗以及結束的區段。

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/4913f88e-2945-467c-9551-db008456d441)

可以發現她會叫你點 600 次以上才結束

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/cebb170d-f9e5-4d24-9c0e-16dc496086d8)

最後通靈一下應該要把 Block 挖出來存起來看看。

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/8a2b2ffe-f6c7-4280-a7e2-b064a5a31978)

因為 600 次太久了，所以把他 patch 成點 1 次就好

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/8a2f7627-1cb1-4f23-ad2f-32cc5bba516f)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/c118eb07-af8f-43a5-a301-408297ae95b8)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/1923ca83-0adb-4a3c-813c-b9014645ac59)

中斷點設置在執行完 Block 以後

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/176512aa-3f28-4a07-8d75-f4102b91f56e)

找到 Block 的位置後，把她的資料在 Hex view 全部選取

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/6b4260c2-15a7-4c4a-af95-7ca64b8ff9ca)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/7707d000-ab8a-49d5-b674-e6c9ac516952)

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/1296e037-2f79-47c1-b3cc-65e3537b379c)

右鍵 save file

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/eb7411d6-450e-4917-a7ec-a131264fd044)

然後開 cmd 用 file 看一下發現他長度有 1440054 bytes

![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/73d6157e-ce99-45f2-b95e-5702cce3484f)

剛剛選取的不夠的話在重新做一次選取 1440054 bytes 然後 save file

最後用圖片的方式開，可以看到這張圖片

## Flag

![data](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/82b2e164-ad8f-41ec-a2a5-f6f7188b1c65)

`AIS3{jUSt_4_5imPLE_clICkEr_g@m3}`
