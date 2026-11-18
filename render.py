#!/usr/bin/env python3
"""Render v2 — "The World in One Day", 17 Nov 2026.

Design language: modern SaaS hero (per the @AZ1Z1M reference) — giant bold
sans headline with ONE vivid-red accent word, clean white background, lots
of breathing room, rounded cards, thin borders, bright colour-coded pills
per region, and a scatter of colourful tiles in the hero.

Content is UNCHANGED from v1: the same 36 verified stories, 6 continents,
same lead (Kerch Bridge) + Iran/Bahrain + Shenzhen. Only the presentation
changed.

Deterministic: no network, no timestamps, no randomness.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
WHITE = (255, 255, 255)
INK = (15, 23, 42)
GREY = (100, 116, 139)
GREY_D = (51, 65, 85)
PANEL = (248, 250, 252)
BORDER = (226, 232, 240)
HAIR = (241, 245, 249)
RED = (225, 29, 72)          # vivid accent red ("taste" red)
BLUE = (37, 99, 235)         # CONNECT blue
YELLOW = (250, 204, 21)      # Explore yellow

# Bright colour code per region
C_EUROPE = (37, 99, 235)     # blue
C_MIDEAST = (234, 88, 12)    # orange
C_ASIA = (124, 58, 237)      # violet
C_AFRICA = (22, 163, 74)     # green
C_NAMER = (13, 148, 136)     # teal
C_LATAM = (219, 39, 119)     # pink

SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


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
        lh = int(font.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def pill(draw, x, y, text, font, bg, fg, pad_x=12, h=26):
    w = int(draw.textlength(text, font=font)) + pad_x * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    draw.text((x + pad_x, y + (h - font.size) // 2 - 1), text, font=font, fill=fg)
    return x + w


def tile(draw, x, y, s, color, kind):
    """A small rounded app-icon-style tile with a white glyph."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=14, fill=color)
    c = s // 2
    if kind == "circle":
        r = s // 5
        draw.ellipse([x + c - r, y + c - r, x + c + r, y + c + r], fill=WHITE)
    elif kind == "triangle":
        draw.polygon([(x + c, y + s // 4), (x + s // 4, y + 3 * s // 4),
                      (x + 3 * s // 4, y + 3 * s // 4)], fill=WHITE)
    elif kind == "diamond":
        draw.polygon([(x + c, y + s // 5), (x + 4 * s // 5, y + c),
                      (x + c, y + 4 * s // 5), (x + s // 5, y + c)], fill=WHITE)
    elif kind == "bolt":
        draw.polygon([(x + c + 6, y + s // 5), (x + c - 8, y + c + 2),
                      (x + c - 1, y + c + 2), (x + c - 6, y + 4 * s // 5),
                      (x + c + 9, y + c - 2), (x + c + 1, y + c - 2)], fill=WHITE)
    elif kind == "num":
        pass  # number drawn by caller


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    M = 28
    X0, X1 = M, W - M

    # ---- Top bar: wordmark + pills (CONNECT / Explore language) ----
    f_logo = F(SANS_B, 26)
    x = X0
    for txt, col in [("THE WORLD IN ONE ", INK), ("DAY", RED)]:
        d.text((x, 20), txt, font=f_logo, fill=col)
        x += d.textlength(txt, font=f_logo)
    # right pills
    f_pill = F(SANS_B, 13)
    p2 = "6 CONTINENTS"
    w2 = int(d.textlength(p2, font=f_pill)) + 24
    p1 = "36 STORIES"
    w1 = int(d.textlength(p1, font=f_pill)) + 24
    d.rounded_rectangle([X1 - w2, 20, X1, 48], radius=14, fill=YELLOW)
    d.text((X1 - w2 + 12, 27), p2, font=f_pill, fill=INK)
    d.rounded_rectangle([X1 - w2 - 10 - w1, 20, X1 - w2 - 10, 48], radius=14, fill=BLUE)
    d.text((X1 - w2 - 10 - w1 + 12, 27), p1, font=f_pill, fill=WHITE)

    d.line([(X0, 62), (X1, 62)], fill=BORDER, width=1)
    d.text((X0, 72), "TUESDAY, 17 NOVEMBER 2026", font=F(SANS_B, 13), fill=GREY)
    tag = "THE WHOLE DAY, SUMMED UP IN ONE IMAGE"
    tw = d.textlength(tag, font=F(SANS_B, 13))
    d.text((X1 - tw, 72), tag, font=F(SANS_B, 13), fill=GREY)

    # ---- HERO ----
    hx0, hy0, hx1, hy1 = X0, 100, X1, 372
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=20, fill=PANEL, outline=BORDER, width=1)
    px = hx0 + 28
    # kicker pill
    pill(d, px, hy0 + 20, "●  LEAD STORY  —  EUROPE", F(SANS_B, 12), RED, WHITE, h=26)
    # giant headline: black line + red accent word
    d.text((px, hy0 + 56), "KERCH BRIDGE", font=F(SANS_B, 62), fill=INK)
    d.text((px, hy0 + 124), "FALLS", font=F(SANS_B, 62), fill=RED)
    d.text((px, hy0 + 196), "Road span collapses as Kyiv bridges burn",
           font=F(SANS_B, 19), fill=INK)
    lead = ("Ukraine struck the 19 km bridge to Crimea for a second straight "
            "night. Russia hit two Kyiv bridges, killing at least two.")
    draw_wrapped(d, px, hy0 + 228, lead, F(SANS, 14), 600, fill=GREY_D, lh=18, max_lines=2)

    # hero right: scatter of colourful tiles (the reference's icon field)
    tx0, ty0 = hx1 - 312, hy0 + 16
    # ~22 tiles in a loose staggered cloud (reference: denser top-right,
    # sparser bottom). Fixed jitter table -> deterministic, no randomness.
    BLACK = (15, 23, 42)
    tiles = [
        # (dx, dy, size, color, kind, label)
        (0, 0, 42, RED, "bolt", None),
        (48, 4, 42, BLUE, "circle", None),
        (96, 0, 42, YELLOW, "num", "2"),
        (144, 4, 42, C_ASIA, "diamond", None),
        (192, 0, 42, BLACK, "triangle", None),
        (240, 4, 42, C_AFRICA, "circle", None),
        (8, 50, 42, C_AFRICA, "triangle", None),
        (54, 54, 42, C_MIDEAST, "num", "3"),
        (100, 50, 42, C_LATAM, "circle", None),
        (146, 54, 42, C_NAMER, "bolt", None),
        (192, 50, 42, YELLOW, "diamond", None),
        (238, 54, 42, RED, "circle", None),
        (0, 100, 42, C_ASIA, "diamond", None),
        (52, 104, 42, BLACK, "bolt", None),
        (104, 100, 42, YELLOW, "num", "4"),
        (156, 104, 42, RED, "triangle", None),
        (208, 100, 42, BLUE, "circle", None),
        (20, 150, 42, C_NAMER, "bolt", None),
        (72, 154, 42, C_LATAM, "diamond", None),
        (124, 150, 42, C_AFRICA, "circle", None),
        (176, 154, 42, C_MIDEAST, "triangle", None),
        (228, 150, 42, BLUE, "bolt", None),
    ]
    for dx, dy, s_, col, kind, label in tiles:
        tile(d, tx0 + dx, ty0 + dy, s_, col, kind)
        if label:
            f_n = F(SANS_B, 20)
            tw2 = d.textlength(label, font=f_n)
            num_col = INK if col == YELLOW else WHITE
            d.text((tx0 + dx + (s_ - tw2) / 2, ty0 + dy + s_ // 2 - 11),
                   label, font=f_n, fill=num_col)
    d.text((tx0, ty0 + 202), "2  IRAN  •  3  SHENZHEN  •  4  HORMUZ",
           font=F(SANS_B, 11), fill=GREY)

    # ---- Top 3 cards ----
    top = [
        ("2", "IRAN DRONES AT US RADAR IN BAHRAIN", RED,
         "Third attack in five days on the Gulf island, home of the US 5th Fleet. Bahrain says it intercepted the drones; no casualties reported."),
        ("3", "TRUMP, XI & PUTIN TO MEET IN SHENZHEN", BLUE,
         "China confirms a trilateral summit on Thursday, 19 Nov, on the APEC sidelines. Trump is in Manila; Xi cuts $280m of Canada tariffs."),
        ("4", "TANKERS HIT BY MINES NEAR HORMUZ", C_MIDEAST,
         "A fourth tanker catches fire in 24 hours on routes Tehran calls unauthorised. A third US carrier, USS Theodore Roosevelt, arrives."),
    ]
    ty = 384
    colw = 312
    for i, (num, head, col, deck) in enumerate(top):
        x = X0 + i * (colw + 16)
        d.rounded_rectangle([x, ty, x + colw, ty + 104], radius=16, fill=WHITE,
                            outline=BORDER, width=1)
        d.rounded_rectangle([x + 12, ty + 12, x + 48, ty + 48], radius=12, fill=col)
        f_n = F(SANS_B, 20)
        tw2 = d.textlength(num, font=f_n)
        d.text((x + 12 + (36 - tw2) / 2, ty + 20), num, font=f_n, fill=WHITE)
        draw_wrapped(d, x + 58, ty + 12, head, F(SANS_B, 15), colw - 70, lh=18, max_lines=2)
        draw_wrapped(d, x + 12, ty + 56, deck, F(SANS, 11), colw - 24, fill=GREY_D,
                     lh=14, max_lines=3)

    # ---- Continent index pills ----
    iy = 502
    d.text((X0, iy + 5), "6 CONTINENTS", font=F(SANS_B, 12), fill=GREY)
    pills = [("EUROPE · 5", C_EUROPE), ("MIDDLE EAST · 5", C_MIDEAST),
             ("ASIA-PACIFIC · 5", C_ASIA), ("AFRICA · 5", C_AFRICA),
             ("N. AMERICA · 5", C_NAMER), ("LATIN AM. & OCEANIA · 5", C_LATAM)]
    f_ip = F(SANS_B, 12)
    total = sum(int(d.textlength(t, font=f_ip)) + 24 for t, _ in pills) + 10 * (len(pills) - 1)
    x = X0 + 118
    # centre the pill row in the remaining width
    x = X0 + 118 + max(0, (X1 - (X0 + 118) - total) // 2)
    for t, col in pills:
        x = pill(d, x, iy, t, f_ip, col, WHITE, h=28) + 10

    # ---- Region grid: 3 cols x 2 rows of soft cards ----
    sections = [
        ("EUROPE", C_EUROPE, [
            ("5", "Russia hits Kyiv bridges, 2 killed in overnight strikes"),
            ("6", "Five EU states plan Rwanda return hub for 2027"),
            ("7", "Depardieu admits sexual assault, drops appeal"),
            ("8", "UK sanctions 8 firms building West Bank settlements"),
            ("9", "UN: 128 states debate ban on killer robots in Geneva"),
        ]),
        ("MIDDLE EAST", C_MIDEAST, [
            ("10", "Houthis take Bab al-Mandab coast as forces fall back to Aden"),
            ("11", "Jordan bans Telegram over national security"),
            ("12", "UK, Australia, Canada, Italy urge Israel to open Gaza aid"),
            ("13", "Settler kills 72-year-old woman in Jericho, West Bank"),
            ("14", "UN: rebuilding Syria will cost $216bn; 4m have returned"),
        ]),
        ("ASIA-PACIFIC", C_ASIA, [
            ("15", "Japan scrambles jets as suspected Russian planes enter airspace"),
            ("16", "Taiwan and S. Korea also track Russian aircraft"),
            ("17", "US closes AI-chip rental loophole aimed at China"),
            ("18", "Singapore seeks trusted access to advanced AI chips"),
            ("19", "India bus plunges into ravine, 6–8 dead in Uttarakhand"),
        ]),
        ("AFRICA", C_AFRICA, [
            ("20", "S. Africa: 17 dead in two separate mass shootings"),
            ("21", "DR Congo Ebola out of control: 5,500 dead, 11,200 cases"),
            ("22", "Guinea arrests 1,263 in gold-mining crackdown"),
            ("23", "Sudan: drones cause ~3 in 4 war deaths this year, UN says"),
            ("24", "S. Sudan: 3 abducted aid workers freed after $2,500 ransom"),
        ]),
        ("NORTH AMERICA", C_NAMER, [
            ("25", "Pentagon fails 9th audit in a row — $4.8tn unverified"),
            ("26", "US measles hits 5,412 cases, most since 1991; 13 babies born with it"),
            ("27", "White House: agencies need approval to testify to Congress"),
            ("28", "Supreme Court declines to revive $59m UC grant cuts"),
            ("29", "US banks hit by outages; Apple and Marriott systems down"),
        ]),
        ("LATIN AMERICA & OCEANIA", C_LATAM, [
            ("30", "Pope Leo XIV ends Peru trip, forgives rosary thrower"),
            ("31", "Pope demands justice for murdered Amazon defenders"),
            ("32", "Costa Rica journalist shot dead after probing drug links"),
            ("33", "Pacific workers need stronger protection, COP31 report warns"),
            ("34", "Scotland edges Australia 15–12; Wales beat NZ after 73 years"),
        ]),
    ]
    gy = 544
    sec_h = 202
    for idx, (name, color, stories) in enumerate(sections):
        col = idx % 3
        row = idx // 3
        x = X0 + col * (colw + 16)
        y = gy + row * (sec_h + 12)
        d.rounded_rectangle([x, y, x + colw, y + sec_h], radius=16, fill=PANEL,
                            outline=BORDER, width=1)
        # header pill
        pill(d, x + 12, y + 12, name, F(SANS_B, 12), color, WHITE, h=26)
        d.text((x + colw - 62, y + 19), "5 STORIES", font=F(SANS_B, 10), fill=GREY)
        iy2 = y + 48
        for j, (num, head) in enumerate(stories):
            d.text((x + 12, iy2), num, font=F(SANS_B, 12), fill=color)
            draw_wrapped(d, x + 40, iy2, head, F(SANS_B, 12), colw - 52, lh=15,
                         max_lines=2)
            iy2 += 30
            if j < len(stories) - 1:
                d.line([(x + 12, iy2 - 3), (x + colw - 12, iy2 - 3)], fill=HAIR, width=1)

    # ---- Also today bar ----
    ay = 544 + 2 * sec_h + 20
    d.rounded_rectangle([X0, ay, X1, ay + 30], radius=15, fill=BLUE)
    d.text((X0 + 16, ay + 7),
           "ALSO TODAY  •  35  COP31 climate summit continues in Antalya, Turkey   •   36  AFCON 2027 qualifiers: Senegal & Cameroon win",
           font=F(SANS_B, 12), fill=WHITE)

    # ---- Footer ----
    fy = ay + 38
    d.text((X0, fy), "36 stories  •  6 continents  •  Sources: AP, Reuters, AFP, BBC, Guardian, Al Jazeera — full list in README",
           font=F(SANS, 11), fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
