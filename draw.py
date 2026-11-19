#!/usr/bin/env python3
"""news-image-20261119 v3 — front page for Thursday 19 November 2026.

One 1024x1024 JPEG, drawn entirely with Pillow (no AI images, no
network), in the winner genre: giant serif date masthead, a region
breakdown bar, three big illustrated lead stories, ten numbered
illustrated cards (4-13), a dotted world map with pins, and a numbered
ALSO ON list (14-50) — 50 verified stories, seven regions, one day.
All text is drawn (no AI text); every illustration is drawn
programmatically. Full story list with sources: STORIES.md.

Deterministic: one fixed random seed, no timestamps, no network.
Two runs produce identical bytes. Saves JPEG as entry.png.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MX = 14
CW = W - 2 * MX  # 996
PAPER = (250, 246, 236)
INK = (20, 20, 20)
RED = (178, 34, 34)
GOLD = (198, 158, 44)
NAVY = (16, 24, 46)
GREY = (96, 96, 96)
DECK = (74, 74, 74)
PANEL_LINE = (180, 175, 165)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

RNG = random.Random(20261119)  # fixed seed only — determinism


def font(path, size):
    return ImageFont.truetype(path, size)


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def dark(col, f):
    return tuple(int(c * f) for c in col)


def vgrad(d, x, y, w, h, top, bottom):
    for i in range(h):
        d.line([(x, y + i), (x + w, y + i)],
               fill=mix(top, bottom, i / max(h - 1, 1)))


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, lh):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def glow_text(d, xy, text, fnt, core, halo, steps=5):
    """Neon-style text: soft halo layers behind a bright core."""
    x, y = xy
    for r in range(steps, 0, -1):
        col = mix(core, halo, r / steps)
        for dx, dy in ((r, 0), (-r, 0), (0, r), (0, -r),
                       (r, r), (-r, -r), (r, -r), (-r, r)):
            d.text((x + dx, y + dy), text, font=fnt, fill=col)
    d.text((x, y), text, font=fnt, fill=core)


def skyline(d, x, y, w, h, base, heights, col, lit):
    """Row of dark buildings with a few lit windows."""
    n = len(heights)
    bw = w / n
    for i, hh in enumerate(heights):
        bx = x + i * bw
        bh = h * hh
        d.rectangle([bx + 1, y + h - bh, bx + bw - 1, y + h], fill=col)
        for wy in range(int(y + h - bh + 6), int(y + h - 4), 12):
            for wx in range(int(bx + 4), int(bx + bw - 4), 10):
                if RNG.random() < 0.28:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=lit)


def palm(d, x, y, s, col):
    """Simple palm silhouette: curved trunk + 6 fronds."""
    d.line([(x, y), (x + 6 * s, y - 52 * s)], fill=col, width=max(2, int(4 * s)))
    top = (x + 6 * s, y - 52 * s)
    for ang in (-150, -120, -95, -70, -40, -15):
        rad = math.radians(ang)
        ex = top[0] + 34 * s * math.cos(rad)
        ey = top[1] + 20 * s * math.sin(rad) + 8 * s
        d.line([top, (ex, ey)], fill=col, width=max(2, int(3 * s)))
        d.line([(ex, ey), (ex + 10 * s * math.cos(rad + 0.5),
                            ey + 12 * s)], fill=col, width=max(1, int(2 * s)))


# ------------------------------------------------------------------ scenes
def scene_vice_city(d, x, y, w, h):
    """Neon Vice City at dusk: gradient sky, sun, skyline, palms, sea."""
    vgrad(d, x, y, w, h, (38, 12, 64), (255, 94, 120))
    vgrad(d, x, y + int(h * 0.55), w, h - int(h * 0.55),
          (255, 94, 120), (255, 166, 77))
    # sun, top right, clear of the neon sign
    sx, sy, sr = x + w * 0.90, y + h * 0.20, 28
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 214, 130))
    d.ellipse([sx - sr - 8, sy - sr - 8, sx + sr + 8, sy + sr + 8],
              outline=(255, 214, 130), width=2)
    # skyline (kept below the neon sub-line)
    skyline(d, x, y + int(h * 0.50), w, int(h * 0.28), 0,
            [0.5, 0.9, 0.65, 1.0, 0.75, 0.95, 0.6, 1.0, 0.8, 0.7, 0.95, 0.55],
            (24, 8, 40), (255, 220, 120))
    # sea strip
    sea_y = y + int(h * 0.78)
    d.rectangle([x, sea_y, x + w, y + h], fill=(16, 42, 84))
    for i in range(5):
        yy = sea_y + 6 + i * 7
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(90, 140, 200), width=1)
    # neon sign
    f_big = font(SANS_B, 74)
    f_sub = font(SANS_B, 30)
    tw = d.textlength("VICE CITY", font=f_big)
    glow_text(d, (x + (w - tw) / 2, y + 8), "VICE CITY", f_big,
              (255, 255, 255), (255, 45, 149), steps=6)
    tw2 = d.textlength("GTA VI  •  OUT TODAY", font=f_sub)
    d.text((x + (w - tw2) / 2, y + 92), "GTA VI  •  OUT TODAY",
           font=f_sub, fill=(255, 240, 120))


def scene_shenzhen(d, x, y, w, h):
    """APEC Shenzhen: dusk sky, tower skyline, three flags."""
    vgrad(d, x, y, w, h, (14, 34, 66), (64, 110, 168))
    skyline(d, x, y + int(h * 0.45), w, int(h * 0.55), 0,
            [0.6, 0.85, 0.5, 1.0, 0.7, 0.9, 0.55, 0.8],
            (10, 20, 38), (255, 200, 90))
    # three flags on poles
    fy = y + 12
    fw, fh = 52, 34
    gap = (w - 3 * fw) / 4
    # USA: stripes + blue canton
    ux = x + gap
    for i in range(7):
        d.rectangle([ux, fy + i * fh / 7, ux + fw, fy + (i + 1) * fh / 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([ux, fy, ux + fw * 0.42, fy + fh * 0.55], fill=(30, 50, 110))
    for r in range(3):
        for c in range(4):
            d.ellipse([ux + 4 + c * 5, fy + 3 + r * 5,
                       ux + 6 + c * 5, fy + 5 + r * 5], fill=(255, 255, 255))
    d.line([(ux, fy), (ux, fy + fh + 26)], fill=(220, 220, 220), width=2)
    # China: red field, gold stars
    cx = x + 2 * gap + fw
    d.rectangle([cx, fy, cx + fw, fy + fh], fill=(222, 41, 16))
    d.ellipse([cx + 6, fy + 5, cx + 16, fy + 15], fill=(255, 222, 0))
    for sx, sy in ((cx + 24, fy + 4), (cx + 32, fy + 10), (cx + 32, fy + 18),
                   (cx + 24, fy + 24)):
        d.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 222, 0))
    d.line([(cx, fy), (cx, fy + fh + 26)], fill=(220, 220, 220), width=2)
    # Russia: white-blue-red tricolour
    rx = x + 3 * gap + 2 * fw
    for i, col in enumerate(((255, 255, 255), (0, 57, 166), (213, 0, 50))):
        d.rectangle([rx, fy + i * fh / 3, rx + fw, fy + (i + 1) * fh / 3],
                    fill=col)
    d.line([(rx, fy), (rx, fy + fh + 26)], fill=(220, 220, 220), width=2)
    # APEC banner
    f = font(SANS_B, 15)
    label = "APEC  •  SHENZHEN"
    tw = d.textlength(label, font=f)
    d.rectangle([x + (w - tw) / 2 - 8, y + h - 26, x + (w + tw) / 2 + 8, y + h - 6],
                fill=(255, 255, 255))
    d.text((x + (w - tw) / 2, y + h - 26), label, font=f, fill=NAVY)


def scene_hague(d, x, y, w, h):
    """Peace Palace, The Hague: classical courthouse + scales of justice."""
    vgrad(d, x, y, w, h, (168, 200, 224), (232, 238, 240))
    # courthouse
    bx, by, bw, bh = x + w * 0.12, y + h * 0.34, w * 0.76, h * 0.5
    d.rectangle([bx, by, bx + bw, by + bh], fill=(238, 230, 210))
    d.polygon([(bx - 8, by), (bx + bw / 2, by - h * 0.16),
               (bx + bw + 8, by)], fill=(180, 60, 50))
    for i in range(5):
        cx = bx + bw * (0.12 + i * 0.19)
        d.rectangle([cx - 5, by + 8, cx + 5, by + bh - 6], fill=(250, 246, 236))
        d.rectangle([cx - 8, by + 4, cx + 8, by + 8], fill=(210, 200, 180))
    d.rectangle([bx + bw * 0.42, by + bh * 0.55, bx + bw * 0.58, by + bh],
                fill=(90, 60, 40))
    # scales of justice, gold, top right of building
    sx, sy = x + w * 0.78, y + h * 0.10
    d.line([(sx, sy), (sx, sy + 26)], fill=GOLD, width=3)
    d.line([(sx - 18, sy + 4), (sx + 18, sy + 4)], fill=GOLD, width=3)
    d.line([(sx - 18, sy + 4), (sx - 18, sy + 16)], fill=GOLD, width=2)
    d.line([(sx + 18, sy + 4), (sx + 18, sy + 16)], fill=GOLD, width=2)
    d.polygon([(sx - 26, sy + 16), (sx - 10, sy + 16), (sx - 18, sy + 24)],
              fill=GOLD)
    d.polygon([(sx + 10, sy + 16), (sx + 26, sy + 16), (sx + 18, sy + 24)],
              fill=GOLD)
    d.ellipse([sx - 3, sy - 4, sx + 3, sy + 2], fill=GOLD)
    # lawn
    d.rectangle([x, y + h * 0.86, x + w, y + h], fill=(90, 140, 80))


def scene_voyager(d, x, y, w, h):
    """Deep space: starfield, Voyager probe with gold dish, tiny Earth."""
    d.rectangle([x, y, x + w, y + h], fill=(6, 8, 26))
    for _ in range(70):
        sx = x + RNG.random() * w
        sy = y + RNG.random() * h
        r = 1 if RNG.random() < 0.8 else 2
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=(255, 255, 255) if RNG.random() < 0.7 else (180, 200, 255))
    # Earth, small, bottom left
    ex, ey, er = x + 26, y + h - 30, 14
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(40, 110, 220))
    d.ellipse([ex - er + 4, ey - er + 3, ex - er + 12, ey - er + 9],
              fill=(120, 200, 120))
    # Voyager probe: gold dish + body + boom
    px, py = x + w * 0.58, y + h * 0.42
    d.line([(px, py), (px + 46, py - 30)], fill=(200, 200, 210), width=3)
    d.ellipse([px + 40, py - 36, px + 52, py - 24], fill=(255, 220, 90))
    d.ellipse([px - 26, py - 20, px + 6, py + 12], outline=(255, 215, 0), width=4)
    d.line([(px - 26, py - 4), (px - 52, py - 16)], fill=(200, 200, 210), width=3)
    d.rectangle([px - 6, py - 6, px + 14, py + 8], fill=(220, 220, 230))
    # signal arcs to Earth (panel headline already says one light-day)
    for r in (34, 48, 62):
        d.arc([px - r, py - r + 10, px + r, py + r + 10],
              start=120, end=240, fill=(120, 200, 255), width=2)


def scene_eu_ukraine(d, x, y, w, h):
    """EU flag field: blue, circle of gold stars, big EUR 45bn figure."""
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    # star circle, kept small and high so the figure below stays clear
    cx, cy, r = x + w * 0.5, y + h * 0.26, min(w, h) * 0.20
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        sx = cx + r * math.cos(ang)
        sy = cy + r * math.sin(ang)
        d.polygon([(sx, sy - 6), (sx + 2, sy - 2), (sx + 6, sy - 1),
                   (sx + 3, sy + 2), (sx + 4, sy + 6), (sx, sy + 4),
                   (sx - 4, sy + 6), (sx - 3, sy + 2), (sx - 6, sy - 1),
                   (sx - 2, sy - 2)], fill=(255, 204, 0))
    f_big = font(SANS_B, int(h * 0.40))
    t1 = "€45 BILLION"
    tw = d.textlength(t1, font=f_big)
    d.text((x + (w - tw) / 2, y + h - 32), t1, font=f_big, fill=(255, 255, 255))


def scene_gaza(d, x, y, w, h):
    """Dusk desert, a dashed Yellow Line, a tank crossing it."""
    vgrad(d, x, y, w, h, (232, 196, 130), (196, 140, 80))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(168, 120, 66))
    # distant buildings
    for bx, bw2, bh2 in ((0.06, 0.16, 0.22), (0.30, 0.12, 0.30),
                         (0.62, 0.18, 0.20), (0.84, 0.12, 0.26)):
        d.rectangle([x + w * bx, y + h * 0.72 - h * bh2,
                     x + w * (bx + bw2), y + h * 0.72], fill=(120, 84, 50))
    # Yellow Line: dashed, vertical, labelled
    lx = x + w * 0.55
    for yy in range(int(y + 6), int(y + h - 6), 14):
        d.line([(lx, yy), (lx, yy + 8)], fill=(255, 215, 0), width=3)
    f = font(SANS_B, 12)
    d.text((lx + 5, y + 8), "YELLOW", font=f, fill=(120, 60, 0))
    d.text((lx + 5, y + 22), "LINE", font=f, fill=(120, 60, 0))
    # tank crossing the line, heading left
    tx, ty = int(x + w * 0.42), int(y + h * 0.60)
    d.rectangle([tx - 34, ty, tx + 30, ty + 16], fill=(74, 84, 60))
    d.rectangle([tx - 26, ty - 10, tx + 6, ty], fill=(74, 84, 60))
    d.line([(tx - 26, ty - 6), (tx - 58, ty - 6)], fill=(60, 68, 48), width=4)
    for wx in range(tx - 34, tx + 30, 10):
        d.ellipse([wx, ty + 16, wx + 8, ty + 24], fill=(40, 44, 34))
    # arrow showing the crossing
    d.line([(x + w * 0.78, ty + 8), (x + w * 0.60, ty + 8)],
           fill=(178, 34, 34), width=3)
    d.polygon([(x + w * 0.60, ty + 8), (x + w * 0.66, ty + 2),
               (x + w * 0.66, ty + 14)], fill=(178, 34, 34))


def scene_measles(d, x, y, w, h):
    """Red virus spheres on pale clinical blue; USA tag."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 244))
    for cx, cy, r, col in ((0.24, 0.34, 26, (200, 40, 40)),
                           (0.62, 0.28, 20, (220, 70, 60)),
                           (0.78, 0.62, 30, (200, 40, 40)),
                           (0.38, 0.68, 18, (230, 90, 80))):
        px, py = x + w * cx, y + h * cy
        for i in range(10):
            ang = math.radians(i * 36)
            ex = px + (r + 7) * math.cos(ang)
            ey = py + (r + 7) * math.sin(ang)
            d.line([(px, py), (ex, ey)], fill=col, width=3)
            d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=col)
        d.ellipse([px - r, py - r, px + r, py + r], fill=col)
        d.ellipse([px - r + 6, py - r + 5, px - r + 16, py - r + 12],
                  fill=(255, 150, 140))
    f = font(SANS_B, 15)
    tag = "26 YEARS — GONE"
    tw = d.textlength(tag, font=f)
    d.rectangle([x + 68, y + h - 28, x + 68 + tw + 12, y + h - 8],
                fill=(255, 255, 255))
    d.text((x + 74, y + h - 27), tag, font=f, fill=RED)


