"""
Shared page shell for generated pages (blog posts, pricing, download,
calculator, legal). Hand-built pages keep their own markup; anything
produced by scripts/build.py goes through page() so the head, consent
defaults, GTM, nav and footer stay identical everywhere.
"""
import json, html

SITE = 'https://tbn.tbbn.in'
GTM = 'GTM-TFBHC2VR'
PHONE_DISPLAY = '+91 88790 70732'
PHONE_TEL = '+918879070732'
WA = '918879070732'
EMAIL = 'tbn@tbbn.in'

DL = {
    'folio_win':   'https://github.com/The-Binary-Brain-Network/folio-releases/releases/latest/download/Folio-Setup.exe',
    'folio_linux': 'https://github.com/The-Binary-Brain-Network/folio-releases/releases/latest/download/Folio-Linux.AppImage',
    'pass_win':    'https://github.com/The-Binary-Brain-Network/pass-releases/releases/latest/download/Pass-Setup.exe',
    'pass_deb':    'https://github.com/The-Binary-Brain-Network/pass-releases/releases/latest/download/Pass-amd64.deb',
    'pass_appimg': 'https://github.com/The-Binary-Brain-Network/pass-releases/releases/latest/download/Pass-x86_64.AppImage',
    'slate_win':   'https://github.com/The-Binary-Brain-Network/slate-releases/releases/latest/download/Slate-Setup.exe',
    'slate_deb':   'https://github.com/The-Binary-Brain-Network/slate-releases/releases/latest/download/Slate-Linux.deb',
    'slate_appimg':'https://github.com/The-Binary-Brain-Network/slate-releases/releases/latest/download/Slate-Linux.AppImage',
    'slate_apk':   'https://github.com/The-Binary-Brain-Network/slate-releases/releases/latest/download/slate.apk',
}

WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Z"/></svg>'
WIN_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5.5 10 4v7H3zM11 3.8 21 2.5V11H11zM3 12h7v7L3 17.5zM11 12h10v8.5L11 19z"/></svg>'
DL_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0-4-4m4 4 4-4M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/></svg>'

CONSENT = ('<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
           '(function(){var c=null;try{c=localStorage.getItem("tbn-consent")}catch(e){}'
           'var g=c==="granted"?"granted":"denied";gtag("consent","default",{ad_storage:g,ad_user_data:g,'
           'ad_personalization:g,analytics_storage:g,functionality_storage:"granted",security_storage:"granted",'
           'wait_for_update:500});gtag("set","ads_data_redaction",true);gtag("set","url_passthrough",true);})();</script>')
GTM_HEAD = ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
            "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})"
            "(window,document,'script','dataLayer','%s');</script>" % GTM)

FOOTER_LINKS = [
    ('/', 'TBN HOME'), ('/folio/', 'FOLIO'), ('/pass/', 'PASS'), ('/slate/', 'SLATE'),
    ('/pricing/', 'PRICING'), ('/download/', 'DOWNLOAD'),
    ('/custom-software/', 'CUSTOM'), ('/compare/', 'COMPARE'), ('/blog/', 'BLOG'),
    ('/glossary/', 'GLOSSARY'), ('/tools/', 'TOOLS'), ('/about/', 'ABOUT'), ('/careers/', 'CAREERS'),
    ('/privacy/', 'PRIVACY'), ('/terms/', 'TERMS'),
]

def esc(s):
    return html.escape(s, quote=True)

def wa_link(text):
    from urllib.parse import quote
    return 'https://wa.me/%s?text=%s' % (WA, quote(text, safe=''))

def jsonld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, ensure_ascii=False, indent=1)

def breadcrumb_ld(crumbs):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': n + 1, 'name': name, 'item': SITE + url}
                                for n, (name, url) in enumerate(crumbs)]}

def faq_ld(faqs):
    import re
    strip = lambda s: re.sub(r'<[^>]+>', '', s)
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': strip(q),
                            'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}} for q, a in faqs]}

def faq_html(faqs):
    return '<div class="faq-list">\n' + '\n'.join(
        '<details class="faq-item"><summary>%s</summary><div class="faq-item__body">%s</div></details>' % (q, a)
        for q, a in faqs) + '\n</div>'

