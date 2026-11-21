#!/usr/bin/env python3
"""THE WORLD -- Saturday 21 November 2026 front page.

Draws one newspaper front page summing up the world news of
Saturday 21 November 2026 and saves it as a 1024x1024 PNG in
$MAKEFUN_OUTPUT_DIR (default /output). Python 3 standard library
only: a flat RGB canvas, a hand-drawn 5x7 letter set, shape drawing
and a from-scratch PNG encoder. No network, no randomness, no
clock: two runs write byte-identical files.

Stories on the page, each first reported on 21 November 2026:
  PERU    A magnitude 6.8 quake strikes Junin in the Andes at
          19:09 local time; felt in Lima 320 km away, where
          residents and lawmakers leave buildings. No deaths
          or major damage reported; depth 129 km. (Reuters.)
  COP31   Climate talks in Antalya slip into overtime with no
          deal; fossil-fuel wording is cut from the draft and
          a third text is promised for Saturday morning.
          (AP; Reuters.)
  KRYVYI  A Russian strike on Kryvyi Rih kills 2 and injures
          42, among them four children. (City officials.)
  GEN Z   Thousands rally across 25 European countries over
          living costs, military spending and climate.
          (Al Jazeera.)
  BRIEFS  Denmark expels a Russian diplomat over an alleged
          plot to kill a Ukrainian rapper; Mamdani sets 2032
          to close Rikers Island; KL Rahul completes the SENA
          set with a century in Wellington; foreign investors
          pour a record Rs 1.22 lakh crore into Indian shares;
          Cyclone Akvan leaves no major damage in Odisha after
          3.72 lakh people were moved to safety.
"""

import math
import os
import struct
import zlib

EDGE = 1024

INK = (26, 24, 20)
PAPER = (247, 242, 228)
PALE = (233, 227, 211)
RED = (168, 32, 32)
BLUE = (30, 80, 122)
NAVY = (15, 27, 50)
NIGHT = (10, 20, 38)
GOLD = (186, 140, 32)
ORANGE = (216, 112, 30)
GREEN = (47, 126, 51)
SKY = (178, 218, 242)
SEA = (35, 92, 112)
ROCK = (96, 78, 62)
SNOW = (244, 246, 248)
WHITE = (255, 255, 255)
GREY = (122, 118, 110)
DUSK = (54, 66, 86)
BROWN = (122, 88, 52)

# ------------------------------------------------------------------ glyphs
# Hand-drawn 5x7 letters. Each glyph is seven rows of five cells;
# "1" means ink, "0" means blank. Only capitals, digits and a few
# punctuation marks are needed, so only those are defined.

GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01110"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00010", "00100", "00100", "00100"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "00000"),
    ",": ("00000", "00000", "00000", "00000", "00000", "01100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00011", "00100", "01000", "01000", "01000", "00100", "00011"),
    ")": ("11000", "00100", "00010", "00010", "00010", "00100", "11000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "'": ("00100", "00100", "00100", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "01100", "01000"),
}