def star(d, cx, cy, r, col):
    """Five-point star polygon."""
    pts = []
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=col)


def scene_australia(d, x, y, w, h):
    """Australian ensign, simplified, with a red SANCTIONS stamp bar."""
    d.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
    cw, ch = int(w * 0.5), int(h * 0.52)
    d.rectangle([x, y, x + cw, y + ch], fill=(0, 20, 80))
    d.line([(x, y), (x + cw, y + ch)], fill=(255, 255, 255), width=3)
    d.line([(x + cw, y), (x, y + ch)], fill=(255, 255, 255), width=3)
    d.line([(x + cw // 2, y), (x + cw // 2, y + ch)], fill=(200, 40, 50), width=4)
    d.line([(x, y + ch // 2), (x + cw, y + ch // 2)], fill=(200, 40, 50), width=4)
    # Federation star + Southern Cross, gold
    star(d, x + w * 0.62, y + h * 0.42, 9, (255, 205, 0))
    for sx, sy, r in ((0.80, 0.30, 5), (0.88, 0.55, 5), (0.70, 0.68, 5),
                      (0.86, 0.78, 4)):
        star(d, x + w * sx, y + h * sy, r, (255, 255, 255))
    f = font(SANS_B, 15)
    label = "SANCTIONS"
    tw = d.textlength(label, font=f)
    d.rectangle([x + (w - tw) / 2 - 8, y + h - 26, x + (w + tw) / 2 + 8, y + h - 6],
                fill=(178, 34, 34))
    d.text((x + (w - tw) / 2, y + h - 25), label, font=f, fill=(255, 255, 255))


def scene_cyclone(d, x, y, w, h):
    """Cyclone spiral: storm-grey sky, swirling white arcs, rain, eye."""
    vgrad(d, x, y, w, h, (58, 68, 88), (138, 152, 172))
    cx, cy = x + w * 0.5, y + h * 0.48
    for r in range(12, 72, 11):
        d.arc([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7],
              start=200, end=60, fill=(255, 255, 255), width=3)
        d.arc([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7],
              start=20, end=240, fill=(198, 208, 220), width=2)
    d.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=(255, 220, 90))
    for i in range(10):
        rx = x + 8 + i * (w - 16) / 10 + (6 if i % 2 else -4)
        ry = y + 4 + (i % 3) * 8
        d.line([(rx, ry), (rx - 4, ry + 11)], fill=(200, 220, 240), width=2)
    f = font(SANS_B, 13)
    label = "LANDFALL EXPECTED"
    tw = d.textlength(label, font=f)
    d.text((x + (w - tw) / 2, y + h - 20), label, font=f, fill=(255, 255, 255))


def scene_alaska(d, x, y, w, h):
    """Alaska state flag: blue field, gold Big Dipper + North Star."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 40, 110))
    star(d, x + w * 0.78, y + h * 0.22, 12, (255, 205, 0))
    for px, py in ((0.16, 0.62), (0.28, 0.55), (0.40, 0.58), (0.50, 0.66),
                   (0.58, 0.52), (0.68, 0.42), (0.78, 0.55)):
        star(d, x + w * px, y + h * py, 7, (255, 205, 0))
    f = font(SANS_B, 15)
    label = "56–44  •  SENATE"
    tw = d.textlength(label, font=f)
    d.text((x + (w - tw) / 2, y + h - 22), label, font=f, fill=(255, 255, 255))


def scene_canada_china(d, x, y, w, h):
    """Canada and China flags side by side, linked by a white arrow."""
    # Canada: red-white-red + maple leaf
    d.rectangle([x, y, x + w // 2, y + h], fill=(255, 0, 0))
    d.rectangle([x + w * 0.12, y, x + w * 0.38, y + h], fill=(255, 255, 255))
    lx, ly, s = x + w * 0.25, y + h * 0.42, 1.0
    leaf = [(0, -15), (4, -7), (12, -11), (8, -3), (15, -1), (8, 3),
            (11, 12), (3, 8), (2, 17), (0, 11), (-2, 17), (-3, 8),
            (-11, 12), (-8, 3), (-15, -1), (-8, -3), (-12, -11), (-4, -7)]
    d.polygon([(lx + px * s, ly + py * s) for px, py in leaf], fill=(255, 0, 0))
    # China: red field + gold stars
    d.rectangle([x + w // 2, y, x + w, y + h], fill=(222, 41, 16))
    star(d, x + w * 0.66, y + h * 0.28, 13, (255, 222, 0))
    for sx, sy in ((0.82, 0.18), (0.90, 0.30), (0.90, 0.44), (0.82, 0.54)):
        star(d, x + w * sx, y + h * sy, 4, (255, 222, 0))
    # double-headed arrow along the bottom
    ay = y + h - 12
    d.line([(x + w * 0.30, ay), (x + w * 0.70, ay)], fill=(255, 255, 255), width=3)
    d.polygon([(x + w * 0.30, ay), (x + w * 0.36, ay - 5),
               (x + w * 0.36, ay + 5)], fill=(255, 255, 255))
    d.polygon([(x + w * 0.70, ay), (x + w * 0.64, ay - 5),
               (x + w * 0.64, ay + 5)], fill=(255, 255, 255))


def scene_saudi(d, x, y, w, h):
    """Saudi green field, white lines + sword, big checkmark: all clear."""
    d.rectangle([x, y, x + w, y + h], fill=(0, 106, 68))
    d.rectangle([x + 20, y + h * 0.16, x + w - 20, y + h * 0.16 + 3],
                fill=(255, 255, 255))
    d.rectangle([x + 20, y + h * 0.24, x + w - 20, y + h * 0.24 + 3],
                fill=(255, 255, 255))
    d.line([(x + w * 0.22, y + h * 0.34), (x + w * 0.78, y + h * 0.34)],
           fill=(255, 255, 255), width=4)
    cx, cy, r = x + w * 0.5, y + h * 0.48, 16
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=4)
    d.line([(cx - 11, cy), (cx - 3, cy + 8)], fill=(255, 255, 255), width=4)
    d.line([(cx - 3, cy + 8), (cx + 12, cy - 9)], fill=(255, 255, 255), width=4)
    f = font(SANS_B, 14)
    label = "ALL CLEAR"
    tw = d.textlength(label, font=f)
    d.text((x + (w - tw) / 2, y + h - 16), label, font=f, fill=(255, 255, 255))


def scene_ai_cyber(d, x, y, w, h):
    """Dark navy, green circuit traces, AI chip, amber warning triangle."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 18, 40))
    for i in range(4):
        yy = y + 10 + i * 12
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(40, 120, 90), width=1)
        for jx in (0.25, 0.5, 0.75):
            d.ellipse([x + w * jx - 3, yy - 3, x + w * jx + 3, yy + 3],
                      fill=(60, 200, 140))
    cx, cy = x + w * 0.5, y + h * 0.58
    d.rectangle([cx - 26, cy - 17, cx + 26, cy + 17], fill=(20, 30, 60),
                outline=(80, 200, 160), width=2)
    f = font(SANS_B, 16)
    t = "AI"
    tw = d.textlength(t, font=f)
    d.text((cx - tw / 2, cy - 11), t, font=f, fill=(120, 230, 180))
    tx, ty = x + w * 0.80, y + 8
    d.polygon([(tx, ty), (tx + 22, ty + 30), (tx - 22, ty + 30)],
              fill=(255, 200, 0))
    d.text((tx - 3, ty + 7), "!", font=font(SANS_B, 18), fill=(0, 0, 0))


# ------------------------------------------------------------------ layout
def masthead(d):
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.rectangle([0, 88, W, 92], fill=GOLD)
    f_title = font(SERIF_B, 27)
    f_date = font(SERIF_B, 42)
    f_side = font(SANS_B, 12)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 2), title, font=f_title, fill=(255, 255, 255))
    date = "Thursday 19 November 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 34), date, font=f_date, fill=GOLD)
    d.text((MX, 12), "EST. 2026", font=f_side, fill=(150, 162, 190))
    d.text((W - MX - 92, 12), "50 STORIES", font=f_side, fill=(150, 162, 190))


def region_bar(d):
    y = 92
    d.rectangle([0, y, W, 114], fill=(232, 226, 214))
    d.line([(0, 114), (W, 114)], fill=PANEL_LINE, width=1)
    f = font(SANS_B, 13)
    parts = [("50 STORIES", RED), ("EUROPE 8", INK), ("MIDDLE EAST 5", INK),
             ("ASIA 10", INK), ("AFRICA 4", INK), ("AMERICAS 14", INK),
             ("OCEANIA 2", INK), ("WORLD 7", INK)]
    # measure and centre the whole line
    sep = "  •  "
    total = d.textlength(sep.join(p[0] for p in parts), font=f)
    x = (W - total) / 2
    for i, (txt, col) in enumerate(parts):
        d.text((x, y + 4), txt, font=f, fill=col)
        x += d.textlength(txt, font=f)
        if i < len(parts) - 1:
            d.text((x, y + 4), sep, font=f, fill=GREY)
            x += d.textlength(sep, font=f)


def number_circle(d, x, y, n, r=13):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED,
              outline=(255, 255, 255), width=2)
    f = font(SANS_B, 15 if n < 10 else 13)
    t = str(n)
    tw = d.textlength(t, font=f)
    th = 15 if n < 10 else 13
    d.text((x - tw / 2, y - th / 2 - 1), t, font=f, fill=(255, 255, 255))


def scene_scaled(d, scene, x, y, w, h, scale=2):
    """Render a scene at 2x into a temp image, then downscale it.

    The v2 scenes were drawn for ~1000px-wide panels with fixed font
    sizes, so drawing them directly into a 194-326px box clips their
    internal text (e.g. VICE CITY, the measles tag). Rendering big and
    downscaling keeps every label proportional and readable. Pastes
    onto the module-level IMG (set by main()).
    """
    tmp = Image.new("RGB", (w * scale, h * scale), (255, 255, 255))
    td = ImageDraw.Draw(tmp)
    scene(td, 0, 0, w * scale, h * scale)
    tmp = tmp.resize((w, h), Image.LANCZOS)
    IMG.paste(tmp, (x, y))


def hero_panel(d, x, y, w, h, num, kicker, scene, headline, deck):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=PANEL_LINE, width=1)
    d.rectangle([x, y, x + w, y + 5], fill=RED)
    ih = 108
    scene_scaled(d, scene, x + 1, y + 6, w - 2, ih - 1)
    d.line([(x, y + 5 + ih), (x + w, y + 5 + ih)], fill=PANEL_LINE, width=1)
    number_circle(d, x + 18, y + 20, num, r=14)
    ty = y + 5 + ih + 7
    f_kick = font(SANS_B, 11)
    d.text((x + 10, ty), kicker, font=f_kick, fill=dark(RED, 0.85))
    ty += 15
    f_head = font(SERIF_B, 19)
    head_lines = wrap(d, headline, f_head, w - 20)[:2]
    for i, line in enumerate(head_lines):
        d.text((x + 10, ty + i * 21), line, font=f_head, fill=INK)
    ty += 21 * len(head_lines) + 2
    f_deck = font(SANS, 12)
    max_deck = max(0, (y + h - 4 - ty) // 15)
    for i, line in enumerate(wrap(d, deck, f_deck, w - 20)[:max_deck]):
        d.text((x + 10, ty + i * 15), line, font=f_deck, fill=DECK)


def card_panel(d, x, y, w, h, num, kicker, scene, headline, deck,
               bg=(255, 255, 255), accent=RED):
    d.rectangle([x, y, x + w, y + h], fill=bg, outline=PANEL_LINE, width=1)
    d.rectangle([x, y, x + w, y + 5], fill=accent)
    ih = 60
    scene_scaled(d, scene, x + 1, y + 6, w - 2, ih - 1)
    d.line([(x, y + 5 + ih), (x + w, y + 5 + ih)], fill=PANEL_LINE, width=1)
    number_circle(d, x + 14, y + 16, num, r=11)
    ty = y + 5 + ih + 5
    f_kick = font(SANS_B, 10)
    d.text((x + 8, ty), kicker, font=f_kick, fill=dark(accent, 0.72))
    ty += 13
    f_head = font(SERIF_B, 14)
    head_lines = wrap(d, headline, f_head, w - 16)[:2]
    for i, line in enumerate(head_lines):
        d.text((x + 8, ty + i * 16), line, font=f_head, fill=INK)
    ty += 16 * len(head_lines) + 1
    f_deck = font(SANS, 10)
    max_deck = max(0, (y + h - 4 - ty) // 13)
    for i, line in enumerate(wrap(d, deck, f_deck, w - 16)[:max_deck]):
        d.text((x + 8, ty + i * 13), line, font=f_deck, fill=DECK)


# Dotted world map: 30 columns x 11 rows, '#' = land.
MAP_ROWS = [
    "..####..................######..",
    ".######....###..###...#########.",
    "..#####....####.###..##########.",
    "...####.....########.########..",
    "....##.......######..######....",
    ".....##......#####....###......",
    ".....###.....####....##........",
    "......##......###.............",
    "......##......##.....####.....",
    ".......#..............###.....",
    "......................##.....",
]
MAP_PINS = [  # (col, row, label) — key story locations
    (2, 1, "ALASKA"), (5, 2, "WASHINGTON"), (14, 2, "THE HAGUE"),
    (16, 2, "KYIV"), (15, 4, "GAZA"), (24, 2, "SHENZHEN"),
    (20, 4, "NEW DELHI"), (16, 4, "RIYADH"), (25, 8, "CANBERRA"),
]


def world_map(d, x, y, w, h):
    cols = len(MAP_ROWS[0])
    rows = len(MAP_ROWS)
    sx = w / cols
    sy = h / rows
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                cx = x + (c + 0.5) * sx
                cy = y + (r + 0.5) * sy
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(120, 120, 120))
    for c, r, _label in MAP_PINS:
        cx = x + (c + 0.5) * sx
        cy = y + (r + 0.5) * sy
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED,
                  outline=(255, 255, 255), width=1)


