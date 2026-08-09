# Riband — photography, Erbil

Trilingual (English / Kurdish Sorani / Arabic) marketing site for **Riband Saadallah**
([@ribandm](https://www.instagram.com/ribandm/), [@bnwlives](https://www.instagram.com/bnwlives/)) —
photographer with twelve years in Finland, now building a wedding / portrait / school-photography
studio in Erbil. Light-editorial luxury design, monochrome imagery, zero dependencies.

## Stack

Plain Python 3 (stdlib only) static-site generator → pure HTML/CSS/JS output. No npm, no frameworks.

```
build.py              the whole generator: templates + SEO + i18n plumbing
content/config.json   contact details, prices, URLs — the ONE place to edit business facts
content/en.json       all English copy
content/ckb.json      Kurdish Sorani copy (draft — needs native review)
content/ar.json       Arabic MSA copy (draft — needs native review)
assets/               css / js / img (SVG placeholders) / favicon
tools/gen_placeholders.py   regenerates placeholder images
tools/serve.py        local preview server
docs/                 BUILD OUTPUT — never edit by hand
```

## Commands

```bash
python3 build.py            # rebuild docs/ from content + assets
python3 tools/serve.py      # preview at http://127.0.0.1:8471
```

## Deploy

`docs/` is a fully static site with **relative URLs** — it works on GitHub Pages
(Settings → Pages → branch `main`, folder `/docs`), Cloudflare Pages, Netlify, or any host.
Commit `docs/` together with source.

URL structure: `/en/…`, `/ku/…`, `/ar/…` with hreflang alternates, per-language sitemap
entries, FAQ + ProfessionalService JSON-LD on service pages. Root `/` auto-detects
browser language and redirects (chooser shown if JS is off).

## Before launch — checklist

Everything below is a placeholder marked `_TODO` in [content/config.json](content/config.json):

1. **Domain** — buy it, set `base_url`, re-run `python3 build.py`.
2. **WhatsApp number** — `whatsapp_e164` (digits only) + `whatsapp_display`.
3. **Calendly** — create the account/event, set `calendly_url` (the contact-page embed
   starts working the moment this URL is real).
4. **Email** — set up on the domain, update `email`.
5. **Prices** — confirm all `prices` values with Riband (currently sensible-guess USD).
6. **Photographs** — replace every SVG in `assets/img/` with real photos. Each placeholder
   states its own target size (e.g. `hero-home` → 1400×1750). Keep the same filename; if
   you export .jpg/.webp instead of .svg, update the matching `"img"` / path references in
   `content/*.json` (they reference names without extension via the build's `img()` helper —
   extension is currently hard-coded to `.svg` in `build.py`, change it there once, or name
   files identically).
7. **Translations** — Sorani (`ckb.json`) and Arabic (`ar.json`) are Claude drafts:
   get a native pass. Marlo covers Sorani.
8. **OG image** — generate a 1200×630 raster from a real photo and add
   `og:image` in `build.py`'s `head()`.

## Positioning decisions (why the site is shaped this way)

- **Weddings lead** — biggest budgets and booming demand in Erbil; it's the hero,
  first nav item, first service, and the most built-out page (packages + FAQ + schema).
- **Schools** — the B2B2C annual-programme page pitches "free for the school,
  parents buy what they love." Sold by outreach; the page is the credibility asset.
- **The signature** — every commission delivered in colour **and** monochrome; the
  black-and-white brand is the differentiator against Erbil's oversaturated glam market.
- **From-pricing** — filters tire-kickers while keeping the luxury register.
- **WhatsApp-first contact** — that's how Erbil actually books; Calendly for
  consultation calls.