# ------------------------------------------------------------------ canvas
class Canvas:
    """A flat RGB buffer with drawing helpers."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = c[0]
            self.px[i + 1] = c[1]
            self.px[i + 2] = c[2]

    def fill(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                j = base + (xx - x0) * 3
                self.px[j] = c[0]
                self.px[j + 1] = c[1]
                self.px[j + 2] = c[2]

    def hline(self, x, y, w, c, t=1):
        self.fill(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.fill(x, y, t, h, c)

    def box(self, x, y, w, h, c, t=1):
        self.hline(x, y, w, c, t)
        self.hline(x, y + h - t, w, c, t)
        self.vline(x, y, h, c, t)
        self.vline(x + w - t, y, h, c, t)

    def line(self, x0, y0, x1, y1, c):
        # Bresenham.
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.put(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            dy = yy - cy
            half = int((r * r - dy * dy) ** 0.5)
            self.fill(cx - half, yy, half * 2 + 1, 1, c)

    def tri(self, x0, y0, x1, y1, x2, y2, c):
        # Scanline-filled triangle.
        pts = sorted(((x0, y0), (x1, y1), (x2, y2)), key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        if ay == cy:
            return

        def at(y, px, py, qx, qy):
            if py == qy:
                return px
            return px + (qx - px) * (y - py) / (qy - py)

        for y in range(ay, cy + 1):
            if y < by:
                xa = at(y, ax, ay, bx, by)
                xb = at(y, ax, ay, cx, cy)
            else:
                xa = at(y, bx, by, cx, cy)
                xb = at(y, ax, ay, cx, cy)
            lo = int(min(xa, xb))
            hi = int(max(xa, xb))
            self.fill(lo, y, hi - lo + 1, 1, c)

    def quad(self, x0, y0, x1, y1, x2, y2, x3, y3, c):
        self.tri(x0, y0, x1, y1, x2, y2, c)
        self.tri(x0, y0, x2, y2, x3, y3, c)

    # ------------------------------------------------------------- text
    def text(self, s, x, y, scale, c):
        cx = x
        for ch in s:
            g = GLYPHS.get(ch)
            if g is None:
                cx += 6 * scale
                continue
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.fill(cx + col * scale, y + row * scale,
                                  scale, scale, c)
            cx += 6 * scale
        return cx

    def twidth(self, s, scale):
        return len(s) * 6 * scale - scale

    def centre(self, s, cx, y, scale, c):
        self.text(s, cx - self.twidth(s, scale) // 2, y, scale, c)

    def wrap(self, s, scale, max_w):
        words = s.split(" ")
        lines = []
        cur = ""
        for wd in words:
            trial = wd if not cur else cur + " " + wd
            if self.twidth(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, s, x, y, scale, max_w, c, lead=None):
        if lead is None:
            lead = 7 * scale + 3
        for ln in self.wrap(s, scale, max_w):
            self.text(ln, x, y, scale, c)
            y += lead
        return y


# -------------------------------------------------------------------- png
def write_png(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    return png


# ------------------------------------------------------------ picture bits
def seismo(cv, x, y, w, c):
    # A seismograph trace: flat, then a violent zigzag, then calm.
    pts = []
    n = 46
    for i in range(n + 1):
        px = x + i * w // n
        if i < 8 or i > 38:
            py = y + (1 if i % 2 else -1)
        elif i < 14:
            py = y + (-6 if i % 2 else 6)
        elif i < 30:
            py = y + (-16 if i % 2 else 16)
        else:
            py = y + (-8 if i % 2 else 8)
        pts.append((px, py))
    for a, b in zip(pts, pts[1:]):
        cv.line(a[0], a[1], b[0], b[1], c)
        cv.line(a[0], a[1] + 1, b[0], b[1] + 1, c)


def mountain(cv, x, base, w, h, c, snow=True):
    cv.tri(x, base, x + w // 2, base - h, x + w, base, c)
    if snow:
        top = (x + w // 2, base - h)
        cv.tri(top[0] - w // 8, base - h + h // 4, top[0], top[1],
               top[0] + w // 8, base - h + h // 4, SNOW)


def crack(cv, x, y, w, c):
    # A jagged ground crack running left to right.
    px, py = x, y
    seg = 0
    while px < x + w:
        nx = px + 26 + (seg * 17) % 22
        ny = y + (-7 if seg % 2 else 7) + (seg % 3 - 1) * 3
        cv.line(px, py, nx, ny, c)
        cv.line(px, py + 1, nx, ny + 1, c)
        px, py = nx, ny
        seg += 1


def leaning_block(cv, x, y, w, h, lean, c, lit):
    # A building leaning by `lean` pixels at the top.
    cv.quad(x, y + h, x + lean, y, x + w + lean, y, x + w, y + h, c)
    for wy in range(y + 8, y + h - 6, 14):
        for wx in range(x + 5, x + w - 4, 12):
            if (wx * 3 + wy * 5) % 5 < 2:
                cv.fill(wx + (wy - y) * lean // h, wy, 4, 5, lit)


def flame(cv, x, y, s):
    cv.tri(x, y, x + 3 * s, y - 6 * s, x + 6 * s, y, ORANGE)
    cv.tri(x + s, y, x + 3 * s, y - 4 * s, x + 5 * s, y, GOLD)
    cv.tri(x + 2 * s, y, x + 3 * s, y - 2 * s, x + 4 * s, y, RED)


def globe(cv, cx, cy, r):
    cv.disc(cx, cy, r, (62, 132, 202))
    cv.disc(cx - r // 3, cy - r // 4, r // 3, GREEN)
    cv.disc(cx + r // 3, cy + r // 3, r // 4, GREEN)
    cv.disc(cx + r // 4, cy - r // 2, r // 5, GREEN)
    cv.fill(cx - r, cy - 2, 2 * r, 3, (202, 222, 242))


def clock_face(cv, cx, cy, r):
    cv.disc(cx, cy, r, WHITE)
    cv.disc(cx, cy, r - 2, PAPER)
    for i in range(12):
        ang = i * 30 * math.pi / 180.0
        cv.line(cx + int((r - 4) * math.sin(ang)),
                cy - int((r - 4) * math.cos(ang)),
                cx + int((r - 8) * math.sin(ang)),
                cy - int((r - 8) * math.cos(ang)), INK)
    cv.line(cx, cy, cx, cy - r + 6, INK)
    cv.line(cx, cy, cx + r - 8, cy + 4, INK)
    cv.disc(cx, cy, 2, RED)


def tower_block(cv, x, base, w, c, lit):
    bx = x
    i = 0
    while bx < x + w - 16:
        bw = 20 + (i * 31) % 24
        bh = 24 + (i * 43) % 42
        top = base - bh
        cv.fill(bx, top, bw, bh, c)
        for wy in range(top + 6, base - 5, 12):
            for wx in range(bx + 4, bx + bw - 3, 10):
                if (wx * 5 + wy * 7 + i) % 4 < 2:
                    cv.fill(wx, wy, 3, 4, lit)
        bx += bw + 5
        i += 1


def streak(cv, x0, y0, x1, y1):
    cv.line(x0, y0, x1, y1, (255, 222, 122))
    cv.line(x0, y0 + 1, x1, y1 + 1, (255, 162, 62))
    cv.disc(x1, y1, 3, (255, 242, 182))


def placard(cv, x, y, s, c, word):
    w = max(7 * s, cv.twidth(word, 1) + s)
    cv.line(x + w // 2, y + 2 * s, x + w // 2, y + 9 * s, INK)
    cv.fill(x, y, w, 3 * s, c)
    cv.box(x, y, w, 3 * s, INK, 1)
    cv.text(word, x + s // 2, y + s, 1, INK)


def head_row(cv, x, y, w, skin, shirt):
    # A row of marchers: heads and shoulders.
    hx = x
    i = 0
    while hx < x + w - 12:
        cv.disc(hx + 6, y + 7, 6, skin)
        cv.fill(hx, y + 14, 13, 8, shirt if i % 2 == 0 else BLUE)
        hx += 22
        i += 1


# ------------------------------------------------------------------- lead
def lead_quake(cv):
    cv.box(24, 146, 976, 326, INK, 2)
    cv.centre("QUAKE SHAKES PERU", 512, 160, 6, INK)
    cv.centre("MAGNITUDE 6.8 HITS JUNIN - FELT IN LIMA", 512, 210, 3, RED)
    cv.centre("NO DEATHS REPORTED - 129 KM DEEP - STREETS AND CONGRESS EVACUATED",
              512, 236, 2, INK)
    # Andes under a shaking sky: peaks, a seismograph trace, a
    # cracked valley floor and leaning Lima blocks below.
    cv.fill(32, 256, 960, 208, SKY)
    cv.disc(892, 288, 18, GOLD)
    mountain(cv, 40, 400, 260, 120, ROCK)
    mountain(cv, 240, 400, 300, 150, BROWN)
    mountain(cv, 500, 400, 260, 110, ROCK)
    mountain(cv, 720, 400, 240, 140, BROWN)
    seismo(cv, 60, 300, 500, RED)
    cv.fill(32, 400, 960, 64, (168, 138, 96))
    crack(cv, 40, 424, 940, INK)
    leaning_block(cv, 90, 386, 44, 62, 8, NAVY, GOLD)
    leaning_block(cv, 180, 392, 38, 56, -7, (30, 44, 70), GOLD)
    leaning_block(cv, 800, 388, 46, 60, -9, NAVY, GOLD)
    leaning_block(cv, 880, 394, 38, 54, 7, (30, 44, 70), GOLD)
    cv.fill(32, 440, 960, 24, SEA)
    for wx in range(44, 980, 36):
        cv.line(wx, 452, wx + 12, 446, WHITE)
        cv.line(wx + 12, 446, wx + 24, 452, WHITE)


# ------------------------------------------------------------- mid panels
def panel_cop(cv, x):
    cv.box(x, 488, 320, 250, INK, 2)
    cv.text("CLIMATE", x + 10, 498, 2, RED)
    cv.text("COP31 IN", x + 10, 518, 3, INK)
    cv.text("OVERTIME", x + 10, 542, 3, INK)
    # Antalya: a warming globe, a clock running past the deadline,
    # and a red FAILURE banner across the hall.
    cv.fill(x + 8, 570, 304, 92, SKY)
    globe(cv, x + 90, 616, 30)
    clock_face(cv, x + 230, 606, 26)
    cv.fill(x + 8, 640, 304, 22, SEA)
    for wx in range(x + 16, x + 300, 34):
        cv.line(wx, 652, wx + 12, 646, WHITE)
        cv.line(wx + 12, 646, wx + 24, 652, WHITE)
    cv.fill(x + 60, 574, 184, 16, RED)
    cv.centre("FAILURE", x + 152, 578, 2, WHITE)
    cv.para("NO DEAL IN ANTALYA - FOSSIL FUELS CUT FROM DRAFT - NEW TEXT DUE SATURDAY",
            x + 10, 672, 2, 300, INK)


def panel_kryvyi(cv, x):
    cv.box(x, 488, 320, 250, INK, 2)
    cv.text("UKRAINE", x + 10, 498, 2, RED)
    cv.text("MISSILES HIT", x + 10, 518, 3, INK)
    cv.text("KRYVYI RIH", x + 10, 542, 3, INK)
    # Night city, incoming missiles, a burning block.
    cv.fill(x + 8, 570, 304, 92, NIGHT)
    for i in range(16):
        sx = x + 8 + (i * 89 + 7) % 304
        sy = 570 + (i * 37 + 3) % 36
        cv.put(sx, sy, WHITE)
    tower_block(cv, x + 8, 662, 304, NIGHT, GOLD)
    streak(cv, x + 40, 578, x + 92, 624)
    streak(cv, x + 262, 574, x + 212, 620)
    streak(cv, x + 152, 572, x + 152, 610)
    flame(cv, x + 132, 652, 4)
    flame(cv, x + 152, 656, 3)
    cv.para("2 DEAD, 42 HURT - FOUR OF THEM CHILDREN - AS STRIKE HITS CITY",
            x + 10, 672, 2, 300, INK)


def panel_protest(cv, x):
    cv.box(x, 488, 320, 250, INK, 2)
    cv.text("EUROPE", x + 10, 498, 2, RED)
    cv.text("GEN Z TAKES", x + 10, 518, 3, INK)
    cv.text("TO THE STREETS", x + 10, 542, 3, INK)
    # A marching crowd with placards under a pale sky.
    cv.fill(x + 8, 570, 304, 92, PALE)
    placard(cv, x + 40, 576, 3, WHITE, "FUTURE")
    placard(cv, x + 150, 580, 3, GOLD, "NO WAR")
    placard(cv, x + 240, 576, 2, WHITE, "RENT")
    head_row(cv, x + 14, 622, 292, (214, 164, 120), RED)
    cv.fill(x + 8, 646, 304, 16, GREY)
    for dx in range(16, 304, 40):
        cv.fill(x + 8 + dx, 652, 18, 2, WHITE)
    cv.para("THOUSANDS MARCH IN 25 COUNTRIES OVER COSTS, WAR AND CLIMATE",
            x + 10, 672, 2, 300, INK)


# ------------------------------------------------------------------- briefs
def icon_denmark(cv, x, y):
    cv.fill(x, y, 34, 34, RED)
    cv.fill(x + 10, y, 5, 34, WHITE)
    cv.fill(x, y + 14, 34, 5, WHITE)


def icon_bars(cv, x, y):
    cv.fill(x, y, 34, 34, NAVY)
    for bx in range(x + 5, x + 30, 7):
        cv.fill(bx, y + 3, 3, 28, GOLD)


def icon_bat(cv, x, y):
    cv.fill(x, y, 34, 34, GREEN)
    cv.line(x + 10, y + 26, x + 22, y + 8, (232, 202, 142))
    cv.line(x + 12, y + 26, x + 24, y + 8, (232, 202, 142))
    cv.fill(x + 20, y + 4, 6, 10, (232, 202, 142))
    cv.disc(x + 26, y + 26, 4, RED)


def icon_chart(cv, x, y):
    cv.fill(x, y, 34, 34, BLUE)
    cv.line(x + 4, y + 28, x + 12, y + 20, WHITE)
    cv.line(x + 12, y + 20, x + 20, y + 22, WHITE)
    cv.line(x + 20, y + 22, x + 30, y + 6, WHITE)
    cv.line(x + 24, y + 6, x + 30, y + 6, WHITE)
    cv.line(x + 30, y + 6, x + 30, y + 12, WHITE)


def icon_spiral(cv, x, y):
    cv.fill(x, y, 34, 34, DUSK)
    cv.disc(x + 17, y + 17, 12, SKY)
    cv.disc(x + 17, y + 17, 8, DUSK)
    cv.disc(x + 17, y + 17, 4, SKY)
    cv.line(x + 17, y + 17, x + 29, y + 17, WHITE)


BRIEFS = (
    (icon_denmark, "DENMARK EXPELS RUSSIAN DIPLOMAT IN 'PLOT' ROW"),
    (icon_bars, "MAMDANI: RIKERS JAIL TO CLOSE BY 2032"),
    (icon_bat, "RAHUL 100 IN WELLINGTON - SENA SET COMPLETE"),
    (icon_chart, "INDIA: RECORD RS 1.22 LAKH CRORE INFLOW"),
    (icon_spiral, "AKVAN: NO MAJOR DAMAGE - 3.72 LAKH MOVED"),
)


def briefs_strip(cv):
    cv.hline(24, 754, 976, INK, 2)
    cv.text("ALSO TODAY", 24, 762, 3, RED)
    cv.hline(24, 788, 976, INK, 1)
    for i, (icon, words) in enumerate(BRIEFS):
        x = 24 + i * 199
        icon(cv, x, 798)
        cv.para(words, x, 840, 2, 185, INK)


# -------------------------------------------------------------- furniture
def masthead(cv):
    cv.hline(24, 6, 976, INK, 2)
    cv.hline(24, 12, 976, INK, 1)
    cv.centre("THE WORLD", 512, 20, 11, INK)
    cv.fill(196, 52, 12, 12, RED)
    cv.fill(816, 52, 12, 12, RED)
    cv.hline(24, 106, 976, INK, 2)
    cv.centre("SATURDAY 21 NOVEMBER 2026", 512, 112, 3, INK)
    cv.hline(24, 138, 976, INK, 3)


def colophon(cv):
    cv.hline(24, 958, 976, INK, 2)
    cv.centre("THE WORLD - SATURDAY 21 NOVEMBER 2026 - ONE DAY, ONE PAGE",
              512, 968, 2, INK)
    cv.centre("ALL STORIES FIRST REPORTED 21 NOVEMBER 2026", 512, 988, 2, RED)
    cv.hline(24, 1012, 976, INK, 2)


def main():
    cv = Canvas(EDGE, EDGE, PAPER)
    masthead(cv)
    lead_quake(cv)
    panel_cop(cv, 24)
    panel_kryvyi(cv, 352)
    panel_protest(cv, 680)
    briefs_strip(cv)
    colophon(cv)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(write_png(cv))
    print("wrote", path)


if __name__ == "__main__":
    main()
