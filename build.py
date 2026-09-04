#!/usr/bin/env python3
"""RIBAND — static site builder. Zero dependencies, Python 3 stdlib only.

Reads content/config.json + content/{en,ckb,ar}.json and renders the full
trilingual site into docs/ (GitHub Pages-ready: Settings → Pages → main /docs).

Run: python3 build.py
"""
import json
import os
import shutil
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")

ROUTES = ["", "weddings", "portraits", "schools", "work", "about", "contact"]

FONTS = (
    "https://fonts.googleapis.com/css2"
    "?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400"
    "&family=Inter:wght@400;500"
    "&family=Noto+Naskh+Arabic:wght@400;500;600"
    "&display=swap"
)


def load(name):
    with open(os.path.join(ROOT, "content", name), encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def wa_url(cfg, lang):
    text = urllib.parse.quote(lang["wa_prefill"])
    return f"https://wa.me/{cfg['whatsapp_e164']}?text={text}"


def img(rel, name, alt, cls="", reveal=True, loading="lazy"):
    r = ' data-reveal=""' if reveal else ""
    c = f' class="{cls}"' if cls else ""
    return (
        f'<div class="ph"{c}{r}><img src="{rel}assets/img/{name}.svg" '
        f'alt="{esc(alt)}" loading="{loading}"></div>'
    )


# ---------------------------------------------------------------- chrome

def head(cfg, lang, page, route, rel):
    slug = lang["slug"]
    path = f"/{slug}/" + (f"{route}/" if route else "")
    url = cfg["base_url"] + path
    alts = "\n  ".join(
        f'<link rel="alternate" hreflang="{h}" '
        f'href="{cfg["base_url"]}/{s}/{(route + "/") if route else ""}">'
        for h, s in (("en", "en"), ("ku", "ku"), ("ar", "ar"), ("x-default", "en"))
    )
    locale = {"en": "en_US", "ku": "ckb_IQ", "ar": "ar_IQ"}[slug]
    return f"""<!DOCTYPE html>
<html lang="{lang['html_lang']}" dir="{lang['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['seo_title'])}</title>
<meta name="description" content="{esc(page['seo_desc'])}">
<link rel="canonical" href="{url}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Riband">
<meta property="og:title" content="{esc(page['seo_title'])}">
<meta property="og:description" content="{esc(page['seo_desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{locale}">
<meta name="theme-color" content="#f5f3ee">
<link rel="icon" type="image/svg+xml" href="{rel}assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{rel}assets/css/main.css">
</head>
<body>"""


def header(cfg, lang, route, rel):
    ch = lang["chrome"]
    slug = lang["slug"]
    links = []
    for r in ROUTES[1:]:
        cur = ' aria-current="page"' if r == route else ""
        links.append(
            f'<a class="navlink" href="{rel}{slug}/{r}/"{cur}>{ch["nav"][r]}</a>'
        )
    lang_links = []
    for s, label in (("en", "EN"), ("ku", "کوردی"), ("ar", "العربية")):
        cls = "active" if s == slug else ""
        href = f"{rel}{s}/" + (f"{route}/" if route else "")
        lang_links.append(f'<a class="{cls}" href="{href}" hreflang="{s}">{label}</a>')
    lang_html = '<span class="sep">·</span>'.join(lang_links)
    return f"""
<a class="visually-hidden" href="#main" style="position:absolute;inset-inline-start:-9999px">{ch['skip']}</a>
<header class="site-head">
  <div class="shell">
    <a class="wordmark" href="{rel}{slug}/">Riband</a>
    <nav class="site-nav" id="nav">{''.join(links)}</nav>
    <div class="head-cta">
      <div class="lang-switch">{lang_html}</div>
      <a class="btn btn-ghost" href="{rel}{slug}/contact/">{ch['book_btn']}</a>
      <button class="menu-btn" aria-expanded="false" aria-controls="nav"
        data-open="{ch['menu_open']}" data-close="{ch['menu_close']}">{ch['menu_open']}</button>
    </div>
  </div>
</header>
<main id="main">"""


def footer(cfg, lang, rel):
    ch = lang["chrome"]
    slug = lang["slug"]
    nav = "".join(
        f'<a href="{rel}{slug}/{r}/">{ch["nav"][r]}</a>' for r in ROUTES[1:]
    )
    return f"""</main>
<footer class="site-foot">
  <div class="shell">
    <div class="foot-main">
      <div>
        <a class="wordmark" href="{rel}{slug}/">Riband</a>
        <p class="foot-tag">{ch['foot_tagline']}</p>
      </div>
      <div class="foot-col"><span class="k">{ch['foot_explore']}</span>{nav}</div>
      <div class="foot-col"><span class="k">{ch['foot_elsewhere']}</span>
        <a href="{cfg['instagram_main']}" rel="noopener">{ch['foot_ig_main']}</a>
        <a href="{cfg['instagram_bnw']}" rel="noopener">{ch['foot_ig_bnw']}</a>
        <a href="{cfg['youtube']}" rel="noopener">{ch['foot_youtube']}</a>
      </div>
      <div class="foot-col"><span class="k">{ch['foot_contact']}</span>
        <a href="{wa_url(cfg, lang)}" rel="noopener">{ch['foot_whatsapp']}</a>
        <a href="mailto:{cfg['email']}">{ch['foot_email']}</a>
      </div>
    </div>
    <div class="foot-base">
      <span>© {cfg['copyright_year']} {ch['copyright']}</span>
      <span><a href="https://bond.krd" rel="noopener">{ch['credit']}</a></span>
    </div>
  </div>
</footer>
<script src="{rel}assets/js/main.js"></script>
</body>
</html>"""


# ---------------------------------------------------------------- partials

def cta_section(cfg, lang, h2, text, wa_label, cal_label, eyebrow=None):
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    tx = f'<p class="lead">{text}</p>' if text else ""
    return f"""
<section class="section-tight">
  <div class="shell">
    <hr class="hairline">
    <div class="section-head center" style="margin-block-start:clamp(3rem,7vw,5rem)" data-reveal="">
      {eb}
      <h2 class="display">{h2}</h2>
      {tx}
      <div class="hero-actions" style="justify-content:center">
        <a class="btn" href="{wa_url(cfg, lang)}" rel="noopener">{wa_label}</a>
        <a class="textlink" href="{cfg['calendly_url']}" rel="noopener">{cal_label}</a>
      </div>
    </div>
  </div>
</section>"""


def packages_block(cfg, page):
    cols = []
    for p in page["packages"]:
        feats = "".join(f"<li>{f}</li>" for f in p["features"])
        tag = (
            f'<span class="name">{p["name"]} · {page["featured_tag"]}</span>'
            if p["featured"]
            else f'<span class="name">{p["name"]}</span>'
        )
        price = cfg["prices"][p["price_key"]]
        cols.append(f"""
      <div class="pkg{' featured' if p['featured'] else ''}" data-reveal="">
        {tag}
        <div class="price"><span class="from">{page['from']}</span><bdi>${price}</bdi></div>
        <ul>{feats}</ul>
      </div>""")
    return f"""
    <div class="packages">{''.join(cols)}</div>
    <p class="body-muted small" style="margin-block-start:1.4rem;max-width:44em">{page['pkg_note']}</p>"""


def faq_block(page):
    items = "".join(
        f"""
      <details data-reveal="">
        <summary>{f['q']}</summary>
        <div class="a">{f['a']}</div>
      </details>"""
        for f in page["faq"]
    )
    return f"""
<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal="">
      <p class="eyebrow">{page['faq_eyebrow']}</p>
      <h2 class="display">{page['faq_h2']}</h2>
    </div>
    <div class="faq">{items}</div>
  </div>
</section>"""


def faq_jsonld(page):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            }
            for f in page["faq"]
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def business_jsonld(cfg, lang, page, route):
    slug = lang["slug"]
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Riband Photography",
        "url": cfg["base_url"] + f"/{slug}/",
        "image": cfg["base_url"] + "/assets/img/band-wide.svg",
        "founder": {
            "@type": "Person",
            "name": "Riband Saadallah",
            "jobTitle": "Photographer",
            "sameAs": [cfg["instagram_main"], cfg["instagram_bnw"]],
        },
        "areaServed": ["Erbil", "Kurdistan Region", "Iraq"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Erbil",
            "addressRegion": "Kurdistan Region",
            "addressCountry": "IQ",
        },
        "priceRange": "$$",
        "sameAs": [cfg["instagram_main"], cfg["instagram_bnw"], cfg["youtube"]],
        "description": page["seo_desc"],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


