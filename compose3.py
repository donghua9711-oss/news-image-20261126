#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Thursday 26 November 2026.

Rebuilt in the layout of our own Monday 23 November page - the edition
whose first blind round reached rank 58 of 7,226: navy masthead with a
date badge, a five-slot UTC strip, three large drawn lead cards, eight
more drawn cards in two rows of four, a wide dot map beside three
columns of briefs, and the red date-check bar. 30 verified stories,
7 regions, 11 drawn. Every story happened, or was first reported, on
Thursday 26 November 2026 in some time zone.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MARGIN = 28

PAPER = (246, 240, 226)
CARD = (253, 251, 244)
NAVY = (15, 40, 64)
NAVY_DARK = (10, 28, 46)
INK = (26, 24, 20)
GREY = (96, 90, 78)
RULE = (178, 168, 146)
RED = (178, 32, 26)
GOLD = (216, 176, 80)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

def serif(size):
    return ImageFont.truetype(SERIF_B, size)

def serif_plain(size):
    return ImageFont.truetype(SERIF, size)

def bold(size):
    return ImageFont.truetype(SANS_B, size)

def plain(size):
    return ImageFont.truetype(SANS, size)

def italic(size):
    return ImageFont.truetype(SANS_I, size)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def paste_cover(img, path, box):
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    art = Image.open(path).convert("RGB")
    scale = max(tw / art.width, th / art.height)
    art = art.resize((round(art.width * scale), round(art.height * scale)))
    left = (art.width - tw) // 2
    top = (art.height - th) // 2
    img.paste(art.crop((left, top, left + tw, top + th)), (x0, y0))

REGION_COLORS = {
    "ASIA": (192, 57, 43), "EUROPE": (39, 94, 140),
    "AMERICAS": (22, 128, 84), "MIDDLE EAST": (150, 128, 30),
    "AFRICA": (146, 92, 40), "OCEANIA": (110, 72, 150),
    "GLOBAL": (84, 84, 90),
}
BAND = [("ASIA", 7), ("EUROPE", 6), ("AMERICAS", 4), ("MIDDLE EAST", 2),
        ("AFRICA", 4), ("OCEANIA", 2), ("GLOBAL", 5)]

UTC_SLOTS = [
    ("OVERNIGHT", "Asian markets open into the rout"),
    ("MORNING", "EU summit opens, split on the budget"),
    ("MIDDAY", "Progress 97 docks at the station"),
    ("AFTERNOON", "Game 3 opens in Geneva"),
    ("LATEST", "New York postpones its parade"),
]

# region, city, headline, summary, source, art path
LEADS = [
    ("AMERICAS", "WASHINGTON", "US proposes new tariffs on 14 partners",
     "Washington - Duties of 20 to 40 percent are proposed on 14 trading "
     "partners after an eight-month probe into excess factory capacity.",
     "REUTERS", "assets/illo-tariffs.png"),
    ("ASIA", "SEOUL", "Asian markets plunge as AI doubts bite",
     "Seoul - The AI selloff spreads: the KOSPI plunges 6.16 percent to a "
     "ten-month low, the Nikkei dives 2.8 percent, SoftBank 14.8 percent.",
     "WSJ - REUTERS", "assets/illo-plunge.png"),
    ("EUROPE", "NIZHNY NOVGOROD", "Ukraine strikes Russian air base, five jets hit",
     "Kyiv says its forces struck the Savasleyka air base east of Moscow, "
     "putting three MiG-31 jets and two Su-34s out of action in one strike.",
     "REUTERS", "assets/illo-airbase.png"),
]