def page(*, path, title, description, body, crumbs, schema=(), section_label='',
         og_image='/og-tbn.svg', og_type='website', wa_text=None, cta_label='WhatsApp',
         extra_css=(), robots='index, follow, max-snippet:-1, max-image-preview:large',
         nav_links=None, final_cta=True):
    url = SITE + path
    wa = wa_link(wa_text or "Hi, I'd like to know more about TBN software.")
    nav_links = nav_links or [('/#products', 'Products'), ('/pricing/', 'Pricing'), ('/download/', 'Download'),
                              ('/blog/', 'Blog'), ('/compare/', 'Compare'), ('/about/', 'About')]
    css = ''.join('<link rel="stylesheet" href="%s">\n' % c for c in ('/assets/page.css',) + tuple(extra_css))
    schema_html = '\n'.join(jsonld(s) for s in list(schema) + [breadcrumb_ld(crumbs)])
    crumb_html = ' / '.join('<a href="%s">%s</a>' % (u, esc(n if n != 'The Binary Brain Network' else 'TBN'))
                            for n, u in crumbs[:-1]) + ' / <span>%s</span>' % esc(crumbs[-1][0])
    nav_html = ''.join('<li><a href="%s">%s</a></li>' % (u, n) for u, n in nav_links)
    footer = ''.join('<a href="%s">%s</a>' % (u, n) for u, n in FOOTER_LINKS)
    cta = ''
    if final_cta:
        cta = '''<section class="cta"><div class="container container--narrow">
  <h2 class="cta__title">Try it on your own property, free.</h2>
  <p class="cta__sub">Every TBN product has a 15-day free trial of the complete software, with no card. Installation and staff training are included when you buy.</p>
  <div class="cta__actions">
    <a href="/download/" class="btn btn--primary">%s Download a free trial</a>
    <a href="%s" target="_blank" rel="noopener" class="btn btn--whatsapp">%s Ask on WhatsApp</a>
  </div>
  <div class="cta__contact"><a href="tel:%s">%s</a><a href="mailto:%s">%s</a></div>
</div></section>''' % (DL_ICON, wa, WA_ICON, PHONE_TEL, PHONE_DISPLAY, EMAIL, EMAIL)
    return '''<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8">
{consent}
{gtm}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_IN">
<meta property="og:site_name" content="The Binary Brain Network">
<meta property="og:image" content="{site}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E1015">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="alternate" type="application/rss+xml" title="TBN Blog" href="/blog/feed.xml">
{schema}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{css}<link rel="stylesheet" href="/assets/tbn.css">
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_id}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<div class="grid-texture"></div>
<header class="nav"><div class="container nav__inner">
  <a href="/" class="nav__brand"><span class="nav__brand-mark">TBN</span><span class="nav__brand-name">The Binary Brain Network <span>/ {label}</span></span></a>
  <nav><ul class="nav__links">{nav}</ul></nav>
  <div class="nav__right"><a href="tel:{tel}" class="nav__phone">{phone}</a><a href="{wa}" target="_blank" rel="noopener" class="nav__cta">{wa_icon}{cta_label}</a></div>
</div></header>
<div class="container"><nav class="breadcrumb">{crumb}</nav></div>
<main>
{body}
</main>
<div class="parent-strip"><div class="container parent-strip__inner">
  <p class="parent-strip__text"><strong>The Binary Brain Network</strong> is the software division of <strong>The Big Brand Network</strong> — a full-service brand ecosystem based in Mumbai, operating pan-India. Trademark registered, MSME certified.</p>
  <a href="https://tbbn.in" target="_blank" rel="noopener" class="parent-strip__link">Visit TBBN Agency</a>
</div></div>
{cta}
<footer class="footer"><div class="container footer__inner">
  <span class="footer__text">© 2026 THE BINARY BRAIN NETWORK — A TBBN DIVISION</span>
  <div class="footer__links">{footer}<a href="tel:{tel}">{phone}</a><a href="mailto:{email}">{email_up}</a></div>
</div></footer>
<script src="/assets/tbn.js" defer></script>
</body>
</html>
'''.format(consent=CONSENT, gtm=GTM_HEAD, title=esc(title), desc=esc(description), robots=robots,
           url=url, og_type=og_type, site=SITE, og_image=og_image, schema=schema_html, css=css,
           gtm_id=GTM, label=esc(section_label), nav=nav_html, tel=PHONE_TEL, phone=PHONE_DISPLAY,
           wa=wa, wa_icon=WA_ICON, cta_label=esc(cta_label), crumb=crumb_html, body=body, cta=cta,
           footer=footer, email=EMAIL, email_up=EMAIL.upper())
