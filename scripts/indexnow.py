"""
Tells Bing, Yandex and other IndexNow engines that pages changed, so they
recrawl within hours instead of weeks. Google does not use IndexNow; submit
the sitemap in Search Console for Google.

Run AFTER the site is deployed (the key file must be live first):
  python scripts/indexnow.py            # submit every URL in sitemap.xml
  python scripts/indexnow.py /blog/x/   # submit specific paths
"""
import os, re, sys, json, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'tbn.tbbn.in'
KEY = '8f3c1b7e2a9d4f60b5e1c7a2d9f04e6b'

if len(sys.argv) > 1:
    urls = ['https://%s%s' % (HOST, p) for p in sys.argv[1:]]
else:
    urls = re.findall(r'<loc>(.*?)</loc>', open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read())

body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': 'https://%s/%s.txt' % (HOST, KEY),
                   'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                             headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print('IndexNow:', r.status, '-', len(urls), 'URLs submitted')
except urllib.error.HTTPError as e:
    print('IndexNow error:', e.code, e.read().decode()[:300])
