"""
Builds blog posts from content/blog/*.html, plus /blog/index.html and
/blog/feed.xml.

Each content file starts with a JSON block inside an HTML comment:

  <!--meta
  {"title": "...", "h1": "...", "description": "...", "category": "Restaurants",
   "product": "pass", "date": "2026-10-19", "read": 9, "lede": "...",
   "answer": "...", "faqs": [["Q", "A"], ...], "related": ["slug", ...]}
  -->
  <h2>...</h2> ...body HTML...

Run:  python scripts/build_blog.py
"""
import os, re, sys, json, glob, datetime, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tbnsite import page, faq_html, faq_ld, wa_link, DL_ICON, WA_ICON, SITE, esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'content', 'blog')

# Hand-built posts that predate the generator. Listed so the index, feed
# and related-post links include them.
LEGACY = [
    dict(slug='gst-for-restaurants-india-explained', title='GST for Restaurants in India, Explained', category='Restaurants',
         description='Composite vs regular scheme, when 5% applies and when 18% does, and what a GST-compliant restaurant bill must show.', date='2026-06-20', read=8, product='pass'),
    dict(slug='restaurant-billing-software-cost-india', title='What Restaurant Billing Software Really Costs in India', category='Restaurants',
         description='Licence vs subscription, the add-ons that inflate the headline price, and a five-year way to compare quotes.', date='2026-06-24', read=8, product='pass'),
    dict(slug='hotel-room-service-billing-setup-guide', title='Room-Service Billing for Small Hotels: A Practical Setup Guide', category='Hotels',
         description='Why most hotel PMS have no room-service module, and the five components of a setup that works.', date='2026-06-28', read=7, product='folio'),
]

PRODUCT_CTA = {
    'folio': ('Folio · Room-service billing for hotels',
              'Tabs per room, kitchen tickets, GST bills, dues and an owner\'s daily report — alongside the PMS you already run. ₹6,500 a year.',
              '/download/#folio', '/folio/', 'See Folio'),
    'pass':  ('Pass · Restaurant POS',
              'Billing, KOT and kitchen display, inventory with recipes, staff and payroll, multiple outlets — offline. ₹7,500 per billing computer a year.',
              '/download/#pass', '/pass/', 'See Pass'),
    'slate': ('Slate · Hotel management system',
              'Bookings, room board, folios, GST invoicing, housekeeping, C-Form and 16 reports. ₹12,000 per property a year — not per room.',
              '/download/#slate', '/slate/', 'See Slate'),
    'custom': ('Custom software from The Binary Brain Network',
               'When no product fits: a written specification you own, a fixed price against fixed scope, and the source code handed over.',
               None, '/custom-software/', 'How we work'),
    'all':   ('Folio, Pass and Slate',
              'Offline-first software for Indian hotels and restaurants, on flat annual licences with installation and training included.',
              '/download/', '/pricing/', 'See pricing'),
}

def load_posts():
    posts = []
    for path in sorted(glob.glob(os.path.join(SRC, '*.html'))):
        raw = open(path, encoding='utf-8').read()
        m = re.match(r'\s*<!--meta\s*(\{.*?\})\s*-->\s*(.*)', raw, re.S)
        if not m:
            raise SystemExit('missing meta block: ' + path)
        meta = json.loads(m.group(1))
        meta['slug'] = os.path.splitext(os.path.basename(path))[0]
        meta['body'] = m.group(2).strip()
        text = meta['body'] + ' ' + meta.get('answer', '') + ' ' + ' '.join(q + ' ' + a for q, a in meta.get('faqs', []))
        words = len(re.sub(r'<[^>]+>', ' ', text).split())
        meta['words'] = words
        meta.setdefault('read', max(4, round(words / 220)))
        posts.append(meta)
    return posts

def human(d):
    return datetime.date.fromisoformat(d).strftime('%d · %m · %Y')

def cta_block(product):
    label, desc, dl, more, more_label = PRODUCT_CTA.get(product, PRODUCT_CTA['all'])
    btns = ''
    if dl:
        btns += '<a href="%s" class="btn btn--primary">%s Free 15-day trial</a>' % (dl, DL_ICON)
    btns += '<a href="%s" class="btn btn--ghost">%s</a>' % (more, more_label)
    return '''<div class="related-cta">
  <div><div class="related-cta__label">From the people who wrote this</div>
  <div class="related-cta__title">%s</div>
  <div class="related-cta__desc">%s</div></div>
  <div class="related-cta__actions">%s</div>
</div>''' % (esc(label), desc, btns)

