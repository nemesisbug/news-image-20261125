#!/usr/bin/env python3
"""Render the news-image-20261125 front page as a 1024x1024 PNG.

Draws the whole page from scratch with Pillow: masthead, lead story
(Shenzhou-24, first Pakistani in orbit), three secondary cards, a
Thanksgiving travel band, four briefs, a numbers strip and a footer.
Every story on the page happened, or was first reported, on Wednesday
25 November 2026. Deterministic: no timestamps, no randomness, no
network. Run: python3 build_image.py  (writes entry.png next to it).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 231)
INK = (20, 20, 20)
NAVY = (13, 36, 66)
NAVY2 = (18, 58, 95)
RED = (179, 38, 30)
GOLD = (201, 162, 39)
TEAL = (15, 118, 110)
ORANGE = (232, 89, 12)
GREY = (90, 88, 82)
LIGHT_LINE = (205, 198, 184)
WHITE = (255, 255, 255)
SKY_TOP = (9, 26, 48)
SKY_BOT = (20, 66, 110)
EARTH = (46, 111, 183)
EARTH_LT = (110, 168, 214)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines fitting width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; returns y just below the last line."""
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# Fixed stars for the lead art panel (deterministic).
STARS = [
    (48, 152, 2), (96, 176, 1), (150, 142, 2), (205, 168, 1),
    (262, 148, 2), (318, 180, 1), (372, 146, 2), (430, 172, 1),
    (486, 150, 2), (540, 178, 1), (70, 230, 1), (128, 262, 2),
    (188, 238, 1), (246, 268, 2), (306, 240, 1), (366, 272, 2),
    (424, 244, 1), (484, 270, 2), (540, 238, 1), (60, 330, 2),
    (120, 360, 1), (180, 332, 2), (240, 366, 1), (300, 336, 2),
    (360, 368, 1), (420, 338, 2), (480, 366, 1), (530, 332, 2),
    (90, 420, 1), (150, 448, 2), (210, 424, 1), (270, 452, 2),
    (330, 426, 1), (390, 454, 2), (450, 428, 1), (510, 452, 2),
]


def draw_rocket(draw, cx, cy, scale=1.0):
    """A small stylised rocket climbing up-right, with flame."""
    flame = [(cx - 14 * scale, cy + 52 * scale), (cx + 14 * scale, cy + 52 * scale),
             (cx + 4 * scale, cy + 92 * scale), (cx, cy + 104 * scale),
             (cx - 4 * scale, cy + 92 * scale)]
    draw.polygon(flame, fill=(232, 89, 12))
    flame2 = [(cx - 8 * scale, cy + 52 * scale), (cx + 8 * scale, cy + 52 * scale),
              (cx, cy + 82 * scale)]
    draw.polygon(flame2, fill=(255, 196, 0))
    draw.polygon([(cx - 16 * scale, cy + 18 * scale), (cx - 16 * scale, cy + 52 * scale),
                  (cx - 34 * scale, cy + 58 * scale)], fill=RED)
    draw.polygon([(cx + 16 * scale, cy + 18 * scale), (cx + 16 * scale, cy + 52 * scale),
                  (cx + 34 * scale, cy + 58 * scale)], fill=RED)
    draw.rounded_rectangle([cx - 16 * scale, cy - 52 * scale, cx + 16 * scale, cy + 52 * scale],
                           radius=8 * scale, fill=WHITE)
    draw.polygon([(cx - 16 * scale, cy - 50 * scale), (cx + 16 * scale, cy - 50 * scale),
                  (cx, cy - 82 * scale)], fill=RED)
    draw.ellipse([cx - 9 * scale, cy - 22 * scale, cx + 9 * scale, cy - 4 * scale],
                 fill=NAVY2, outline=GOLD, width=2)
    draw.rectangle([cx - 16 * scale, cy + 26 * scale, cx + 16 * scale, cy + 34 * scale],
                   fill=RED)