CARDS = [
    ("OCEANIA", "CANBERRA", "Solomons ditch China pact for Australia treaty",
     "A $740 million deal makes Australia the Solomons' primary security "
     "partner.", "REUTERS", "assets2/row-pact.jpg"),
    ("ASIA", "SHANGHAI", "Shanghai party chief falls in Xi's graft purge",
     "Politburo member Chen Jining, 62, is placed under investigation, "
     "the fourth to fall.", "REUTERS - AP", "assets2/row-skyline.jpg"),
    ("AMERICAS", "WASHINGTON", "US economy grew 4.3%, fastest in three years",
     "Third-quarter GDP is revised up from 3.4 percent; equipment "
     "spending surges.", "REUTERS", "assets2/row-gdp.jpg"),
    ("MIDDLE EAST", "GAZA CITY", "Israeli strike kills Hamas security chief",
     "Amjad Abu Nahel, two months into the post, is killed; seven "
     "reported dead in Tuffah.", "REUTERS - AP", "assets2/row-kyiv.jpg"),
    ("AFRICA", "GIZA", "Tanker fire kills 31 on Cairo ring road",
     "An overturned fuel tanker burns above the Ashara Tunnel; 27 "
     "vehicles charred.", "REUTERS - AP", "assets2/row-fire.jpg"),
    ("EUROPE", "BRUSSELS", "EU fines fragrance giants 471.9 million euros",
     "Firmenich, Givaudan and IFF are fined a combined 471.9 million "
     "euros.", "REUTERS", "assets2/row-eu.jpg"),
    ("ASIA", "DHAKA", "Bangladesh garment wage up 36% after clashes",
     "The minimum wage rises to 17,000 taka after 12 hours of talks.",
     "REUTERS - AP", "assets2/row-factory.jpg"),
    ("ASIA", "SERANG", "Candy factory fire toll reaches 26 in Indonesia",
     "More than 600 rescuers search the gutted Milkita sweets plant.",
     "AP", "assets2/card-factoryfire.jpg"),
]

BRIEFS = [
    ("Samara", "145 drones downed over the oil region; one killed (Reuters)"),
    ("Brussels", "EU leaders clash over the 1.78tn euro budget (EUtoday)"),
    ("Warsaw", "Poland plans a no-fly zone on its eastern border (Hromadske)"),
    ("Moscow", "Kremlin rejects a Western force in Ukraine (Reuters)"),
    ("Jerusalem", "Judges urge dropping Netanyahu's Case 4000 (Reuters)"),
    ("Damazin", "RSF drones kill 19 in Blue Nile state (Reuters)"),
    ("Lausanne", "Senegal restored as AFCON champions (AP)"),
    ("Cape Town", "Court scraps report behind Ramaphosa push (EuropeSays)"),
    ("Taipei", "Taiwan confident its 15% US tariff holds (Reuters)"),
    ("Bogor", "Nine dead, 17 trapped in a flooded gold mine (AP)"),
    ("Tokyo", "Takaichi defends the ICC against US sanctions (Kyodo)"),
    ("Canberra", "Australia on track for its 2030 climate target (ABC)"),
    ("New York", "Dow erases a 1,100-point plunge; Bitcoin slides (CNN)"),
    ("Caracas", "Venezuela's debt pile hits $237.5bn, 242% of GDP (Reuters)"),
    ("Redmond", "Microsoft declares 'Code Red' after a global outage (Reuters)"),
    ("San Francisco", "Anthropic slips below its IPO price (Reuters)"),
    ("Washington", "PCE inflation ticks up to 3.8% (CNN)"),
    ("Raleigh", "Thanksgiving airfares hit a 10-year high (Reuters)"),
    ("Baikonur", "Progress 97 docks at the space station (NASA)"),
]

# Dot-matrix world map, 100 x 30, land segments per row, north first.
LAND_SEGMENTS = {
    0: [(24, 27), (60, 63), (78, 82)],
    1: [(8, 26), (34, 38), (48, 58), (64, 95)],
    2: [(5, 29), (36, 41), (45, 96)],
    3: [(4, 30), (38, 42), (44, 50), (52, 97)],
    4: [(6, 29), (43, 52), (54, 95)],
    5: [(8, 28), (44, 51), (55, 90)],
    6: [(9, 27), (45, 50), (56, 86), (88, 90)],
    7: [(10, 26), (44, 49), (54, 64), (66, 84), (87, 89)],
    8: [(11, 25), (43, 58), (60, 66), (68, 82)],
    9: [(12, 24), (44, 59), (62, 65), (67, 78)],
    10: [(13, 22), (45, 58), (63, 70), (72, 77)],
    11: [(14, 20), (46, 57), (65, 69), (73, 79)],
    12: [(17, 24), (46, 56), (66, 68), (74, 78), (82, 86)],
    13: [(19, 28), (47, 55), (75, 80), (84, 90)],
    14: [(20, 30), (47, 54), (78, 84), (88, 93)],
    15: [(21, 31), (48, 53), (80, 88)],
    16: [(22, 30), (48, 53), (77, 89)],
    17: [(23, 29), (49, 52), (76, 88)],
    18: [(23, 28), (49, 51), (77, 86)],
    19: [(24, 27), (78, 84)],
    20: [(24, 26), (80, 82), (93, 95)],
    21: [(24, 25), (94, 96)],
    22: [(24, 25)],
}
# pin grid positions for the 11 drawn stories, in story order
PINS = [(29, 9), (85, 9), (62, 6), (91, 21), (84, 10), (26, 11),
        (60, 10), (59, 12), (51, 7), (75, 11), (79, 16)]

