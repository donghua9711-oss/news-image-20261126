#!/usr/bin/env python3
"""Compose the one-page newspaper for news-image-20261126 — REVISION 2.

"The World in One Day — Thursday 26 November 2026": a single 1024x1024
cream-paper page in the classic broadsheet manner, carrying 36 verified
stories from 9 regions — 3 drawn lead scenes, 10 row cards, a BY THE
NUMBERS strip, a dot-matrix world map with numbered pins, 23 one-line
briefs, a status label on every drawn story and a DATE CHECK box naming
what was left out for not being 26 November news. Every story happened,
or was first reported, on 26 November 2026 in some time zone, and is
credited to the outlet that reported it. All scenes are drawn, not
photographed.
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
MARGIN = 28

INK = (24, 22, 18)
PAPER = (247, 241, 227)
CARD = (253, 250, 240)
GREY = (96, 90, 78)
RULE = (172, 160, 138)
RED = (168, 32, 26)
NAVY = (18, 32, 58)
STRIP = (240, 233, 214)
BLACK = (16, 15, 13)

REGION_COLORS = {
    "NORTH AMERICA": (39, 110, 74),
    "SOUTH AMERICA": (64, 145, 108),
    "EUROPE": (46, 111, 167),
    "MIDDLE EAST": (166, 124, 0),
    "AFRICA": (141, 85, 36),
    "SOUTH ASIA": (176, 58, 46),
    "EAST ASIA": (192, 84, 40),
    "OCEANIA": (108, 52, 131),
    "WORLD": (84, 84, 90),
}
REGION_ORDER = ["NORTH AMERICA", "SOUTH AMERICA", "EUROPE", "MIDDLE EAST",
                "AFRICA", "SOUTH ASIA", "EAST ASIA", "OCEANIA", "WORLD"]
BAND_LABELS = {"NORTH AMERICA": "N. AMERICA", "SOUTH AMERICA": "S. AMERICA",
               "MIDDLE EAST": "M. EAST", "SOUTH ASIA": "S. ASIA",
               "EAST ASIA": "E. ASIA"}

# --- the 36 stories ---------------------------------------------------------
# leads: (region, headline, city, summary, source, status, scene)
LEADS = [
    ("NORTH AMERICA",
     "MACY'S 100TH PARADE POSTPONED BY THE STORM",
     "New York",
     "A nor'easter packing gusts of 60 mph forces the first weather "
     "postponement in the parade's 100 years. The balloons are deflated "
     "overnight and the march moves to Saturday.",
     "AP / Reuters", "CONFIRMED", "parade"),
    ("SOUTH ASIA",
     "INDIA MARKS 18 YEARS SINCE THE 26/11 ATTACKS",
     "Mumbai",
     "Candles and tributes remember the 166 people killed in the 2008 "
     "attacks on the city, on a day India also marks as Constitution Day.",
     "PTI", "OFFICIAL", "mumbai"),
    ("WORLD",
     "GUKESH MEETS SINDAROV IN GAME 3 OF THE TITLE MATCH",
     "Geneva",
     "The youngest world title match ever played stands at 1-1 after two "
     "draws. Sindarov has White in Game 3, the last before the rest day.",
     "FIDE", "ONGOING", "chess"),
]

# rows: (region, headline, city, summary, source, status)
ROWS = [
    ("EUROPE",
     "EU LEADERS MEET ON BUDGET AND UKRAINE AID",
     "Brussels",
     "The summit weighs a long-term budget of up to 2 trillion euros and "
     "a 145 billion euro loan to keep Kyiv funded through 2027.",
     "Reuters", "OFFICIAL"),
    ("MIDDLE EAST",
     "HOUTHIS STRIKE SAUDI PORT AND REFINERY",
     "Jizan",
     "Missiles hit Jizan port and damage the refinery at Ras Tanura as "
     "Red Sea tensions flare again; no casualties are reported.",
     "Reuters", "REPORTED"),
    ("EUROPE",
     "RUSSIAN MISSILES HIT KYIV, SEVEN WOUNDED",
     "Kyiv",
     "Ballistic missiles strike the capital overnight, and Russian "
     "forces also hit grain ships near Odesa.",
     "Reuters", "REPORTED"),
    ("EAST ASIA",
     "ASIAN MARKETS PLUNGE AS AI DOUBTS BITE",
     "Seoul",
     "The KOSPI plunges 6.16 percent to a ten-month low; the Nikkei "
     "falls 2.8 percent, Taiwan's Taiex 4.8 percent, SoftBank 14.8 percent.",
     "WSJ / Reuters", "CONFIRMED"),
    ("NORTH AMERICA",
     "US TARIFF PLAN DRAWS FIRE FROM 14 PARTNERS",
     "Washington",
     "Duties of up to 25 percent are proposed on Indian goods as "
     "lawmakers condemn the plan aimed at 14 mostly Asian economies.",
     "Reuters", "OFFICIAL"),
    ("AFRICA",
     "TANKER FIRE KILLS 31 ON CAIRO RING ROAD",
     "Giza",
     "An overturned fuel tanker burns above the Ashara Tunnel in "
     "Al-Warraq; 27 vehicles are charred and 21 people injured.",
     "Reuters / AP", "CONFIRMED"),
    ("SOUTH ASIA",
     "BANGLADESH GARMENT WAGE UP 36% AFTER CLASHES",
     "Dhaka",
     "The minimum wage rises to 17,000 taka after 12 hours of talks; "
     "workers who demanded 30,000 had blocked highways in Gazipur.",
     "Reuters / AP", "CONFIRMED"),
    ("EAST ASIA",
     "SHANGHAI PARTY CHIEF FALLS IN GRAFT PURGE",
     "Shanghai",
     "Politburo member Chen Jining is placed under investigation - the "
     "fourth sitting member to fall since 2025.",
     "Reuters", "REPORTED"),
    ("OCEANIA",
     "SOLOMONS SIGN SECURITY PACT WITH AUSTRALIA",
     "Canberra",
     "A$740 million deal makes Australia the Solomons' primary security "
     "partner, with a pledge of no foreign military base.",
     "Reuters / AP", "OFFICIAL"),
    ("NORTH AMERICA",
     "US ECONOMY GREW 4.3%, FASTEST IN THREE YEARS",
     "Washington",
     "Third-quarter GDP is revised up from 3.4 percent; equipment "
     "spending surges 21.8 percent on the AI build-out.",
     "Reuters", "OFFICIAL"),
]

# briefs: (region, city, one-line text, source)
BRIEFS = [
    ("MIDDLE EAST", "Gaza", "Israeli strikes kill nine, incl. the Hamas-appointed deputy education minister", "Reuters"),
    ("MIDDLE EAST", "Jerusalem", "Judges urge dropping the Netanyahu bribery case, Case 4000", "Reuters"),
    ("AFRICA", "Kinshasa", "DR Congo Ebola cases pass 12,000 in the country's worst outbreak", "Reuters"),
    ("NORTH AMERICA", "Washington", "FCC approves SpaceX plan for up to one million satellites", "FCC"),
    ("EAST ASIA", "Tokyo", "Takaichi defends the ICC, defying US sanctions on the court", "Kyodo"),
    ("SOUTH ASIA", "New Delhi", "India marks Constitution Day, 76 years since the charter's adoption", "PTI"),
    ("AFRICA", "Cape Town", "Court scraps the report behind the Ramaphosa impeachment push", "EuropeSays"),
    ("AFRICA", "Lausanne", "Court restores Senegal as AFCON champions over Morocco", "AP"),
    ("AFRICA", "Damazin", "RSF drones kill 19 civilians in Sudan's Blue Nile state", "Reuters"),
    ("EUROPE", "Warsaw", "Poland plans a no-fly zone along its eastern border", "Hromadske"),
    ("EUROPE", "Brussels", "EU fines fragrance giants a combined 471.9 million euros over a cartel", "Reuters"),
    ("EAST ASIA", "Pyongyang", "Kim calls tactical nuclear deployment an urgent task", "KCNA"),
    ("EAST ASIA", "Taipei", "Taiwan confident its 15% US tariff holds despite the new salvo", "Reuters"),
    ("SOUTH AMERICA", "Caracas", "Venezuela reveals a $237.5 billion debt pile - 242% of GDP", "Reuters"),
    ("NORTH AMERICA", "Redmond", "Microsoft declares 'Code Red' after a 24-hour worldwide outage", "Reuters"),
    ("NORTH AMERICA", "San Francisco", "Anthropic slips below its IPO price days after listing", "Reuters"),
    ("NORTH AMERICA", "Washington", "PCE inflation ticks up to 3.8%, a point above the Fed's target", "CNN"),
    ("OCEANIA", "Canberra", "Australia on track to hit its 2030 climate target, government says", "ABC"),
    ("SOUTH ASIA", "Serang", "Candy factory fire toll reaches 26; a negligence probe opens", "AP"),
    ("SOUTH ASIA", "Bogor", "Nine dead and 17 trapped in a flooded illegal gold mine at Pongkor", "AP"),
    ("WORLD", "Baikonur", "Progress 97 cargo ship docks at the space station", "NASA"),
    ("WORLD", "New York", "Dow erases a 1,100-point plunge; Bitcoin slips below $58,000", "CNN"),
    ("EUROPE", "Samara", "145 drones downed as Ukraine hits the oil region; one person killed", "Reuters"),
]

NUMBERS = [
    ("100", "parade years - first storm delay"),
    ("166", "26/11 victims remembered"),
    ("31", "dead in Cairo tanker fire"),
    ("12,000", "Ebola cases in DR Congo"),
    ("14", "US tariff-plan partners"),
    ("471.9M", "euros of EU fragrance fines"),
]

# The day in UTC - clock times verified from the reports.
MOMENTS = [
    ("00:00", "Thanksgiving in the US"),
    ("05:00", "Constitution Day, India"),
    ("09:00", "EU summit, Brussels"),
    ("12:11", "Progress 97 docks"),
    ("14:00", "Chess Game 3, Geneva"),
]

DATE_CHECK = [
    "COP31 ends without a pact - 22 NOV",
    "Real Madrid 5-1 PSV - 24 NOV",
    "Shenzhen-24 docks at Tiangong - 25 NOV",
]

ALL_STORIES = LEADS + ROWS + BRIEFS
REGION_COUNTS = {}
for _s in ALL_STORIES:
    REGION_COUNTS[_s[0]] = REGION_COUNTS.get(_s[0], 0) + 1
SOURCES = set()
for _s in LEADS + ROWS:
    for _o in _s[4].split("/"):
        SOURCES.add(_o.strip())
for _s in BRIEFS:
    SOURCES.add(_s[3].strip())

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

# pin positions (grid x, y) for the 13 drawn stories, in story order
PINS = [
    (23, 8),   # 1 New York - parade
    (68, 11),  # 2 Mumbai - 26/11 anniversary
    (46, 4),   # 3 Geneva - chess Game 3
    (45, 6),   # 4 Brussels - EU summit
    (56, 10),  # 5 Jizan - Houthi strike
    (52, 4),   # 6 Kyiv - missiles
    (84, 7),   # 7 Seoul - markets plunge
    (21, 9),   # 8 Washington - tariff plan
    (51, 11),  # 9 Giza - tanker fire
    (71, 10),  # 10 Dhaka - garment wage
    (81, 8),   # 11 Shanghai - graft purge
    (87, 19),  # 12 Canberra - Solomons pact
    (24, 10),  # 13 Washington - GDP
]

# --- fonts -------------------------------------------------------------------
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

# --- drawn lead scenes (flat illustration, drawn not photographed) -----------
def scene_parade(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(74, 88, 112))  # storm-dusk sky
    # skyline
    for bx, bw, bh in [(0, 34, 62), (38, 26, 84), (68, 40, 55), (112, 30, 92),
                       (146, 36, 66), (186, 28, 80), (218, 42, 58), (264, 30, 74)]:
        d.rectangle([x0 + bx, y1 - 34 - bh, x0 + bx + bw, y1 - 34], fill=(38, 44, 58))
        for wy in range(y1 - 34 - bh + 8, y1 - 42, 12):
            for wx in range(x0 + bx + 5, x0 + bx + bw - 6, 9):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(240, 200, 90))
    d.rectangle([x0, y1 - 34, x1, y1], fill=(52, 50, 48))  # street
    # three parade balloons, tethered low against the wind
    for cx, cy, r, col in [(70, 52, 30, (216, 84, 60)), (160, 40, 36, (232, 178, 60)),
                           (248, 54, 28, (96, 150, 205))]:
        d.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r], fill=col)
        d.ellipse([x0 + cx - r // 3, y0 + cy - r // 2, x0 + cx, y0 + cy - r // 6],
                  fill=(255, 255, 255))
        d.line([x0 + cx - 8, y0 + cy + r, x0 + cx - 3, y1 - 36], fill=(230, 225, 210), width=1)
        d.line([x0 + cx + 8, y0 + cy + r, x0 + cx + 3, y1 - 36], fill=(230, 225, 210), width=1)
    # red postponement banner
    d.rectangle([x0, y1 - 30, x1, y1], fill=RED)
    d.text(((x0 + x1) / 2, y1 - 21), "POSTPONED TO SATURDAY", font=bold(13),
           fill=(255, 246, 235), anchor="ma")

def scene_mumbai(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(24, 30, 52))  # night
    cx = (x0 + x1) / 2
    # Gateway of India silhouette: base, columns, great arch, dome
    d.rectangle([cx - 62, y1 - 66, cx + 62, y1 - 30], fill=(196, 164, 96))
    d.rectangle([cx - 52, y1 - 92, cx + 52, y1 - 66], fill=(206, 176, 106))
    d.pieslice([cx - 26, y1 - 122, cx + 26, y1 - 70], 180, 360, fill=(216, 186, 116))
    d.rectangle([cx - 14, y1 - 84, cx + 14, y1 - 30], fill=(24, 30, 52))
    d.pieslice([cx - 14, y1 - 96, cx + 14, y1 - 72], 180, 360, fill=(24, 30, 52))
    d.rectangle([x0, y1 - 30, x1, y1], fill=(14, 18, 32))  # plaza
    # rows of memorial candles
    for i in range(18):
        fx = x0 + 18 + i * 16
        for fy, s in [(y1 - 22, 1), (y1 - 12, 1)]:
            d.ellipse([fx - 2, fy - 7 * s, fx + 2, fy - 2 * s], fill=(255, 176, 66))
            d.rectangle([fx - 1, fy - 2 * s, fx + 1, fy], fill=(240, 230, 205))
    # gold badge
    d.ellipse([x1 - 76, y0 + 10, x1 - 14, y0 + 72], fill=(216, 176, 80),
              outline=(255, 246, 220), width=2)
    d.text((x1 - 45, y0 + 24), "18", font=serif(24), fill=(40, 30, 8), anchor="ma")
    d.text((x1 - 45, y0 + 52), "YEARS", font=bold(9), fill=(40, 30, 8), anchor="ma")

def scene_chess(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(43, 34, 26))
    # the board, flat, filling most of the scene
    bx0, by0 = x0 + 26, y0 + 12
    sq = 15
    for r in range(8):
        for c in range(8):
            col = (238, 226, 198) if (r + c) % 2 == 0 else (146, 102, 62)
            d.rectangle([bx0 + c * sq, by0 + r * sq, bx0 + (c + 1) * sq, by0 + (r + 1) * sq],
                        fill=col)
    d.rectangle([bx0, by0, bx0 + 8 * sq, by0 + 8 * sq], outline=(20, 14, 8), width=2)
    # two kings facing off at the centre
    def king(kx, ky, body, trim):
        d.polygon([(kx - 15, ky + 34), (kx - 11, ky - 8), (kx - 5, ky + 5),
                   (kx, ky - 16), (kx + 5, ky + 5), (kx + 11, ky - 8),
                   (kx + 15, ky + 34)], fill=body, outline=trim)
        d.rectangle([kx - 17, ky + 34, kx + 17, ky + 40], fill=body, outline=trim)
        d.line([kx, ky - 28, kx, ky - 17], fill=trim, width=3)
        d.line([kx - 5, ky - 23, kx + 5, ky - 23], fill=trim, width=3)
    king(bx0 + 45, by0 + 42, (240, 236, 224), (60, 50, 40))
    king(bx0 + 82, by0 + 42, (30, 26, 22), (200, 180, 140))
    # a few pawns
    for px, py, col in [(18, 96, (240, 236, 224)), (108, 96, (30, 26, 22)), (63, 104, (240, 236, 224))]:
        d.ellipse([bx0 + px - 6, by0 + py - 14, bx0 + px + 6, by0 + py - 2], fill=col)
        d.rectangle([bx0 + px - 8, by0 + py - 2, bx0 + px + 8, by0 + py + 3], fill=col)
    # score plate on the right
    px0 = bx0 + 8 * sq + 16
    d.rectangle([px0, by0 + 8, x1 - 14, by0 + 66], fill=(250, 246, 235))
    d.text(((px0 + x1 - 14) / 2, by0 + 14), "GAME 3", font=serif(17), fill=INK, anchor="ma")
    d.text(((px0 + x1 - 14) / 2, by0 + 38), "1 - 1", font=bold(15), fill=RED, anchor="ma")
    d.text(((px0 + x1 - 14) / 2, by0 + 76), "GUKESH", font=bold(11), fill=INK, anchor="ma")
    d.text(((px0 + x1 - 14) / 2, by0 + 92), "SINDAROV", font=bold(11), fill=INK, anchor="ma")
    d.text(((px0 + x1 - 14) / 2, by0 + 108), "GENEVA", font=plain(9), fill=GREY, anchor="ma")

SCENES = {"parade": scene_parade, "mumbai": scene_mumbai, "chess": scene_chess}

# --- page sections -------------------------------------------------------------
def draw_masthead(d):
    d.text((MARGIN, 12), "THE WORLD IN ONE DAY", font=serif(47), fill=INK)
    d.text((W - MARGIN, 26), "THURSDAY", font=bold(14), fill=INK, anchor="ra")
    d.text((W - MARGIN, 44), "26 NOVEMBER 2026", font=serif(17), fill=RED, anchor="ra")
    d.line([MARGIN, 66, W - MARGIN, 66], fill=INK, width=3)
    d.line([MARGIN, 71, W - MARGIN, 71], fill=RED, width=1)
    meta = (f"{len(ALL_STORIES)} STORIES · {len(REGION_COUNTS)} REGIONS · "
            f"{len(SOURCES)} SOURCES · ONE PAGE · DRAWN, NOT PHOTOGRAPHED")
    d.text((MARGIN, 78), meta, font=bold(12), fill=GREY)
    d.text((W - MARGIN, 78), "LATE EDITION", font=bold(12), fill=GREY, anchor="ra")

def draw_region_band(d):
    y0, y1 = 100, 126
    total = len(ALL_STORIES)
    x = 0
    for r in REGION_ORDER:
        wseg = round(W * REGION_COUNTS[r] / total)
        d.rectangle([x, y0, x + wseg, y1], fill=REGION_COLORS[r])
        label = f"{BAND_LABELS.get(r, r)} {REGION_COUNTS[r]}"
        fnt = bold(11) if wseg >= 96 else bold(9)
        if d.textlength(label, font=fnt) > wseg - 4:
            label = str(REGION_COUNTS[r])  # segment too narrow for the name
        d.text((x + wseg / 2, y0 + 7), label, font=fnt,
               fill=(255, 255, 255), anchor="ma")
        x += wseg

def draw_moments(d):
    y0, y1 = 126, 156
    d.rectangle([0, y0, W, y1], fill=STRIP)
    d.line([0, y1, W, y1], fill=RULE, width=1)
    d.text((MARGIN, y0 + 9), "THE DAY IN UTC", font=bold(11), fill=NAVY)
    x = MARGIN + 122
    for when, what in MOMENTS:
        label = f"{when}  {what}"
        if x + d.textlength(label, font=plain(11)) > W - MARGIN:
            break
        d.text((x, y0 + 10), label, font=plain(11), fill=INK)
        x += d.textlength(label, font=plain(11)) + 22
        d.text((x - 16, y0 + 10), "·", font=bold(11), fill=GREY)

def draw_numbers(d):
    y0, y1 = 162, 206
    d.rectangle([MARGIN, y0, W - MARGIN, y1], fill=BLACK)
    d.text((MARGIN + 12, y0 + 5), "BY THE NUMBERS", font=bold(9), fill=(240, 200, 90))
    cw = (W - 2 * MARGIN - 16) / len(NUMBERS)
    for i, (num, what) in enumerate(NUMBERS):
        x = MARGIN + 10 + i * cw
        d.text((x, y0 + 16), num, font=serif(16), fill=(250, 246, 235))
        d.text((x, y0 + 35), fit(d, what, plain(8), cw - 8), font=plain(8),
               fill=(206, 198, 178))

def draw_leads(d):
    y0, y1 = 214, 486
    gap = 8
    cw = (W - 2 * MARGIN - 2 * gap) // 3
    for i, (region, head, city, summary, source, status, scene) in enumerate(LEADS):
        x0 = MARGIN + i * (cw + gap)
        x1 = x0 + cw
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=1)
        SCENES[scene](d, (x0 + 1, y0 + 1, x1 - 1, y0 + 138))
        d.rectangle([x0 + 10, y0 + 146, x0 + 10 + d.textlength(region, font=bold(10)) + 12, y0 + 164],
                    fill=REGION_COLORS[region])
        d.text((x0 + 16, y0 + 150), region, font=bold(10), fill=(255, 255, 255))
        d.text((x1 - 10, y0 + 150), status, font=bold(10), fill=RED, anchor="ra")
        ty = y0 + 170
        for line in wrap(d, head, bold(14), cw - 20)[:3]:
            d.text((x0 + 10, ty), line, font=bold(14), fill=INK)
            ty += 18
        ty += 2
        body = f"{city} - {summary}"
        for line in wrap(d, body, plain(10), cw - 20)[:5]:
            d.text((x0 + 10, ty), line, font=plain(10), fill=(52, 50, 44))
            ty += 13
        d.text((x0 + 10, y1 - 17), f"No. {i + 1} · Source: {source}", font=plain(9), fill=GREY)

def draw_rows(d):
    x0, x1 = MARGIN, 640
    y = 494
    rh = 23.6
    for i, (region, head, city, summary, source, status) in enumerate(ROWS):
        n = i + 4
        d.rectangle([x0, y, x1, y + rh - 2], fill=CARD, outline=RULE, width=1)
        d.rectangle([x0, y, x0 + 28, y + rh - 2], fill=REGION_COLORS[region])
        d.text((x0 + 14, y + 5), str(n), font=bold(12), fill=(255, 255, 255), anchor="ma")
        d.text((x0 + 38, y + 2), fit(d, head, bold(11), x1 - x0 - 130), font=bold(11), fill=INK)
        d.text((x1 - 8, y + 3), status, font=bold(8), fill=RED, anchor="ra")
        line2 = fit(d, f"{city} - {summary} ({source})", plain(9), x1 - x0 - 48)
        d.text((x0 + 38, y + 14), line2, font=plain(9), fill=GREY)
        y += rh

def draw_map(d):
    x0, y0, x1, y1 = 652, 494, W - MARGIN, 730
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
    ly = y1 - 38
    d.text((x0 + 12, ly), "Numbered pins: the 13 drawn stories.", font=plain(10), fill=GREY)
    d.text((x0 + 12, ly + 15), "The 23 briefs below span the same map.", font=plain(10), fill=GREY)

def draw_briefs(d):
    y0 = 738
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + 22], fill=NAVY)
    d.text((MARGIN + 10, y0 + 5), "ALSO TODAY - 23 BRIEFS IN ONE LINE EACH",
           font=bold(11), fill=(250, 248, 240))
    col_w = (W - 2 * MARGIN - 24) // 2
    cols = [BRIEFS[:12], BRIEFS[12:]]
    for ci, col in enumerate(cols):
        x = MARGIN + ci * (col_w + 24)
        y = y0 + 30
        for j, (region, city, text, source) in enumerate(col):
            n = 14 + ci * 12 + j
            d.text((x, y + 1), f"{n}", font=bold(9), fill=RED)
            d.rectangle([x + 22, y + 3, x + 30, y + 11], fill=REGION_COLORS[region])
            line = fit(d, f"{city} - {text} ({source})", plain(9), col_w - 38)
            d.text((x + 36, y + 1), line, font=plain(9), fill=INK)
            y += 15.5

def draw_footer(d):
    y0 = 946
    d.line([MARGIN, y0, W - MARGIN, y0], fill=RULE, width=1)
    d.text((MARGIN, y0 + 7), "DATE CHECK - LEFT OUT, NOT 26 NOVEMBER:", font=bold(10), fill=RED)
    d.text((MARGIN + 268, y0 + 7), "  ·  ".join(DATE_CHECK), font=plain(10), fill=INK)
    d.text((MARGIN, y0 + 24),
           "Labels: OFFICIAL - announced by the body itself · CONFIRMED - two or more wires agree · REPORTED - a single wire · "
           "ONGOING - still developing.",
           font=plain(10), fill=GREY)
    d.text((MARGIN, y0 + 40),
           "Every story happened, or was first reported, on Thursday 26 November 2026 in some time zone. Nothing here is invented.",
           font=plain(10), fill=GREY)
    srcs = " · ".join(sorted(SOURCES))
    d.text((MARGIN, y0 + 56), f"Sources: {srcs}", font=bold(10), fill=NAVY)
    d.text((W - MARGIN, y0 + 56), "THE WORLD IN ONE DAY · p.1 of 1", font=plain(10),
           fill=GREY, anchor="ra")

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_region_band(d)
    draw_moments(d)
    draw_numbers(d)
    draw_leads(d)
    draw_rows(d)
    draw_map(d)
    draw_briefs(d)
    draw_footer(d)
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")

if __name__ == "__main__":
    main()
