# TBN website — build and maintenance

## Generated pages and build scripts

Hand-built pages (homepage, product pages, compare guides, glossary) are edited
directly. Everything below is generated — edit the source, then rebuild:

| Output | Source | Command |
|---|---|---|
| `/blog/<slug>/`, `/blog/`, `/blog/feed.xml` | `content/blog/<slug>.html` (JSON meta block + body) | `python scripts/build_blog.py` |
| `/download/`, `/pricing/`, `/tools/software-cost-calculator/`, `/privacy/`, `/terms/` | `scripts/build_pages.py` (prices and versions in `FACTS`) | `python scripts/build_pages.py` |
| `sitemap.xml` | every `index.html` | `python scripts/build_sitemap.py` |
| `llms-full.txt` | pricing, download, spec and guide pages | `python scripts/build_llms_full.py` |
| `ops/gtm-container.json` | `scripts/build_gtm_container.py` | `python scripts/build_gtm_container.py` |

Before pushing, run `python scripts/check_site.py` — it validates JSON-LD,
internal links, consent/GTM tags and a list of known-stale product claims.
After deploying, `python scripts/indexnow.py` asks Bing and other IndexNow
engines to recrawl. Tracking setup: `ops/TRACKING_SETUP.md`.

When a product releases: update versions and facts in `scripts/build_pages.py`,
the product page and its `/features/` page, and `llms.txt`; then rebuild and check.
