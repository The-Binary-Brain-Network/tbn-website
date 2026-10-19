# Tracking setup — The Binary Brain Network

The website already pushes these events into `dataLayer` (see `assets/tbn.js`):

| Event | When | Parameters |
|---|---|---|
| `trial_download` | Any installer link clicked | `product`, `os`, `file`, `cta_location`, `lead_source` |
| `whatsapp_click` | Any wa.me link | `product`, `cta_location`, `lead_source` |
| `phone_click` / `email_click` | tel: / mailto: links | `cta_location`, `lead_source` |
| `pricing_view` | Pricing section seen, or /pricing/ opened | `product` |
| `calculator_used` | Cost calculator first changed | `product` |
| `command_copy` | A Linux command copied | `command`, `product` |
| `scroll_depth` | 25 / 50 / 75 / 90% | `percent` |
| `cta_click` | Links to /download/ or /pricing/ | `target`, `cta_location` |
| `consent_granted` / `consent_denied` | Cookie bar choice | — |

`lead_source` is the visitor's first touch this session: `google-ads`, `meta`,
`microsoft-ads`, `linkedin`, UTM tags (`source/medium/campaign`), a referring
site, or `direct`. The same reference is appended to every pre-filled WhatsApp
message, so each sales chat shows where the lead came from.

Consent: Google Consent Mode v2 defaults are set in every page's `<head>`
before GTM loads. Everything is `denied` until the visitor clicks Accept;
Google tags then send cookieless pings only. Ad pixels in the container
require `ad_storage` consent and do not fire until Accept.

---

## 1. Create the accounts (under The Binary Brain Network, not TBBN)

Use **tbn@tbbn.in** (or a dedicated Google account for TBN) as the owner of
each. Do **not** add these to The Big Brand Network's existing Business
Manager, MCC or GA account — create new, separate ones.

| Account | Where | What you need back |
|---|---|---|
| Google Tag Manager | tagmanager.google.com → Create Account "The Binary Brain Network", container `tbn.tbbn.in` (Web) | Container ID `GTM-XXXXXXX` (only if GTM-TFBHC2VR turns out to belong to TBBN — see below) |
| Google Analytics 4 | analytics.google.com → Admin → Create account "The Binary Brain Network" → property "tbn.tbbn.in", India, INR → Web stream | Measurement ID `G-XXXXXXXXXX` |
| Google Ads | ads.google.com → new account, "Switch to Expert Mode" → skip campaign → Goals → Conversions → create two Website conversions set up "manually with Google Tag Manager": **Trial download** (category: Download) and **WhatsApp lead** (category: Contact) | Conversion ID `AW-XXXXXXXXXX` and the two conversion labels |
| Meta Business + Pixel | business.facebook.com → Create account "The Binary Brain Network" → Events Manager → Connect data source → Web → name "TBN website" | Pixel ID (15–16 digits) |
| Microsoft Clarity | clarity.microsoft.com → New project "tbn.tbbn.in" | Project ID (10 characters) |
| Microsoft Advertising | ads.microsoft.com → new account → Tools → UET tag → Create | UET tag ID (8 digits) |
| LinkedIn (optional, for custom-software campaigns) | Campaign Manager → Analyze → Insight tag | Partner ID |
| Google Search Console | search.google.com/search-console → Domain property `tbn.tbbn.in` (DNS TXT record in Cloudflare) → submit `https://tbn.tbbn.in/sitemap.xml` | — |
| Bing Webmaster Tools | bing.com/webmasters → Import from Search Console, or add site → submit sitemap | — |
| Google Business Profile | business.google.com → "The Binary Brain Network", category "Software company", service area India | — |

**GTM-TFBHC2VR:** check in tagmanager.google.com which account it sits under.
If it is inside a TBBN account, create a new container in a new TBN account
(GTM containers cannot be moved between accounts), send the new ID, and the
snippet on every page will be swapped for it.

## 2. Import the container

1. GTM → Admin → **Import Container** → choose `ops/gtm-container.json`.
2. Workspace: existing (or new) → **Merge** → "Rename conflicting tags".
3. Variables → User-Defined → replace each `ID - …` constant with the real IDs.
4. Tags → un-pause the tags for the accounts you created (all are paused on
   import so nothing fires with a placeholder ID).
5. Preview with Tag Assistant on tbn.tbbn.in: accept the cookie bar, click a
   download link and a WhatsApp button, and check the tags fire.
6. Submit and publish.

Regenerate the file after editing the script: `python scripts/build_gtm_container.py`.

## 3. In GA4, after the first data arrives

- Admin → Events → mark `trial_download` and `whatsapp_click` as **key events**.
- Admin → Custom definitions → add event-scoped dimensions `product`, `os`,
  `cta_location`, `lead_source`.
- Link GA4 to Google Ads and to Search Console.
