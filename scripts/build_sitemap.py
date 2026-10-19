"""
Regenerates sitemap.xml from every index.html in the site.
lastmod comes from the page's JSON-LD dateModified (or datePublished),
falling back to the file's last git commit date.

Run:  python scripts/build_sitemap.py
"""
import os, re, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://tbn.tbbn.in'
SKIP = ('content', 'scripts', 'ops', 'node_modules', '.git', '.github', 'assets')

PRIORITY = [
    (r'^/$', '1.0', 'weekly'),
    (r'^/(folio|pass|slate)/$', '0.95', 'weekly'),
    (r'^/(download|pricing)/$', '0.95', 'weekly'),
    (r'^/(compare|custom-software)/', '0.9', 'monthly'),
    (r'^/(folio|pass|slate)/features/$', '0.85', 'monthly'),
    (r'^/blog/$', '0.8', 'weekly'),
    (r'^/blog/.+', '0.75', 'monthly'),
    (r'^/(folio|pass)/for-', '0.7', 'monthly'),
    (r'^/tools/', '0.7', 'monthly'),
    (r'^/about/$', '0.6', 'monthly'),
    (r'^/glossary/', '0.55', 'monthly'),
    (r'^/(careers|privacy|terms)/$', '0.4', 'yearly'),
]
IMAGES = {'/folio/': '/og-folio.svg', '/pass/': '/og-pass.svg', '/slate/': '/og-slate.svg'}

def git_date(path):
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', path], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
        return out or None
    except Exception:
        return None

entries = []
for dirpath, dirs, files in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT).replace('\\', '/')
    if rel.split('/')[0] in SKIP:
        dirs[:] = []
        continue
    if 'index.html' not in files:
        continue
    url = '/' if rel == '.' else '/' + rel + '/'
    s = open(os.path.join(dirpath, 'index.html'), encoding='utf-8').read()
    if 'noindex' in s[:3000]:
        continue
    dates = re.findall(r'"date(?:Modified|Published)"\s*:\s*"(\d{4}-\d{2}-\d{2})', s)
    lastmod = max(dates) if dates else (git_date(os.path.join(dirpath, 'index.html')) or datetime.date.today().isoformat())
    pri, freq = '0.5', 'monthly'
    for pat, p, f in PRIORITY:
        if re.search(pat, url):
            pri, freq = p, f
            break
    entries.append((float(pri), url, lastmod, freq, pri))

entries.sort(key=lambda e: (-e[0], e[1]))
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
       '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for _, url, lastmod, freq, pri in entries:
    xml.append('  <url>')
    xml.append('    <loc>%s%s</loc>' % (SITE, url))
    xml.append('    <lastmod>%s</lastmod>' % lastmod)
    xml.append('    <changefreq>%s</changefreq>' % freq)
    xml.append('    <priority>%s</priority>' % pri)
    if url in IMAGES:
        xml.append('    <image:image><image:loc>%s%s</image:loc></image:image>' % (SITE, IMAGES[url]))
    xml.append('  </url>')
xml.append('</urlset>')
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write('\n'.join(xml) + '\n')
print('sitemap.xml:', len(entries), 'URLs')
