#!/usr/bin/env python3
"""Variant B — "Vintage broadsheet" for news-image-20261117.

Classic 19th-century newspaper, clean and readable. Warm cream paper,
black ink, serif everywhere (DejaVu Serif), thin double rules, centred
ornate masthead, drop-cap lead paragraph. Spot colour used sparingly:
dark red for the accent word FALLS and for rules/numbers.

Content comes verbatim from stories.py — same 36 stories as v2.1.
Deterministic: PIL only, no network, no random, no timestamps.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stories import (  # noqa: E402
    LEAD_KICKER, LEAD_HEADLINE, LEAD_SUB, LEAD_SUMMARY,
    TOP3, SECTIONS, ALSO_TODAY, DATE_LINE, MASTHEAD, FOOTER,
)

W, H = 1024, 1024
PAPER = (245, 238, 221)   # warm cream
INK = (26, 26, 26)
RED = (139, 26, 26)       # dark red, used sparingly
GREY = (90, 82, 72)
HAIR = (190, 180, 160)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, fill=INK, lh=None, max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    if lh is None:
        lh = int(font.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def spaced_width(draw, text, font, spacing):
    w = 0
    for ch in text:
        w += draw.textlength(ch, font=font) + spacing
    return w - spacing


def draw_spaced(draw, x, y, text, font, fill, spacing=2):
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing


def draw_spaced_centred(draw, cx, y, text, font, fill, spacing=2):
    w = spaced_width(draw, text, font, spacing)
    draw_spaced(draw, cx - w / 2, y, text, font, fill, spacing)


def diamond(draw, cx, cy, r, fill):
    draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)


def double_rule(draw, x0, x1, y):
    draw.line([(x0, y), (x1, y)], fill=INK, width=3)
    draw.line([(x0, y + 5), (x1, y + 5)], fill=INK, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28
    X0, X1 = M, W - M

    # ---- Top line: EST. 2026 / edition note ----
    f_small = F(SERIF_B, 11)
    draw_spaced(d, X0, 14, "EST. 2026", f_small, INK, 2)
    right = "VOL. I  —  No. 17"
    rw = spaced_width(d, right, f_small, 2)
    draw_spaced(d, X1 - rw, 14, right, f_small, INK, 2)

    # ---- Ornate centred masthead ----
    f_mast = F(SERIF_B, 46)
    tw = d.textlength(MASTHEAD, font=f_mast)
    d.text(((W - tw) / 2, 30), MASTHEAD, font=f_mast, fill=INK)
    # ornament row: rule — diamond — rule
    oy = 88
    d.line([(X0, oy), (W / 2 - 60, oy)], fill=INK, width=1)
    d.line([(W / 2 + 60, oy), (X1, oy)], fill=INK, width=1)
    diamond(d, W / 2, oy, 6, RED)
    diamond(d, W / 2 - 22, oy, 3, INK)
    diamond(d, W / 2 + 22, oy, 3, INK)

    double_rule(d, X0, X1, 98)

    # ---- Date line, centred small caps ----
    date_txt = DATE_LINE + "  •  36 STORIES  •  SIX CONTINENTS"
    draw_spaced_centred(d, W / 2, 112, date_txt, F(SERIF_B, 13), INK, 2)

    # ---- Lead story ----
    ly = 138
    draw_spaced(d, X0, ly, LEAD_KICKER, F(SERIF_B, 12), RED, 2)
    # giant serif headline: black line, red accent word
    f_lead = F(SERIF_B, 56)
    d.text((X0, ly + 22), LEAD_HEADLINE[0], font=f_lead, fill=INK)
    d.text((X0, ly + 88), LEAD_HEADLINE[1], font=f_lead, fill=RED)
    # subhead in serif (no italic face available)
    d.text((X0, ly + 156), LEAD_SUB, font=F(SERIF, 19), fill=INK)
    # drop-cap summary: giant first letter, text flows around it
    sy = ly + 190
    drop = LEAD_SUMMARY[0]
    rest = LEAD_SUMMARY[1:]
    f_drop = F(SERIF_B, 46)
    d.text((X0, sy - 4), drop, font=f_drop, fill=INK)
    drop_w = d.textlength(drop, font=f_drop) + 10
    # first two lines narrower (beside drop cap), rest full width
    lines = wrap(d, rest, F(SERIF, 15), 640 - drop_w)
    y = sy
    for i, ln in enumerate(lines[:2]):
        d.text((X0 + drop_w, y), ln, font=F(SERIF, 15), fill=INK)
        y += 19
    if len(lines) > 2:
        tail = " ".join(lines[2:])
        y = draw_wrapped(d, X0, y, tail, F(SERIF, 15), 640, lh=19)

    # framed engraving-style bridge box, right of lead
    bx0, by0, bx1, by1 = 700, ly, X1, ly + 148
    d.rectangle([bx0, by0, bx1, by1], outline=INK, width=2)
    d.rectangle([bx0 + 5, by0 + 5, bx1 - 5, by1 - 5], outline=INK, width=1)
    d.text((bx0 + 14, by0 + 10), "THE KERCH BRIDGE", font=F(SERIF_B, 13), fill=INK)
    # ink-line bridge: deck left + right, middle span collapsed (red)
    d.line([(bx0 + 14, by0 + 66), (bx0 + 108, by0 + 66)], fill=INK, width=5)
    d.line([(bx0 + 178, by0 + 66), (bx1 - 14, by0 + 66)], fill=INK, width=5)
    d.line([(bx0 + 108, by0 + 66), (bx0 + 143, by0 + 104)], fill=RED, width=5)
    d.line([(bx0 + 143, by0 + 104), (bx0 + 178, by0 + 66)], fill=RED, width=5)
    for px in (bx0 + 36, bx0 + 72, bx0 + 206, bx0 + 242):
        d.line([(px, by0 + 40), (px, by0 + 66)], fill=INK, width=3)
    # water hatching
    for wx in range(bx0 + 16, bx1 - 16, 22):
        d.line([(wx, by1 - 26), (wx + 12, by1 - 26)], fill=GREY, width=1)
    d.text((bx0 + 14, by1 - 44), "Road span down in the strait.",
           font=F(SERIF, 12), fill=INK)

    d.line([(X0, 384), (X1, 384)], fill=INK, width=1)

    # ---- Top 3: three columns divided by vertical rules ----
    colw = 306
    gap = 24
    ty = 396
    for i, (num, head, deck) in enumerate(TOP3):
        x = X0 + i * (colw + gap)
        if i:
            d.line([(x - gap // 2, ty), (x - gap // 2, ty + 96)], fill=HAIR, width=1)
        d.text((x, ty), num + ".", font=F(SERIF_B, 15), fill=RED)
        draw_wrapped(d, x, ty + 24, head, F(SERIF_B, 15), colw, lh=18, max_lines=2)
        draw_wrapped(d, x, ty + 62, deck, F(SERIF, 12), colw, fill=GREY, lh=15,
                     max_lines=3)

    double_rule(d, X0, X1, 508)

    # ---- Region grid: 3 cols x 2 rows ----
    gy = 520
    sec_h = 208
    for idx, (name, stories) in enumerate(SECTIONS):
        col = idx % 3
        row = idx // 3
        x = X0 + col * (colw + gap)
        y = gy + row * (sec_h + 12)
        # small-caps header, left-aligned, count right-aligned, rule below
        f_hdr = F(SERIF_B, 13)
        draw_spaced(d, x, y, name, f_hdr, INK, 2)
        lab = "5 stories"
        lw = d.textlength(lab, font=F(SERIF, 10))
        d.text((x + colw - lw, y + 2), lab, font=F(SERIF, 10), fill=GREY)
        d.line([(x, y + 20), (x + colw, y + 20)], fill=INK, width=1)
        iy = y + 28
        for j, (num, head) in enumerate(stories):
            d.text((x, iy), num, font=F(SERIF_B, 12), fill=RED)
            draw_wrapped(d, x + 28, iy, head, F(SERIF_B, 12), colw - 28, lh=15,
                         max_lines=2)
            iy += 35
            if j < len(stories) - 1:
                d.line([(x, iy - 4), (x + colw, iy - 4)], fill=HAIR, width=1)

    # ---- Also today + footer ----
    ay = gy + 2 * sec_h + 22
    d.line([(X0, ay), (X1, ay)], fill=INK, width=1)
    also = ("ALSO TODAY  —  " + ALSO_TODAY[0] + "  " + ALSO_TODAY[1] +
            "    •    " + ALSO_TODAY[2] + "  " + ALSO_TODAY[3])
    f_also = F(SERIF_B, 12)
    aw = d.textlength(also, font=f_also)
    d.text(((W - aw) / 2, ay + 8), also, font=f_also, fill=INK)
    d.line([(X0, ay + 30), (X1, ay + 30)], fill=INK, width=1)
    fw = d.textlength(FOOTER, font=F(SERIF, 11))
    d.text(((W - fw) / 2, ay + 38), FOOTER, font=F(SERIF, 11), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("saved", out, img.size)


if __name__ == "__main__":
    main()
