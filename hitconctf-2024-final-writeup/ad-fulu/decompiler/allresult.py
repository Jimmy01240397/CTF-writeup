# Import header start
import sys
import hashlib
import base64
import json
import os
import hmac
import hashlib
from db import connect
import random
import re
import time
from urllib.parse import urlparse, parse_qs
# Import header end

def content_type(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _e8484006 = 0
    _d34f0d0e = 0
    _9f3eb4f3 = 0
    _0f4a0c84 = 0
    _2c411011 = 0
# Var header end
    _e8484006 = dict()
    _e8484006["png"] = "image/png"
    _e8484006["jpg"] = "image/jpg"
    _e8484006["txt"] = "text/plain"
    _e8484006["html"] = "text/html"
    _e8484006["css"] = "text/css"
    _e8484006["js"] = "text/javascript"
    _d34f0d0e = "application/octet-stream"
    _9f3eb4f3 = arg1.split(".")
    _0f4a0c84 = _9f3eb4f3[(-1)]
    return _e8484006.get(_0f4a0c84, _d34f0d0e)

def cookie_logic(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _c14e4aa7 = 0
    _51aee973 = 0
    _4c0a2db0 = 0
    _b4850f7c = 0
    _f06f0984 = 0
    _998c7b85 = 0
    _f13401ea = 0
    _e712f255 = 0
    _36625c8f = 0
    _2c411011 = 0
# Var header end
    _c14e4aa7 = parse_cookie()
    if _c14e4aa7:
        _51aee973 = _c14e4aa7.get("e", (-1))
        _51aee973 = int(_51aee973)
        _4c0a2db0 = _c14e4aa7.get("n", (-1))
        _4c0a2db0 = int(_4c0a2db0)
        _b4850f7c = _c14e4aa7.get("k", (-1))
        _b4850f7c = int(_b4850f7c)
        if (_b4850f7c > 5):
            return None
        else:
            pass
        if (_51aee973 > 50):
            return None
        else:
            pass
        if (1 > _4c0a2db0):
            return None
        else:
            pass
        _f06f0984 = 1
        for _998c7b85 in range(_b4850f7c):
            _f13401ea = (_f06f0984 * _51aee973)
            _f06f0984 = _f13401ea
        _e712f255 = (_f06f0984 % _4c0a2db0)
        _36625c8f = (_e712f255 == 0)
        return _36625c8f
    else:
        pass
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def debug(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _cd49df89 = 0
    _7dcd9d3f = 0
    _2c411011 = 0
# Var header end
    print("Content-Type: text/html\n", flush=True)
    print(get_all_string(), flush=True)
    _cd49df89 = read_flag()
    _cd49df89 = (_cd49df89 + arg1)
    _cd49df89 = _cd49df89.encode()
    _7dcd9d3f = _051a0925.blake2b(_cd49df89)
    _7dcd9d3f = _7dcd9d3f.hexdigest()
    print(_7dcd9d3f, flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def decode_dict(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _e1f463f2 = 0
    _ca73d5c2 = 0
    _30d1641c = 0
    _2c411011 = 0
# Var header end
    _e1f463f2 = arg1.encode()
    _ca73d5c2 = decode_payload(_e1f463f2)
    _30d1641c = _209b01af.loads(_ca73d5c2)
    return _30d1641c

def decode_payload(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _e918d361 = 0
    _8cb402c6 = 0
    _baae64b8 = 0
    _9b5d0732 = 0
    _30d1641c = 0
    _2c411011 = 0
# Var header end
    _e918d361 = (-len(arg1))
    _8cb402c6 = (_e918d361 % 4)
    _baae64b8 = (b'=' * _8cb402c6)
    _9b5d0732 = (arg1 + _baae64b8)
    _30d1641c = _26c54c9e.urlsafe_b64decode(_9b5d0732)
    return _30d1641c

def do_GET(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _a0bfb1f7 = 0
    _0d217581 = 0
    _9f757196 = 0
    _c8bbc40c = 0
    _79028c95 = 0
    _49a5cf47 = 0
    _b99eaf90 = 0
    _889b1cd6 = 0
    _9e29d9a3 = 0
    _8c9bae25 = 0
    _2c411011 = 0
# Var header end
    _a0bfb1f7 = _34592586.getenv("REQUEST_URI", "")
    _0d217581 = urlparse(_a0bfb1f7)
    _9f757196 = _0d217581.path
    _9f757196 = parse_path(_9f757196, "/cgi-bin/index.py")
    _c8bbc40c = _34592586.getenv("QUERY_STRING", "")
    _79028c95 = parse_qs(_c8bbc40c)
    if (_9f757196 == "/"):
        serve_home()
    else:
        if _9f757196.startswith("/static/"):
            _49a5cf47 = parse_path(_9f757196, "/static/")
            serve_static(_49a5cf47)
        else:
            if (_9f757196 == "/debug"):
                _b99eaf90 = _79028c95.get("salt", [""])
                _b99eaf90 = _b99eaf90[0]
                debug(_b99eaf90)
            else:
                if (_9f757196 == "/login"):
                    serve_login()
                else:
                    if (_9f757196 == "/logout"):
                        serve_logout()
                    else:
                        _889b1cd6 = cookie_logic()
                        if (_889b1cd6 == False):
                            send_status(404, True)
                        else:
                            pass
                        if _9f757196.startswith("/poetry/"):
                            _49a5cf47 = parse_path(_9f757196, "/poetry/")
                            _9e29d9a3 = int(_49a5cf47)
                            serve_poetry(_9e29d9a3)
                        else:
                            if (_9f757196 == "/poetry"):
                                serve_poetry(None)
                            else:
                                if (_9f757196 == "/register"):
                                    serve_register()
                                else:
                                    if (_9f757196 == "/credit/flag"):
                                        serve_credit_prize()
                                    else:
                                        if (_9f757196 == "/credit"):
                                            if _79028c95.get("name"):
                                                _8c9bae25 = _79028c95.get("name", [""])
                                                _8c9bae25 = _8c9bae25[0]
                                                serve_credit_detail(_8c9bae25)
                                            else:
                                                serve_credit()
                                        else:
                                            if (_9f757196 == "/light"):
                                                serve_light()
                                            else:
                                                if (_9f757196 == "/poe"):
                                                    serve_poe()
                                                else:
                                                    send_status(404, True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def do_HEAD(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _a0bfb1f7 = 0
    _0d217581 = 0
    _9f757196 = 0
    _c8bbc40c = 0
    _79028c95 = 0
    _2c411011 = 0
# Var header end
    _a0bfb1f7 = _34592586.getenv("REQUEST_URI", "")
    _0d217581 = urlparse(_a0bfb1f7)
    _9f757196 = _0d217581.path
    _9f757196 = parse_path(_9f757196, "/cgi-bin/index.py")
    _c8bbc40c = _34592586.getenv("QUERY_STRING", "")
    _79028c95 = parse_qs(_c8bbc40c)
    print("Content-Type: text/html\n", flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def do_OPTIONS(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _a0bfb1f7 = 0
    _0d217581 = 0
    _9f757196 = 0
    _c8bbc40c = 0
    _79028c95 = 0
    _2c411011 = 0
# Var header end
    _a0bfb1f7 = _34592586.getenv("REQUEST_URI", "")
    _0d217581 = urlparse(_a0bfb1f7)
    _9f757196 = _0d217581.path
    _9f757196 = parse_path(_9f757196, "/cgi-bin/index.py")
    _c8bbc40c = _34592586.getenv("QUERY_STRING", "")
    _79028c95 = parse_qs(_c8bbc40c)
    print("Content-Type: text/html\n", flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def do_POST(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _a0bfb1f7 = 0
    _0d217581 = 0
    _9f757196 = 0
    _c8bbc40c = 0
    _79028c95 = 0
    _889b1cd6 = 0
    _2c411011 = 0
# Var header end
    _a0bfb1f7 = _34592586.getenv("REQUEST_URI", "")
    _0d217581 = urlparse(_a0bfb1f7)
    _9f757196 = _0d217581.path
    _9f757196 = parse_path(_9f757196, "/cgi-bin/index.py")
    _c8bbc40c = _34592586.getenv("QUERY_STRING", "")
    _79028c95 = parse_qs(_c8bbc40c)
    if (_9f757196 == "/login"):
        login()
    else:
        _889b1cd6 = cookie_logic()
        if (_889b1cd6 == False):
            send_status(404, True)
        else:
            if (_9f757196 == "/register"):
                handle_register()
            else:
                if (_9f757196 == "/poetry"):
                    handle_poetry()
                else:
                    if (_9f757196 == "/credit"):
                        handle_credit()
                    else:
                        if (_9f757196 == "/light"):
                            handle_light()
                        else:
                            if (_9f757196 == "/poe"):
                                handle_poe()
                            else:
                                send_status(404, True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def draw_poetry(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _0d795380 = 0
    _2c411011 = 0
# Var header end
    _0d795380 = range(60)
    return _eb09e7b4.choice(_0d795380)

def encode_dict(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _9afdb9ef = 0
    _30d1641c = 0
    _2c411011 = 0
# Var header end
    _9afdb9ef = _209b01af.dumps(arg1)
    _9afdb9ef = _9afdb9ef.encode()
    _30d1641c = encode_payload(_9afdb9ef)
    return _30d1641c

def encode_payload(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _9afdb9ef = 0
    _30d1641c = 0
    _2c411011 = 0
# Var header end
    _9afdb9ef = _26c54c9e.urlsafe_b64encode(arg1)
    _30d1641c = _9afdb9ef.replace(b'=', b'')
    return _30d1641c

def generate_jwt(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _95907f49 = 0
    _68638e9f = 0
    _d3c0131a = 0
    _f00c9bc8 = 0
    _032939c7 = 0
    _277829a6 = 0
    _4f684b22 = 0
    _bdfcc3a7 = 0
    _3dd511ed = 0
    _30d1641c = 0
    _2c411011 = 0
# Var header end
    _95907f49 = dict()
    _95907f49["alg"] = "HS256"
    _95907f49["typ"] = "JWT"
    _68638e9f = _34592586.getrandom(16)
    _68638e9f = encode_payload(_68638e9f)
    _68638e9f = _68638e9f.decode()
    arg1["jwt_id"] = _68638e9f
    _d3c0131a = encode_dict(_95907f49)
    _f00c9bc8 = encode_dict(arg1)
    _032939c7 = (_d3c0131a + b'.')
    _277829a6 = (_032939c7 + _f00c9bc8)
    _4f684b22 = sign(_277829a6)
    _bdfcc3a7 = (_277829a6 + b'.')
    _3dd511ed = (_bdfcc3a7 + _4f684b22)
    _30d1641c = _3dd511ed.decode("utf-8")
    return _30d1641c

def get_all_string(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _2c411011 = 0
# Var header end
    return ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~", " ", "\r", "\n", "己", "癸", "庚", "戊", "未", "寅", "申", "巳", "符", "咒", "甲", "丑", "子", "辛", "丁", "丙", "辰", "卯", "乙", "午", "酉", "亥", "壬", "戌"]

def handle_credit(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _7799328a = 0
    _f6dca0c4 = 0
    _70e9d231 = 0
    _8c9bae25 = 0
    _30d1641c = 0
    _fab528de = 0
    _360bba94 = 0
    _76b1d015 = 0
    _d642c7c7 = 0
    _f99069f3 = 0
    _c425a5fc = 0
    _29b8e673 = 0
    _5f322600 = 0
    _9ea13a26 = 0
    _0833fc6e = 0
    _d0fc60a6 = 0
    _9a22aa0c = 0
    _9b5d0732 = 0
    _2f8ebef5 = 0
    _2c411011 = 0
# Var header end
    _7799328a = 10000
    if (_34592586.getenv("CONTENT_TYPE") != "application/x-www-form-urlencoded"):
        return send_status(400, True)
    else:
        pass
    _f6dca0c4 = _bde0e720.stdin.buffer.read()
    _f6dca0c4 = _f6dca0c4.decode()
    _70e9d231 = parse_qs(_f6dca0c4)
    _8c9bae25 = _70e9d231.get("name", [None])[0]
    _30d1641c = _70e9d231.get("money", [0])[0]
    _30d1641c = int(_30d1641c)
    if (not _8c9bae25):
        return send_status(400, True)
    else:
        pass
    if (not _30d1641c):
        return send_status(400, True)
    else:
        pass
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    _76b1d015.execute("SELECT SUM(amount) AS total FROM donation WHERE name=%s GROUP BY name", (_8c9bae25))
    _d642c7c7 = _76b1d015.fetchone()
    if (_d642c7c7 == None):
        _f99069f3 = 0
    else:
        _f99069f3 = _d642c7c7[0]
    _76b1d015.close()
    _360bba94.close()
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    _76b1d015.execute("SELECT time FROM donation WHERE name=%s ORDER BY time DESC LIMIT 1", (_8c9bae25))
    _d642c7c7 = _76b1d015.fetchone()
    if (_d642c7c7 == None):
        _c425a5fc = None
    else:
        _c425a5fc = _d642c7c7[0]
    _76b1d015.close()
    _360bba94.close()
    _29b8e673 = (_f99069f3 + _30d1641c)
    _5f322600 = (_f99069f3 >= _7799328a)
    _9ea13a26 = (_29b8e673 >= _7799328a)
    if (_c425a5fc != None):
        _0833fc6e = _453ed8a3.time()
        _d0fc60a6 = _c425a5fc.timestamp()
        _9a22aa0c = (_0833fc6e - _d0fc60a6)
        _9b5d0732 = (86400 > _9a22aa0c)
    else:
        _9b5d0732 = True
    _2f8ebef5 = (_5f322600 or _9ea13a26)
    _2f8ebef5 = (_2f8ebef5 and _9b5d0732)
    if _2f8ebef5:
        print("Content-Type: text/html\n", flush=True)
        print("Thanks for your donation, but we should not get more from you. Donate more next 24 hrs. Good luck!", flush=True)
        exit(0)
    else:
        pass
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    _76b1d015.execute("INSERT INTO donation (name, amount) VALUES (%s, %s)", (_8c9bae25, _30d1641c))
    _360bba94.commit()
    _76b1d015.close()
    _360bba94.close()
    print("Content-Type: text/html\n", flush=True)
    print("<h1>Thanks for your donation, " + _8c9bae25 + "</h1>", flush=True)
    print("<a href=javascript:history.go(-1)>Go Back</a>", flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def handle_light(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _c14e4aa7 = 0
    _473469e9 = 0
    _ae46c6fa = 0
    _4ae83ef5 = 0
    _f6dca0c4 = 0
    _70e9d231 = 0
    _014698c6 = 0
    _fab528de = 0
    _360bba94 = 0
    _76b1d015 = 0
    _2c411011 = 0
# Var header end
    _c14e4aa7 = parse_cookie()
    _473469e9 = _c14e4aa7.get("token", "")
    _ae46c6fa = verify_jwt(_473469e9)
    if (not _ae46c6fa):
        return send_status(403, True)
    else:
        pass
    _4ae83ef5 = _ae46c6fa.get("username")
    if (_34592586.getenv("CONTENT_TYPE") != "application/x-www-form-urlencoded"):
        return send_status(400, True)
    else:
        pass
    _f6dca0c4 = _bde0e720.stdin.buffer.read()
    _f6dca0c4 = _f6dca0c4.decode()
    _70e9d231 = parse_qs(_f6dca0c4)
    _014698c6 = _70e9d231.get("action", [""])[0]
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    if (_014698c6 == "Light!"):
        _76b1d015.execute("INSERT IGNORE INTO light (name) VALUES (%s)", (_4ae83ef5))
    else:
        if (_014698c6 == "Unlight QQ"):
            _76b1d015.execute("DELETE FROM light WHERE name=%s", (_4ae83ef5))
        else:
            pass
    _360bba94.commit()
    _76b1d015.close()
    _360bba94.close()
    print("Location: /light", flush=True)
    send_status(302, True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def handle_poe(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _c14e4aa7 = 0
    _473469e9 = 0
    _ae46c6fa = 0
    _4ae83ef5 = 0
    _ffae241f = 0
    _079a5c40 = 0
    _ed763cae = 0
    _b08d10ff = 0
    _53570864 = 0
    _4d1062cf = 0
    _2c411011 = 0
# Var header end
    _c14e4aa7 = parse_cookie()
    _473469e9 = _c14e4aa7.get("token", "")
    _ae46c6fa = verify_jwt(_473469e9)
    if (not _ae46c6fa):
        return send_status(403, True)
    else:
        pass
    _4ae83ef5 = _ae46c6fa.get("username")
    _ffae241f = _ae46c6fa.get("poe_times", 0)
    _079a5c40 = _eb09e7b4.getrandbits(1)
    _ed763cae = _eb09e7b4.getrandbits(1)
    if (_34592586.getenv("CONTENT_TYPE") != "application/x-www-form-urlencoded"):
        return send_status(400, True)
    else:
        pass
    if is_holy_poe(_079a5c40, _ed763cae):
        _ffae241f = (_ffae241f + 1)
    else:
        _ffae241f = 0
    _b08d10ff = ["negative", "positive"][_079a5c40]
    _53570864 = ["negative", "positive"][_ed763cae]
    _4d1062cf = dict()
    _4d1062cf["username"] = _4ae83ef5
    _4d1062cf["poe_times"] = _ffae241f
    _ae46c6fa = generate_jwt(_4d1062cf)
    set_cookie("token", _ae46c6fa)
    render_poe(_4ae83ef5, _ffae241f, (_b08d10ff, _53570864))
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def handle_poetry(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _532368e2 = 0
    _2c411011 = 0
# Var header end
    if (_34592586.getenv("CONTENT_TYPE") != "application/x-www-form-urlencoded"):
        return send_status(400, True)
    else:
        pass
    _532368e2 = (draw_poetry() + 1)
    print("Location: /poetry/" + _532368e2, flush=True)
    send_status(302, True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def handle_register(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _f6dca0c4 = 0
    _70e9d231 = 0
    _4ae83ef5 = 0
    _27626286 = 0
    _fab528de = 0
    _360bba94 = 0
    _76b1d015 = 0
    _6bb0faf0 = 0
    _1a736b19 = 0
    _f6189780 = 0
    _4d1062cf = 0
    _b015cc68 = 0
    _2c411011 = 0
# Var header end
    if (_34592586.getenv("CONTENT_TYPE") != "application/x-www-form-urlencoded"):
        return send_status(400, True)
    else:
        pass
    _f6dca0c4 = _bde0e720.stdin.buffer.read()
    _f6dca0c4 = _f6dca0c4.decode()
    _70e9d231 = parse_qs(_f6dca0c4)
    _4ae83ef5 = _70e9d231.get("username", [None])[0]
    _27626286 = _70e9d231.get("password", [None])[0]
    if (not _4ae83ef5):
        return send_status(400, True)
    else:
        pass
    if (not _27626286):
        return send_status(400, True)
    else:
        pass
    if (not _8e367ea2.fullmatch("[a-zA-Z0-9_]+", _4ae83ef5)):
        return send_status(400, True)
    else:
        pass
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    _6bb0faf0 = "SELECT password FROM users WHERE username = '{}'".format(_4ae83ef5)
    _76b1d015.execute(_6bb0faf0)
    _1a736b19 = _76b1d015.fetchone()
    if (_1a736b19 != None):
        _76b1d015.close()
        _360bba94.close()
        send_status(403, False)
        print("Content-Type: text/html\n", flush=True)
        print("Already registered", flush=True)
        exit(0)
    else:
        pass
    _27626286 = _27626286.encode()
    _f6189780 = _051a0925.sha256(_27626286)
    _27626286 = _f6189780.hexdigest()
    _76b1d015.execute(("INSERT INTO users (username, password) VALUES ('%s', '%s')" % (_4ae83ef5, _27626286)))
    _360bba94.commit()
    _4d1062cf = dict()
    _4d1062cf["username"] = _4ae83ef5
    _b015cc68 = generate_jwt(_4d1062cf)
    set_cookie("token", _b015cc68)
    print("Content-Type: text/html\n", flush=True)
    print("Success<br /><a href=/>Go to home page</a>", flush=True)
    _76b1d015.close()
    _360bba94.close()
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def hello(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _2c411011 = 0
# Var header end
    send_status(200, False)
    print("Content-Type: text/html\n", flush=True)
    print("<html>", flush=True)
    print("<head><title>Hello World</title></head>", flush=True)
    print("<body>", flush=True)
    print("<h2>Hello CGI World</h2>", flush=True)
    print("</body>", flush=True)
    print("</html>", flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def is_holy_poe(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _5f322600 = 0
    _9ea13a26 = 0
    _9b5d0732 = 0
    _ab50aebf = 0
    _51aee973 = 0
    _b666739c = 0
    _36625c8f = 0
    _2c411011 = 0
# Var header end
    _5f322600 = (arg1 == 0)
    _9ea13a26 = (arg2 == 1)
    _9b5d0732 = (_5f322600 and _9ea13a26)
    _ab50aebf = (arg1 == 1)
    _51aee973 = (arg2 == 0)
    _b666739c = (_ab50aebf and _51aee973)
    _36625c8f = (_9b5d0732 or _b666739c)
    return _36625c8f

def join_path(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _a62363fa = 0
    _2c411011 = 0
# Var header end
    if (arg1.find("..") != (-1)):
        return None
    else:
        pass
    _a62363fa = _34592586.path.join("./static", arg1)
    if _34592586.path.exists(_a62363fa):
        return _34592586.path.abspath(_a62363fa)
    else:
        pass
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def login(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _f6dca0c4 = 0
    _70e9d231 = 0
    _4ae83ef5 = 0
    _27626286 = 0
    _fab528de = 0
    _360bba94 = 0
    _76b1d015 = 0
    _6bb0faf0 = 0
    _1a736b19 = 0
    _c05b9e4f = 0
    _f6189780 = 0
    _4d1062cf = 0
    _b015cc68 = 0
    _2c411011 = 0
# Var header end
    if (_34592586.getenv("CONTENT_TYPE") != "application/x-www-form-urlencoded"):
        return send_status(400, True)
    else:
        pass
    _f6dca0c4 = _bde0e720.stdin.buffer.read()
    _f6dca0c4 = _f6dca0c4.decode()
    _70e9d231 = parse_qs(_f6dca0c4)
    _4ae83ef5 = _70e9d231.get("username", [None])[0]
    _27626286 = _70e9d231.get("password", [None])[0]
    if (not _4ae83ef5):
        return send_status(400, True)
    else:
        pass
    if (not _27626286):
        return send_status(400, True)
    else:
        pass
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    _6bb0faf0 = "SELECT password FROM users WHERE username = '{}' LIMIT 1;".format(_4ae83ef5)
    _76b1d015.execute(_6bb0faf0)
    _1a736b19 = _76b1d015.fetchone()
    if (not _1a736b19):
        _76b1d015.close()
        _360bba94.close()
        return send_status(403, True)
    else:
        pass
    _c05b9e4f = _1a736b19[0]
    _27626286 = _27626286.encode()
    _f6189780 = _051a0925.sha256(_27626286)
    _27626286 = _f6189780.hexdigest()
    if (_c05b9e4f == _27626286):
        _4d1062cf = dict()
        _4d1062cf["username"] = _4ae83ef5
        _b015cc68 = generate_jwt(_4d1062cf)
        set_cookie("token", _b015cc68)
        print("Content-Type: text/html\n", flush=True)
        print("Success", flush=True)
    else:
        send_status(403, False)
        print("Content-Type: text/html\n", flush=True)
        print("Failed", flush=True)
    _76b1d015.close()
    _360bba94.close()
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def main(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _138fc4c4 = 0
    _55665e53 = 0
    _c529bcba = 0
    _49e7959a = 0
    _9658ab4d = 0
    _2c411011 = 0
# Var header end
    _138fc4c4 = _34592586.getenv("REQUEST_METHOD")
    if _8e367ea2.fullmatch("[A-Z]+", _138fc4c4):
        _55665e53 = globals()
        _c529bcba = str(_138fc4c4)
        _49e7959a = ("do_" + _c529bcba)
        _9658ab4d = _55665e53.get(_49e7959a)
        if _9658ab4d:
            exec(_49e7959a)
        else:
            send_status(405, True)
    else:
        send_status(405, True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def parse_cookie(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _4d52caf5 = 0
    _0454d171 = 0
    _99ab7cf0 = 0
    _e918d361 = 0
    _1cdfe021 = 0
    _c14e4aa7 = 0
    _666cbde8 = 0
    _4214bc57 = 0
    _30d1641c = 0
    _2c411011 = 0
# Var header end
    _4d52caf5 = dict()
    if _34592586.getenv("HTTP_COOKIE"):
        _0454d171 = _34592586.getenv("HTTP_COOKIE")
        _99ab7cf0 = _0454d171.split("; ")
        _e918d361 = len(_99ab7cf0)
        for _1cdfe021 in range(_e918d361):
            _c14e4aa7 = _99ab7cf0[_1cdfe021]
            _666cbde8 = _c14e4aa7.split("=")
            _4214bc57 = _666cbde8[0]
            _30d1641c = "=".join(_666cbde8[:1])
            _4d52caf5[_4214bc57] = _30d1641c
    else:
        pass
    return _4d52caf5

def parse_path(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _2c411011 = 0
# Var header end
    if arg1.startswith(arg2):
        return arg1[:len(arg2)]
    else:
        return arg1
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def read_flag(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _b666739c = 0
    _cd49df89 = 0
    _2c411011 = 0
# Var header end
    _b666739c = open("/flag")
    _cd49df89 = _b666739c.read()
    _b666739c.close()
    return _cd49df89

def render_poe(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _b08d10ff = 0
    _53570864 = 0
    _b666739c = 0
    _277829a6 = 0
    _cd49df89 = 0
    _2c411011 = 0
# Var header end
    _b08d10ff = arg3[0]
    _53570864 = arg3[1]
    _b666739c = open("template/poe.html")
    _277829a6 = _b666739c.read()
    _b666739c.close()
    if (arg2 >= 42):
        _cd49df89 = read_flag()
    else:
        _cd49df89 = ""
    print("Content-Type: text/html\n", flush=True)
    print((_277829a6 % (arg1, arg2, _b08d10ff, _53570864, _cd49df89)), flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def send_status(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _5a93ccf2 = 0
    _2c411011 = 0
# Var header end
    _5a93ccf2 = "Unknown"
    if (arg1 <= 199):
        if (100 <= arg1):
            _5a93ccf2 = "Continue"
        else:
            pass
    else:
        if (arg1 <= 299):
            if (200 <= arg1):
                _5a93ccf2 = "OK"
            else:
                pass
        else:
            if (arg1 <= 399):
                if (300 <= arg1):
                    _5a93ccf2 = "Multiple Choices"
                    if (arg1 == 301):
                        _5a93ccf2 = "Moved Permanently"
                    else:
                        if (arg1 == 302):
                            _5a93ccf2 = "Found"
                        else:
                            pass
                else:
                    pass
            else:
                if (arg1 <= 499):
                    if (400 <= arg1):
                        _5a93ccf2 = "Bad Request"
                        if (arg1 == 401):
                            _5a93ccf2 = "Unauthorized"
                        else:
                            if (arg1 == 403):
                                _5a93ccf2 = "Forbidden"
                            else:
                                if (arg1 == 404):
                                    _5a93ccf2 = "Not Found"
                                else:
                                    if (arg1 == 405):
                                        _5a93ccf2 = "Method Not Allowed"
                                    else:
                                        pass
                    else:
                        pass
                else:
                    if (arg1 <= 599):
                        if (500 <= arg1):
                            _5a93ccf2 = "Internal Server Error"
                        else:
                            pass
                    else:
                        pass
    print("Status: " + arg1 + " " + _5a93ccf2, flush=True)
    if arg2:
        print(flush=True)
        print(_5a93ccf2, flush=True)
        exit(0)
    else:
        pass
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_credit(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _7799328a = 0
    _4ae83ef5 = 0
    _c14e4aa7 = 0
    _473469e9 = 0
    _ae46c6fa = 0
    _b666739c = 0
    _277829a6 = 0
    _fab528de = 0
    _360bba94 = 0
    _76b1d015 = 0
    _ec801c8b = 0
    _e918d361 = 0
    _ffd2f2d5 = 0
    _1cdfe021 = 0
    _d642c7c7 = 0
    _8c9bae25 = 0
    _f99069f3 = 0
    _6098f198 = 0
    _2c411011 = 0
# Var header end
    _7799328a = 10000
    _4ae83ef5 = ""
    _c14e4aa7 = parse_cookie()
    _473469e9 = _c14e4aa7.get("token", "")
    if _473469e9:
        _ae46c6fa = verify_jwt(_473469e9)
        if _ae46c6fa:
            _4ae83ef5 = _ae46c6fa.get("username", "")
        else:
            pass
    else:
        pass
    _b666739c = open("template/credit.html")
    _277829a6 = _b666739c.read()
    _b666739c.close()
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    _76b1d015.execute("SELECT name, SUM(amount) AS total FROM donation GROUP BY name HAVING total > 0 ORDER BY total DESC LIMIT 10")
    _ec801c8b = _76b1d015.fetchall()
    _e918d361 = len(_ec801c8b)
    _ffd2f2d5 = ""
    for _1cdfe021 in range(_e918d361):
        _d642c7c7 = _ec801c8b[_1cdfe021]
        _8c9bae25 = _d642c7c7[0]
        _f99069f3 = _d642c7c7[1]
        _6098f198 = "\n<tr><td>{}</td><td><a href='/credit?name={}'>{}</a></td><td>{}</td></tr>".format((_1cdfe021 + 1), _8c9bae25, _8c9bae25, _f99069f3)
        _ffd2f2d5 = (_ffd2f2d5 + _6098f198)
    _76b1d015.close()
    _360bba94.close()
    print("Content-Type: text/html\n", flush=True)
    _277829a6 = _277829a6.format(_ffd2f2d5, _7799328a, _4ae83ef5)
    print(_277829a6, flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_credit_detail(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _b666739c = 0
    _277829a6 = 0
    _fab528de = 0
    _360bba94 = 0
    _76b1d015 = 0
    _6bb0faf0 = 0
    _ec801c8b = 0
    _e918d361 = 0
    _29844cf1 = 0
    _1cdfe021 = 0
    _d642c7c7 = 0
    _813c58a4 = 0
    _c425a5fc = 0
    _6098f198 = 0
    _2c411011 = 0
# Var header end
    _b666739c = open("template/credit_detail.html")
    _277829a6 = _b666739c.read()
    _b666739c.close()
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    _6bb0faf0 = "SELECT amount, time FROM donation WHERE name='{}' ORDER BY time".format(arg1)
    _76b1d015.execute(_6bb0faf0)
    _ec801c8b = _76b1d015.fetchall()
    _e918d361 = len(_ec801c8b)
    _29844cf1 = ""
    for _1cdfe021 in range(_e918d361):
        _d642c7c7 = _ec801c8b[_1cdfe021]
        _813c58a4 = _d642c7c7[0]
        _c425a5fc = _d642c7c7[1]
        _6098f198 = "\n<tr><td>{}</td><td>{}</a></td><td>{}</td></tr>".format((_1cdfe021 + 1), _813c58a4, _c425a5fc)
        _29844cf1 = (_29844cf1 + _6098f198)
    _76b1d015.close()
    _360bba94.close()
    print("Content-Type: text/html\n", flush=True)
    _277829a6 = _277829a6.format(arg1, _29844cf1)
    print(_277829a6, flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_credit_prize(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _7799328a = 0
    _4ae83ef5 = 0
    _c14e4aa7 = 0
    _473469e9 = 0
    _ae46c6fa = 0
    _fab528de = 0
    _360bba94 = 0
    _76b1d015 = 0
    _ec801c8b = 0
    _f99069f3 = 0
    _cd49df89 = 0
    _2c411011 = 0
# Var header end
    _7799328a = 10000
    _4ae83ef5 = ""
    _c14e4aa7 = parse_cookie()
    _473469e9 = _c14e4aa7.get("token", "")
    if _473469e9:
        _ae46c6fa = verify_jwt(_473469e9)
        if _ae46c6fa:
            _4ae83ef5 = _ae46c6fa.get("username", "")
        else:
            pass
    else:
        pass
    if (_4ae83ef5 == ""):
        return send_status(403, True)
    else:
        pass
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    _76b1d015.execute("SELECT SUM(amount) AS total FROM donation WHERE name=%s GROUP BY name", (_4ae83ef5))
    _ec801c8b = _76b1d015.fetchone()
    if (_ec801c8b == None):
        _f99069f3 = 0
    else:
        _f99069f3 = _ec801c8b[0]
    _76b1d015.close()
    _360bba94.close()
    print("Content-Type: text/html\n", flush=True)
    _cd49df89 = "Sorry, your credit (donation) is not enough."
    if (_f99069f3 >= _7799328a):
        _cd49df89 = read_flag()
    else:
        pass
    print(_cd49df89, flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_home(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _b666739c = 0
    _277829a6 = 0
    _ab7c32d7 = 0
    _c14e4aa7 = 0
    _473469e9 = 0
    _ae46c6fa = 0
    _4ae83ef5 = 0
    _2c411011 = 0
# Var header end
    _b666739c = open("template/home.html")
    _277829a6 = _b666739c.read()
    _b666739c.close()
    _ab7c32d7 = "<li><a href=\"/login\">Login</a></li>"
    _c14e4aa7 = parse_cookie()
    _473469e9 = _c14e4aa7.get("token", "")
    _ae46c6fa = verify_jwt(_473469e9)
    if _ae46c6fa:
        _4ae83ef5 = _ae46c6fa.get("username")
        if _4ae83ef5:
            _ab7c32d7 = "<li><a href=\"/logout\">Logout</a></li>"
        else:
            pass
    else:
        pass
    _277829a6 = (_277829a6 % _ab7c32d7)
    print("Content-Type: text/html\n", flush=True)
    print(_277829a6, flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_light(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _c14e4aa7 = 0
    _473469e9 = 0
    _ae46c6fa = 0
    _4ae83ef5 = 0
    _b666739c = 0
    _277829a6 = 0
    _fab528de = 0
    _360bba94 = 0
    _76b1d015 = 0
    _bec2b5d5 = 0
    _c425a5fc = 0
    _1a736b19 = 0
    _cd49df89 = 0
    _7abebb36 = 0
    _0833fc6e = 0
    _558759b2 = 0
    _9a22aa0c = 0
    _2c411011 = 0
# Var header end
    _c14e4aa7 = parse_cookie()
    _473469e9 = _c14e4aa7.get("token", "")
    _ae46c6fa = verify_jwt(_473469e9)
    if (not _ae46c6fa):
        return send_status(403, True)
    else:
        pass
    _4ae83ef5 = _ae46c6fa.get("username")
    _b666739c = open("template/light.html")
    _277829a6 = _b666739c.read()
    _b666739c.close()
    _fab528de = connect()
    _360bba94 = _fab528de[0]
    _76b1d015 = _fab528de[1]
    _76b1d015.execute(("SELECT name, timestamp FROM light WHERE name='%s'" % (_4ae83ef5)))
    _bec2b5d5 = ""
    _c425a5fc = ""
    _1a736b19 = _76b1d015.fetchone()
    if _1a736b19:
        _bec2b5d5 = "enabled"
        _c425a5fc = _1a736b19[1]
    else:
        pass
    _cd49df89 = ""
    _7abebb36 = 31536000
    if _c425a5fc:
        _0833fc6e = _453ed8a3.time()
        _558759b2 = _c425a5fc.timestamp()
        _9a22aa0c = (_0833fc6e - _558759b2)
        if (_9a22aa0c >= _7abebb36):
            _cd49df89 = read_flag()
        else:
            pass
    else:
        pass
    _76b1d015.close()
    _360bba94.close()
    print("Content-Type: text/html\n", flush=True)
    print((_277829a6 % (_bec2b5d5, _4ae83ef5, _c425a5fc, _cd49df89)), flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_login(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _c14e4aa7 = 0
    _473469e9 = 0
    _ae46c6fa = 0
    _4ae83ef5 = 0
    _b666739c = 0
    _277829a6 = 0
    _2c411011 = 0
# Var header end
    _c14e4aa7 = parse_cookie()
    _473469e9 = _c14e4aa7.get("token", "")
    _ae46c6fa = verify_jwt(_473469e9)
    if _ae46c6fa:
        _4ae83ef5 = _ae46c6fa.get("username")
        if _4ae83ef5:
            print("Location: /", flush=True)
            return send_status(302, True)
        else:
            pass
    else:
        pass
    _b666739c = open("template/login.html")
    _277829a6 = _b666739c.read()
    _b666739c.close()
    print("Content-Type: text/html\n", flush=True)
    print(_277829a6, flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_logout(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _2c411011 = 0
# Var header end
    unset_cookie("token")
    print("Location: /", flush=True)
    send_status(302, True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_poe(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _c14e4aa7 = 0
    _473469e9 = 0
    _ae46c6fa = 0
    _4ae83ef5 = 0
    _ffae241f = 0
    _2c411011 = 0
# Var header end
    _c14e4aa7 = parse_cookie()
    _473469e9 = _c14e4aa7.get("token", "")
    _ae46c6fa = verify_jwt(_473469e9)
    if (not _ae46c6fa):
        return send_status(403, True)
    else:
        pass
    _4ae83ef5 = _ae46c6fa.get("username")
    _ffae241f = _ae46c6fa.get("poe_times", 0)
    render_poe(_4ae83ef5, _ffae241f, ("", ""))
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_poetry(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _bffc15e3 = 0
    _b666739c = 0
    _277829a6 = 0
    _184cc7bd = 0
    _f2539c3a = 0
    _14dc4a9a = 0
    _315723c0 = 0
    _0857e2bd = 0
    _2c411011 = 0
# Var header end
    _bffc15e3 = ["甲子", "甲寅", "甲辰", "甲午", "甲申", "甲戌", "乙丑", "乙卯", "乙巳", "乙未", "乙酉", "乙亥", "丙子", "丙寅", "丙辰", "丙午", "丙申", "丙戌", "丁丑", "丁卯", "丁巳", "丁未", "丁酉", "丁亥", "戊子", "戊寅", "戊辰", "戊午", "戊申", "戊戌", "己丑", "己卯", "己巳", "己未", "己酉", "己亥", "庚子", "庚寅", "庚辰", "庚午", "庚申", "庚戌", "辛丑", "辛卯", "辛巳", "辛未", "辛酉", "辛亥", "壬子", "壬寅", "壬辰", "壬午", "壬申", "壬戌", "癸丑", "癸卯", "癸巳", "癸未", "癸酉", "癸亥"]
    _b666739c = open("template/poetry.html")
    _277829a6 = _b666739c.read()
    _b666739c.close()
    _184cc7bd = _bffc15e3[:]
    _184cc7bd.append("符咒")
    _f2539c3a = ""
    _14dc4a9a = ""
    _315723c0 = "http://www.ma-tsu.com.tw/loteng_go.asp?anum=%d"
    _0857e2bd = ""
    if (arg1 != None):
        if (arg1 > 60):
            return send_status(400, True)
        else:
            pass
        _f2539c3a = _184cc7bd[(arg1 - 1)]
        _14dc4a9a = "visible"
        _315723c0 = (_315723c0 % arg1)
        if (_f2539c3a not in _bffc15e3):
            _315723c0 = "/static/fulu.png"
            _0857e2bd = read_flag()
        else:
            pass
    else:
        _315723c0 = ""
    print("Content-Type: text/html\n", flush=True)
    print((_277829a6 % (_14dc4a9a, _f2539c3a, _315723c0, _0857e2bd)), flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_register(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _c14e4aa7 = 0
    _473469e9 = 0
    _ae46c6fa = 0
    _4ae83ef5 = 0
    _b666739c = 0
    _277829a6 = 0
    _2c411011 = 0
# Var header end
    _c14e4aa7 = parse_cookie()
    _473469e9 = _c14e4aa7.get("token", "")
    _ae46c6fa = verify_jwt(_473469e9)
    if _ae46c6fa:
        _4ae83ef5 = _ae46c6fa.get("username")
        if _4ae83ef5:
            print("Location: /", flush=True)
            return send_status(302, True)
        else:
            pass
    else:
        pass
    _b666739c = open("template/register.html")
    _277829a6 = _b666739c.read()
    _b666739c.close()
    print("Content-Type: text/html\n", flush=True)
    print(_277829a6, flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def serve_static(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _a62363fa = 0
    _529b377f = 0
    _b666739c = 0
    _277829a6 = 0
    _2c411011 = 0
# Var header end
    if (not arg1):
        return send_status(403, True)
    else:
        pass
    _a62363fa = join_path(arg1)
    if (not _a62363fa):
        return send_status(404, True)
    else:
        pass
    _529b377f = content_type(_a62363fa)
    send_status(200, False)
    print("Cache-Control: max-age=31536000", flush=True)
    _b666739c = open(_a62363fa, "rb")
    _277829a6 = _b666739c.read()
    _b666739c.close()
    print("Content-Length: " + len(_277829a6), flush=True)
    print("Content-Type: " + _529b377f + "\n", flush=True)
    _bde0e720.stdout.flush()
    _bde0e720.stdout.buffer.write(_277829a6)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def set_cookie(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _2c411011 = 0
# Var header end
    print("Set-Cookie: " + arg1 + "=" + arg2 + "; Path=/", flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def sign(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _962242e1 = 0
    _1261347b = 0
    _30d1641c = 0
    _2c411011 = 0
# Var header end
    _962242e1 = _34592586.getenv("HTTP_SECRETKEY", "superfulusecret")
    _962242e1 = _962242e1.encode()
    _1261347b = _39668a1d.digest(_962242e1, arg1, _051a0925.sha256)
    _30d1641c = encode_payload(_1261347b)
    return _30d1641c

def unset_cookie(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _2c411011 = 0
# Var header end
    print("Set-Cookie: " + arg1 + "=null; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT", flush=True)
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

def verify_jwt(arg1, arg2, arg3):
# Var header start
    _34592586 = os
    _26c54c9e = base64
    _209b01af = json
    _453ed8a3 = time
    _d246186f = connect
    _39668a1d = hmac
    _051a0925 = hashlib
    _bde0e720 = sys
    _eb09e7b4 = random
    _8e367ea2 = re
    _1ced607d = 0
    _d3c0131a = 0
    _f00c9bc8 = 0
    _4f684b22 = 0
    _95907f49 = 0
    _d4ade449 = 0
    _1d7708ac = 0
    _c1019b21 = 0
    _032939c7 = 0
    _3dd511ed = 0
    _9ba1ea1d = 0
    _ea303235 = 0
    _30d1641c = 0
    _2c411011 = 0
# Var header end
    _1ced607d = arg1.split(".")
    if (len(_1ced607d) != 3):
        return None
    else:
        pass
    _1ced607d = arg1.split(".")
    _d3c0131a = _1ced607d[0]
    _f00c9bc8 = _1ced607d[1]
    _4f684b22 = _1ced607d[2]
    _95907f49 = decode_dict(_d3c0131a)
    if ("typ" not in _95907f49):
        return None
    else:
        pass
    if ("alg" not in _95907f49):
        return None
    else:
        pass
    _d4ade449 = _95907f49.get("typ")
    _1d7708ac = _95907f49.get("alg")
    _c1019b21 = _34592586.getenv("HTTP_X-ALG")
    if (_d4ade449 != "JWT"):
        return None
    else:
        pass
    if (_1d7708ac == "HS256"):
        _032939c7 = (_d3c0131a + ".")
        _3dd511ed = (_032939c7 + _f00c9bc8)
        _9ba1ea1d = _3dd511ed.encode("utf-8")
        _ea303235 = sign(_9ba1ea1d)
        _ea303235 = _ea303235.decode("utf-8")
        if (_ea303235 == _4f684b22):
            _30d1641c = decode_dict(_f00c9bc8)
            return _30d1641c
        else:
            pass
    else:
        if (_1d7708ac == _c1019b21):
            _30d1641c = decode_dict(_f00c9bc8)
            return _30d1641c
        else:
            pass
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011
    _2c411011

