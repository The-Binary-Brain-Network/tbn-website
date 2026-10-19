"""
Pre-push checks: JSON-LD parses, internal links resolve, every page has the
consent defaults, GTM, canonical and shared script, and no known-stale claims
have crept back in.

Run:  python scripts/check_site.py
"""
import io, glob, re, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SKIP = ('content', 'scripts', 'ops', '.github', 'node_modules')
STALE = [
    (r'7-day free trial|14-day free trial|30-day free trial|free for (?:a|one) week|free for a month|two weeks', 'old trial length'),
    (r'unlimited outlets', 'Pass is now per billing computer'),
    (r'12% up to ₹7,500|attract 12%|generally attract 12', 'old hotel room GST'),
    (r'Markup modes', 'removed from Folio'),
    (r'AI-powered|AI insights|AI Insights', 'Pass AI page is hidden'),
    (r'Windows \(7 / 8|Windows 7 / 8', 'Electron 31 needs Windows 10+'),
    (r'Twelve reports|12 reports', 'Slate has 16 reports'),
    (r'Loyalty points</strong> earning|loyalty points on a single bill', 'Pass loyalty not wired'),
]

pages = [f for f in glob.glob('**/index.html', recursive=True)
         if f.replace(os.sep, '/').split('/')[0] not in SKIP]
problems = 0; blocks = 0; broken = set()
for f in pages:
    s = io.open(f, encoding='utf-8').read()
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        blocks += 1
        try: json.loads(b)
        except Exception as e: problems += 1; print('JSON-LD invalid:', f, e)
    for need, label in [('gtag("consent","default"', 'consent default'), ('GTM-TFBHC2VR', 'GTM'),
                        ('/assets/tbn.js', 'tbn.js'), ('rel="canonical"', 'canonical')]:
        if need not in s: problems += 1; print('missing', label, ':', f)
    for h in re.findall(r'href="(/[^"#?]*)', s):
        if h.startswith('//'): continue
        p = h.lstrip('/')
        if not (p == '' or os.path.isfile(p) or os.path.isfile(os.path.join(p, 'index.html'))):
            broken.add((h, f))
    for pat, why in STALE:
        for m in re.finditer(pat, s):
            problems += 1; print('stale (%s): %s :: %s' % (why, f, s[max(0, m.start()-60):m.end()+30].replace('\n', ' ')))
for t in ('llms.txt', 'llms-full.txt'):
    s = io.open(t, encoding='utf-8').read()
    for pat, why in STALE:
        if re.search(pat, s): problems += 1; print('stale (%s) in %s' % (why, t))
for h, f in sorted(broken):
    problems += 1; print('broken link', h, 'in', f)
print('%d pages, %d JSON-LD blocks, %d problems' % (len(pages), blocks, problems))
sys.exit(1 if problems else 0)
