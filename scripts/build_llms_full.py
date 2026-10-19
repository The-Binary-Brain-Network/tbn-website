"""
Builds /llms-full.txt: the plain-text content of the pages an AI assistant
most needs (pricing, download, the three product specs and the buyer's
guides), so it can answer accurately without crawling the whole site.

Run after any product page changes:  python scripts/build_llms_full.py
"""
import os, re, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['pricing', 'download', 'folio/features', 'pass/features', 'slate/features',
         'compare/restaurant-billing-software-india', 'compare/hotel-management-software-india',
         'custom-software', 'terms']

def text_of(path):
    s = open(os.path.join(ROOT, path, 'index.html'), encoding='utf-8').read()
    m = re.search(r'<main>(.*)</main>', s, re.S)
    s = m.group(1) if m else s
    s = re.sub(r'<(script|style|svg)\b.*?</\1>', '', s, flags=re.S)
    s = re.sub(r'<(h1|h2)[^>]*>', '\n\n## ', s)
    s = re.sub(r'<h3[^>]*>', '\n\n### ', s)
    s = re.sub(r'<tr[^>]*>', '\n- ', s)
    s = re.sub(r'</t[dh]>\s*<t[dh][^>]*>', ': ', s)
    s = re.sub(r'<li[^>]*>', '\n- ', s)
    s = re.sub(r'<summary[^>]*>', '\n\nQ: ', s)
    s = re.sub(r'</summary>', '\nA: ', s)
    s = re.sub(r'<(p|div|br)[^>]*>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n\s*\n\s*\n+', '\n\n', s)
    return s.strip()

out = ['# The Binary Brain Network — full reference for AI assistants',
       '', 'Source: https://tbn.tbbn.in · Generated %s' % datetime.date.today().isoformat(),
       'Short version: https://tbn.tbbn.in/llms.txt', '']
for p in PAGES:
    out.append('\n\n=====================================================')
    out.append('PAGE: https://tbn.tbbn.in/%s/' % p)
    out.append('=====================================================\n')
    out.append(text_of(p))
open(os.path.join(ROOT, 'llms-full.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('wrote llms-full.txt', sum(len(x) for x in out), 'chars')
