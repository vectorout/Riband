#!/usr/bin/env python3
"""Generate monochrome SVG placeholder images for every image slot on the site.

Each placeholder states its slot name and target size, so swapping in real
photographs is mechanical: export a photo at (or above) the stated size, give
it the same filename (.jpg/.webp/.avif all fine), drop it in assets/img/, and
update the path in content/*.json if the extension changed.

Run: python3 tools/gen_placeholders.py
"""
import os
import re

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

# slot name, width, height, palette index, label
SLOTS = [
    ("hero-home", 1400, 1750, 0, "HOME HERO"),
    ("band-wide", 2400, 1100, 2, "FULL-BLEED BAND"),
    ("wedding-01", 1400, 1750, 2, "WEDDING 01"),
    ("wedding-02", 1400, 1050, 0, "WEDDING 02"),
    ("wedding-03", 1400, 1400, 3, "WEDDING 03"),
    ("portrait-01", 1400, 1750, 1, "PORTRAIT 01"),
    ("portrait-02", 1400, 1050, 2, "PORTRAIT 02"),
    ("school-01", 1400, 1050, 3, "SCHOOL 01"),
    ("school-02", 1400, 1400, 0, "SCHOOL 02"),
    ("about-portrait", 1400, 1750, 2, "RIBAND — PORTRAIT"),
    ("contact-band", 2400, 1100, 3, "CONTACT BAND"),
    ("work-01", 1200, 1500, 0, "WORK 01 · WEDDING"),
    ("work-02", 1200, 900, 1, "WORK 02 · STREET"),
    ("work-03", 1200, 1200, 2, "WORK 03 · PORTRAIT"),
    ("work-04", 1200, 1500, 3, "WORK 04 · WEDDING"),
    ("work-05", 1200, 900, 2, "WORK 05 · PORTRAIT"),
    ("work-06", 1200, 1500, 1, "WORK 06 · STREET"),
    ("work-07", 1200, 1200, 0, "WORK 07 · WEDDING"),
    ("work-08", 1200, 1500, 2, "WORK 08 · STREET"),
    ("work-09", 1200, 900, 3, "WORK 09 · WEDDING"),
    ("work-10", 1200, 1500, 0, "WORK 10 · PORTRAIT"),
    ("work-11", 1200, 1200, 1, "WORK 11 · STREET"),
    ("work-12", 1200, 1500, 2, "WORK 12 · WEDDING"),
]

# warm-neutral monochrome pairs: top, bottom, highlight opacity
PALETTES = [
    ("#1a1917", "#3d3b37", 0.10),
    ("#c9c6c0", "#8e8b85", 0.16),
    ("#55524d", "#242220", 0.12),
    ("#2e2c29", "#6b6862", 0.10),
]


def svg(name, w, h, p, label):
    c1, c2, hi = PALETTES[p]
    light = p == 1
    ink = "#3d3b37" if light else "#d9d6d0"
    uid = re.sub(r"[^a-z0-9]", "", name)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="g{uid}" x1="0" y1="0" x2="0.7" y2="1">
      <stop offset="0" stop-color="{c1}"/>
      <stop offset="1" stop-color="{c2}"/>
    </linearGradient>
    <radialGradient id="r{uid}" cx="0.32" cy="0.28" r="0.9">
      <stop offset="0" stop-color="#ffffff" stop-opacity="{hi}"/>
      <stop offset="0.6" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <filter id="n{uid}">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.055"/></feComponentTransfer>
    </filter>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#g{uid})"/>
  <rect width="{w}" height="{h}" fill="url(#r{uid})"/>
  <rect width="{w}" height="{h}" filter="url(#n{uid})"/>
  <rect x="{w * 0.045:.0f}" y="{w * 0.045:.0f}" width="{w - w * 0.09:.0f}" height="{h - w * 0.09:.0f}" fill="none" stroke="{ink}" stroke-opacity="0.35" stroke-width="1.5"/>
  <text x="{w * 0.075:.0f}" y="{h - w * 0.075:.0f}" font-family="Georgia, serif" font-size="{w * 0.021:.0f}" letter-spacing="{w * 0.006:.1f}" fill="{ink}" fill-opacity="0.85">{label}</text>
  <text x="{w * 0.075:.0f}" y="{h - w * 0.075 + w * 0.032:.0f}" font-family="Georgia, serif" font-size="{w * 0.014:.0f}" letter-spacing="{w * 0.003:.1f}" fill="{ink}" fill-opacity="0.5">PLACEHOLDER — REPLACE WITH PHOTOGRAPH {w} × {h}</text>
</svg>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, w, h, p, label in SLOTS:
        with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
            f.write(svg(name, w, h, p, label))
    print(f"Wrote {len(SLOTS)} placeholders to {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
