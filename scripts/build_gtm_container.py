"""
Builds ops/gtm-container.json: a Google Tag Manager container you can import
(Admin -> Import Container -> Merge) into GTM-TFBHC2VR, or into a new TBN
container. The website pushes plain dataLayer events (see assets/tbn.js);
this container decides which vendors receive them.

Every account ID is a Constant variable with a placeholder value. Replace
the placeholders in GTM (Variables -> User-Defined) and publish. Tags whose
ID is still a placeholder are paused, so nothing fires with a dummy ID.

Run:  python scripts/build_gtm_container.py
"""
import json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'ops', 'gtm-container.json')

_ids = {'tag': 0, 'trigger': 0, 'variable': 0}
def nid(kind):
    _ids[kind] += 1
    return str(_ids[kind])

def t(key, value):  return {'type': 'template', 'key': key, 'value': value}
def b(key, value):  return {'type': 'boolean', 'key': key, 'value': 'true' if value else 'false'}
def i(key, value):  return {'type': 'integer', 'key': key, 'value': str(value)}

ACC = {'accountId': '0', 'containerId': '0'}

# ---------------------------------------------------------------- variables
variables = []
def constant(name, value):
    variables.append(dict(ACC, variableId=nid('variable'), name=name, type='c',
                          parameter=[t('value', value)]))
def dlv(name, key):
    variables.append(dict(ACC, variableId=nid('variable'), name=name, type='v',
                          parameter=[i('dataLayerVersion', 2), b('setDefaultValue', False), t('name', key)]))

constant('ID - GA4 Measurement ID', 'G-XXXXXXXXXX')
constant('ID - Google Ads Conversion ID', 'AW-XXXXXXXXXX')
constant('ID - Google Ads Label Trial Download', 'XXXXXXXXXXXXXXXXXXX')
constant('ID - Google Ads Label WhatsApp Lead', 'XXXXXXXXXXXXXXXXXXX')
constant('ID - Meta Pixel ID', '000000000000000')
constant('ID - Microsoft Clarity Project ID', 'xxxxxxxxxx')
constant('ID - Microsoft UET Tag ID', '00000000')
constant('ID - LinkedIn Partner ID', '0000000')

for name, key in [('product', 'product'), ('os', 'os'), ('file', 'file'),
                  ('cta_location', 'cta_location'), ('lead_source', 'lead_source'),
                  ('percent', 'percent'), ('command', 'command'), ('target', 'target'),
                  ('page_path', 'page_path')]:
    dlv('DLV - ' + name, key)

# ---------------------------------------------------------------- triggers
triggers = []
ALL_PAGES = '2147479553'          # GTM built-in "All Pages"
INIT = '2147479573'               # GTM built-in "Initialization - All Pages"
def custom_event(evt):
    tid = nid('trigger')
    triggers.append(dict(ACC, triggerId=tid, name='CE - ' + evt, type='CUSTOM_EVENT',
        customEventFilter=[{'type': 'EQUALS', 'parameter': [t('arg0', '{{_event}}'), t('arg1', evt)]}]))
    return tid

EVENTS = ['trial_download', 'whatsapp_click', 'phone_click', 'email_click', 'command_copy',
          'scroll_depth', 'pricing_view', 'calculator_used', 'cta_click', 'consent_granted']
TR = {e: custom_event(e) for e in EVENTS}

# ---------------------------------------------------------------- tags
tags = []
def consent(*types):
    return {'consentStatus': 'NEEDED',
            'consentType': {'type': 'list', 'list': [{'type': 'template', 'value': c} for c in types]}}

def tag(name, ttype, params, firing, paused=False, consent_types=None):
    d = dict(ACC, tagId=nid('tag'), name=name, type=ttype, parameter=params,
             firingTriggerId=firing, tagFiringOption='ONCE_PER_EVENT')
    if paused: d['paused'] = True
    d['consentSettings'] = consent(*consent_types) if consent_types else {'consentStatus': 'NOT_SET'}
    tags.append(d)

# Google tag (GA4). Consent Mode handles cookieless pings before consent.
tag('GA4 - Google tag', 'googtag', [t('tagId', '{{ID - GA4 Measurement ID}}')], [INIT], paused=True)

def ga4_event(evt, params):
    rows = [{'type': 'map', 'map': [t('parameter', p), t('parameterValue', '{{DLV - %s}}' % p)]} for p in params]
    tag('GA4 - event - ' + evt, 'gaawe',
        [t('eventName', evt), t('measurementIdOverride', '{{ID - GA4 Measurement ID}}'),
         {'type': 'list', 'key': 'eventSettingsTable', 'list': rows}],
        [TR[evt]], paused=True)

ga4_event('trial_download', ['product', 'os', 'file', 'cta_location', 'lead_source'])
ga4_event('whatsapp_click', ['product', 'cta_location', 'lead_source'])
ga4_event('phone_click', ['cta_location', 'lead_source'])
ga4_event('email_click', ['cta_location', 'lead_source'])
ga4_event('command_copy', ['product', 'command'])
ga4_event('scroll_depth', ['percent'])
ga4_event('pricing_view', ['product'])
ga4_event('calculator_used', ['product'])
ga4_event('cta_click', ['target', 'cta_location'])

# Google Ads
tag('Google Ads - Conversion Linker', 'gclidw', [b('enableCrossDomain', False)], [ALL_PAGES], paused=True)
tag('Google Ads - Conversion - Trial download', 'awct',
    [t('conversionId', '{{ID - Google Ads Conversion ID}}'),
     t('conversionLabel', '{{ID - Google Ads Label Trial Download}}'),
     t('conversionValue', '1'), t('currencyCode', 'INR')],
    [TR['trial_download']], paused=True)