def build_post(p, by_slug):
    rel = [by_slug[s] for s in p.get('related', []) if s in by_slug][:3]
    if len(rel) < 3:
        rel += [q for q in by_slug.values() if q['slug'] != p['slug'] and q not in rel
                and q['category'] == p['category']][:3 - len(rel)]
    rel_html = ''.join('<a class="related-item" href="/blog/%s/"><div class="related-item__cat">%s</div><div class="related-item__title">%s</div></a>'
                       % (r['slug'], esc(r['category']), esc(r['title'])) for r in rel)
    faqs = [tuple(x) for x in p.get('faqs', [])]
    url = '/blog/%s/' % p['slug']
    body = '''<article>
  <header class="article-head"><div class="container container--narrow">
    <div class="article-meta"><span>{cat}</span><span>{date}</span><span>{read} min read</span></div>
    <h1 class="article-title">{h1}</h1>
    <p class="article-lede">{lede}</p>
  </div></header>
  <div class="article-body"><div class="container container--narrow">
    <div class="answer"><div class="answer__label">Short answer</div><p>{answer}</p></div>
{body}
{cta}
    {faq}
    <div class="author-box"><strong>Written by The Binary Brain Network</strong> — the software division of The Big Brand Network, Mumbai. We build Folio, Pass and Slate, so where our own products come up we say so, and we say where they are the wrong fit. Last reviewed {upd}.</div>
  </div></div>
</article>
<section class="related-posts"><div class="container container--narrow">
  <div class="related-posts__head">Keep reading</div>
  <div class="related-list">{rel}</div>
</div></section>'''.format(cat=esc(p['category']), date=human(p['date']), read=p['read'],
        h1=p.get('h1', esc(p['title'])), lede=p['lede'], answer=p['answer'], body=p['body'],
        cta=cta_block(p.get('product', 'all')),
        faq=('<div class="post-faq"><h2>Common questions</h2>%s</div>' % faq_html(faqs)) if faqs else '',
        upd=datetime.date.fromisoformat(p.get('modified', p['date'])).strftime('%d %B %Y'), rel=rel_html)
    article_ld = {
        '@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'][:110],
        'description': p['description'], 'datePublished': p['date'], 'dateModified': p.get('modified', p['date']),
        'inLanguage': 'en-IN', 'wordCount': p['words'], 'articleSection': p['category'],
        'keywords': ', '.join(p.get('keywords', [])),
        'author': {'@type': 'Organization', '@id': SITE + '/#organization', 'name': 'The Binary Brain Network'},
        'publisher': {'@id': SITE + '/#organization'},
        'mainEntityOfPage': SITE + url, 'image': SITE + p.get('image', '/og-tbn.svg'),
        'isPartOf': {'@type': 'Blog', '@id': SITE + '/blog/#blog'},
        'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['.article-title', '.answer']},
    }
    schema = [article_ld] + ([faq_ld(faqs)] if faqs else [])
    wa = {'folio': "Hi, I read your article and I'd like to know more about Folio.",
          'pass': "Hi, I read your article and I'd like to know more about Pass.",
          'slate': "Hi, I read your article and I'd like to know more about Slate.",
          'custom': "Hi, I read your article and I'd like to discuss a custom software project."}.get(p.get('product'), "Hi, I read your article on tbn.tbbn.in.")
    out = page(path=url, title=p['title'] + ' | TBN', description=p['description'], body=body,
               crumbs=[('The Binary Brain Network', '/'), ('Blog', '/blog/'), (p.get('crumb', p['title']), url)],
               schema=schema, section_label='Blog', og_type='article', og_image=p.get('image', '/og-tbn.svg'),
               wa_text=wa, extra_css=('/assets/article.css',))
    out = out.replace('<meta property="og:type" content="article">',
                      '<meta property="og:type" content="article">\n<meta property="article:published_time" content="%s">\n<meta property="article:section" content="%s">' % (p['date'], esc(p['category'])))
    dest = os.path.join(ROOT, 'blog', p['slug'], 'index.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf-8', newline='\n').write(out)

