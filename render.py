#!/usr/bin/env python3
"""Render THE WORLD TODAY, issue No. 332: the world news of Friday 27 November 2026.

Draws a one-page newspaper front page with Pillow primitives only. Run:
    python3 render.py            # writes entry.png next to this file
Deterministic: fixed coordinates, fixed fonts, no randomness, no timestamps.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 230)
INK = (26, 26, 26)
NAVY = (20, 36, 62)
NAVY_LIGHT = (38, 58, 90)
RED = (179, 38, 30)
GREY = (90, 96, 104)
LIGHT_LINE = (198, 190, 172)
CARD = (255, 255, 255)
SEA = (46, 94, 122)
SEA_DARK = (28, 62, 84)
SKY_STORM = (58, 68, 82)
SKY_STORM_DARK = (40, 48, 60)
YELLOW = (242, 201, 76)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", width=None):
    """Draw lines starting at (x, y); returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        if align == "center" and width is not None:
            lx = x + (width - draw.textlength(line, font=fnt)) // 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def storm_scene(draw, x, y, w, h):
    """Night storm over a city skyline: cloud bands, rain, lightning."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY_STORM_DARK)
    # sky bands
    for i, c in enumerate([(58, 68, 82), (52, 62, 76), (46, 56, 70)]):
        draw.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=c)
    # clouds
    for cx, cy, cw, ch in [(x + 60, y + 18, 260, 70), (x + 300, y + 6, 300, 78),
                           (x + 620, y + 22, 280, 66), (x + 420, y + 52, 240, 60)]:
        draw.ellipse([cx, cy, cx + cw, cy + ch], fill=(70, 80, 96))
        draw.ellipse([cx + 40, cy - 18, cx + cw - 30, cy + ch - 22], fill=(78, 88, 104))
    # lightning bolt
    bolt = [(x + 700, y + 6), (x + 668, y + 76), (x + 692, y + 76),
            (x + 660, y + 146), (x + 716, y + 64), (x + 690, y + 64)]
    draw.polygon(bolt, fill=YELLOW)
    # rain streaks
    for rx in range(x + 20, x + w - 10, 34):
        draw.line([(rx, y + 92), (rx - 12, y + 132)], fill=(150, 165, 185), width=2)
        draw.line([(rx + 14, y + 124), (rx + 2, y + 162)], fill=(140, 155, 175), width=2)
    # skyline
    base = y + h
    for bx, bw, bh in [(x + 10, 90, 74), (x + 110, 70, 108), (x + 190, 110, 62),
                       (x + 310, 80, 96), (x + 400, 100, 70), (x + 510, 64, 118),
                       (x + 584, 96, 82), (x + 690, 76, 104), (x + 776, 108, 66),
                       (x + 894, 84, 92)]:
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(24, 30, 40))
        for wy in range(base - bh + 12, base - 8, 18):
            for wx in range(bx + 10, bx + bw - 8, 20):
                if (wx // 20 + wy // 18) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 6, wy + 8], fill=YELLOW)


def rocket_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 34, 44))
    for sx, sy in [(x + 24, y + 20), (x + 90, y + 48), (x + 170, y + 14),
                   (x + 240, y + 44), (x + 280, y + 22)]:
        draw.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 255, 255))
    # rocket body
    cx = x + w // 2
    draw.polygon([(cx, y + 8), (cx + 22, y + 44), (cx + 22, y + 84),
                  (cx - 22, y + 84), (cx - 22, y + 44)], fill=(226, 226, 226))
    draw.polygon([(cx, y + 8), (cx + 22, y + 44), (cx - 22, y + 44)], fill=(179, 38, 30))
    draw.polygon([(cx - 22, y + 68), (cx - 44, y + 92), (cx - 22, y + 92)], fill=(179, 38, 30))
    draw.polygon([(cx + 22, y + 68), (cx + 44, y + 92), (cx + 22, y + 92)], fill=(179, 38, 30))
    draw.ellipse([cx - 7, y + 48, cx + 7, y + 62], fill=(46, 94, 122))
    # flame
    draw.polygon([(cx - 12, y + 92), (cx + 12, y + 92), (cx, y + 116)], fill=(242, 160, 60))
    draw.polygon([(cx - 6, y + 92), (cx + 6, y + 92), (cx, y + 108)], fill=YELLOW)
    # ground line
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=(20, 24, 32))


def tanker_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(178, 205, 219))
    draw.ellipse([x + 30, y + 12, x + 130, y + 44], fill=(240, 244, 246))
    draw.ellipse([x + 190, y + 6, x + 300, y + 34], fill=(240, 244, 246))
    # sea
    draw.rectangle([x, y + h // 2, x + w, y + h], fill=SEA)
    draw.rectangle([x, y + h // 2, x + w, y + h // 2 + 6], fill=(120, 165, 190))
    # tanker hull
    draw.polygon([(x + 30, y + 72), (x + w - 24, y + 72), (x + w - 52, y + 104),
                  (x + 58, y + 104)], fill=(52, 52, 58))
    draw.rectangle([x + 40, y + 50, x + w - 40, y + 72], fill=(140, 40, 34))
    for cx in range(x + 56, x + w - 60, 44):
        draw.rectangle([cx, y + 55, cx + 30, y + 68], fill=(226, 226, 226))
    # funnel with smoke
    draw.rectangle([x + w - 120, y + 30, x + w - 92, y + 50], fill=(26, 26, 26))
    draw.ellipse([x + w - 118, y + 16, x + w - 92, y + 32], fill=(120, 120, 120))
    draw.ellipse([x + w - 108, y + 4, x + w - 84, y + 20], fill=(140, 140, 140))
    # spiked mine in the water
    mx, my = x + 52, y + 106
    for ang in range(0, 360, 45):
        import math
        dx = math.cos(math.radians(ang)) * 13
        dy = math.sin(math.radians(ang)) * 13
        draw.line([(mx, my), (mx + dx, my + dy)], fill=(20, 20, 20), width=3)
    draw.ellipse([mx - 13, my - 13, mx + 13, my + 13], fill=(20, 20, 20))


def chart_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    base = y + h - 22
    # descending bars: 1997 high to today low
    bars = [66, 60, 52, 44, 34, 24, 14]
    bw = 26
    gap = (w - 40 - bw * len(bars)) // (len(bars) - 1)
    bx = x + 20
    for v in bars:
        draw.rectangle([bx, base - v, bx + bw, base], fill=NAVY)
        bx += bw + gap
    draw.rectangle([x + 16, base - 72, x + 20, base], fill=INK)
    draw.line([(x + 16, base), (x + w - 12, base)], fill=INK, width=2)
    draw.text((x + 22, y + 6), "NET MIGRATION", font=SANS_B(15), fill=GREY)
    draw.text((x + w - 78, y + 6), "77,000", font=SANS_B(15), fill=RED)


def bank_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 218))
    # pediment
    draw.polygon([(x + 6, y + 30), (x + w // 2, y + 8), (x + w - 6, y + 30)], fill=NAVY)
    draw.ellipse([x + w // 2 - 7, y + 14, x + w // 2 + 7, y + 28], fill=YELLOW)
    # columns
    for cx in [x + 14, x + 44, x + 74]:
        draw.rectangle([cx, y + 36, cx + 14, y + 84], fill=(255, 255, 255))
        draw.rectangle([cx - 3, y + 33, cx + 17, y + 38], fill=(255, 255, 255))
        draw.rectangle([cx - 3, y + 84, cx + 17, y + 89], fill=(255, 255, 255))
    draw.rectangle([x + 8, y + 89, x + w - 8, y + 96], fill=NAVY)


def shop_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    # awning stripes
    for i in range(4):
        c = RED if i % 2 == 0 else (255, 255, 255)
        draw.polygon([(x + 6 + i * 23, y + 12), (x + 27 + i * 23, y + 12),
                      (x + 24 + i * 23, y + 32), (x + 3 + i * 23, y + 32)], fill=c)
    draw.rectangle([x + 6, y + 32, x + w - 6, y + 86], fill=(196, 178, 148))
    draw.rectangle([x + 14, y + 40, x + 38, y + 68], fill=(178, 205, 219))
    draw.rectangle([x + 66, y + 40, x + w - 14, y + 68], fill=(178, 205, 219))
    draw.rectangle([x + 44, y + 40, x + 60, y + 86], fill=(58, 68, 82))


def tower_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(40, 44, 54))
    # tower block
    draw.rectangle([x + 32, y + 8, x + w - 32, y + 82], fill=(96, 102, 116))
    for wy in range(y + 16, y + 76, 14):
        for wx in range(x + 38, x + w - 50, 16):
            lit = (wx // 16 + wy // 14) % 3 == 0
            draw.rectangle([wx, wy, wx + 9, wy + 8],
                           fill=YELLOW if lit else (58, 64, 76))
    # candle flame of remembrance
    draw.ellipse([x + w // 2 - 5, y + 84, x + w // 2 + 5, y + 96], fill=YELLOW)
    draw.polygon([(x + w // 2, y + 80), (x + w // 2 - 7, y + 94),
                  (x + w // 2 + 7, y + 94)], fill=(242, 160, 60))


def card(draw, x, y, w, h, kicker, headline, body, art, art_h=114):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=LIGHT_LINE, width=2)
    art(draw, x + 8, y + 8, w - 16, art_h)
    ty = y + 8 + art_h + 8
    ty = text_block(draw, x + 12, ty, [kicker], SANS_B(17), fill=RED)
    ty += 2
    ty = text_block(draw, x + 12, ty, wrap(draw, headline, SERIF_B(25), w - 24),
                    SERIF_B(25), leading=29)
    ty += 4
    text_block(draw, x + 12, ty, wrap(draw, body, SANS(19), w - 24), SANS(19), leading=23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=RED)
    text_block(d, 0, 18, ["THE WORLD TODAY"], SERIF_B(84), fill=(255, 255, 255),
               align="center", width=W)
    d.text((28, 108), "No. 332", font=SANS(22), fill=(200, 210, 225))
    d.text((W - 28 - d.textlength("ONE PAGE  •  ONE DAY", font=SANS(22)), 108),
           "ONE PAGE  •  ONE DAY", font=SANS(22), fill=(200, 210, 225))
    d.text((W // 2 - d.textlength("FRIDAY 27 NOVEMBER 2026", font=SANS_B(26)) // 2, 106),
           "FRIDAY 27 NOVEMBER 2026", font=SANS_B(26), fill=YELLOW)

    # ---- lead art + headline ----
    storm_scene(d, 28, 170, W - 56, 178)
    y = 356
    y = text_block(d, 28, y,
                   wrap(d, "THANKSGIVING STORM CUTS POWER ON THE US EAST COAST",
                        SERIF_B(40), W - 56), SERIF_B(40), leading=48)
    y += 6
    y = text_block(d, 28, y,
                   wrap(d, "A powerful storm swept the Eastern Seaboard on Thanksgiving, "
                           "knocking out power and grounding holiday flights.",
                        SANS(24), W - 56), SANS(24), leading=30)
    hline(d, 28, W - 28, 528, fill=INK, width=3)

    # ---- middle row: three stories ----
    my = 544
    cw = (W - 56 - 32) // 3
    chh = 264
    card(d, 28, my, cw, chh, "NORTH KOREA",
         "Kim orders nuclear expansion",
         "Pyongyang vows to widen tactical nuclear deployment.",
         rocket_scene)
    card(d, 28 + cw + 16, my, cw, chh, "STRAIT OF HORMUZ",
         "Iran says three tankers hit mines",
         "Oil climbs as the busiest oil lane faces fresh attacks.",
         tanker_scene)
    card(d, 28 + 2 * (cw + 16), my, cw, chh, "BRITAIN",
         "Net migration falls to 77,000",
         "Tighter rules cut arrivals to a near three-decade low.",
         chart_scene)

    # ---- bottom row: three stories (kicker + headline only) ----
    by = 824
    bh = 112
    bw = (W - 56 - 32) // 3
    bottom = [
        ("EUROPE", "Hernandez de Cos named next ECB chief", bank_scene),
        ("COLOMBIA", "All hostages freed after 16-hour siege", shop_scene),
        ("HONG KONG", "City marks a year since deadly tower fire", tower_scene),
    ]
    for i, (kick, head, art) in enumerate(bottom):
        x = 28 + i * (bw + 16)
        d.rectangle([x, by, x + bw, by + bh], fill=CARD, outline=LIGHT_LINE, width=2)
        art(d, x + 8, by + 8, 104, 96)
        tx = x + 122
        ty = by + 10
        ty = text_block(d, tx, ty, [kick], SANS_B(15), fill=RED)
        text_block(d, tx, ty + 2, wrap(d, head, SERIF_B(19), bw - 134), SERIF_B(19), leading=23)

    # ---- footer strip ----
    fy = 948
    hline(d, 28, W - 28, fy, fill=INK, width=2)
    y = fy + 8
    y = text_block(d, 28, y,
                   wrap(d, "ALSO TODAY:  SpaceX wins approval for a million satellites  •  "
                           "Bangkok oil depot blast injures seven  •  EU split over budget "
                           "and a $49bn Ukraine loan",
                        SANS_B(18), W - 56), SANS_B(18), leading=23)
    text_block(d, 28, y + 2,
               ["THE WORLD TODAY  •  FRIDAY 27 NOVEMBER 2026  •  THE WORLD IN ONE PAGE"],
               SANS(15), fill=GREY, align="center", width=W - 56)

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
