#!/usr/bin/env python3
"""Compose the one-page newspaper for news-image-20261126.

"The World in One Day — Thursday 26 November 2026": a single 1024x1024
page carrying 30 verified stories from 7 regions — 3 illustrated leads,
8 row cards, a dot-matrix world map with numbered pins, and 19 one-line
briefs. Every story happened, or was first reported, on 26 November 2026
in some time zone, and is credited to the outlet that reported it.
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
MARGIN = 28

INK = (26, 26, 32)
PAPER = (247, 243, 234)
NAVY = (16, 34, 64)
CARD = (255, 254, 249)
GREY = (96, 96, 102)
RULE = (178, 170, 152)
STRIP = (239, 233, 218)

REGION_COLORS = {
    "ASIA": (176, 58, 46),
    "EUROPE": (46, 111, 167),
    "AMERICAS": (39, 134, 74),
    "MIDDLE EAST": (166, 137, 0),
    "AFRICA": (141, 85, 36),
    "OCEANIA": (108, 52, 131),
    "GLOBAL": (84, 84, 90),
}
REGION_ORDER = ["ASIA", "EUROPE", "AMERICAS", "MIDDLE EAST", "AFRICA", "OCEANIA", "GLOBAL"]

# --- the 30 stories -------------------------------------------------------
# leads: (region, headline, city, summary, source, illustration file)
LEADS = [
    ("AMERICAS",
     "US PROPOSES NEW TARIFFS ON 14 PARTNERS",
     "Washington",
     "Duties of 20 to 40 percent are proposed on 14 trading partners "
     "after an eight-month probe into excess factory capacity. China "
     "faces a 20 percent levy on top of existing duties.",
     "Reuters", "illo-tariffs.png"),
    ("ASIA",
     "ASIAN MARKETS PLUNGE AS AI DOUBTS BITE",
     "Seoul",
     "The AI selloff spreads: South Korea's KOSPI plunges 6.16 percent "
     "to a ten-month low, the Nikkei falls 2.8 percent, Taiwan's Taiex "
     "4.8 percent. SoftBank dives 14.8 percent.",
     "WSJ / Reuters", "illo-plunge.png"),
    ("EUROPE",
     "UKRAINE STRIKES RUSSIAN AIR BASE, FIVE JETS HIT",
     "Nizhny Novgorod",
     "Kyiv says its forces struck the Savasleyka air base east of "
     "Moscow, putting three MiG-31 jets and two Su-34 fighter-bombers "
     "out of action in one strike.",
     "Reuters", "illo-airbase.png"),
]

# rows: (region, headline, city, summary, source)
ROWS = [
    ("OCEANIA",
     "SOLOMONS DITCH CHINA PACT FOR AUSTRALIA TREATY",
     "Canberra",
     "A$740 million deal makes Australia the Solomons' primary security "
     "partner, with a pledge of no foreign military base.",
     "Reuters / AP"),
    ("ASIA",
     "SHANGHAI PARTY CHIEF FALLS IN XI'S GRAFT PURGE",
     "Shanghai",
     "Politburo member Chen Jining, 62, is placed under investigation — "
     "the fourth sitting member to fall since 2025.",
     "Reuters"),
    ("AMERICAS",
     "US ECONOMY GREW 4.3%, FASTEST IN THREE YEARS",
     "Washington",
     "Third-quarter GDP is revised up from 3.4 percent; equipment "
     "spending surges 21.8 percent on the AI build-out.",
     "Reuters"),
    ("MIDDLE EAST",
     "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
     "Gaza City",
     "Naeem Abu Nahel, two months into the post, is killed; seven "
     "Palestinians are reported dead in Tuesday's strikes.",
     "BBC"),
    ("AFRICA",
     "TANKER FIRE KILLS 31 ON CAIRO RING ROAD",
     "Giza",
     "An overturned fuel tanker burns above Tunnel 10 in Al-Warraq; "
     "27 vehicles are charred and 21 people injured.",
     "Reuters / AP"),
    ("EUROPE",
     "EU FINES FRAGRANCE GIANTS 471.9 MILLION EUROS",
     "Brussels",
     "Firmenich, Givaudan and International Flavors & Fragrances are "
     "fined a combined 471.9 million euros over a cartel.",
     "Reuters"),
    ("ASIA",
     "BANGLADESH GARMENT WAGE UP 36% AFTER CLASHES",
     "Dhaka",
     "The minimum wage rises to 17,000 taka after 12 hours of talks; "
     "workers who demanded 30,000 blocked highways in Gazipur.",
     "Reuters / AP"),
    ("ASIA",
     "CANDY FACTORY FIRE TOLL REACHES 26 IN INDONESIA",
     "Serang",
     "More than 600 rescuers search the gutted Milkita sweets plant; "
     "police open a criminal negligence probe.",
     "AP"),
]

# briefs: (region, city, one-line text, source)
BRIEFS = [
    ("EUROPE", "Samara", "145 drones downed as Ukraine hits the oil region; one person killed", "Reuters"),
    ("EUROPE", "Brussels", "EU leaders clash over the 1.78 trillion euro budget at summit", "EUtoday"),
    ("EUROPE", "Warsaw", "Poland plans a no-fly zone along its eastern border", "Hromadske"),
    ("EUROPE", "Moscow", "Kremlin rejects Johnson's call for a Western force in Ukraine", "Reuters"),
    ("MIDDLE EAST", "Jerusalem", "Judges urge dropping the Netanyahu bribery case, Case 4000", "Reuters"),
    ("AFRICA", "Damazin", "RSF drones kill 19 civilians in Sudan's Blue Nile state", "Reuters"),
    ("AFRICA", "Lausanne", "Court restores Senegal as AFCON champions over Morocco", "AP"),
    ("AFRICA", "Cape Town", "High Court scraps the panel report against Ramaphosa", "EuropeSays"),
    ("ASIA", "Taipei", "Taiwan confident its 15% US tariff holds despite new salvo", "Reuters"),
    ("ASIA", "Bogor", "Nine dead and 17 trapped in a flooded illegal gold mine at Pongkor", "AP"),
    ("ASIA", "Tokyo", "Takaichi defends the ICC, defying US sanctions on the court", "Kyodo"),
    ("OCEANIA", "Canberra", "Australia on track to hit its 2030 climate target, government says", "ABC"),
    ("AMERICAS", "New York", "Dow erases a 1,100-point plunge; Bitcoin slips below $58,000", "CNN"),
    ("AMERICAS", "Caracas", "Venezuela reveals a $237.5 billion debt pile — 242% of GDP", "Reuters"),
    ("GLOBAL", "Redmond", "Microsoft declares 'Code Red' after a 24-hour worldwide outage", "Reuters"),
    ("GLOBAL", "San Francisco", "Anthropic slips below its IPO price days after listing", "Reuters"),
    ("GLOBAL", "Washington", "PCE inflation ticks up to 3.8%, a full point above the Fed's target", "CNN"),
    ("GLOBAL", "Raleigh", "Thanksgiving airfares hit a 10-year high after FAA chaos", "Reuters"),
    ("GLOBAL", "Baikonur", "Progress 97 cargo ship docks at the space station", "NASA"),
]

# The day in UTC — only clock times verified from the reports are printed.
MOMENTS = [
    ("00:00", "Asian markets open into the rout"),
    ("12:11", "Progress 97 docks at the station"),
    ("BRUSSELS", "EU summit opens split on budget"),
    ("US", "Thanksgiving travel peaks"),
]

REGION_COUNTS = {}
for _r in [x[0] for x in LEADS] + [x[0] for x in ROWS] + [x[0] for x in BRIEFS]:
    REGION_COUNTS[_r] = REGION_COUNTS.get(_r, 0) + 1

# Dot-matrix world map, 100 x 30, built from land segments per row so the
# continents stay recognisable: {row: [(x_start, x_end), ...]}, north first.
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
LAND = []
for _ry in range(30):
    _cells = [" "] * 100
    for _x0, _x1 in LAND_SEGMENTS.get(_ry, []):
        for _x in range(_x0, _x1 + 1):
            _cells[_x] = "#"
    LAND.append("".join(_cells))

# pin positions (grid x, y) for the 11 drawn stories, in story order
PINS = [
    (24, 8),   # 1 Washington — tariffs
    (83, 7),   # 2 Seoul — markets plunge
    (58, 4),   # 3 Nizhny Novgorod — air base
    (86, 19),  # 4 Canberra — Solomons treaty
    (80, 8),   # 5 Shanghai — graft purge
    (21, 9),   # 6 Washington — GDP (offset from pin 1)
    (55, 9),   # 7 Gaza City — Hamas chief
    (52, 10),  # 8 Giza — tanker fire
    (46, 5),   # 9 Brussels — fragrance fine
    (71, 10),  # 10 Dhaka — garment wage
    (78, 14),  # 11 Serang — factory fire
]

# --- fonts -----------------------------------------------------------------
_FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(_FONT_DIR, name), size)

def serif(size):
    return font("DejaVuSerif-Bold.ttf", size)

def bold(size):
    return font("DejaVuSans-Bold.ttf", size)

def plain(size):
    return font("DejaVuSans.ttf", size)

def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def fit(draw, text, fnt, width):
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "...", font=fnt) > width:
        text = text[:-1]
    return text.rstrip() + "..."

# --- drawing ---------------------------------------------------------------
def draw_masthead(d):
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((MARGIN, 18), "THE DAY IN FULL", font=serif(52), fill=(250, 248, 240))
    d.text((MARGIN, 80), "THE WORLD IN ONE DAY — ONE PAGE, THIRTY VERIFIED STORIES",
           font=bold(13), fill=(196, 208, 230))
    # date badge
    bx0, by0, bx1, by1 = W - MARGIN - 252, 14, W - MARGIN, 94
    d.rectangle([bx0, by0, bx1, by1], outline=(250, 248, 240), width=2)
    d.text(((bx0 + bx1) / 2, by0 + 8), "THURSDAY", font=bold(15),
           fill=(250, 248, 240), anchor="ma")
    d.text(((bx0 + bx1) / 2, by0 + 32), "26 NOVEMBER 2026", font=serif(19),
           fill=(250, 248, 240), anchor="ma")
    d.text(((bx0 + bx1) / 2, by0 + 58), "30 STORIES · 7 REGIONS", font=bold(11),
           fill=(196, 208, 230), anchor="ma")

BAND_LABELS = {"MIDDLE EAST": "M. EAST"}

def draw_region_band(d):
    y0, y1 = 108, 136
    total = sum(REGION_COUNTS[r] for r in REGION_ORDER)
    x = 0
    for r in REGION_ORDER:
        wseg = round(W * REGION_COUNTS[r] / total)
        d.rectangle([x, y0, x + wseg, y1], fill=REGION_COLORS[r])
        label = f"{BAND_LABELS.get(r, r)} {REGION_COUNTS[r]}"
        fnt = bold(12) if wseg >= 110 else bold(10)
        d.text((x + wseg / 2, y0 + 8), label, font=fnt,
               fill=(255, 255, 255), anchor="ma")
        x += wseg

def draw_moments(d):
    y0, y1 = 136, 172
    d.rectangle([0, y0, W, y1], fill=STRIP)
    d.line([0, y1, W, y1], fill=RULE, width=1)
    d.text((MARGIN, y0 + 11), "THE DAY IN UTC", font=bold(12), fill=NAVY)
    x = MARGIN + 128
    for when, what in MOMENTS:
        label = f"{when}  {what}"
        if x + d.textlength(label, font=plain(11)) > W - MARGIN:
            break
        d.text((x, y0 + 12), label, font=plain(11), fill=INK)
        x += d.textlength(label, font=plain(11)) + 24
        d.text((x - 18, y0 + 12), "·", font=bold(11), fill=GREY)

def paste_cover(img, path, box):
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    art = Image.open(path).convert("RGB")
    scale = max(tw / art.width, th / art.height)
    art = art.resize((round(art.width * scale), round(art.height * scale)))
    left = (art.width - tw) // 2
    top = (art.height - th) // 2
    img.paste(art.crop((left, top, left + tw, top + th)), (x0, y0))

def draw_leads(img, d):
    y0, y1 = 182, 500
    gap = 8
    cw = (W - 2 * MARGIN - 2 * gap) // 3
    for i, (region, head, city, summary, source, illo) in enumerate(LEADS):
        x0 = MARGIN + i * (cw + gap)
        x1 = x0 + cw
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=1)
        paste_cover(img, os.path.join(HERE, "assets", illo), (x0 + 1, y0 + 1, x1 - 1, y0 + 150))
        d.rectangle([x0 + 10, y0 + 158, x0 + 10 + d.textlength(region, font=bold(11)) + 14, y0 + 178],
                    fill=REGION_COLORS[region])
        d.text((x0 + 17, y0 + 162), region, font=bold(11), fill=(255, 255, 255))
        d.text((x1 - 12, y0 + 162), f"No. {i + 1}", font=bold(11), fill=GREY, anchor="ra")
        ty = y0 + 184
        for line in wrap(d, head, bold(15), cw - 20)[:2]:
            d.text((x0 + 10, ty), line, font=bold(15), fill=INK)
            ty += 19
        ty += 3
        body = f"{city} — {summary}"
        for line in wrap(d, body, plain(11), cw - 20)[:5]:
            d.text((x0 + 10, ty), line, font=plain(11), fill=(52, 52, 58))
            ty += 14
        d.text((x0 + 10, y1 - 18), f"Source: {source}", font=plain(10), fill=GREY)

def draw_rows(d):
    x0, x1 = MARGIN, 640
    y = 508
    rh = 31
    for i, (region, head, city, summary, source) in enumerate(ROWS):
        n = i + 4
        d.rectangle([x0, y, x1, y + rh - 2], fill=CARD, outline=RULE, width=1)
        d.rectangle([x0, y, x0 + 30, y + rh - 2], fill=REGION_COLORS[region])
        d.text((x0 + 15, y + 8), str(n), font=bold(13), fill=(255, 255, 255), anchor="ma")
        d.text((x0 + 40, y + 3), fit(d, head, bold(12), x1 - x0 - 52), font=bold(12), fill=INK)
        line2 = fit(d, f"{city} — {summary} ({source})", plain(10), x1 - x0 - 52)
        d.text((x0 + 40, y + 18), line2, font=plain(10), fill=GREY)
        y += rh

def draw_map(d):
    x0, y0, x1, y1 = 652, 508, W - MARGIN, 756
    d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=1)
    d.text((x0 + 12, y0 + 8), "WHERE IT HAPPENED", font=bold(12), fill=NAVY)
    gx, gy = x0 + 8, y0 + 32
    cell = (x1 - x0 - 16) / 100
    vstep = 5.9
    dot = max(1, round(cell * 0.42))
    for ry, row in enumerate(LAND):
        for rx, ch in enumerate(row):
            if ch == "#":
                cx, cy = gx + rx * cell, gy + ry * vstep
                d.ellipse([cx, cy, cx + dot, cy + dot], fill=(168, 160, 140))
    for i, (px, py) in enumerate(PINS):
        cx, cy = gx + px * cell, gy + py * vstep
        col = REGION_COLORS[(LEADS + ROWS)[i][0]]
        r = 8
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(255, 255, 255), width=1)
        d.text((cx, cy - 6), str(i + 1), font=bold(10), fill=(255, 255, 255), anchor="ma")
    ly = y1 - 40
    d.text((x0 + 12, ly), "Numbered pins: the 11 drawn stories.", font=plain(11), fill=GREY)
    d.text((x0 + 12, ly + 16), "The 19 briefs below span the same map.", font=plain(11), fill=GREY)

def draw_briefs(d):
    y0 = 764
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + 24], fill=NAVY)
    d.text((MARGIN + 10, y0 + 5), "ALSO TODAY — 19 BRIEFS IN ONE LINE EACH",
           font=bold(12), fill=(250, 248, 240))
    col_w = (W - 2 * MARGIN - 24) // 2
    cols = [BRIEFS[:10], BRIEFS[10:]]
    for ci, col in enumerate(cols):
        x = MARGIN + ci * (col_w + 24)
        y = y0 + 32
        for region, city, text, source in col:
            d.rectangle([x, y + 3, x + 8, y + 11], fill=REGION_COLORS[region])
            line = fit(d, f"{city} — {text} ({source})", plain(10), col_w - 16)
            d.text((x + 16, y + 1), line, font=plain(10), fill=INK)
            y += 16

def draw_footer(d):
    y0 = 962
    d.line([MARGIN, y0, W - MARGIN, y0], fill=RULE, width=1)
    d.text((MARGIN, y0 + 8),
           "DATE CHECK — every story on this page happened, or was first reported, on Thursday 26 November 2026 in some time zone,",
           font=plain(11), fill=GREY)
    d.text((MARGIN, y0 + 24),
           "and each is credited to the outlet that reported it. Nothing here is invented; developing stories may move after this page was set.",
           font=plain(11), fill=GREY)
    d.text((MARGIN, y0 + 42),
           "Sources: Reuters · AP · BBC · WSJ · CNN · ABC · NASA · Kyodo · Hromadske · EUtoday · EuropeSays",
           font=bold(11), fill=NAVY)
    d.text((W - MARGIN, y0 + 42), "THE DAY IN FULL · p.1 of 1", font=plain(11),
           fill=GREY, anchor="ra")

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_region_band(d)
    draw_moments(d)
    draw_leads(img, d)
    d = ImageDraw.Draw(img)
    draw_rows(d)
    draw_map(d)
    draw_briefs(d)
    draw_footer(d)
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")

if __name__ == "__main__":
    main()
