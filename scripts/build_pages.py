"""
Builds the generated landing pages: /download/, /pricing/,
/tools/software-cost-calculator/, /privacy/, /terms/.

Run:  python scripts/build_pages.py
Facts here must match the product repos. When a price, trial length or
platform changes, change it in FACTS below and rebuild.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tbnsite import page, DL, WA_ICON, WIN_ICON, DL_ICON, wa_link, faq_html, faq_ld, SITE, esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = '2026-10-19'
UPDATED_HUMAN = '19 October 2026'

FACTS = {
    'folio': dict(name='Folio', price='6,500', unit='per property per year', version='3.15.0',
                  status='Live in production', os='Windows 10/11 · Linux'),
    'pass':  dict(name='Pass', price='7,500', unit='per billing computer per year', version='1.0.12',
                  status='In trials', os='Windows 10/11 · Linux'),
    'slate': dict(name='Slate', price='12,000', unit='per property per year', version='0.5.9',
                  status='In trials', os='Windows 10/11 · Linux · Android'),
}

LINUX_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.5c-2 0-3 1.7-3 3.6 0 1.5.2 2.3-.6 3.4C7.2 11.3 6 13.4 6 15.6c0 2.3 1.4 3.6 2.7 4.2.6.3 1 .9 1.1 1.4h4.4c.1-.5.5-1.1 1.1-1.4 1.3-.6 2.7-1.9 2.7-4.2 0-2.2-1.2-4.3-2.4-6.1-.8-1.1-.6-1.9-.6-3.4 0-1.9-1-3.6-3-3.6z"/></svg>'
ANDROID_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><rect x="5" y="9" width="14" height="10" rx="2"/><path d="M8 9a4 4 0 0 1 8 0M8 5l1.2 1.8M16 5l-1.2 1.8"/></svg>'

PAGE_CSS = '''<style>
.dl-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;}
@media(max-width:980px){.dl-grid{grid-template-columns:1fr;}}
.dl-grid > *{min-width:0;}
.dl{background:var(--ink2);border:1px solid var(--line);padding:30px 28px;display:flex;flex-direction:column;}
.dl__top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:6px;}
.dl__name{font-size:24px;font-weight:800;letter-spacing:-.01em;}
.dl__status{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);border:1px solid var(--amber-dim);padding:4px 8px;white-space:nowrap;}
.dl__status--live{color:#6FCB9A;border-color:var(--green);}
.dl__for{color:var(--slate-light);font-size:14px;line-height:1.6;margin-bottom:18px;}
.dl__meta{font-family:var(--mono);font-size:11.5px;color:var(--slate-light);line-height:1.9;margin-bottom:20px;border-top:1px dashed var(--line);border-bottom:1px dashed var(--line);padding:12px 0;}
.dl__meta b{color:var(--paper-dim);font-weight:700;}
.dl__btns{display:flex;flex-direction:column;gap:10px;margin-bottom:18px;}
.dl__btns .btn{justify-content:center;}
.dl__btns .btn svg{fill:none;}
.dl__btns .btn--primary svg{fill:currentColor;}
.dl__trial{font-size:13.5px;color:var(--paper-dim);line-height:1.65;margin-top:auto;background:rgba(232,163,61,.06);border-left:2px solid var(--amber-dim);padding:12px 14px;}
.dl__trial a{color:var(--amber);border-bottom:1px solid var(--amber-dim);}
.steps{counter-reset:s;display:grid;gap:14px;max-width:780px;}
.steps li{list-style:none;counter-increment:s;position:relative;padding-left:44px;color:var(--paper-dim);font-size:15px;line-height:1.75;}
.steps li::before{content:counter(s,decimal-leading-zero);position:absolute;left:0;top:1px;font-family:var(--mono);font-size:12px;color:var(--amber);font-weight:700;}
.steps li strong{color:var(--paper);}
.price-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;}
@media(max-width:980px){.price-grid{grid-template-columns:1fr;}}
.price-grid > *{min-width:0;}
.pcard{background:var(--ink2);border:1px solid var(--line);padding:32px 28px;display:flex;flex-direction:column;}
.pcard--feature{border-color:var(--amber-dim);}
.pcard__name{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:10px;}
.pcard__for{font-size:15px;color:var(--paper-dim);margin-bottom:18px;line-height:1.55;min-height:46px;}
.pcard__price{font-size:40px;font-weight:800;letter-spacing:-.02em;line-height:1;}
.pcard__unit{font-family:var(--mono);font-size:11.5px;color:var(--slate-light);margin:8px 0 22px;}
.pcard ul{list-style:none;display:flex;flex-direction:column;gap:10px;margin-bottom:24px;}
.pcard li{font-size:14px;color:var(--paper-dim);padding-left:20px;position:relative;line-height:1.55;}
.pcard li::before{content:'';position:absolute;left:0;top:9px;width:9px;height:1px;background:var(--amber);}
.pcard .btn{justify-content:center;margin-top:auto;}
.calc{background:var(--ink2);border:1px solid var(--line);padding:30px;display:grid;grid-template-columns:1fr 1fr;gap:32px;}
@media(max-width:860px){.calc{grid-template-columns:1fr;padding:22px 18px;}}
.calc > *{min-width:0;}
.calc label{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--slate-light);margin:0 0 8px;}
.calc .field{margin-bottom:20px;}
.calc input,.calc select{width:100%;background:var(--ink);border:1px solid var(--line);color:var(--paper);font-family:var(--mono);font-size:15px;padding:12px 14px;}
.calc input:focus,.calc select:focus{outline:none;border-color:var(--amber);}
.calc .hint{font-size:12.5px;color:var(--slate);margin-top:6px;line-height:1.5;}
.out{border-left:2px solid var(--amber);padding-left:24px;}
@media(max-width:860px){.out{border-left:none;border-top:2px solid var(--amber);padding:22px 0 0;}}
.out__row{display:flex;justify-content:space-between;gap:12px;padding:12px 0;border-bottom:1px dashed var(--line);font-size:14.5px;color:var(--slate-light);}
.out__row b{font-family:var(--mono);color:var(--paper);font-size:16px;white-space:nowrap;}
.out__big{margin-top:20px;}
.out__big .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);}
.out__big .val{font-size:38px;font-weight:800;letter-spacing:-.02em;margin:6px 0;}
.out__note{font-size:12.5px;color:var(--slate);line-height:1.6;margin-top:14px;}
.legal h2{font-size:22px;font-weight:800;margin:44px 0 14px;letter-spacing:-.01em;}
.legal h2:first-child{margin-top:0;}
.legal h3{font-size:17px;font-weight:700;margin:26px 0 10px;}
.legal p,.legal li{font-size:15px;color:var(--paper-dim);line-height:1.8;}
.legal p{margin-bottom:16px;}
.legal ul{margin:0 0 18px 20px;}
.legal li{margin-bottom:8px;}
.legal a{color:var(--amber);border-bottom:1px solid var(--amber-dim);}
.legal strong{color:var(--paper);}
.note{font-family:var(--mono);font-size:12px;color:var(--slate-light);background:rgba(232,163,61,.06);border:1px dashed var(--amber-dim);padding:14px 16px;margin-bottom:34px;line-height:1.7;}
</style>'''

def write(path, content):
    full = os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.replace('</head>', PAGE_CSS + '\n</head>', 1))
    print('wrote', full)

def btn(href, label, cls='btn--ghost', icon=DL_ICON):
    return '<a href="%s" class="btn %s">%s%s</a>' % (href, cls, icon, label)

# ======================================================================
# /download/
# ======================================================================
def download_page():
    f, p, s = FACTS['folio'], FACTS['pass'], FACTS['slate']
    cards = '''
<div class="dl-grid">
  <div class="dl" id="folio">
    <div class="dl__top"><span class="dl__name">Folio</span><span class="dl__status dl__status--live">Live</span></div>
    <p class="dl__for">Room-service ordering and billing for hotels that already run a hotel management system.</p>
    <div class="dl__meta"><b>Version</b> {fv} · <b>Runs on</b> {fos}<br><b>Price</b> ₹{fp} {fu}</div>
    <div class="dl__btns">
      {f_win}
      {f_lin}
    </div>
    <p class="dl__trial"><strong>Trial starts in the app.</strong> On first launch choose <em>Try Folio free for 15 days</em> and enter your hotel's name and phone. Needs internet for that one step. <a href="/folio/">About Folio</a></p>
  </div>
  <div class="dl" id="pass">
    <div class="dl__top"><span class="dl__name">Pass</span><span class="dl__status">In trials</span></div>
    <p class="dl__for">Restaurant POS and management — billing, KOT and kitchen display, inventory, staff, multiple outlets.</p>
    <div class="dl__meta"><b>Version</b> {pv} · <b>Runs on</b> {pos}<br><b>Price</b> ₹{pp} {pu}</div>
    <div class="dl__btns">
      {p_win}
      {p_deb}
      {p_app}
    </div>
    <p class="dl__trial"><strong>Trial key on WhatsApp.</strong> Install, then <a href="{p_wa}" target="_blank" rel="noopener">message us</a> for your 15-day key — usually within minutes in working hours. <a href="/pass/">About Pass</a></p>
  </div>
  <div class="dl" id="slate">
    <div class="dl__top"><span class="dl__name">Slate</span><span class="dl__status">In trials</span></div>
    <p class="dl__for">Hotel management system — bookings, room board, folios, GST invoicing, housekeeping, C-Form, night audit.</p>
    <div class="dl__meta"><b>Version</b> {sv} · <b>Runs on</b> {sos}<br><b>Price</b> ₹{sp} {su}</div>
    <div class="dl__btns">
      {s_win}
      {s_deb}
      {s_app}
      {s_apk}
    </div>
    <p class="dl__trial"><strong>Trial key on WhatsApp.</strong> Install on the front-desk PC, then <a href="{s_wa}" target="_blank" rel="noopener">message us</a> for your 15-day key. The Android app pairs with that PC over your Wi-Fi. <a href="/slate/">About Slate</a></p>
  </div>
</div>'''.format(
        fv=f['version'], fos=f['os'], fp=f['price'], fu=f['unit'],
        pv=p['version'], pos=p['os'], pp=p['price'], pu=p['unit'],
        sv=s['version'], sos=s['os'], sp=s['price'], su=s['unit'],
        f_win=btn(DL['folio_win'], 'Windows installer', 'btn--primary', WIN_ICON),
        f_lin=btn(DL['folio_linux'], 'Linux AppImage', 'btn--ghost', LINUX_ICON),
        p_win=btn(DL['pass_win'], 'Windows installer', 'btn--primary', WIN_ICON),
        p_deb=btn(DL['pass_deb'], 'Linux .deb (Ubuntu, Debian, Mint)', 'btn--ghost', LINUX_ICON),
        p_app=btn(DL['pass_appimg'], 'Linux AppImage', 'btn--ghost', LINUX_ICON),
        s_win=btn(DL['slate_win'], 'Windows installer', 'btn--primary', WIN_ICON),
        s_deb=btn(DL['slate_deb'], 'Linux .deb (Ubuntu, Debian, Mint)', 'btn--ghost', LINUX_ICON),
        s_app=btn(DL['slate_appimg'], 'Linux AppImage', 'btn--ghost', LINUX_ICON),
        s_apk=btn(DL['slate_apk'], 'Android app (APK)', 'btn--ghost', ANDROID_ICON),
        p_wa=wa_link("Hi, I've downloaded Pass. Please send my 15-day trial key."),
        s_wa=wa_link("Hi, I've downloaded Slate. Please send my 15-day trial key."))

    faqs = [
        ('Is the trial really free?', 'Yes. Every TBN product runs as the complete software for 15 days with no card taken and no feature switched off. If you do nothing at the end of the trial, nothing is charged — the software simply asks for a licence key.'),
        ('What happens when the 15 days end?', 'The app stops at its licence screen until a paid key is entered. Your data stays on your computer; nothing is deleted. Enter the paid key and you carry on exactly where you left off.'),
        ('Windows says "Windows protected your PC". Is it safe?', 'Yes. Our Windows installers are not code-signed yet, so SmartScreen shows a warning for any publisher it has not seen before. Click <strong>More info</strong>, then <strong>Run anyway</strong>. The files come straight from our official GitHub release pages, and we are arranging a signing certificate.'),
        ('Which Windows versions are supported?', 'Windows 10 and Windows 11, 64-bit. Windows 7 and 8 are not supported.'),
        ('Which Linux file should I take?', 'On Ubuntu, Debian, Linux Mint, Pop!_OS or elementary, take the <strong>.deb</strong> where one is offered. Anything else, take the <strong>AppImage</strong>. If an AppImage complains about <code>libfuse.so.2</code>, run <code>sudo apt install libfuse2</code> once. Full commands are on each product page.'),
        ('Can I trial on more than one computer?', 'Each computer gets one trial per product, and trying Folio does not use up a Pass or Slate trial. If you need a second machine for testing, message us.'),
        ('Do I need internet?', 'Only briefly. Starting a trial and receiving updates need a connection; billing, printing, reports and backups all run fully offline after that.'),
        ('Will you help me install it?', 'Yes. Installation, onboarding and staff training are included with every licence, and we are happy to do the trial install with you over a call.'),
    ]
    body = '''<section class="hero"><div class="container">
  <span class="hero__eyebrow">Free 15-day trial · No card</span>
  <h1 class="hero__title">Download TBN software, <em>free for 15 days.</em></h1>
  <p class="hero__lede">The complete software, not a demo. Pick your product, pick your computer, and you can be billing within the hour. Every download below is the latest release, straight from our official GitHub release page.</p>
  <p class="updated">Versions checked {upd} · download links verified weekly</p>
</div></section>
<section class="section" id="downloads"><div class="container">
{cards}
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="section-tag">Windows</div><h2 class="section-title">Installing on Windows.</h2></div>
  <ol class="steps">
    <li><strong>Download the Windows installer</strong> for your product above.</li>
    <li><strong>Open it.</strong> If Windows shows "Windows protected your PC", click <strong>More info</strong> and then <strong>Run anyway</strong> — this appears because the installer is not code-signed yet.</li>
    <li><strong>Start the trial.</strong> Folio offers the 15-day trial on its first screen. For Pass and Slate, message us on WhatsApp and we send a 15-day key.</li>
    <li><strong>Run the setup wizard</strong> — business details, GSTIN, rooms or tables, and printer. Most properties are done in a few minutes.</li>
  </ol>
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="section-tag">Linux</div><h2 class="section-title">Installing on Linux.</h2>
  <p class="section-sub">Copy-paste commands for each product, including the .deb and AppImage options and the fix for the common <code>libfuse.so.2</code> error: <a href="/folio/#linux">Folio on Linux</a> · <a href="/pass/#linux">Pass on Linux</a> · <a href="/slate/#linux">Slate on Linux</a>.</p></div>
  <div class="cmd">wget {pass_deb}</div>
  <div class="cmd">sudo apt install ./Pass-amd64.deb</div>
  <p class="section-sub" style="margin-top:12px">Example shown for Pass. Launch it afterwards from your applications menu, or with <code>pass-pos</code>.</p>
</div></section>
<section class="section"><div class="container container--narrow">
  <div class="section-head"><div class="section-tag">Questions</div><h2 class="section-title">Before you download.</h2></div>
  {faq}
</div></section>'''.format(upd=UPDATED_HUMAN, cards=cards, pass_deb=DL['pass_deb'], faq=faq_html(faqs))

    apps = []
    for key, cat, osys, durls, extra in [
        ('folio', 'BusinessApplication', 'Windows 10, Windows 11, Linux', [DL['folio_win'], DL['folio_linux']], 'Hotel room-service ordering and billing software.'),
        ('pass', 'BusinessApplication', 'Windows 10, Windows 11, Linux', [DL['pass_win'], DL['pass_deb'], DL['pass_appimg']], 'Restaurant POS and management software.'),
        ('slate', 'BusinessApplication', 'Windows 10, Windows 11, Linux, Android', [DL['slate_win'], DL['slate_deb'], DL['slate_appimg'], DL['slate_apk']], 'Hotel management system (PMS).'),
    ]:
        fx = FACTS[key]
        apps.append({'@type': 'SoftwareApplication', 'name': fx['name'], 'applicationCategory': cat,
                     'operatingSystem': osys, 'softwareVersion': fx['version'], 'description': extra,
                     'downloadUrl': durls, 'url': SITE + '/' + key + '/',
                     'offers': {'@type': 'Offer', 'price': fx['price'].replace(',', ''), 'priceCurrency': 'INR',
                                'description': '₹%s %s. 15-day free trial.' % (fx['price'], fx['unit'])},
                     'publisher': {'@id': SITE + '/#organization'}})
    schema = [
        {'@context': 'https://schema.org', '@type': 'WebPage', '@id': SITE + '/download/#webpage',
         'url': SITE + '/download/', 'name': 'Download TBN software — free 15-day trial',
         'inLanguage': 'en-IN', 'dateModified': UPDATED, 'isPartOf': {'@id': SITE + '/#website'},
         'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': n + 1, 'item': a} for n, a in enumerate(apps)]}},
        dict(faq_ld(faqs)),
    ]
    write('/download/', page(
        path='/download/', title='Download Folio, Pass & Slate — Free 15-Day Trial | TBN',
        description='Download hotel and restaurant billing software for Windows, Linux and Android. Folio, Pass and Slate — the complete software free for 15 days, no card. Latest versions, install steps and Linux commands.',
        body=body, crumbs=[('The Binary Brain Network', '/'), ('Download', '/download/')], schema=schema,
        section_label='Download', wa_text="Hi, I'd like help installing a TBN free trial.", final_cta=False))

# ======================================================================
# /pricing/
# ======================================================================
def pricing_page():
    f, p, s = FACTS['folio'], FACTS['pass'], FACTS['slate']
    cards = '''<div class="price-grid">
  <div class="pcard">
    <div class="pcard__name">Folio · Live</div>
    <p class="pcard__for">Room-service billing for hotels that already have a PMS.</p>
    <div class="pcard__price">₹{fp}</div><div class="pcard__unit">{fu} · flat</div>
    <ul><li>Unlimited rooms, tabs, menu items and partner restaurants</li><li>GST, composition (Bill of Supply) and FSSAI on bills</li><li>Dues with aging, bill rectification, owner's daily report</li><li>Hourly encrypted backups, auto-recovery, full CSV export</li><li>Windows and Linux</li></ul>
    <a href="/download/#folio" class="btn btn--primary">{dl} Start 15-day trial</a>
  </div>
  <div class="pcard pcard--feature">
    <div class="pcard__name">Pass · In trials</div>
    <p class="pcard__for">Restaurant POS for cafés, QSRs, bars, bakeries and multi-outlet groups.</p>
    <div class="pcard__price">₹{pp}</div><div class="pcard__unit">{pu} · flat</div>
    <ul><li>Every outlet run from that computer included — separate GSTIN and bill series each</li><li>Kitchen Display System and station-wise KOT routing included</li><li>Inventory with recipes, suppliers and purchase orders</li><li>Staff attendance and payroll, UPI QR, split bills</li><li>Windows and Linux</li></ul>
    <a href="/download/#pass" class="btn btn--primary">{dl} Start 15-day trial</a>
  </div>
  <div class="pcard">
    <div class="pcard__name">Slate · In trials</div>
    <p class="pcard__for">Full hotel management system for 5 to 100 rooms.</p>
    <div class="pcard__price">₹{sp}</div><div class="pcard__unit">{su} · flat</div>
    <ul><li>Not per room and not per device — unlimited phones and tablets on your network</li><li>Bookings, room board, rates, hourly stays, groups, folios</li><li>GST invoicing, C-Form, GSTR-1 and Tally export, 16 reports</li><li>Housekeeping, F&amp;B till, inventory, laundry, payroll</li><li>Windows, Linux and Android</li></ul>
    <a href="/download/#slate" class="btn btn--primary">{dl} Start 15-day trial</a>
  </div>
</div>'''.format(fp=f['price'], fu=f['unit'], pp=p['price'], pu=p['unit'], sp=s['price'], su=s['unit'], dl=DL_ICON)

    table = '''<div class="ctable-wrap"><table class="ctable">
<thead><tr><th>Scenario</th><th>Typical cloud subscription</th><th>TBN</th><th>5-year difference</th></tr></thead>
<tbody>
<tr><td>20-room hotel, full PMS</td><td>₹100 per room per month = ₹24,000 a year → <strong>₹1,20,000</strong> over 5 years</td><td>Slate ₹12,000 a year → <strong>₹60,000</strong></td><td class="yes">₹60,000 less</td></tr>
<tr><td>40-room hotel, full PMS</td><td>₹100 per room per month = ₹48,000 a year → <strong>₹2,40,000</strong></td><td>Slate → <strong>₹60,000</strong> (same price at any size)</td><td class="yes">₹1,80,000 less</td></tr>
<tr><td>Single restaurant, one billing PC</td><td>₹1,500 a month = ₹18,000 a year → <strong>₹90,000</strong></td><td>Pass ₹7,500 a year → <strong>₹37,500</strong></td><td class="yes">₹52,500 less</td></tr>
<tr><td>Hotel with a PMS but no room-service module</td><td>Separate restaurant POS at ₹1,000 a month → <strong>₹60,000</strong></td><td>Folio ₹6,500 a year → <strong>₹32,500</strong></td><td class="yes">₹27,500 less</td></tr>
</tbody></table></div>
<p class="section-sub">Subscription figures are illustrative, taken from the middle of the ranges commonly quoted in India (₹50–₹200 per room per month for hotel PMS; ₹800–₹2,500 a month for cloud restaurant POS). Your own quote may be higher or lower — run your real numbers in the <a href="/tools/software-cost-calculator/">cost calculator</a>.</p>'''

    faqs = [
        ('How much does TBN software cost?', 'Folio costs ₹6,500 per property per year. Pass costs ₹7,500 per billing computer per year, with every outlet run from that computer included. Slate costs ₹12,000 per property per year, not per room and not per device. Each has a 15-day free trial of the complete software.'),
        ('Is it a subscription?', 'It is an annual licence, not a monthly SaaS plan. You pay once a year; there are no per-seat, per-room or per-device charges and no paid add-on tiers. Renewal is never automatic — we contact you before it is due and you confirm.'),
        ('What is included in the price?', 'The complete product, installation, onboarding, staff training, updates for the year and a direct WhatsApp support line. Nothing is held back for a higher tier.'),
        ('Why does Pass charge per computer?', 'Each Pass installation is its own billing station, and the licence is bound to that computer. Everything you run from it — any number of outlets, each with its own GSTIN and bill series — is included.'),
        ('Is there a discount for referrals?', 'Yes. Refer another business that buys a licence and you get ₹1,500 off, credited immediately rather than held for renewal. It stacks across referrals. The business you refer pays the standard price.'),
        ('Do I need to buy new hardware?', 'Usually not. Every product runs on a Windows 10/11 or Linux PC you already own, with a standard thermal receipt printer. Slate adds Android phones you already have.'),
        ('What happens to my data if I stop paying?', 'It stays on your computer. Every product exports your data — Folio as 16 CSV files, Pass and Slate to Excel and PDF — so leaving never means losing your records.'),
    ]
    offers = [{'@type': 'Offer', 'name': FACTS[k]['name'], 'price': FACTS[k]['price'].replace(',', ''),
               'priceCurrency': 'INR', 'url': SITE + '/' + k + '/',
               'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': FACTS[k]['price'].replace(',', ''),
                                      'priceCurrency': 'INR', 'unitText': FACTS[k]['unit']}} for k in ('folio', 'pass', 'slate')]
    schema = [{'@context': 'https://schema.org', '@type': 'WebPage', '@id': SITE + '/pricing/#webpage',
               'url': SITE + '/pricing/', 'name': 'TBN software pricing', 'inLanguage': 'en-IN',
               'dateModified': UPDATED, 'isPartOf': {'@id': SITE + '/#website'},
               'about': {'@type': 'OfferCatalog', 'name': 'TBN software licences', 'itemListElement': offers}},
              faq_ld(faqs)]
    body = '''<section class="hero"><div class="container">
  <span class="hero__eyebrow">Published prices · No demo call needed</span>
  <h1 class="hero__title">Pricing that fits on <em>one line.</em></h1>
  <p class="hero__lede">Flat annual licences. No per-room, per-seat or per-device charges, no add-on tiers, no monthly bill. Installation and training included. Every product free for 15 days first.</p>
</div></section>
<section class="section"><div class="container">
  <div class="answer"><div class="answer__label">The short answer</div>
  <p><strong>Folio ₹6,500 per property per year. Pass ₹7,500 per billing computer per year. Slate ₹12,000 per property per year.</strong> All three include installation, training and a year of updates, and each runs free for 15 days with no card.</p></div>
  {cards}
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="section-tag">Five-year view</div><h2 class="section-title">What a flat licence saves against a subscription.</h2>
  <p class="section-sub">Software is a five-year decision, so compare five-year totals rather than the first month.</p></div>
  {table}
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="section-tag">Every licence</div><h2 class="section-title">Included, whichever product you choose.</h2></div>
  <div class="cards cards--3">
    <div class="card"><div class="card__num">01</div><h3 class="card__title">Installation and training</h3><p class="card__desc">We set it up with you and train your staff on a live walkthrough. No setup fee.</p></div>
    <div class="card"><div class="card__num">02</div><h3 class="card__title">Works offline</h3><p class="card__desc">Billing, printing, reports and backups run with the internet unplugged. Your data lives on your own machine.</p></div>
    <div class="card"><div class="card__num">03</div><h3 class="card__title">Updates for the year</h3><p class="card__desc">New releases download in the background and install on restart — never mid-shift.</p></div>
    <div class="card"><div class="card__num">04</div><h3 class="card__title">Your data, exportable</h3><p class="card__desc">Excel, PDF and CSV exports. Leaving never means losing your records.</p></div>
    <div class="card"><div class="card__num">05</div><h3 class="card__title">Direct WhatsApp support</h3><p class="card__desc">A real person on +91 88790 70732, not a ticket queue.</p></div>
    <div class="card"><div class="card__num">06</div><h3 class="card__title">₹1,500 per referral</h3><p class="card__desc">Credited immediately when a business you refer buys a licence. Stacks across referrals.</p></div>
  </div>
</div></section>
<section class="section"><div class="container container--narrow">
  <div class="section-head"><div class="section-tag">Questions</div><h2 class="section-title">Pricing questions, answered.</h2></div>
  {faq}
  <p class="updated">Prices current as of {upd}. Terms: <a href="/terms/" style="color:var(--amber)">licence, trial and referral terms</a>.</p>
</div></section>'''.format(cards=cards, table=table, faq=faq_html(faqs), upd=UPDATED_HUMAN)
    write('/pricing/', page(
        path='/pricing/', title='Pricing — Hotel & Restaurant Software from ₹6,500/year | TBN',
        description='Published prices: Folio ₹6,500/property/year, Pass ₹7,500/billing computer/year, Slate ₹12,000/property/year. No per-room or per-device fees, installation and training included, 15-day free trial.',
        body=body, crumbs=[('The Binary Brain Network', '/'), ('Pricing', '/pricing/')], schema=schema,
        section_label='Pricing', wa_text="Hi, I have a question about TBN pricing."))

# ======================================================================
# /tools/software-cost-calculator/
# ======================================================================
def calculator_page():
    body = '''<section class="hero"><div class="container">
  <span class="hero__eyebrow">Free tool · No signup</span>
  <h1 class="hero__title">Hotel &amp; restaurant software <em>cost calculator.</em></h1>
  <p class="hero__lede">What will your current software cost over three or five years — and what would a flat annual licence cost instead? Enter what you pay today.</p>
</div></section>
<section class="section"><div class="container">
  <div class="calc" id="calc">
    <div>
      <div class="field"><label for="c-type">Your business</label>
        <select id="c-type"><option value="hotel">Hotel — full management system</option><option value="rs">Hotel — room-service billing only</option><option value="rest">Restaurant / café / bar</option></select></div>
      <div class="field"><label for="c-model">How you are charged today</label>
        <select id="c-model"><option value="room">Per room, per month</option><option value="month">Flat, per month</option><option value="year">Flat, per year</option></select></div>
      <div class="field" id="f-rooms"><label for="c-rooms">Number of rooms</label><input id="c-rooms" type="number" min="1" value="20" inputmode="numeric"></div>
      <div class="field" id="f-pcs" hidden><label for="c-pcs">Billing computers</label><input id="c-pcs" type="number" min="1" value="1" inputmode="numeric"><p class="hint">Pass is licensed per billing computer; every outlet run from it is included.</p></div>
      <div class="field"><label for="c-amt">What you pay (₹)</label><input id="c-amt" type="number" min="0" value="100" inputmode="numeric"><p class="hint" id="c-amt-hint">Per room, per month.</p></div>
      <div class="field"><label for="c-yrs">Over how many years</label><select id="c-yrs"><option>3</option><option selected>5</option></select></div>
    </div>
    <div class="out" aria-live="polite">
      <div class="out__row"><span>Your current software</span><b id="o-cur">—</b></div>
      <div class="out__row"><span id="o-tbn-l">TBN equivalent</span><b id="o-tbn">—</b></div>
      <div class="out__big"><div class="lbl" id="o-lbl">Difference</div><div class="val" id="o-diff">—</div></div>
      <p class="out__note" id="o-note"></p>
      <a href="/download/" class="btn btn--primary" style="margin-top:18px">Try it free for 15 days</a>
    </div>
  </div>
  <p class="section-sub" style="margin-top:22px">The TBN figure is the published licence price — <a href="/pricing/">Folio ₹6,500, Pass ₹7,500 per computer, Slate ₹12,000</a> a year — with installation and training included. It assumes today's prices hold; renewals are always confirmed in advance. Your current software may include things ours does not, such as an OTA channel manager; <a href="/compare/">our buyer's guides</a> say where.</p>
</div></section>
<script>
(function(){
  var $=function(i){return document.getElementById(i)};
  var price={hotel:12000,rs:6500,rest:7500}, name={hotel:'Slate',rs:'Folio',rest:'Pass'};
  var used=false;
  function fmt(n){return '₹'+Math.round(n).toLocaleString('en-IN');}
  function calc(){
    var t=$('c-type').value, m=$('c-model').value, yrs=+$('c-yrs').value;
    var rooms=Math.max(1,+$('c-rooms').value||1), pcs=Math.max(1,+$('c-pcs').value||1), amt=Math.max(0,+$('c-amt').value||0);
    $('f-pcs').hidden = t!=='rest';
    $('f-rooms').hidden = m!=='room';
    $('c-amt-hint').textContent = m==='room'?'Per room, per month.':m==='month'?'Per month, in total.':'Per year, in total.';
    var perYear = m==='room'? amt*rooms*12 : m==='month'? amt*12 : amt;
    var cur = perYear*yrs;
    var tbn = price[t]*(t==='rest'?pcs:1)*yrs;
    $('o-cur').textContent=fmt(cur);
    $('o-tbn-l').textContent=name[t]+' over '+yrs+' years';
    $('o-tbn').textContent=fmt(tbn);
    var d=cur-tbn;
    $('o-lbl').textContent = d>=0 ? 'You would spend less with '+name[t] : 'Your current software costs less';
    $('o-diff').textContent = fmt(Math.abs(d));
    $('o-note').textContent = d>=0 ? 'That is '+Math.round(d/Math.max(cur,1)*100)+'% of your current '+yrs+'-year spend.' : 'If you are already paying less than our licence, staying put may be the right call.';
  }
  ['c-type','c-model','c-rooms','c-pcs','c-amt','c-yrs'].forEach(function(id){
    $(id).addEventListener('input',function(){calc(); if(!used){used=true; window.tbnTrack&&window.tbnTrack('calculator_used',{product:name[$('c-type').value].toLowerCase()});}});
  });
  calc();
})();
</script>'''
    faqs = [
        ('How much does hotel management software cost in India?', 'Cloud hotel PMS in India is commonly priced at ₹50 to ₹200 per room per month, or ₹10,000 to ₹25,000 a year for flat-priced products. Slate is ₹12,000 per property per year regardless of room count.'),
        ('How much does restaurant billing software cost in India?', 'Cloud restaurant POS commonly runs ₹800 to ₹2,500 a month; self-hosted licences are typically ₹6,000 to ₹9,000 a year. Pass is ₹7,500 per billing computer per year.'),
    ]
    schema = [{'@context': 'https://schema.org', '@type': 'WebApplication', 'name': 'Hotel & restaurant software cost calculator',
               'url': SITE + '/tools/software-cost-calculator/', 'applicationCategory': 'BusinessApplication',
               'operatingSystem': 'Any (web browser)', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'INR'},
               'publisher': {'@id': SITE + '/#organization'}, 'dateModified': UPDATED}, faq_ld(faqs)]
    body += '<section class="section"><div class="container container--narrow"><div class="section-head"><div class="section-tag">Market prices</div><h2 class="section-title">Typical prices in India.</h2></div>%s</div></section>' % faq_html(faqs)
    write('/tools/software-cost-calculator/', page(
        path='/tools/software-cost-calculator/', title='Hotel & Restaurant Software Cost Calculator (India) | TBN',
        description='Free calculator: what your hotel PMS or restaurant POS subscription costs over 3 or 5 years, compared with a flat annual licence. Per-room, monthly or yearly pricing. No signup.',
        body=body, crumbs=[('The Binary Brain Network', '/'), ('Tools', '/tools/'), ('Software cost calculator', '/tools/software-cost-calculator/')],
        schema=schema, section_label='Tools'))

# ======================================================================
# /privacy/ and /terms/
# ======================================================================
def privacy_page():
    body = '''<section class="hero"><div class="container container--narrow">
  <span class="hero__eyebrow">Effective {upd}</span>
  <h1 class="hero__title">Privacy policy</h1>
  <p class="hero__lede">What this website and our software collect, why, and what you can do about it — in plain language.</p>
</div></section>
<section class="section"><div class="container container--narrow legal">
<h2>Who we are</h2>
<p>This website, tbn.tbbn.in, is run by <strong>The Binary Brain Network</strong> ("TBN", "we"), the software division of The Big Brand Network, Mumbai, Maharashtra, India. For anything in this policy, write to <a href="mailto:tbn@tbbn.in">tbn@tbbn.in</a> or WhatsApp <a href="tel:+918879070732">+91 88790 70732</a>. We act as the data fiduciary for the personal data described here, under India's Digital Personal Data Protection Act, 2023.</p>

<h2>What this website collects</h2>
<h3>When you contact us</h3>
<p>The site has no forms. If you message us on WhatsApp, call or email, we receive what you send — usually your name, phone number, business name and your question — and use it only to reply, arrange a trial or demo, and provide support. Pre-filled WhatsApp messages include a short reference to the page you came from (for example <em>ref: /pass/</em>) so we know what you were reading; you can delete it before sending.</p>
<h3>Measurement and advertising</h3>
<p>We use Google Tag Manager to load measurement and advertising tools. <strong>Until you choose "Accept" on the cookie bar, these run without cookies or identifiers</strong> (Google's consent mode), and advertising tools do not load at all. If you accept, the following may set cookies or similar identifiers:</p>
<ul>
<li><strong>Google Analytics</strong> — which pages are read and which downloads are started.</li>
<li><strong>Google Ads, Meta (Facebook and Instagram), Microsoft Advertising and LinkedIn</strong> — whether a visit that came from one of our ads went on to download a trial or contact us, so we can measure and improve the ads.</li>
<li><strong>Microsoft Clarity</strong> — anonymised heatmaps and session replays that show where a page confuses people. Clarity masks text you type.</li>
</ul>
<p>These providers process data under their own privacy policies and may do so outside India. We do not sell personal data, and we do not use it to make decisions about you.</p>
<h3>Choices you have</h3>
<p>You can decline on the cookie bar and the site works exactly the same. To change your mind, clear this site's data in your browser and the bar will appear again. Browser settings and ad-blockers also block these tools.</p>

<h2>What our software collects</h2>
<p>Folio, Pass and Slate are <strong>installed on your own computer and keep your business data there</strong> — your bills, guests, menu, staff and reports are not sent to us.</p>
<ul>
<li><strong>Licence and trial activation.</strong> When you start a trial or activate a licence, the software sends your business name, phone number and an identifier derived from your computer to our licence server, so that each computer gets one trial and a key cannot be copied to another machine. We are notified by email of each new trial so we can offer help.</li>
<li><strong>Licence checks.</strong> When online, the software periodically checks whether its key has been revoked.</li>
<li><strong>Updates.</strong> The software checks our GitHub release page for new versions.</li>
<li><strong>Crash reports.</strong> If the software crashes it can send an error report with personal details removed. You can switch this off in the app's settings.</li>
<li><strong>Features you switch on.</strong> Some optional features use the internet on your instruction — sending a bill or alert on WhatsApp, emailing a report from your own email account, or confirming a UPI payment with Razorpay or PhonePe. That data goes to the service you chose, not to us.</li>
</ul>
<p>Each product also includes its own privacy notice inside the app.</p>

<h2>How long we keep it</h2>
<p>Conversations and customer records are kept while we have a business relationship with you and for as long afterwards as tax and accounting law requires. Licence and trial records are kept for the life of the licence plus that period. Analytics data is kept for the retention period set in each tool, at most 14 months for Google Analytics.</p>

<h2>Your rights</h2>
<p>You may ask us to tell you what personal data we hold about you, correct it, or erase it where we are not required to keep it; withdraw consent at any time; and nominate someone to exercise these rights on your behalf. Write to <a href="mailto:tbn@tbbn.in">tbn@tbbn.in</a>; we reply within 30 days. If you are not satisfied, you may approach the Data Protection Board of India.</p>

<h2>Grievance officer</h2>
<p>The Binary Brain Network, Mumbai, Maharashtra — <a href="mailto:tbn@tbbn.in">tbn@tbbn.in</a>, +91 88790 70732.</p>

<h2>Children</h2>
<p>This website and our software are meant for businesses and are not directed at children.</p>

<h2>Changes</h2>
<p>If we change this policy we will update the date at the top. Significant changes will be shown on this page for at least 30 days.</p>
</div></section>'''.format(upd=UPDATED_HUMAN)
    schema = [{'@context': 'https://schema.org', '@type': 'WebPage', 'url': SITE + '/privacy/', 'name': 'Privacy policy',
               'inLanguage': 'en-IN', 'dateModified': UPDATED, 'isPartOf': {'@id': SITE + '/#website'},
               'publisher': {'@id': SITE + '/#organization'}}]
    write('/privacy/', page(path='/privacy/', title='Privacy Policy | The Binary Brain Network',
        description='How The Binary Brain Network handles personal data on tbn.tbbn.in and in Folio, Pass and Slate: cookies and consent, licence activation, your rights under the DPDP Act 2023.',
        body=body, crumbs=[('The Binary Brain Network', '/'), ('Privacy', '/privacy/')], schema=schema,
        section_label='Privacy', final_cta=False))

def terms_page():
    body = '''<section class="hero"><div class="container container--narrow">
  <span class="hero__eyebrow">Effective {upd}</span>
  <h1 class="hero__title">Terms: website, trials, licences and referrals</h1>
  <p class="hero__lede">The commercial terms behind the prices on this site. Each product's full licence agreement (EULA) is shown inside the software and accepted on installation; if anything here conflicts with it, the in-app agreement applies.</p>
</div></section>
<section class="section"><div class="container container--narrow legal">
<h2>1. The website</h2>
<p>tbn.tbbn.in is published by The Binary Brain Network, the software division of The Big Brand Network, Mumbai. We try hard to keep it accurate — features we have not shipped are labelled "Coming Soon" — but product details, prices and availability can change. Buyer's guides and blog posts are general information, not tax, legal or financial advice; confirm GST and compliance questions with your accountant.</p>

<h2>2. Free trials</h2>
<ul>
<li>Folio, Pass and Slate each offer a <strong>15-day free trial of the complete software</strong>. No payment details are taken.</li>
<li>One trial per product per computer. Trialling one product does not use up the trial of another.</li>
<li>Starting a trial needs an internet connection once. Folio starts its trial from inside the app; for Pass and Slate we issue the trial key on request.</li>
<li>When the trial ends the software stops at its licence screen until a paid key is entered. Your data stays on your computer and is not deleted.</li>
<li>Nothing is charged automatically at the end of a trial.</li>
</ul>

<h2>3. Licences and prices</h2>
<ul>
<li><strong>Folio</strong> — ₹6,500 per property per year.</li>
<li><strong>Pass</strong> — ₹7,500 per billing computer per year. Every outlet operated from that computer's installation is included.</li>
<li><strong>Slate</strong> — ₹12,000 per property per year, not per room and not per device. Phones and tablets connecting to the licensed front-desk computer on the property's network are included.</li>
<li>Licences run for one year and are bound to the computer they are activated on.</li>
<li>Installation, onboarding and staff training are included. Updates released during the licence year are included.</li>
<li>Renewal is not automatic. We contact you before renewal; the renewal price is confirmed with you in advance and never changes during a licence term.</li>
</ul>

<h2>4. Referral credit</h2>
<ul>
<li>If a business you refer buys a paid licence for any TBN product, <strong>you — the referring customer — receive a ₹1,500 credit</strong>, applied immediately against your account rather than held until renewal.</li>
<li>Credits stack across successful referrals. The referred business pays the standard price, and can then earn referral credit of its own.</li>
<li>Credit is given once per referred business.</li>
</ul>

<h2>5. Your data</h2>
<p>Your business data stays on your hardware and remains yours. Every product exports it in standard formats. Our handling of the limited data we do receive is described in the <a href="/privacy/">privacy policy</a>.</p>

<h2>6. Responsibility</h2>
<p>The software helps you produce correct bills, tax documents and compliance records, but you remain responsible for the information you enter, the GST rates and registrations you configure, and your filings. Keep backups — each product makes them automatically — and keep copies off the machine for anything you cannot afford to lose. Our liability is limited as set out in each product's licence agreement.</p>

<h2>7. Contact and jurisdiction</h2>
<p>Questions: <a href="mailto:tbn@tbbn.in">tbn@tbbn.in</a> or +91 88790 70732. These terms are governed by the laws of India, with courts at Mumbai having jurisdiction.</p>
</div></section>'''.format(upd=UPDATED_HUMAN)
    schema = [{'@context': 'https://schema.org', '@type': 'WebPage', 'url': SITE + '/terms/', 'name': 'Terms',
               'inLanguage': 'en-IN', 'dateModified': UPDATED, 'isPartOf': {'@id': SITE + '/#website'},
               'publisher': {'@id': SITE + '/#organization'}}]
    write('/terms/', page(path='/terms/', title='Terms — Trials, Licences & Referrals | The Binary Brain Network',
        description='Commercial terms for Folio, Pass and Slate: 15-day free trials, annual licence pricing, renewal, ₹1,500 referral credit, and website terms.',
        body=body, crumbs=[('The Binary Brain Network', '/'), ('Terms', '/terms/')], schema=schema,
        section_label='Terms', final_cta=False))

if __name__ == '__main__':
    download_page(); pricing_page(); calculator_page(); privacy_page(); terms_page()