# ---------------------------------------------------------------- pages

def render_home(cfg, lang, rel):
    p = lang["home"]
    stats = "".join(
        f'<div class="stat" data-reveal=""><div class="n">{s["n"]}</div><div class="l">{s["l"]}</div></div>'
        for s in p["stats"]
    )
    svcs = []
    for s, r in zip(p["services"], ("weddings", "portraits", "schools")):
        svcs.append(f"""
      <a class="svc" href="{rel}{lang['slug']}/{r}/" data-reveal="">
        <span class="num">{s['num']}</span>
        {img(rel, s['img'], s['alt'], reveal=False)}
        <h3>{s['title']}</h3>
        <p>{s['text']}</p>
        <span class="textlink">{s['link']}</span>
      </a>""")
    work = "".join(img(rel, w["img"], w["alt"]) for w in p["work_imgs"])
    return f"""
<section class="hero">
  <div class="shell hero-grid">
    <div class="hero-copy">
      <p class="eyebrow" data-reveal="">{p['hero_eyebrow']}</p>
      <h1 class="display" data-reveal="">{p['hero_h1']}</h1>
      <p class="lead" data-reveal="">{p['hero_lead']}</p>
      <div class="hero-actions" data-reveal="">
        <a class="btn" href="{cfg['calendly_url']}" rel="noopener">{p['hero_cta_book']}</a>
        <a class="textlink" href="{rel}{lang['slug']}/work/">{p['hero_cta_work']}</a>
      </div>
    </div>
    <div class="offset-frame" data-reveal="">
      <div class="matte">{img(rel, 'hero-home', p['hero_img_alt'], reveal=False, loading='eager')}</div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="shell"><div class="stats">{stats}</div></div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal="">
      <p class="eyebrow">{p['svc_eyebrow']}</p>
      <h2 class="display">{p['svc_h2']}</h2>
    </div>
    <div class="svc-grid">{''.join(svcs)}</div>
  </div>
</section>

<section class="band">
  <div class="bg"><img src="{rel}assets/img/band-wide.svg" alt="" loading="lazy"></div>
  <div class="shell">
    <h2 class="display" data-reveal="">{p['band_quote']}</h2>
    <a class="btn" href="{rel}{lang['slug']}/about/" data-reveal="">{p['band_cta']}</a>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal="">
      <p class="eyebrow">{p['work_eyebrow']}</p>
      <h2 class="display">{p['work_h2']}</h2>
    </div>
    <div class="strip">{work}</div>
    <p style="margin-block-start:2.4rem" data-reveal="">
      <a class="textlink" href="{rel}{lang['slug']}/work/">{p['work_link']}</a>
    </p>
  </div>
</section>

<section class="section" style="padding-block-start:0">
  <div class="shell split">
    <div class="offset-frame" data-reveal="">
      <div class="matte">{img(rel, 'about-portrait', p['about_img_alt'], reveal=False)}</div>
    </div>
    <div class="copy">
      <p class="eyebrow" data-reveal="">{p['about_eyebrow']}</p>
      <h2 class="display" data-reveal="">{p['about_h2']}</h2>
      <p class="lead" data-reveal="">{p['about_text']}</p>
      <p data-reveal=""><a class="textlink" href="{rel}{lang['slug']}/about/">{p['about_link']}</a></p>
    </div>
  </div>
</section>
{cta_section(cfg, lang, p['cta_h2'], p['cta_text'], p['cta_btn_wa'], p['cta_btn_cal'], p['cta_eyebrow'])}
{business_jsonld(cfg, lang, p, '')}"""