def build_index(allposts):
    cats = []
    for p in allposts:
        if p['category'] not in cats: cats.append(p['category'])
    filters = '<button type="button" class="is-on" data-cat="all">All</button>' + ''.join(
        '<button type="button" data-cat="%s">%s</button>' % (esc(c), esc(c)) for c in cats)
    cards = ''.join('''<a class="post-card" href="/blog/{slug}/" data-cat="{cat}">
  <div class="post-card__cat">{cat}</div><h2 class="post-card__title">{title}</h2>
  <p class="post-card__desc">{desc}</p><div class="post-card__meta">{date} · {read} min</div></a>'''.format(
        slug=p['slug'], cat=esc(p['category']), title=esc(p['title']), desc=esc(p['description']),
        date=human(p['date']), read=p['read']) for p in allposts)
    body = '''<section class="hero"><div class="container">
  <span class="hero__eyebrow">Guides for Indian hotels &amp; restaurants</span>
  <h1 class="hero__title">The TBN blog: <em>practical, specific, honest.</em></h1>
  <p class="hero__lede">GST, billing, kitchen operations, front-desk compliance and the real cost of software — written by the team that builds Folio, Pass and Slate, from three generations of running hospitality businesses.</p>
  <p class="updated"><a href="/blog/feed.xml" style="color:var(--amber)">RSS feed</a> · {n} articles</p>
</div></section>
<section class="section"><div class="container">
  <div class="blog-filters" role="group" aria-label="Filter by topic">{filters}</div>
  <div class="post-grid">{cards}</div>
</div></section>
<script>
(function(){{var b=document.querySelectorAll('.blog-filters button'),c=document.querySelectorAll('.post-card');
Array.prototype.forEach.call(b,function(x){{x.addEventListener('click',function(){{
Array.prototype.forEach.call(b,function(y){{y.classList.toggle('is-on',y===x)}});var k=x.getAttribute('data-cat');
Array.prototype.forEach.call(c,function(p){{p.hidden=!(k==='all'||p.getAttribute('data-cat')===k)}});}})}});}})();
</script>'''.format(n=len(allposts), filters=filters, cards=cards)
    schema = [{'@context': 'https://schema.org', '@type': 'Blog', '@id': SITE + '/blog/#blog', 'url': SITE + '/blog/',
               'name': 'The Binary Brain Network blog', 'inLanguage': 'en-IN',
               'publisher': {'@id': SITE + '/#organization'},
               'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': SITE + '/blog/%s/' % p['slug'],
                             'datePublished': p['date']} for p in allposts]}]
    out = page(path='/blog/', title='Blog — Hotel & Restaurant Software, GST and Operations Guides | TBN',
               description='Practical guides for Indian hotels and restaurants: GST, billing, KOT and kitchen display, C-Form, night audit, inventory, payroll and what software really costs.',
               body=body, crumbs=[('The Binary Brain Network', '/'), ('Blog', '/blog/')], schema=schema,
               section_label='Blog', extra_css=('/assets/article.css',))
    open(os.path.join(ROOT, 'blog', 'index.html'), 'w', encoding='utf-8', newline='\n').write(out)

def build_feed(allposts):
    items = ''.join('''  <item>
    <title>{t}</title>
    <link>{u}</link>
    <guid isPermaLink="true">{u}</guid>
    <pubDate>{d}</pubDate>
    <category>{c}</category>
    <description>{desc}</description>
  </item>
'''.format(t=H.escape(p['title']), u=SITE + '/blog/%s/' % p['slug'],
           d=datetime.datetime.fromisoformat(p['date'] + 'T09:00:00+05:30').strftime('%a, %d %b %Y %H:%M:%S +0530'),
           c=H.escape(p['category']), desc=H.escape(p['description'])) for p in allposts)
    feed = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>The Binary Brain Network — Blog</title>
  <link>{s}/blog/</link>
  <atom:link href="{s}/blog/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Guides for Indian hotels and restaurants: GST, billing, kitchen operations, compliance and software costs.</description>
  <language>en-in</language>
{items}</channel>
</rss>
'''.format(s=SITE, items=items)
    open(os.path.join(ROOT, 'blog', 'feed.xml'), 'w', encoding='utf-8', newline='\n').write(feed)

if __name__ == '__main__':
    posts = load_posts()
    allposts = sorted(posts + LEGACY, key=lambda p: (p['date'], p.get('order', 0)), reverse=True)
    by_slug = {p['slug']: p for p in allposts}
    for p in posts:
        build_post(p, by_slug)
    build_index(allposts)
    build_feed(allposts)
    short = [(p['slug'], p['words']) for p in posts if p['words'] < 1100]
    print('built %d posts (%d total in index). Under 1,100 words: %s' % (len(posts), len(allposts), short or 'none'))