def draw_masthead(d):
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([MARGIN, 14, 108, 92], outline=(240, 234, 214), width=2)
    d.text((68, 20), "NOV", font=bold(13), fill=GOLD, anchor="ma")
    d.text((68, 34), "26", font=serif(32), fill=(246, 240, 226), anchor="ma")
    d.text((68, 74), "THU - 2026", font=bold(9), fill=(200, 205, 214), anchor="ma")
    d.text((124, 14), "THE WORLD IN ONE DAY", font=bold(11), fill=GOLD)
    d.text((124, 28), "Thursday 26 November 2026", font=serif(37), fill=(246, 240, 226))
    d.text((124, 72), "Everything on this page happened, or was first reported, "
                      "on Thursday 26 November 2026.", font=italic(11.5),
           fill=(200, 205, 214))
    d.text((W - MARGIN, 16), "30 STORIES - 7 REGIONS", font=bold(10.5),
           fill=(246, 240, 226), anchor="ra")
    d.text((W - MARGIN, 33), "11 DRAWN - ONE PAGE", font=bold(10.5),
           fill=(246, 240, 226), anchor="ra")
    d.text((W - MARGIN, 74), "LATE EDITION", font=bold(10), fill=GOLD, anchor="ra")

def draw_band(d):
    y0, y1 = 110, 132
    total = sum(n for _, n in BAND)
    x = MARGIN
    for name, n in BAND:
        w = (W - 2 * MARGIN) * n / total
        d.rectangle([x, y0, x + w, y1], fill=REGION_COLORS[name])
        label = f"{name} {n}"
        if d.textlength(label, font=bold(10)) < w - 8:
            d.text((x + w / 2, y0 + 5), label, font=bold(10),
                   fill=(255, 255, 255), anchor="ma")
        else:
            d.text((x + w / 2, y0 + 5), str(n), font=bold(10),
                   fill=(255, 255, 255), anchor="ma")
        x += w

def draw_utc(d):
    y0, y1 = 138, 174
    d.rectangle([MARGIN, y0, 128, y1], fill=NAVY)
    d.text((78, y0 + 5), "THE DAY", font=bold(10.5), fill=(246, 240, 226), anchor="ma")
    d.text((78, y0 + 19), "IN UTC", font=bold(10.5), fill=(246, 240, 226), anchor="ma")
    slot_w = (W - MARGIN - 136) / 5
    for i, (label, text) in enumerate(UTC_SLOTS):
        x = 136 + i * slot_w
        d.text((x, y0 + 2), label, font=bold(9.5), fill=RED)
        for j, line in enumerate(wrap(d, text, plain(9.5), slot_w - 8)[:2]):
            d.text((x, y0 + 15 + j * 11), line, font=plain(9.5), fill=INK)

def number_badge(d, cx, cy, n, col):
    r = 11
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(255, 255, 255), width=2)
    d.text((cx, cy - 7), str(n), font=bold(11), fill=(255, 255, 255), anchor="ma")

def draw_leads(img, d):
    y0, y1 = 182, 460
    gap = 8
    cw = (W - 2 * MARGIN - 2 * gap) // 3
    for i, (region, city, head, summary, source, art) in enumerate(LEADS):
        x0 = MARGIN + i * (cw + gap)
        x1 = x0 + cw
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=1)
        paste_cover(img, os.path.join(HERE, art), (x0 + 1, y0 + 1, x1 - 1, y0 + 142))
        d = ImageDraw.Draw(img)
        number_badge(d, x1 - 18, y0 + 124, i + 1, REGION_COLORS[region])
        ty = y0 + 148
        d.text((x0 + 10, ty), region, font=bold(10), fill=REGION_COLORS[region])
        rw = d.textlength(region, font=bold(10))
        d.text((x0 + 14 + rw, ty), f"- {city}", font=bold(10), fill=GREY)
        ty += 15
        for line in wrap(d, head, serif(21), cw - 20)[:3]:
            d.text((x0 + 10, ty), line, font=serif(21), fill=INK)
            ty += 25
        ty += 2
        for line in wrap(d, summary, plain(11), cw - 20)[:3]:
            d.text((x0 + 10, ty), line, font=plain(11), fill=(52, 48, 40))
            ty += 14.5
        d.text((x0 + 10, y1 - 16), source, font=bold(8.5), fill=GREY)