def render_weddings(cfg, lang, rel):
    p = lang["weddings"]
    steps = "".join(
        f'<div class="step" data-reveal=""><div class="num">{s["num"]}</div><h3>{s["title"]}</h3><p>{s["text"]}</p></div>'
        for s in p["steps"]
    )
    gal = "".join(img(rel, g["img"], g["alt"]) for g in p["gallery"])
    return f"""
<section class="page-intro">
  <div class="shell">
    <p class="eyebrow" data-reveal="">{p['eyebrow']}</p>
    <h1 class="display" data-reveal="">{p['h1']}</h1>
    <p class="lead" data-reveal="">{p['lead']}</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal="">
      <p class="eyebrow">{p['approach_eyebrow']}</p>
      <h2 class="display">{p['approach_h2']}</h2>
    </div>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="section-tight">
  <div class="shell"><div class="strip">{gal}</div></div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal="">
      <p class="eyebrow">{p['pkg_eyebrow']}</p>
      <h2 class="display">{p['pkg_h2']}</h2>
    </div>
    {packages_block(cfg, p)}
    <div class="hero-actions" data-reveal="">
      <a class="btn" href="{wa_url(cfg, lang)}" rel="noopener">{p['pkg_cta']}</a>
    </div>
  </div>
</section>
{faq_block(p)}
{cta_section(cfg, lang, p['cta_h2'], p['cta_text'], p['cta_btn_wa'], p['cta_btn_cal'])}
{business_jsonld(cfg, lang, p, 'weddings')}
{faq_jsonld(p)}"""