tag('Google Ads - Conversion - WhatsApp lead', 'awct',
    [t('conversionId', '{{ID - Google Ads Conversion ID}}'),
     t('conversionLabel', '{{ID - Google Ads Label WhatsApp Lead}}'),
     t('conversionValue', '1'), t('currencyCode', 'INR')],
    [TR['whatsapp_click']], paused=True)

# Meta Pixel. Fires only with ad_storage consent; re-tries on consent_granted.
META_BASE = """<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
if(!window.__tbnFbInit){window.__tbnFbInit=1;fbq('init','{{ID - Meta Pixel ID}}');fbq('track','PageView');}
</script>"""
tag('Meta - Pixel base', 'html', [t('html', META_BASE), b('supportDocumentWrite', False)],
    [ALL_PAGES, TR['consent_granted']], paused=True, consent_types=['ad_storage'])
tag('Meta - StartTrial (download)', 'html',
    [t('html', "<script>window.fbq&&fbq('track','StartTrial',{content_name:'{{DLV - product}}',content_category:'{{DLV - os}}'});</script>")],
    [TR['trial_download']], paused=True, consent_types=['ad_storage'])
tag('Meta - Lead (WhatsApp)', 'html',
    [t('html', "<script>window.fbq&&fbq('track','Lead',{content_name:'{{DLV - product}}'});</script>")],
    [TR['whatsapp_click']], paused=True, consent_types=['ad_storage'])
tag('Meta - Contact (call or email)', 'html',
    [t('html', "<script>window.fbq&&fbq('track','Contact');</script>")],
    [TR['phone_click'], TR['email_click']], paused=True, consent_types=['ad_storage'])
tag('Meta - ViewContent (pricing)', 'html',
    [t('html', "<script>window.fbq&&fbq('track','ViewContent',{content_name:'pricing {{DLV - product}}'});</script>")],
    [TR['pricing_view']], paused=True, consent_types=['ad_storage'])

# Microsoft Clarity (session recordings, heatmaps). Analytics consent.
CLARITY = """<script>
(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","{{ID - Microsoft Clarity Project ID}}");
window.clarity('consent');
</script>"""
tag('Microsoft - Clarity', 'html', [t('html', CLARITY)],
    [ALL_PAGES, TR['consent_granted']], paused=True, consent_types=['analytics_storage'])

# Microsoft Advertising UET
UET = """<script>
(function(w,d,t,r,u){var f,n,i;w[u]=w[u]||[],f=function(){var o={ti:"{{ID - Microsoft UET Tag ID}}",enableAutoSpaTracking:true};
o.q=w[u],w[u]=new UET(o),w[u].push("pageLoad")},n=d.createElement(t),n.src=r,n.async=1,n.onload=n.onreadystatechange=function(){
var s=this.readyState;s&&s!=="loaded"&&s!=="complete"||(f(),n.onload=n.onreadystatechange=null)},i=d.getElementsByTagName(t)[0],
i.parentNode.insertBefore(n,i)})(window,document,"script","//bat.bing.com/bat.js","uetq");
</script>"""
tag('Microsoft Ads - UET base', 'html', [t('html', UET)],
    [ALL_PAGES, TR['consent_granted']], paused=True, consent_types=['ad_storage'])
tag('Microsoft Ads - trial_download', 'html',
    [t('html', "<script>window.uetq=window.uetq||[];uetq.push('event','trial_download',{event_category:'{{DLV - product}}',event_label:'{{DLV - os}}'});</script>")],
    [TR['trial_download']], paused=True, consent_types=['ad_storage'])
tag('Microsoft Ads - whatsapp_click', 'html',
    [t('html', "<script>window.uetq=window.uetq||[];uetq.push('event','whatsapp_click',{event_category:'{{DLV - product}}'});</script>")],
    [TR['whatsapp_click']], paused=True, consent_types=['ad_storage'])

# LinkedIn Insight (for custom-software B2B campaigns). Paused by default.
LINKEDIN = """<script>
_linkedin_partner_id="{{ID - LinkedIn Partner ID}}";window._linkedin_data_partner_ids=window._linkedin_data_partner_ids||[];
window._linkedin_data_partner_ids.push(_linkedin_partner_id);
(function(l){if(!l){window.lintrk=function(a,b){window.lintrk.q.push([a,b])};window.lintrk.q=[]}
var s=document.getElementsByTagName("script")[0];var b=document.createElement("script");b.type="text/javascript";b.async=true;
b.src="https://snap.licdn.com/li.lms-analytics/insight.min.js";s.parentNode.insertBefore(b,s);})(window.lintrk);
</script>"""
tag('LinkedIn - Insight tag', 'html', [t('html', LINKEDIN)],
    [ALL_PAGES, TR['consent_granted']], paused=True, consent_types=['ad_storage'])

container = {
    'exportFormatVersion': 2,
    'exportTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'containerVersion': dict(ACC,
        path='accounts/0/containers/0/versions/0', containerVersionId='0',
        container=dict(ACC, path='accounts/0/containers/0', name='The Binary Brain Network',
                       publicId='GTM-TFBHC2VR', usageContext=['WEB']),
        tag=tags, trigger=triggers, variable=variables,
        builtInVariable=[dict(ACC, type=x, name=n) for x, n in
                         [('PAGE_URL', 'Page URL'), ('PAGE_PATH', 'Page Path'),
                          ('PAGE_HOSTNAME', 'Page Hostname'), ('REFERRER', 'Referrer'),
                          ('EVENT', 'Event'), ('CLICK_URL', 'Click URL')]],
        fingerprint='0'),
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(container, f, indent=2, ensure_ascii=False)
print('wrote', OUT, '-', len(tags), 'tags,', len(triggers), 'triggers,', len(variables), 'variables')