def draw_station(draw, cx, cy, scale=1.0):
    """A small Tiangong-style station: core module, panels, dish."""
    draw.rectangle([cx - 52 * scale, cy - 7 * scale, cx - 14 * scale, cy + 7 * scale],
                   fill=(70, 110, 180))
    draw.rectangle([cx + 14 * scale, cy - 7 * scale, cx + 52 * scale, cy + 7 * scale],
                   fill=(70, 110, 180))
    draw.line([(cx - 52 * scale, cy - 7 * scale), (cx - 52 * scale, cy + 7 * scale)],
              fill=GOLD, width=2)
    draw.line([(cx + 52 * scale, cy - 7 * scale), (cx + 52 * scale, cy + 7 * scale)],
              fill=GOLD, width=2)
    draw.rounded_rectangle([cx - 16 * scale, cy - 12 * scale, cx + 16 * scale, cy + 12 * scale],
                           radius=6 * scale, fill=WHITE)
    draw.ellipse([cx - 5 * scale, cy - 5 * scale, cx + 5 * scale, cy + 5 * scale],
                 fill=NAVY2)
    draw.line([(cx + 10 * scale, cy - 12 * scale), (cx + 26 * scale, cy - 30 * scale)],
              fill=GOLD, width=2)
    draw.ellipse([cx + 20 * scale, cy - 36 * scale, cx + 32 * scale, cy - 24 * scale],
                 outline=GOLD, width=2)


def draw_pak_flag(draw, x, y, w=34, h=23):
    """A tiny Pakistan flag: green field, white hoist stripe, crescent."""
    draw.rectangle([x, y, x + w, y + h], fill=(20, 90, 50))
    draw.rectangle([x, y, x + int(w * 0.24), y + h], fill=WHITE)
    cx, cy, r = x + int(w * 0.62), y + h // 2, 7
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    draw.ellipse([cx - r + 3, cy - r, cx + r + 3, cy + r], fill=(20, 90, 50))
    draw.polygon([(x + int(w * 0.74), y + 5), (x + int(w * 0.80), y + 9),
                  (x + int(w * 0.74), y + 13), (x + int(w * 0.70), y + 9)],
                 fill=WHITE)