def also_on(d, x, y, w, h, items):
    f_head = font(SERIF_B, 17)
    d.text((x, y), "ALSO ON THURSDAY 19 NOVEMBER", font=f_head, fill=INK)
    d.rectangle([x, y + 24, x + w, y + 27], fill=RED)
    col_w = (w - 2 * 12) // 3
    f_item = font(SANS, 11)
    f_num = font(SANS_B, 11)
    pitch = 24
    per_col = [13, 12, 12]
    idx = 0
    for ci, count in enumerate(per_col):
        cx = x + ci * (col_w + 12)
        for j in range(count):
            num, headline = items[idx]
            idx += 1
            iy = y + 34 + j * pitch
            d.text((cx, iy), f"{num}.", font=f_num, fill=RED)
            num_w = d.textlength(f"{num}. ", font=f_num)
            # truncate the headline to one fitting line
            max_w = col_w - num_w - 2
            txt = headline
            while d.textlength(txt, font=f_item) > max_w and len(txt) > 4:
                txt = txt[:-4] + "…"
            d.text((cx + num_w, iy), txt, font=f_item, fill=INK)


def date_check(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    d.rectangle([x, y, x + w, y + 24], fill=RED)
    f_h = font(SANS_B, 13)
    d.text((x + 10, y + 5), "DATE CHECK", font=f_h, fill=(255, 255, 255))
    f_b = font(SERIF_B, 15)
    d.text((x + 10, y + 32), "Thursday 19 November 2026", font=f_b, fill=INK)
    f_s = font(SANS, 11)
    for i, line in enumerate(wrap(d, "All 50 stories verified from reports "
                                  "published on the day. Sources: Reuters, "
                                  "AP, AFP, NASA, ICJ, IMF — see STORIES.md.",
                                  f_s, w - 20)):
        d.text((x + 10, y + 54 + i * 14), line, font=f_s, fill=DECK)


def footer(d):
    y = H - 28
    d.line([(MX, y), (W - MX, y)], fill=PANEL_LINE, width=1)
    f = font(SANS_B, 11)
    line = "THE WORLD TODAY  •  THURSDAY 19 NOVEMBER 2026  •  50 STORIES, SEVEN REGIONS, ONE DAY"
    tw = d.textlength(line, font=f)
    d.text(((W - tw) / 2, y + 7), line, font=f, fill=GREY)


def main():
    global IMG
    img = Image.new("RGB", (W, H), PAPER)
    IMG = img
    d = ImageDraw.Draw(img)
    masthead(d)
    region_bar(d)
    # --- three big illustrated lead stories -------------------------------
    heroes = [
        (1, "WORLD  •  GLOBAL", scene_vice_city,
         "VICE CITY OPENS",
         "GTA VI rolls out worldwide at midnight — 13 years after GTA V, "
         "a $1bn epic."),
        (2, "SUMMIT  •  SHENZHEN", scene_shenzhen,
         "Trump, Xi & Putin meet today",
         "First trilateral of the three presidents."),
        (3, "JUSTICE  •  THE HAGUE", scene_hague,
         "World court rules on Rohingya",
         "ICJ delivers its verdict on Myanmar."),
    ]
    gap = 8
    hw = (CW - 2 * gap) // 3
    hh = 208
    hy = 120
    for i, (num, kick, scene, head, deck) in enumerate(heroes):
        hero_panel(d, MX + i * (hw + gap), hy, hw, hh,
                   num, kick, scene, head, deck)
    # --- ten numbered illustrated cards, 2 rows x 5 -----------------------
    # (kicker, scene, headline, deck, pastel bg, accent)
    panels = [
        ("SPACE  •  DEEP SPACE", scene_voyager,
         "Voyager 1, a light-day away",
         "A 49-year-old probe sets a record.",
         (199, 237, 232), (0, 120, 110)),
        ("EUROPE  •  BRUSSELS", scene_eu_ukraine,
         "EU proposes €45bn for Kyiv",
         "Loan covers Ukraine's budget gap.",
         (252, 240, 192), (180, 140, 0)),
        ("MIDDLE EAST  •  GAZA", scene_gaza,
         "Troops cross the Yellow Line",
         "Israeli forces push into Gaza.",
         (248, 220, 194), (200, 100, 20)),
        ("HEALTH  •  AMERICA", scene_measles,
         "US loses measles-free status",
         "Elimination ends after 26 years.",
         (249, 213, 213), (178, 34, 34)),
        ("SANCTIONS  •  CANBERRA", scene_australia,
         "Australia sanctions settlers",
         "Canberra blacklists Israeli settlers.",
         (211, 238, 210), (30, 120, 50)),
        ("WEATHER  •  INDIA", scene_cyclone,
         "Cyclone Akvan nears India",
         "Storm nears India's east coast.",
         (220, 226, 235), (70, 90, 120)),
        ("POLITICS  •  ALASKA", scene_alaska,
         "Peltola wins Alaska",
         "Democrats take the Senate 56–44.",
         (253, 233, 200), (190, 130, 0)),
        ("DIPLOMACY  •  OTTAWA", scene_canada_china,
         "Canada resets China ties",
         "Carney reopens ties with Beijing.",
         (234, 242, 210), (120, 150, 30)),
        ("MIDDLE EAST  •  RIYADH", scene_saudi,
         "Saudi: danger has passed",
         "All-clear in three southern cities.",
         (210, 234, 217), (0, 106, 68)),
        ("TECH  •  WASHINGTON", scene_ai_cyber,
         "AI cyber threats surge",
         "US senators warn attacks outpace defences.",
         (242, 216, 236), (170, 40, 130)),
    ]
    cgap = 6
    pw = (CW - 4 * cgap) // 5
    ph = 144
    py = 336
    for row in range(2):
        for col in range(5):
            p = panels[row * 5 + col]
            card_panel(d, MX + col * (pw + cgap), py + row * (ph + cgap),
                       pw, ph, 4 + row * 5 + col,
                       p[0], p[1], p[2], p[3], bg=p[4], accent=p[5])
    # --- bottom zone: map + DATE CHECK (left), ALSO ON list (right) -------
    by = 638
    bh = 352
    map_w = 292
    d.rectangle([MX, by, MX + map_w, by + bh], fill=(255, 255, 255),
                outline=PANEL_LINE, width=1)
    f_map = font(SANS_B, 13)
    d.text((MX + 10, by + 8), "WHERE IT HAPPENED", font=f_map, fill=RED)
    world_map(d, MX + 10, by + 32, map_w - 20, 150)
    date_check(d, MX + 10, by + 192, map_w - 20, bh - 202)
    also_items = [
        (14, "Coalition meets in Berlin on Ukraine"),
        (15, "Russian strike kills 4 in Odesa"),
        (16, "Lavrov accuses France on troops"),
        (17, "IMF lifts Germany growth to 1.3%"),
        (18, "Drought hits 82% of England"),
        (19, "LPG tanker sunk in the Black Sea"),
        (20, "ATP Finals: Zverev faces Fils"),
        (21, "Board of Peace faults Israel, Hamas"),
        (22, "Iran hits US airbase in Kuwait"),
        (23, "US jets hit Qeshm missile site"),
        (24, "IMF unlocks $2.3bn for Egypt"),
        (25, "Ethiopia, Eritrea mass troops"),
        (26, "Amnesty: RSF raids are war crimes"),
        (27, "Nigeria kills 21 ISWAP fighters"),
        (28, "India, Japan hold 2+2 talks"),
        (29, "Korea, China agree FTA push"),
        (30, "Indonesia passes asset-seizure bill"),
        (31, "Bangladesh deploys paramilitary"),
        (32, "Mongolia debates president's exit"),
        (33, "Japan visitors hit record 3.91m"),
        (34, "ASEAN advances digital pact"),
        (35, "ASEAN chief visits Pakistan"),
        (36, "Anthropic debuts on Nasdaq at $83"),
        (37, "Nvidia posts $115.8bn quarter"),
        (38, "Fed minutes back a rate rise"),
        (39, "Dow falls 561 points"),
        (40, "UnitedHealth slides 10.2%"),
        (41, "Brazil Senate backs Lula fiscal plan"),
        (42, "FAA grounds router after stop"),
        (43, "Jeffries nominated House Speaker"),
        (44, "Newsom seeks AI kill-switch"),
        (45, "SpaceX launches secret USSF-317"),
        (46, "Australia reserves gas for home use"),
        (47, "Kelp wins a seat at COP31"),
        (48, "COP31 deadlocked on fossil fuels"),
        (49, "COP31 urged to tax big polluters"),
        (50, "Oracle patches 655 flaws, 948 CVEs"),
    ]
    also_on(d, MX + map_w + 8, by, CW - map_w - 8, bh, also_items)
    footer(d)
    out = os.path.join(HERE, "entry.png")
    img.save(out, "JPEG", quality=88, optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