def render_portraits(cfg, lang, rel):
    p = lang["portraits"]
    gal = "".join(img(rel, g["img"], g["alt"]) for g in p["gallery"])
    return f"""
<section class="page-intro">
  <div class="shell">
    <p class="eyebrow" data-reveal="">{p['eyebrow']}</p>
    <h1 class="display" data-reveal="">{p['h1']}</h1>
    <p class="lead" data-reveal="">{p['lead']}</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal="">
      <p class="eyebrow">{p['pkg_eyebrow']}</p>
      <h2 class="display">{p['pkg_h2']}</h2>
    </div>
    {packages_block(cfg, p)}
    <div class="hero-actions" data-reveal="">
      <a class="btn" href="{wa_url(cfg, lang)}" rel="noopener">{p['pkg_cta']}</a>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="shell split" style="align-items:start">
    {gal}
  </div>
</section>

<section class="section-tight">
  <div class="shell">
    <div class="section-head" data-reveal="">
      <h2 class="display">{p['note_h2']}</h2>
      <p class="lead">{p['note_text']}</p>
    </div>
  </div>
</section>
{cta_section(cfg, lang, p['cta_h2'], None, p['cta_btn_wa'], p['cta_btn_cal'])}
{business_jsonld(cfg, lang, p, 'portraits')}"""


def render_schools(cfg, lang, rel):
    p = lang["schools"]
    steps = "".join(
        f'<div class="step" data-reveal=""><div class="num">{s["num"]}</div><h3>{s["title"]}</h3><p>{s["text"]}</p></div>'
        for s in p["steps"]
    )
    return f"""
<section class="page-intro">
  <div class="shell">
    <p class="eyebrow" data-reveal="">{p['eyebrow']}</p>
    <h1 class="display" data-reveal="">{p['h1']}</h1>
    <p class="lead" data-reveal="">{p['lead']}</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal="">
      <p class="eyebrow">{p['how_eyebrow']}</p>
      <h2 class="display">{p['how_h2']}</h2>
    </div>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="section-tight">
  <div class="shell split" style="align-items:start">
    {img(rel, p['gallery'][0]['img'], p['gallery'][0]['alt'])}
    {img(rel, p['gallery'][1]['img'], p['gallery'][1]['alt'])}
  </div>
</section>

<section class="section">
  <div class="shell split" style="align-items:start">
    <div class="copy">
      <h2 class="display" data-reveal="">{p['parents_h2']}</h2>
      <p data-reveal="">{p['parents_text']}</p>
    </div>
    <div class="copy">
      <h2 class="display" data-reveal="">{p['why_h2']}</h2>
      <p data-reveal="">{p['why_text']}</p>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="shell">
    <hr class="hairline">
    <div class="section-head" style="margin-block-start:clamp(3rem,7vw,5rem)" data-reveal="">
      <h2 class="display">{p['pricing_h2']}</h2>
      <p class="lead">{p['pricing_text']}</p>
    </div>
  </div>
</section>
{faq_block(p)}
{cta_section(cfg, lang, p['cta_h2'], p['cta_text'], p['cta_btn_wa'], p['cta_btn_cal'])}
{business_jsonld(cfg, lang, p, 'schools')}
{faq_jsonld(p)}"""