def draw_plane(draw, cx, cy, scale=1.0):
    """A simple white airliner silhouette, nose to the right."""
    body = [(cx - 52 * scale, cy), (cx - 30 * scale, cy - 9 * scale),
            (cx + 38 * scale, cy - 8 * scale), (cx + 56 * scale, cy - 1 * scale),
            (cx + 38 * scale, cy + 7 * scale), (cx - 30 * scale, cy + 8 * scale)]
    draw.polygon(body, fill=WHITE)
    draw.polygon([(cx - 8 * scale, cy - 6 * scale), (cx + 6 * scale, cy - 30 * scale),
                  (cx + 16 * scale, cy - 30 * scale), (cx + 12 * scale, cy - 4 * scale)],
                 fill=WHITE)
    draw.polygon([(cx - 2 * scale, cy + 5 * scale), (cx + 10 * scale, cy + 26 * scale),
                  (cx + 18 * scale, cy + 26 * scale), (cx + 14 * scale, cy + 5 * scale)],
                 fill=WHITE)
    draw.polygon([(cx - 48 * scale, cy - 2 * scale), (cx - 58 * scale, cy - 18 * scale),
                  (cx - 50 * scale, cy - 18 * scale), (cx - 40 * scale, cy - 2 * scale)],
                 fill=WHITE)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((24, 18), "THE WORLD IN ONE IMAGE", font=font(F_SERIF_B, 40), fill=WHITE)
    d.text((24, 66), "A front page of Wednesday's world news",
           font=font(F_SANS, 16), fill=(180, 200, 220))
    d.text((W - 24, 16), "WEDNESDAY", font=font(F_SANS_B, 20), fill=GOLD, anchor="ra")
    d.text((W - 24, 42), "25 NOVEMBER 2026", font=font(F_SANS_B, 26), fill=WHITE, anchor="ra")
    d.text((W - 24, 72), "make.fun  •  news-image-20261125",
           font=font(F_SANS, 14), fill=(180, 200, 220), anchor="ra")
    d.rectangle([0, 96, W, 100], fill=GOLD)

    # ---- Dateline strip -------------------------------------------
    d.text((W // 2, 108), "THE DAY IN ONE PICTURE  —  EVERY STORY HAPPENED OR WAS FIRST REPORTED TODAY",
           font=font(F_SANS_B, 15), fill=GREY, anchor="ma")
    hline(d, 24, W - 24, 126, fill=INK, width=2)

    # ---- Lead: art panel ------------------------------------------
    ax0, ay0, ax1, ay1 = 24, 136, 596, 492
    for yy in range(ay0, ay1):
        t = (yy - ay0) / (ay1 - ay0)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        d.line([(ax0, yy), (ax1, yy)], fill=(r, g, b))
    for (sx, sy, sr) in STARS:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=WHITE)
    # Earth arc along the bottom of the panel.
    d.ellipse([ax0 - 180, ay1 - 120, ax1 + 180, ay1 + 260], fill=EARTH)
    d.ellipse([ax0 + 60, ay1 - 60, ax0 + 260, ay1 + 60], fill=EARTH_LT)
    d.ellipse([ax0 + 330, ay1 - 40, ax0 + 470, ay1 + 40], fill=EARTH_LT)
    draw_station(d, 470, 190, scale=0.9)
    draw_rocket(d, 300, 330, scale=1.05)
    d.text((ax0 + 14, ay0 + 12), "JIUQUAN  •  00:18 UTC",
           font=font(F_SANS_B, 16), fill=GOLD)
    # Crew strip along the bottom of the panel.
    d.rectangle([ax0, ay1 - 34, ax1, ay1], fill=NAVY)
    d.rectangle([ax0, ay1 - 34, ax1, ay1 - 32], fill=GOLD)
    draw_pak_flag(d, ax0 + 12, ay1 - 27, w=30, h=20)
    d.text((ax0 + 52, ay1 - 26), "CREW: TANG HONGBO  •  WU YI  •  MUHAMMAD ZEESHAN ALI",
           font=font(F_SANS_B, 14), fill=WHITE)

    # ---- Lead: text column -----------------------------------------
    tx, tw = 620, 380
    d.text((tx, 138), "SPACE  •  LEAD STORY", font=font(F_SANS_B, 17), fill=RED)
    d.text((tx, 162), "PAKISTAN", font=font(F_SERIF_B, 46), fill=INK)
    d.text((tx, 212), "REACHES", font=font(F_SERIF_B, 46), fill=INK)
    d.text((tx, 262), "ORBIT", font=font(F_SERIF_B, 46), fill=INK)
    hline(d, tx, tx + tw, 318, fill=RED, width=3)
    y = para(d, (tx, 330),
             "Shenzhou-24 lifted off today with the first Pakistani ever "
             "in space.",
             font(F_SANS_B, 20), tw, leading=26)
    para(d, (tx, y + 10),
         "Muhammad Zeeshan Ali, 40, flew with Tang Hongbo and Wu Yi — the "
         "first foreign astronaut to visit Tiangong. Five to ten days "
         "aboard; docking later today.",
         font(F_SANS, 17), tw, leading=22)

    # ---- Secondary row: three cards --------------------------------
    cards = [
        ("IOWA", RED, "BRACES FOR A 5-TON BLAST",
         "At 9 a.m. today the Army detonates 9,500 lb of unstable lead "
         "azide at Middletown. Neighbours must leave or stay indoors — "
         "the lead-dust plume may drift 100 miles."),
        ("TRADE", NAVY2, "NEW US TARIFFS DUE TODAY",
         "Washington is poised to unveil duties on 16 trading partners "
         "after a probe into excess factory capacity — rebuilding the "
         "tariff wall the Supreme Court struck down."),
        ("GERMANY", TEAL, "TAX TOPS €1 TRILLION",
         "Berlin forecasts record tax revenue of more than one trillion "
         "euros in 2027."),
    ]
    cx0, cw, gap = 24, 317, 8
    cy0, ch = 510, 196
    for i, (kicker, colour, head, body) in enumerate(cards):
        x0 = cx0 + i * (cw + gap)
        d.rounded_rectangle([x0, cy0, x0 + cw, cy0 + ch], radius=8,
                            outline=LIGHT_LINE, width=2, fill=WHITE)
        d.text((x0 + 14, cy0 + 12), kicker, font=font(F_SANS_B, 15), fill=colour)
        para(d, (x0 + 14, cy0 + 36), head, font(F_SERIF_B, 22), cw - 28 - 44,
             leading=27)
        para(d, (x0 + 14, cy0 + 96), body, font(F_SANS, 16), cw - 28, leading=20)
    # Small drawn icons in the card headers' right corners.
    starburst(d, cx0 + cw - 26, cy0 + 26, 16, 7, 10, fill=ORANGE)
    d.ellipse([cx0 + 2 * cw + gap * 2 - 41, cy0 + 11, cx0 + 2 * cw + gap * 2 - 11, cy0 + 41],
              fill=NAVY2)
    d.text((cx0 + 2 * cw + gap * 2 - 26, cy0 + 26), "16", font=font(F_SANS_B, 17),
           fill=WHITE, anchor="mm")
    d.ellipse([cx0 + 3 * cw + gap * 3 - 41, cy0 + 11, cx0 + 3 * cw + gap * 3 - 11, cy0 + 41],
              fill=TEAL)
    d.text((cx0 + 3 * cw + gap * 3 - 26, cy0 + 26), "€", font=font(F_SANS_B, 20),
           fill=WHITE, anchor="mm")

    # ---- Thanksgiving band -----------------------------------------
    by0, by1 = 716, 806
    d.rounded_rectangle([24, by0, W - 24, by1], radius=10, fill=TEAL)
    draw_plane(d, 92, by0 + 44, scale=0.85)
    d.text((150, by0 + 10), "THANKSGIVING EVE — AMERICA HITS THE ROAD",
           font=font(F_SANS_B, 24), fill=WHITE)
    para(d, (150, by0 + 44),
         "81.5 million Americans are travelling for the holiday; today is "
         "the peak day out, with 17.6 million people to pass through "
         "airport security by Monday — the busiest skies in 16 years.",
         font(F_SANS, 18), W - 24 - 150 - 16, fill=WHITE, leading=23)

    # ---- Briefs: 2 x 2 grid ----------------------------------------
    briefs = [
        ("A DAY TO END VIOLENCE", ORANGE,
         "Today is the UN's International Day for the Elimination of "
         "Violence against Women."),
        ("SPAIN VOTES SUNDAY", NAVY2,
         "Polls put the conservative People's Party ahead of the "
         "Socialists before Sunday's vote."),
        ("ROBOT RIDES TO THE ISS", RED,
         "Russia's Progress MS-36 chases the station carrying Teledroid, "
         "its first humanoid robot. It docks Thursday."),
        ("THREE SHIPS, TWO STATIONS", TEAL,
         "Shenzhou-24, Progress MS-36 and Cygnus XL are all bound for "
         "orbit this week; Cygnus launches Sunday."),
    ]
    bw, bh = 492, 64
    for i, (head, colour, body) in enumerate(briefs):
        x0 = 24 + (i % 2) * (bw + 8)
        y0 = 818 + (i // 2) * 72
        d.rectangle([x0, y0, x0 + 5, y0 + bh], fill=colour)
        d.text((x0 + 14, y0), head, font=font(F_SANS_B, 19), fill=INK)
        para(d, (x0 + 14, y0 + 26), body, font(F_SANS, 16), bw - 14, leading=20)

    # ---- Numbers strip ----------------------------------------------
    ny = 962
    hline(d, 24, W - 24, ny, fill=INK, width=2)
    d.text((W // 2, ny + 6),
           "00:18 UTC liftoff  •  9,500 lb of explosive  •  81.5m travellers  •  "
           "€1tn German tax  •  5–10 days in orbit",
           font=font(F_SANS_B, 16), fill=INK, anchor="ma")

    # ---- Footer -------------------------------------------------------
    fy = 986
    hline(d, 24, W - 24, fy, fill=LIGHT_LINE, width=1)
    d.text((24, fy + 6),
           "Yesterday's news — the CIA breach, the Riyadh tower strike, Anthropic's broken IPO — "
           "is not today's news and is not shown here.",
           font=font(F_SANS, 13), fill=GREY)
    d.text((24, fy + 22),
           "Sources: Reuters, Xinhua, AP, AAA, TSA, FAA, United Nations, The Germany Eye.",
           font=font(F_SANS, 13), fill=GREY)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img = render()
    assert img.size == (1024, 1024), img.size
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    assert size <= 1048576, size
    print(f"wrote {out} ({size} bytes)")


if __name__ == "__main__":
    main()
