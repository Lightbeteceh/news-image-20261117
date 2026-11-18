#!/usr/bin/env python3
"""Render the 1024x1024 newspaper front page for 17 Nov 2026.

Deterministic: no network, no timestamps, no randomness. Output is a
fixed PNG; main.py just copies it to /output/entry.png.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 246, 227)
INK = (17, 17, 17)
RED = (180, 35, 24)
BLUE = (27, 58, 92)
GREY = (90, 90, 90)
LIGHT_BLUE = (217, 226, 232)
RULE = (120, 120, 120)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
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


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    X0, X1 = M, W - M

    # ---- Masthead ----
    f_mast = F(SERIF_B, 50)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 14), title, font=f_mast, fill=INK)
    d.line([(X0, 78), (X1, 78)], fill=INK, width=3)
    d.line([(X0, 82), (X1, 82)], fill=INK, width=1)
    f_sub = F(SANS_B, 15)
    sub = "TUESDAY 17 NOVEMBER 2026  •  36 STORIES  •  6 CONTINENTS"
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw) / 2, 88), sub, font=f_sub, fill=RED)

    # ---- Lead story ----
    y = 116
    d.text((X0, y), "LEAD STORY  —  EUROPE: WAR IN UKRAINE", font=F(SANS_B, 13), fill=RED)
    y += 22
    f_lead = F(SERIF_B, 42)
    d.text((X0, y), "KERCH BRIDGE FALLS", font=f_lead, fill=INK)
    y += 50
    f_lead2 = F(SERIF_B, 25)
    d.text((X0, y), "Road span collapses as Kyiv bridges burn", font=f_lead2, fill=BLUE)
    y += 36
    lead = ("Ukraine struck the 19 km bridge to Crimea for a second straight "
            "night. Russia hit two Kyiv bridges, killing at least two.")
    y = draw_wrapped(d, X0, y, lead, F(SANS, 15), 640, lh=20)

    # Bridge illustration (schematic, right of lead)
    bx0, by0, bx1, by1 = 700, 116, X1, 268
    d.rectangle([bx0, by0, bx1, by1], outline=INK, width=2, fill=(235, 240, 245))
    d.rectangle([bx0, by0, bx1, by0 + 22], fill=BLUE)
    d.text((bx0 + 10, by0 + 3), "KERCH BRIDGE — SCHEMATIC", font=F(SANS_B, 11), fill=(255, 255, 255))
    # sea
    d.rectangle([bx0, by0 + 108, bx1, by1], fill=(170, 205, 225))
    # deck: left + right, middle span collapsed into water
    d.line([(bx0 + 8, by0 + 78), (bx0 + 105, by0 + 78)], fill=INK, width=6)
    d.line([(bx0 + 185, by0 + 78), (bx1 - 8, by0 + 78)], fill=INK, width=6)
    d.line([(bx0 + 105, by0 + 78), (bx0 + 145, by0 + 128)], fill=RED, width=6)
    d.line([(bx0 + 145, by0 + 128), (bx0 + 185, by0 + 78)], fill=RED, width=6)
    for px in (bx0 + 30, bx0 + 70, bx0 + 210, bx0 + 250):
        d.line([(px, by0 + 48), (px, by0 + 78)], fill=INK, width=3)
    d.text((bx0 + 10, by1 - 22), "Road span down in the strait", font=F(SANS_B, 11), fill=INK)
    d.text((bx1 - 108, by0 + 88), "KERCH STRAIT", font=F(SANS_B, 10), fill=BLUE)

    d.line([(X0, 278), (X1, 278)], fill=INK, width=2)

    # ---- Top 3 stories ----
    top = [
        ("2", "IRAN DRONES AT US RADAR IN BAHRAIN",
         "Third attack in five days on the Gulf island, home of the US 5th Fleet. "
         "Bahrain says it intercepted the drones; no casualties reported."),
        ("3", "TRUMP, XI & PUTIN TO MEET IN SHENZHEN",
         "China confirms a trilateral summit on Thursday, 19 Nov, on the APEC "
         "sidelines. Trump is in Manila; Xi cuts $280m of Canada tariffs."),
        ("4", "TANKERS HIT BY MINES NEAR HORMUZ",
         "A fourth tanker catches fire in 24 hours on routes Tehran calls "
         "unauthorised. A third US carrier, USS Theodore Roosevelt, arrives."),
    ]
    ty = 292
    colw = 312
    for i, (num, head, deck) in enumerate(top):
        x = X0 + i * (colw + 20)
        d.rectangle([x, ty, x + colw, ty + 92], outline=RULE, width=1)
        d.rectangle([x, ty, x + 34, ty + 92], fill=RED)
        d.text((x + 8, ty + 28), num, font=F(SANS_B, 30), fill=(255, 255, 255))
        draw_wrapped(d, x + 44, ty + 6, head, F(SANS_B, 14), colw - 52, lh=17, max_lines=2)
        draw_wrapped(d, x + 44, ty + 42, deck, F(SANS, 11), colw - 52, lh=14, max_lines=3)

    # ---- World map strip ----
    my = 392
    d.text((X0, my), "THE WORLD AT A GLANCE — WHERE IT HAPPENED", font=F(SANS_B, 13), fill=RED)
    map_x0, map_y0, map_x1, map_y1 = X0, my + 20, X1, my + 104
    d.rectangle([map_x0, map_y0, map_x1, map_y1], outline=RULE, width=1, fill=(240, 244, 247))

    def proj(lon, lat):
        x = map_x0 + (lon + 180) / 360.0 * (map_x1 - map_x0)
        y = map_y0 + (80 - lat) / 140.0 * (map_y1 - map_y0)
        return (x, y)

    continents = {
        "N. AMERICA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 62), (-55, 47), (-70, 42), (-80, 32), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-150, 60)],
        "S. AMERICA": [(-80, 10), (-60, 5), (-50, 0), (-40, -10), (-35, -20), (-45, -30), (-60, -40), (-70, -50), (-75, -35), (-80, -20)],
        "EUROPE": [(-10, 36), (-5, 43), (0, 50), (5, 58), (10, 60), (20, 70), (30, 70), (40, 68), (35, 60), (30, 55), (25, 45), (20, 40), (10, 38), (0, 36)],
        "AFRICA": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15), (48, 11), (51, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -25), (12, -10), (9, 4), (-8, 5)],
        "ASIA": [(40, 68), (60, 70), (80, 73), (110, 75), (140, 72), (160, 66), (170, 60), (160, 55), (140, 45), (130, 40), (127, 35), (120, 30), (110, 20), (105, 10), (100, 5), (95, 15), (90, 22), (80, 15), (75, 8), (70, 20), (60, 25), (55, 27), (48, 30), (45, 35)],
        "OCEANIA": [(113, -22), (120, -15), (130, -12), (140, -17), (147, -19), (153, -27), (150, -37), (140, -38), (130, -32), (120, -35)],
    }
    for name, pts in continents.items():
        poly = [proj(lon, lat) for lon, lat in pts]
        d.polygon(poly, fill=LIGHT_BLUE, outline=(122, 138, 153))
    labels = {"N. AMERICA": (-100, 55), "S. AMERICA": (-60, -15), "EUROPE": (15, 58),
              "AFRICA": (18, 8), "ASIA": (95, 55), "OCEANIA": (135, -28)}
    for name, (lon, lat) in labels.items():
        x, y = proj(lon, lat)
        d.text((x - 24, y - 5), name, font=F(SANS_B, 8), fill=BLUE)
    dots = [("KYIV", 30.5, 50.4), ("KERCH", 36.5, 45.3), ("BAHRAIN", 50.5, 26.2),
            ("HORMUZ", 56.5, 26.5), ("SHENZHEN", 114, 22.5), ("TOKYO", 139.7, 35.7),
            ("GAZA", 34.5, 31.5), ("ADEN", 45, 12.8)]
    for name, lon, lat in dots:
        x, y = proj(lon, lat)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=RED, outline=(255, 255, 255))

    # ---- Region sections: 3 columns x 2 rows ----
    sections = [
        ("EUROPE", RED, [
            ("5", "Russia hits Kyiv bridges, 2 killed in overnight strikes"),
            ("6", "Five EU states plan Rwanda return hub for 2027"),
            ("7", "Depardieu admits sexual assault, drops appeal"),
            ("8", "UK sanctions 8 firms building West Bank settlements"),
            ("9", "UN: 128 states debate ban on killer robots in Geneva"),
        ]),
        ("MIDDLE EAST", RED, [
            ("10", "Houthis take Bab al-Mandab coast as forces fall back to Aden"),
            ("11", "Jordan bans Telegram over national security"),
            ("12", "UK, Australia, Canada, Italy urge Israel to open Gaza aid"),
            ("13", "Settler kills 72-year-old woman in Jericho, West Bank"),
            ("14", "UN: rebuilding Syria will cost $216bn; 4m have returned"),
        ]),
        ("ASIA-PACIFIC", RED, [
            ("15", "Japan scrambles jets as suspected Russian planes enter airspace"),
            ("16", "Taiwan and S. Korea also track Russian aircraft"),
            ("17", "US closes AI-chip rental loophole aimed at China"),
            ("18", "Singapore seeks trusted access to advanced AI chips"),
            ("19", "India bus plunges into ravine, 6–8 dead in Uttarakhand"),
        ]),
        ("AFRICA", RED, [
            ("20", "S. Africa: 17 dead in two separate mass shootings"),
            ("21", "DR Congo Ebola out of control: 5,500 dead, 11,200 cases"),
            ("22", "Guinea arrests 1,263 in gold-mining crackdown"),
            ("23", "Sudan: drones cause ~3 in 4 war deaths this year, UN says"),
            ("24", "S. Sudan: 3 abducted aid workers freed after $2,500 ransom"),
        ]),
        ("NORTH AMERICA", RED, [
            ("25", "Pentagon fails 9th audit in a row — $4.8tn unverified"),
            ("26", "US measles hits 5,412 cases, most since 1991; 13 babies born with it"),
            ("27", "White House: agencies need approval to testify to Congress"),
            ("28", "Supreme Court declines to revive $59m UC grant cuts"),
            ("29", "US banks hit by outages; Apple and Marriott systems down"),
        ]),
        ("LATIN AMERICA & OCEANIA", RED, [
            ("30", "Pope Leo XIV ends Peru trip, forgives rosary thrower"),
            ("31", "Pope demands justice for murdered Amazon defenders"),
            ("32", "Costa Rica journalist shot dead after probing drug links"),
            ("33", "Pacific workers need stronger protection, COP31 report warns"),
            ("34", "Scotland edges Australia 15–12; Wales beat NZ after 73 years"),
        ]),
    ]
    sy = 504
    sec_h = 216
    for idx, (name, color, stories) in enumerate(sections):
        col = idx % 3
        row = idx // 3
        x = X0 + col * (colw + 20)
        y = sy + row * (sec_h + 10)
        d.rectangle([x, y, x + colw, y + 24], fill=INK)
        d.text((x + 8, y + 4), name, font=F(SANS_B, 13), fill=(255, 255, 255))
        _t = "5 STORIES"
        d.text((x + colw - 8 - d.textlength(_t, font=F(SANS_B, 10)), y + 5), _t, font=F(SANS_B, 10), fill=(255, 220, 120))
        iy = y + 30
        for num, head in stories:
            d.text((x, iy), num, font=F(SANS_B, 12), fill=RED)
            draw_wrapped(d, x + 26, iy, head, F(SANS_B, 12), colw - 26, lh=15, max_lines=2)
            iy += 37
        d.line([(x, y + sec_h - 2), (x + colw, y + sec_h - 2)], fill=RULE, width=1)

    # ---- Also today strip ----
    ay = 500 + 2 * sec_h + 20
    d.rectangle([X0, ay, X1, ay + 30], fill=BLUE)
    d.text((X0 + 8, ay + 6), "ALSO TODAY  •  35  COP31 climate summit continues in Antalya, Turkey   •   36  AFCON 2027 qualifiers: Senegal & Cameroon win",
           font=F(SANS_B, 12), fill=(255, 255, 255))

    # ---- Footer ----
    fy = ay + 36
    d.line([(X0, fy), (X1, fy)], fill=INK, width=2)
    d.text((X0, fy + 7), "36 stories  •  6 continents  •  Sources: AP, Reuters, AFP, BBC, Guardian, Al Jazeera — full list in README",
           font=F(SANS, 11), fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