def draw_cards(img, d):
    gap = 8
    cw = (W - 2 * MARGIN - 3 * gap) // 4
    ch = 154
    for idx, (region, city, head, summary, source, art) in enumerate(CARDS):
        row, col = divmod(idx, 4)
        x0 = MARGIN + col * (cw + gap)
        y0 = 468 + row * (ch + 8)
        x1, y1 = x0 + cw, y0 + ch
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=1)
        paste_cover(img, os.path.join(HERE, art), (x0 + 1, y0 + 1, x1 - 1, y0 + 66))
        d = ImageDraw.Draw(img)
        number_badge(d, x1 - 15, y0 + 52, idx + 4, REGION_COLORS[region])
        ty = y0 + 70
        d.text((x0 + 8, ty), region, font=bold(8), fill=REGION_COLORS[region])
        rw = d.textlength(region, font=bold(8))
        d.text((x0 + 11 + rw, ty), f"- {city}", font=bold(8), fill=GREY)
        ty += 11
        for line in wrap(d, head, serif(14), cw - 16)[:2]:
            d.text((x0 + 8, ty), line, font=serif(14), fill=INK)
            ty += 16.5
        for line in wrap(d, summary, plain(8.5), cw - 16)[:2]:
            d.text((x0 + 8, ty), line, font=plain(8.5), fill=(52, 48, 40))
            ty += 10.5
        d.text((x0 + 8, y1 - 12), source, font=bold(7.5), fill=GREY)

def draw_bottom(d):
    y0 = 792
    d.text((MARGIN, y0), "WHERE IT HAPPENED", font=bold(11), fill=NAVY)
    mx0, my0 = MARGIN, y0 + 18
    mw, mh = 372, 118
    cell_w, cell_h = mw / 100, mh / 30
    for ry, segs in LAND_SEGMENTS.items():
        for x0s, x1s in segs:
            for gx in range(x0s, x1s + 1):
                cx, cy = mx0 + gx * cell_w, my0 + ry * cell_h
                d.ellipse([cx, cy, cx + 2.2, cy + 2.2], fill=(168, 158, 132))
    stories = LEADS + CARDS
    for i, (px, py) in enumerate(PINS):
        cx, cy = mx0 + px * cell_w, my0 + py * cell_h
        col = REGION_COLORS[stories[i][0]]
        r = 8
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(255, 255, 255), width=1)
        d.text((cx, cy - 6), str(i + 1), font=bold(9.5), fill=(255, 255, 255), anchor="ma")
    d.text((MARGIN, my0 + mh + 6),
           "ASIA 7 - EUROPE 6 - AMERICAS 4 - MID EAST 2 - AFRICA 4 - OCEANIA 2 - GLOBAL 5",
           font=bold(8.5), fill=GREY)
    bx = 428
    d.text((bx, y0), "ALSO ON THURSDAY 26 NOVEMBER", font=bold(11), fill=NAVY)
    col_w = (W - MARGIN - bx) / 3
    for i, (place, text) in enumerate(BRIEFS):
        col, row = divmod(i, 7)
        x = bx + col * col_w
        y = y0 + 19 + row * 22.5
        d.text((x, y), str(i + 12), font=bold(9.5), fill=RED)
        lines = wrap(d, f"{place}: {text}", plain(8.5), col_w - 26)
        for j, line in enumerate(lines[:2]):
            d.text((x + 20, y + j * 10.5), line, font=plain(8.5), fill=INK)

def draw_footer(d):
    d.rectangle([MARGIN, 966, W - MARGIN, 990], fill=RED)
    d.text((MARGIN + 10, 970),
           "DATE CHECK - Every story here happened, or was first reported, on Thursday 26 November 2026.",
           font=bold(9), fill=(255, 246, 235))
    d.text((MARGIN + 10, 981),
           "Thursday was still young when this page closed; developing stories are framed as reports, and claims are attributed.",
           font=plain(8.5), fill=(255, 226, 214))
    d.text((MARGIN, 996),
           "Sources: Reuters - AP - BBC - WSJ - CNN - ABC - NASA - Kyodo - Hromadske - EUtoday - EuropeSays",
           font=plain(9), fill=GREY)
    d.text((W - MARGIN, 996), "THE WORLD IN ONE DAY - p.1 of 1", font=plain(9),
           fill=GREY, anchor="ra")

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_band(d)
    draw_utc(d)
    draw_leads(img, d)
    d = ImageDraw.Draw(img)
    draw_cards(img, d)
    d = ImageDraw.Draw(img)
    draw_bottom(d)
    draw_footer(d)
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")

if __name__ == "__main__":
    main()
