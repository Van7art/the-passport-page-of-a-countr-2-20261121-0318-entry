#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There — Republic of Solmaria.

Self-contained renderer: pure Python 3.13 stdlib, no network, no Pillow.
Draws an open passport spread (data page + visas page) and writes it to
/output/entry.png. Deterministic: same bytes on every run.

DRAFT (step 1 of 2): complete first version; a revision pass follows after
a visual check of the rendered output.

REVISION (step 2 of 2): after viewing the draft render — lowercase letters
were missing from the font (signature and handwritten note showed blanks),
the officer's-note lines ran past the right page border, and the portrait
hair blobs sat too low. Fixed: lowercase falls back to the uppercase glyph,
note block moved left and shortened, hair raised.
"""

import hashlib
import math
import struct
import zlib
from pathlib import Path

W = H = 1024

# ---------------------------------------------------------------------------
# 5x7 bitmap font: each glyph is 7 rows of 5 bits ("1" = ink).
# ---------------------------------------------------------------------------
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
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
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
}

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
PAPER = (239, 230, 208)
INK = (31, 42, 68)
INK_SOFT = (74, 84, 110)
GOLD = (176, 141, 63)
SEA = (178, 205, 208)
LAND = (214, 206, 164)
SKIN = (232, 195, 154)
HAIR = (58, 42, 30)
NAVY = (38, 54, 96)
WHITE = (245, 244, 238)
STAMP_PURPLE = (91, 58, 142)
STAMP_BLUE = (43, 76, 155)
STAMP_RED = (163, 58, 46)
STAMP_GREEN = (46, 107, 74)
HAND_BLUE = (44, 62, 140)


def _det_hash(x, y):
    """Deterministic pseudo-random 0..255 from integer coords."""
    h = (x * 73856093) ^ (y * 19349663)
    h = (h ^ (h >> 13)) * 1274126177
    return (h ^ (h >> 16)) & 0xFF


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(bytes(bg) * (w * h))

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.buf[i:i + len(row)] = row

    def border(self, x, y, w, h, c, t=2):
        self.rect(x, y, w, t, c)
        self.rect(x, y + h - t, w, t, c)
        self.rect(x, y, t, h, c)
        self.rect(x + w - t, y, t, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=False):
        if fill:
            for yy in range(cy - r, cy + r + 1):
                d = r * r - (yy - cy) ** 2
                half = int(d ** 0.5) if d >= 0 else 0
                for xx in range(cx - half, cx + half + 1):
                    self.px(xx, yy, c)
        else:
            steps = max(8, int(2 * math.pi * r))
            for i in range(steps):
                a = 2 * math.pi * i / steps
                self.px(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), c)

    def ellipse(self, cx, cy, rx, ry, c, fill=True):
        for yy in range(cy - ry, cy + ry + 1):
            t = 1 - ((yy - cy) / ry) ** 2
            if t < 0:
                continue
            half = int(rx * t ** 0.5)
            if fill:
                for xx in range(cx - half, cx + half + 1):
                    self.px(xx, yy, c)
            else:
                self.px(cx - half, yy, c)
                self.px(cx + half, yy, c)

    def poly(self, pts, c):
        """Scanline fill of a simple polygon."""
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    t = (y - y0) / (y1 - y0)
                    xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                for x in range(int(xs[j]), int(xs[j + 1]) + 1):
                    self.px(x, y, c)

    def text(self, x, y, s, scale, c, slant=0):
        cx = x
        for ch in s:
            glyph = FONT.get(ch) or FONT.get(ch.upper(), FONT[" "])
            for row in range(7):
                bits = glyph[row]
                shift = int((6 - row) * slant)
                for col in range(5):
                    if bits[col] == "1":
                        for dy in range(scale):
                            for dx in range(scale):
                                self.px(cx + col * scale + dx + shift,
                                        y + row * scale + dy, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_center(self, x, y, s, scale, c, width=None, slant=0):
        w = self.text_w(s, scale)
        start = x + (width - w) // 2 if width else x - w // 2
        self.text(start, y, s, scale, c, slant)


# ---------------------------------------------------------------------------
# MRZ (ICAO 9303, weights 7-3-1)
# ---------------------------------------------------------------------------
_MRZ_VALS = {ch: i for i, ch in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ<")}


def _mrz_cd(s):
    total = 0
    for i, ch in enumerate(s):
        total += _MRZ_VALS[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<SMRSOLENNE<<MARA"
    line1 = line1 + "<" * (44 - len(line1))
    doc, nat = "SM0417829", "SMR"
    dob, sex, exp = "880512", "F", "340314"
    personal = "<" * 14
    body = (doc + _mrz_cd(doc) + nat + dob + _mrz_cd(dob) + sex + exp
            + _mrz_cd(exp) + personal + _mrz_cd(personal))
    line2 = body + _mrz_cd(body)
    return line1, line2


# ---------------------------------------------------------------------------
# Portrait: lighthouse keeper, navy uniform, halftone texture
# ---------------------------------------------------------------------------
def draw_portrait(cv, x, y, w, h):
    cv.rect(x, y, w, h, (127, 163, 160))
    cv.rect(x, y, w, h // 3, (143, 176, 172))
    cv.rect(x, y + int(h * 0.62), w, h - int(h * 0.62), (96, 138, 148))
    # distant lighthouse silhouette
    lx, ly = x + w - 52, y + 58
    cv.poly([(lx, ly + 46), (lx + 8, ly), (lx + 16, ly + 46)], (70, 96, 110))
    cv.rect(lx + 5, ly - 8, 6, 8, (70, 96, 110))
    cv.circle(lx + 8, ly - 4, 4, (240, 220, 140), fill=True)
    # shoulders / uniform
    cx = x + w // 2
    cv.poly([(cx - 88, y + h), (cx - 74, y + 196), (cx - 30, y + 178),
             (cx + 30, y + 178), (cx + 74, y + 196), (cx + 88, y + h)], NAVY)
    # collar + shirt
    cv.poly([(cx - 16, y + 182), (cx, y + 208), (cx + 16, y + 182)], WHITE)
    cv.poly([(cx - 30, y + 180), (cx - 16, y + 182), (cx, y + 208),
             (cx - 30, y + 196)], (220, 222, 226))
    cv.poly([(cx + 30, y + 180), (cx + 16, y + 182), (cx, y + 208),
             (cx + 30, y + 196)], (220, 222, 226))
    # gold buttons + epaulettes
    cv.circle(cx - 52, y + 216, 4, GOLD, fill=True)
    cv.circle(cx + 52, y + 216, 4, GOLD, fill=True)
    cv.circle(cx, y + 232, 4, GOLD, fill=True)
    cv.rect(cx - 78, y + 192, 26, 7, GOLD)
    cv.rect(cx + 52, y + 192, 26, 7, GOLD)
    # neck + head
    cv.rect(cx - 14, y + 148, 28, 36, SKIN)
    cv.ellipse(cx, y + 104, 46, 56, SKIN)
    # hair at the sides
    cv.ellipse(cx - 38, y + 78, 10, 26, HAIR)
    cv.ellipse(cx + 38, y + 78, 10, 26, HAIR)
    # cap: crown + brim + gold emblem
    cv.ellipse(cx, y + 62, 50, 22, NAVY)
    cv.rect(cx - 50, y + 52, 100, 16, NAVY)
    cv.ellipse(cx, y + 74, 54, 10, (24, 38, 70))
    cv.circle(cx, y + 62, 7, GOLD, fill=True)
    cv.circle(cx, y + 62, 3, (24, 38, 70), fill=True)
    # face: eyes, brows, nose, mouth
    cv.ellipse(cx - 18, y + 100, 5, 3, INK)
    cv.ellipse(cx + 18, y + 100, 5, 3, INK)
    cv.line(cx - 24, y + 90, cx - 12, y + 88, HAIR)
    cv.line(cx + 12, y + 88, cx + 24, y + 90, HAIR)
    cv.line(cx, y + 104, cx - 3, y + 118, (190, 150, 110))
    cv.line(cx - 10, y + 132, cx + 10, y + 132, (150, 90, 70))
    # halftone dots (deterministic)
    for yy in range(y + 4, y + h - 4, 6):
        for xx in range(x + 4, x + w - 4, 6):
            if _det_hash(xx, yy) < 34:
                cv.px(xx, yy, (60, 70, 84))
    cv.border(x, y, w, h, INK, 3)


# ---------------------------------------------------------------------------
# Stamps
# ---------------------------------------------------------------------------
def draw_stamp(cv, x, y, w, h, color, lines, scale=2):
    cv.border(x, y, w, h, color, 3)
    cv.border(x + 8, y + 8, w - 16, h - 16, color, 2)
    total = len(lines) * (7 * scale + 6)
    yy = y + (h - total) // 2
    for ln in lines:
        cv.text_center(x + w // 2, yy, ln, scale, color)
        yy += 7 * scale + 6


def draw_round_stamp(cv, cx, cy, r, color, lines, scale=2):
    cv.circle(cx, cy, r, color)
    cv.circle(cx, cy, r - 6, color)
    total = len(lines) * (7 * scale + 5)
    yy = cy - total // 2
    for ln in lines:
        cv.text_center(cx, yy, ln, scale, color)
        yy += 7 * scale + 5


# ---------------------------------------------------------------------------
# Island map
# ---------------------------------------------------------------------------
def draw_map(cv, x, y, w, h):
    cv.rect(x, y, w, h, SEA)
    cv.border(x, y, w, h, INK, 2)
    island = [(x + 58, y + 62), (x + 118, y + 40), (x + 176, y + 72),
              (x + 196, y + 142), (x + 168, y + 222), (x + 118, y + 282),
              (x + 68, y + 242), (x + 38, y + 150)]
    cv.poly(island, LAND)
    for i in range(len(island)):
        x0, y0 = island[i]
        x1, y1 = island[(i + 1) % len(island)]
        cv.line(x0, y0, x1, y1, INK_SOFT)
    # compass
    cv.circle(x + w - 34, y + 30, 14, INK)
    cv.text(x + w - 38, y + 22, "N", 2, INK)
    # Aurelia + lighthouse
    ax, ay = x + 118, y + 150
    cv.poly([(ax - 7, ay + 12), (ax, ay - 16), (ax + 7, ay + 12)], (70, 96, 110))
    cv.circle(ax, ay - 18, 4, (240, 220, 140), fill=True)
    cv.circle(ax, ay + 14, 4, STAMP_RED, fill=True)
    cv.text(x + 96, y + 168, "AURELIA", 2, INK)
    # Pt. Merrow
    mx, my = x + 176, y + 232
    cv.circle(mx, my, 4, INK, fill=True)
    cv.text(x + 108, y + 244, "PT. MERROW", 2, INK)
    # scale bar
    cv.line(x + 24, y + h - 26, x + 84, y + h - 26, INK)
    cv.line(x + 24, y + h - 31, x + 24, y + h - 21, INK)
    cv.line(x + 84, y + h - 31, x + 84, y + h - 21, INK)
    cv.text(x + 30, y + h - 46, "10 KM", 2, INK)
    cv.text_center(x + w // 2, y + 8, "SOLMARIA", 2, INK)


# ---------------------------------------------------------------------------
# Build the spread
# ---------------------------------------------------------------------------
def build():
    cv = Canvas(W, H, PAPER)
    # page edge + spine
    cv.border(8, 8, W - 16, H - 16, GOLD, 2)
    cv.rect(508, 12, 8, H - 24, (196, 178, 140))
    cv.line(512, 12, 512, H - 12, (150, 128, 88))

    # ---- LEFT PAGE: data page -------------------------------------------
    cv.text_center(256, 34, "REPUBLIC OF SOLMARIA", 3, INK)
    cv.text_center(256, 78, "ISLAND OF THE LANTERN", 2, INK_SOFT)
    cv.line(40, 108, 472, 108, GOLD)
    cv.text_center(256, 118, "PASSPORT", 4, INK)
    cv.text_center(256, 152, "PASSEPORT", 2, INK_SOFT)

    # portrait
    draw_portrait(cv, 44, 186, 210, 270)
    # signature under portrait
    cv.text(52, 470, "Mara Solenne", 2, HAND_BLUE, slant=0.35)
    cv.line(44, 498, 254, 498, INK_SOFT)
    cv.text_center(149, 504, "HOLDER'S SIGNATURE", 1, INK_SOFT)

    # data fields (label small, value larger), right of portrait
    fields = [
        ("SURNAME", "SOLENNE"),
        ("GIVEN NAMES", "MARA"),
        ("NATIONALITY", "SOLMARIAN"),
        ("DATE OF BIRTH", "12 MAY 1988"),
        ("SEX", "F"),
        ("PLACE OF BIRTH", "AURELIA"),
        ("DATE OF ISSUE", "14 MAR 2024"),
        ("DATE OF EXPIRY", "14 MAR 2034"),
        ("PASSPORT NO.", "SM 0417829"),
    ]
    fy = 186
    for label, value in fields:
        cv.text(280, fy, label, 1, INK_SOFT)
        cv.text(280, fy + 10, value, 2, INK)
        fy += 36

    # remarks box + coat of arms
    cv.border(280, 528, 216, 96, INK_SOFT, 2)
    cv.text(292, 540, "REMARKS", 2, INK)
    cv.text(292, 566, "HOLDER IS A", 2, INK)
    cv.text(292, 588, "LIGHTHOUSE KEEPER", 2, INK)
    cv.circle(72, 576, 26, GOLD)
    cv.circle(72, 576, 21, INK)
    cv.poly([(72 - 6, 576 + 12), (72, 576 - 14), (72 + 6, 576 + 12)], (240, 220, 140))
    cv.text_center(72, 606, "EST. 1811", 1, INK_SOFT)

    # ---- RIGHT PAGE: visas ----------------------------------------------
    cv.text_center(768, 34, "VISAS", 4, INK)
    cv.line(540, 108, 984, 108, GOLD)
    draw_stamp(cv, 540, 128, 210, 132, STAMP_PURPLE,
               ["CORSANO", "ARRIVAL", "02 JUN 2024"])
    draw_stamp(cv, 774, 128, 210, 132, STAMP_BLUE,
               ["CORSANO", "DEPARTURE", "09 JUN 2024"])
    draw_stamp(cv, 540, 276, 210, 132, STAMP_GREEN,
               ["VELLORE", "ENTRY", "18 SEP 2025"])
    draw_stamp(cv, 774, 276, 210, 132, STAMP_RED,
               ["SOLMARIA", "RE-ENTRY", "21 SEP 2025"])

    # ferry condition box + fee stamp
    cv.border(540, 428, 444, 92, STAMP_RED, 3)
    cv.text(560, 448, "ENTRY BY FERRY ONLY", 2, STAMP_RED)
    cv.text(560, 474, "NO AIRPORT ON SOLMARIA", 2, STAMP_RED)
    draw_round_stamp(cv, 916, 474, 40, STAMP_RED, ["FERRY", "TAX", "12 AUR"])

    # map + officer's note
    draw_map(cv, 540, 544, 230, 352)
    cv.text(790, 556, "OFFICER'S NOTE", 2, INK)
    cv.line(790, 580, 984, 580, INK_SOFT)
    cv.text(790, 596, "return to", 2, HAND_BLUE, slant=0.4)
    cv.text(790, 622, "Aurelia by", 2, HAND_BLUE, slant=0.4)
    cv.text(790, 648, "21 Sep", 2, HAND_BLUE, slant=0.4)
    cv.line(790, 682, 934, 676, HAND_BLUE)
    cv.line(934, 676, 918, 690, HAND_BLUE)
    cv.text(790, 712, "FERRY FROM CORSANO", 2, INK)
    cv.text(790, 736, "DEPARTS 07:00", 2, INK)
    cv.text(790, 760, "NO FLIGHTS. NO", 2, INK)
    cv.text(790, 784, "EXCEPTIONS.", 2, INK)

    # ---- MRZ band across the spread --------------------------------------
    cv.line(24, 924, 1000, 924, GOLD)
    line1, line2 = mrz_lines()
    cv.text_center(512, 936, line1, 2, INK)
    cv.text_center(512, 962, line2, 2, INK)
    return cv


def write_png(path, w, h, rgb):
    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data
                + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    raw = b"".join(b"\x00" + rgb[y * w * 3:(y + 1) * w * 3] for y in range(h))
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 6))
           + chunk(b"IEND", b""))
    Path(path).write_bytes(png)
    return png


def main():
    out = Path("/output")
    out.mkdir(parents=True, exist_ok=True)
    cv = build()
    data = write_png(out / "entry.png", W, H, bytes(cv.buf))
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote /output/entry.png ({len(data)} bytes, sha256={digest})")


if __name__ == "__main__":
    main()