def render_work(cfg, lang, rel):
    p = lang["work"]
    filters = "".join(
        f'<button class="filter-btn{" active" if f["key"] == "all" else ""}" data-filter="{f["key"]}">{f["label"]}</button>'
        for f in p["filters"]
    )
    items = "".join(
        f"""
      <figure class="item" data-cat="{it['cat']}" data-reveal="">
        {img(rel, it['img'], it['alt'], reveal=False)}
        <figcaption>{it['caption']}</figcaption>
      </figure>"""
        for it in p["items"]
    )
    return f"""
<section class="page-intro">
  <div class="shell">
    <p class="eyebrow" data-reveal="">{p['eyebrow']}</p>
    <h1 class="display" data-reveal="">{p['h1']}</h1>
    <p class="lead" data-reveal="">{p['lead']}</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="filters" data-reveal="">{filters}</div>
    <div class="masonry">{items}</div>
    <p class="body-muted" style="margin-block-start:2.6rem" data-reveal="">
      {p['more_text']}
      <a class="textlink" href="{cfg['instagram_main']}" rel="noopener"><bdi>@ribandm</bdi></a> ·
      <a class="textlink" href="{cfg['instagram_bnw']}" rel="noopener"><bdi>@bnwlives</bdi></a>
    </p>
  </div>
</section>
{cta_section(cfg, lang, p['cta_h2'], None, p['cta_btn_wa'], p['cta_btn_cal'])}"""


def render_about(cfg, lang, rel):
    p = lang["about"]
    chapters = "".join(f'<div class="stat" data-reveal=""><div class="n">{c}</div></div>' for c in p["chapters"])
    return f"""
<section class="page-intro">
  <div class="shell">
    <p class="eyebrow" data-reveal="">{p['eyebrow']}</p>
    <h1 class="display" data-reveal="">{p['h1']}</h1>
  </div>
</section>

<section class="section">
  <div class="shell split" style="align-items:start">
    <div class="copy">
      <p class="lead" data-reveal="">{p['p1']}</p>
      <p data-reveal="">{p['p2']}</p>
      <p data-reveal="">{p['p3']}</p>
    </div>
    <div class="offset-frame" data-reveal="">
      <div class="matte">{img(rel, 'about-portrait', p['img_alt'], reveal=False)}</div>
    </div>
  </div>
</section>

<section class="band">
  <div class="bg"><img src="{rel}assets/img/contact-band.svg" alt="" loading="lazy"></div>
  <div class="shell">
    <h2 class="display" data-reveal="">{p['quote']}</h2>
  </div>
</section>

<section class="section">
  <div class="shell">
    <p class="eyebrow" style="text-align:center;margin-block-end:1.6rem" data-reveal="">{p['chapters_eyebrow']}</p>
    <div class="stats" style="grid-template-columns:repeat(5,1fr)">{chapters}</div>
  </div>
</section>

<section class="section-tight">
  <div class="shell">
    <div class="section-head" data-reveal="">
      <h2 class="display">{p['sig_h2']}</h2>
      <p class="lead">{p['sig_text']}</p>
    </div>
  </div>
</section>
{cta_section(cfg, lang, p['cta_h2'], None, p['cta_btn_wa'], p['cta_btn_cal'])}"""


