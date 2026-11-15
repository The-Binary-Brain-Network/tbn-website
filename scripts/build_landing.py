"""
High-intent "free download" landing pages — the exact phrases Indian owners
search for ("restaurant billing software free download for pc", etc.).
Each is honest: it's a free 15-day trial of the full product, not freeware.

Run:  python scripts/build_landing.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tbnsite import page, DL, WA_ICON, WIN_ICON, DL_ICON, wa_link, faq_html, faq_ld, SITE
from build_pages import FACTS, write, btn, LINUX_ICON, ANDROID_ICON, UPDATED

COMMON_FAQ = [
    ('Is it really free?', 'The download is free and the complete software runs free for 15 days, with no card and no feature switched off. After that it needs a paid licence; your data stays on your computer either way.'),
    ('Is it safe to install? Windows shows a warning.', 'Yes. The installer is not code-signed yet, so Windows SmartScreen shows "Windows protected your PC" for any new publisher. Click <strong>More info</strong>, then <strong>Run anyway</strong>. Files come straight from our official GitHub release page.'),
    ('Which Windows versions does it run on?', 'Windows 10 and Windows 11, 64-bit. Linux (64-bit) is supported too. Windows 7 and 8 are not.'),
    ('Does it need internet?', 'Only to start the trial and get updates. Billing, printing, reports and backups all work offline.'),
    ('Will someone help me set it up?', 'Yes. Message us on WhatsApp at +91 88790 70732 and we will install it with you over a call. Installation and staff training are included when you buy.'),
]

def landing(*, path, title, description, eyebrow, h1, lede, answer, product, buttons, trial_note, bullets, who, faqs, wa_text, crumb):
    f = FACTS[product]
    li = ''.join('<li>%s</li>' % b for b in bullets)
    body = '''<section class="hero"><div class="container">
  <span class="hero__eyebrow">{eyebrow}</span>
  <h1 class="hero__title">{h1}</h1>
  <p class="hero__lede">{lede}</p>
  <div class="hero__actions">{buttons}<a href="{wa}" target="_blank" rel="noopener" class="btn btn--whatsapp">{wa_icon} Help me install</a></div>
  <p class="updated">{name} {ver} · {os} · ₹{price} {unit} after the trial</p>
</div></section>
<section class="section"><div class="container container--narrow">
  <div class="answer"><div class="answer__label">Short answer</div><p>{answer}</p></div>
  <div class="note">{trial_note}</div>
  <div class="section-head"><div class="section-tag">What you get in the free trial</div><h2 class="section-title">The complete software, not a demo.</h2></div>
  <div class="prose"><ul>{li}</ul></div>
</div></section>
<section class="section"><div class="container container--narrow">
  <div class="section-head"><div class="section-tag">Install in 3 steps</div><h2 class="section-title">From download to first bill.</h2></div>
  <ol class="steps">
    <li><strong>Download</strong> the installer above (Windows) or the Linux file.</li>
    <li><strong>Open it.</strong> If Windows shows "Windows protected your PC", click <strong>More info</strong> → <strong>Run anyway</strong>.</li>
    <li><strong>Start the 15-day trial</strong> — {trial_short} — and run the short setup wizard.</li>
  </ol>
  <p class="section-sub" style="margin-top:18px">Who it's for: {who} Not sure it fits? See <a href="/{product}/">the full {name} page</a>, <a href="/pricing/">pricing</a> or <a href="/download/">all downloads</a>.</p>
</div></section>
<section class="section"><div class="container container--narrow">
  <div class="section-head"><div class="section-tag">Questions</div><h2 class="section-title">Before you download.</h2></div>
  {faq}
</div></section>'''.format(eyebrow=eyebrow, h1=h1, lede=lede, buttons=buttons, wa=wa_link(wa_text), wa_icon=WA_ICON,
        name=f['name'], ver=f['version'], os=f['os'], price=f['price'], unit=f['unit'], answer=answer,
        trial_note=trial_note, li=li, trial_short=('choose "Try free for 15 days" on the first screen' if product == 'folio' else 'message us on WhatsApp and we send your 15-day key within minutes in working hours'),
        who=who, product=product, faq=faq_html(faqs + COMMON_FAQ))
    app = {'@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': f['name'],
           'applicationCategory': 'BusinessApplication', 'operatingSystem': f['os'].replace(' · ', ', ').replace('/11', ', Windows 11'),
           'softwareVersion': f['version'], 'url': SITE + '/' + product + '/', 'downloadUrl': SITE + '/download/#' + product,
           'offers': {'@type': 'Offer', 'price': f['price'].replace(',', ''), 'priceCurrency': 'INR',
                      'description': '15-day free trial, then ₹%s %s' % (f['price'], f['unit'])},
           'publisher': {'@id': SITE + '/#organization'}, 'dateModified': UPDATED}
    write(path, page(path=path, title=title, description=description, body=body,
                     crumbs=[('The Binary Brain Network', '/'), ('Download', '/download/'), (crumb, path)],
                     schema=[app, faq_ld(faqs + COMMON_FAQ)], section_label='Free Download',
                     wa_text=wa_text, og_image='/og-%s.svg' % product))

def main():
    landing(
        path='/restaurant-billing-software-free-download/',
        title='Restaurant Billing Software Free Download for PC (Windows 10/11, Linux) | Pass',
        description='Download Pass restaurant billing software for PC free — full POS for 15 days, no card. GST bills, KOT, kitchen display, UPI QR, inventory, works offline. Windows 10/11 and Linux.',
        eyebrow='Free download · 15-day full trial · No card',
        h1='Restaurant billing software, <em>free download for PC.</em>',
        lede='Pass is a complete restaurant POS for Windows and Linux: GST bills, KOT by kitchen station, a kitchen display, UPI QR, split bills, inventory and staff — and it keeps billing when the internet drops.',
        answer='You can download Pass, a restaurant billing software for Windows 10/11 and Linux, free from this page. It runs as the complete product for 15 days with no card. After the trial it costs ₹7,500 per billing computer per year — no monthly fees.',
        product='pass',
        buttons=btn(DL['pass_win'], 'Download for Windows', 'btn--primary', WIN_ICON) + btn('/pass/#linux', 'Linux (.deb / AppImage)', 'btn--ghost', LINUX_ICON),
        trial_note='After installing, message us on WhatsApp for your 15-day trial key — it is issued straight away in working hours. Full product, nothing locked.',
        bullets=['GST-compliant bills — flat, per-item or composition-scheme Bill of Supply, with GSTIN and FSSAI',
                 'Dine-in, takeaway and delivery; table floor plan; merge tables',
                 'KOT printed by kitchen station, plus a kitchen display screen at no extra cost',
                 'Split bills and split payments; static UPI QR or Razorpay / PhonePe QR that confirms itself',
                 'Inventory with recipes, suppliers and purchase orders; low-stock alerts',
                 'Staff attendance and salary sheet; PIN login per staff member',
                 'Multiple outlets, each with its own GSTIN and bill series',
                 'Reports: sales, items, GST, P&amp;L, expenses — export to Excel and PDF',
                 'Works fully offline; hourly automatic backups'],
        who='restaurants, cafés, QSRs, bars, bakeries and small groups that want predictable cost and offline billing. Not yet a fit if Swiggy/Zomato orders are most of your business, or you need several counters on one shared database today.',
        faqs=[('What is the best free billing software for a restaurant?', 'Truly free software usually lacks GST-correct bills, kitchen routing or support. Pass gives you the complete product free for 15 days to test on real service, then ₹7,500 a year per billing computer — less than most monthly cloud POS plans.'),
              ('Does it print KOT and bills on a thermal printer?', 'Yes — on 80mm thermal printers over USB or network, with separate printers for each kitchen station and for bills. 58mm is not supported yet.')],
        wa_text="Hi, I'd like to download Pass restaurant billing software. Please send my 15-day trial key.",
        crumb='Restaurant billing software free download')

    landing(
        path='/hotel-management-software-free-download/',
        title='Hotel Management Software Free Download (Windows, Linux, Android) | Slate',
        description='Download Slate hotel management software free — complete PMS for 15 days, no card. Bookings, room board, GST invoices, C-Form, housekeeping, night audit. Not per room: ₹12,000/year after.',
        eyebrow='Free download · 15-day full trial · No card',
        h1='Hotel management software, <em>free download.</em>',
        lede='Slate runs your front desk from one PC — bookings, room board, folios, GST invoices, Form-III (C-Form) for foreign guests, housekeeping on phones, night audit and 16 reports. Works offline.',
        answer='You can download Slate, a hotel management system (PMS) for Windows 10/11, Linux and Android, free from this page. The complete product runs for 15 days with no card. After that it costs ₹12,000 per property per year — not per room, not per device.',
        product='slate',
        buttons=btn(DL['slate_win'], 'Download for Windows', 'btn--primary', WIN_ICON) + btn('/slate/#linux', 'Linux', 'btn--ghost', LINUX_ICON) + btn(DL['slate_apk'], 'Android app', 'btn--ghost', ANDROID_ICON),
        trial_note='Install Slate on the front-desk PC, then message us on WhatsApp for your 15-day trial key. Phones and tablets connect over your hotel Wi-Fi at no extra charge.',
        bullets=['Walk-in and advance bookings, booking calendar, room moves',
                 'Live room board: occupied, dirty, clean, out of order, arrivals and departures',
                 'Rate plans and seasons, hourly stays, group bookings with master folio',
                 'GST invoices with configurable room-tariff bands (5% / 18%)',
                 'C-Form / Form-III register with passport scans and overdue flags',
                 'Housekeeping from any phone; inventory and laundry tracking',
                 'F&amp;B / room-service till that charges to the room',
                 'Night audit, staff attendance and payroll, GSTR-1 and Tally export',
                 '16 reports, 6 staff roles, daily automatic backups'],
        who='hotels, resorts, guest houses and lodges of roughly 5 to 100 rooms. Not yet a fit if you need a live OTA channel manager today (Slate\'s is in testing and partnership approval) or manage several properties from one system.',
        faqs=[('Is there free hotel management software in India?', 'Fully free hotel software rarely includes GST invoicing, Form-III or support. Slate is free for 15 days as the complete product, then ₹12,000 a year flat — a 20-room hotel paying ₹100 per room per month for a cloud PMS spends ₹24,000 a year.'),
              ('Does it work on mobile?', 'Yes. The front-desk PC runs Slate, and staff use the Android app or the installable web app (including on iPhone) over the hotel Wi-Fi.')],
        wa_text="Hi, I'd like to download Slate hotel management software. Please send my 15-day trial key.",
        crumb='Hotel management software free download')

    landing(
        path='/hotel-billing-software-free-download/',
        title='Hotel Billing Software Free Download — Room Service & Restaurant Bills | Folio',
        description='Download Folio hotel billing software free for 15 days — starts in the app, no card. Room-service tabs per room, GST bills, KOTs, dues, owner\'s daily report. Windows 10/11 and Linux, works offline.',
        eyebrow='Free download · trial starts in the app · No card',
        h1='Hotel billing software, <em>free download.</em>',
        lede='Folio bills everything your hotel sells after check-in — room service, restaurant orders, partner-restaurant food — with a tab per room, GST bills, dues tracking and an owner\'s report that prints itself. It runs alongside your existing hotel software.',
        answer='You can download Folio, hotel room-service and food billing software for Windows 10/11 and Linux, free from this page. Choose "Try Folio free for 15 days" on its first screen — no card, no call needed. After the trial it costs ₹6,500 per property per year.',
        product='folio',
        buttons=btn(DL['folio_win'], 'Download for Windows', 'btn--primary', WIN_ICON) + btn('/folio/#linux', 'Linux AppImage', 'btn--ghost', LINUX_ICON),
        trial_note='Folio starts its own 15-day trial: open it, choose "Try Folio free for 15 days", enter your hotel name and phone. It needs internet for that one step only.',
        bullets=['One open tab per room, with guest name and running total',
                 'Orders from your kitchen, a partner restaurant, or both — tracked to delivery',
                 'GST bills (regular) or Bill of Supply (composition), with FSSAI number',
                 'Combined bill for groups; bill corrections that keep the original',
                 'Dues and pay-later with aging (0–7, 8–30, 31–60, 60+ days)',
                 'Owner\'s daily report printed automatically; day close and shift handover',
                 '80mm and 58mm thermal printers, set up automatically',
                 'Encrypted database, hourly backups, full export to Excel/CSV'],
        who='hotels and guest houses that already have booking/front-desk software but no proper system for food and room-service bills. Live in production at a 34-room hotel in Mumbai.',
        faqs=[('Can I use it with my existing hotel software?', 'Yes. Folio runs alongside your current PMS on the same PC. Your PMS keeps bookings and check-ins; Folio handles room-service and food billing.')],
        wa_text="Hi, I've downloaded Folio. Can you help me set it up?",
        crumb='Hotel billing software free download')

if __name__ == '__main__':
    main()