def render_contact(cfg, lang, rel):
    p = lang["contact"]
    cal = cfg["calendly_url"]
    return f"""
<section class="page-intro">
  <div class="shell">
    <p class="eyebrow" data-reveal="">{p['eyebrow']}</p>
    <h1 class="display" data-reveal="">{p['h1']}</h1>
    <p class="lead" data-reveal="">{p['lead']}</p>
  </div>
</section>

<section class="section">
  <div class="shell split" style="align-items:start">
    <div class="copy">
      <div class="contact-list">
        <div class="row" data-reveal="">
          <span class="k">{p['wa_label']}</span>
          <span class="v"><a href="{wa_url(cfg, lang)}" rel="noopener" class="wa-btn"><bdi>{cfg['whatsapp_display']}</bdi></a></span>
        </div>
        <div class="row" data-reveal="">
          <span class="k">{p['email_label']}</span>
          <span class="v"><a href="mailto:{cfg['email']}">{cfg['email']}</a></span>
        </div>
        <div class="row" data-reveal="">
          <span class="k">{p['ig_label']}</span>
          <span class="v"><a href="{cfg['instagram_main']}" rel="noopener"><bdi>@ribandm</bdi></a> · <a href="{cfg['instagram_bnw']}" rel="noopener"><bdi>@bnwlives</bdi></a></span>
        </div>
        <div class="row" data-reveal="">
          <span class="k">{p['studio_label']}</span>
          <span class="v">{p['studio_value']}</span>
        </div>
      </div>
      <p class="body-muted small" style="margin-block-start:2rem" data-reveal="">{p['reply_note']}</p>
      <div style="margin-block-start:2.6rem" data-reveal="">
        <a class="btn" href="{wa_url(cfg, lang)}" rel="noopener">{p['wa_label']}</a>
      </div>
    </div>
    <div class="copy">
      <h2 class="display" style="margin-block-end:1.6rem" data-reveal="">{p['cal_h2']}</h2>
      <div class="calendly-box">
        <div class="calendly-inline-widget" data-url="{cal}?hide_gdpr_banner=1" style="min-width:280px;height:640px"></div>
        <script src="https://assets.calendly.com/assets/external/widget.js" async></script>
      </div>
      <p class="body-muted small" style="margin-block-start:1rem">
        {p['cal_fallback']} <a class="textlink" href="{cal}" rel="noopener">{p['cal_link']}</a>
      </p>
    </div>
  </div>
</section>"""


RENDERERS = {
    "": ("home", render_home),
    "weddings": ("weddings", render_weddings),
    "portraits": ("portraits", render_portraits),
    "schools": ("schools", render_schools),
    "work": ("work", render_work),
    "about": ("about", render_about),
    "contact": ("contact", render_contact),
}


# ---------------------------------------------------------------- root & seo files

def root_index(cfg):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Riband — Photographer, Erbil</title>
<meta name="robots" content="noindex">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/css/main.css">
<script>
(function () {{
  var l = (navigator.languages || [navigator.language || "en"]).join(" ").toLowerCase();
  var t = "en";
  if (/(^|[^a-z])(ckb|ku)([^a-z]|$)/.test(l)) t = "ku";
  else if (/(^|[^a-z])ar([^a-z]|$)/.test(l)) t = "ar";
  location.replace(t + "/");
}})();
</script>
</head>
<body>
<div class="lang-gate">
  <span class="wordmark">Riband</span>
  <nav>
    <a class="biglink" href="en/">English</a>
    <a class="biglink rtl" href="ku/" lang="ckb" dir="rtl">کوردی</a>
    <a class="biglink rtl" href="ar/" lang="ar" dir="rtl">العربية</a>
  </nav>
</div>
</body>
</html>"""


def sitemap(cfg):
    urls = []
    for route in ROUTES:
        tail = f"{route}/" if route else ""
        alts = "".join(
            f'<xhtml:link rel="alternate" hreflang="{h}" href="{cfg["base_url"]}/{s}/{tail}"/>'
            for h, s in (("en", "en"), ("ku", "ku"), ("ar", "ar"), ("x-default", "en"))
        )
        for slug in ("en", "ku", "ar"):
            urls.append(f"<url><loc>{cfg['base_url']}/{slug}/{tail}</loc>{alts}</url>")
    body = "\n".join(urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{body}\n</urlset>\n"
    )


# ---------------------------------------------------------------- main

def main():
    cfg = load("config.json")
    langs = [load(entry["file"]) for entry in cfg["languages"]]

    os.makedirs(DOCS, exist_ok=True)
    for entry in os.listdir(DOCS):
        path = os.path.join(DOCS, entry)
        shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)

    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DOCS, "assets"))

    pages = 0
    for lang in langs:
        for route, (key, renderer) in RENDERERS.items():
            rel = "../" if route == "" else "../../"
            page = lang[key]
            html = (
                head(cfg, lang, page, route, rel)
                + header(cfg, lang, route, rel)
                + renderer(cfg, lang, rel)
                + footer(cfg, lang, rel)
            )
            out_dir = os.path.join(DOCS, lang["slug"], route) if route else os.path.join(DOCS, lang["slug"])
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            pages += 1

    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
        f.write(root_index(cfg))
    with open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap(cfg))
    with open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {cfg['base_url']}/sitemap.xml\n")
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    print(f"Built {pages} pages (+ root, sitemap, robots) into {DOCS}")


if __name__ == "__main__":
    main()
