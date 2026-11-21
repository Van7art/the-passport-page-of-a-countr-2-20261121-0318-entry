#!/usr/bin/env python3
"""Render one variant of the invented-passport spread (1024x700).
Shared layout; variants differ in country, palette, holder, stamps, detail.
"""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 700
FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"
def F(name, size):
    base = FL if name.startswith("LIB:") else FD
    return ImageFont.truetype(base + name.replace("LIB:", ""), size)

SERIF = "DejaVuSerif.ttf"; SERIFB = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"; SANSB = "DejaVuSans-Bold.ttf"
MONO = "DejaVuSansMono.ttf"; ITALIC = "LIB:LiberationSerif-Italic.ttf"

def check_digit(s):
    vals = {}
    for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[c] = i
    vals["<"] = 0
    total = 0
    for i, ch in enumerate(s):
        total += vals[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)

def mrz_lines(code, surname, given, docno, dob, sex, expiry, personal):
    # TD3, 44 chars per line; MRZ alphabet is A-Z, 0-9 and '<' only.
    def clean(s):
        return "".join(c if ("A" <= c <= "Z" or "0" <= c <= "9") else "<"
                       for c in s.upper())
    surname, given = clean(surname), clean(given)
    docno, personal = clean(docno), clean(personal)
    name = (surname + "<<" + given.replace(" ", "<")).ljust(39, "<")[:39]
    l1 = ("P<" + code + name).ljust(44, "<")[:44]
    dob_c = check_digit(dob); exp_c = check_digit(expiry)
    pers = personal.ljust(14, "<")[:14]
    pers_c = check_digit(pers)
    l2core = docno + check_digit(docno) + code + dob + dob_c + sex + expiry + exp_c + pers + pers_c
    comp = check_digit(docno + check_digit(docno) + dob + dob_c + expiry + exp_c + pers + pers_c)
    l2 = (l2core + comp).ljust(44, "<")[:44]
    assert len(l1) == 44 and len(l2) == 44, (l1, l2)
    return l1, l2

VARIANTS = {
 "v1": dict(
    country="REPUBLIC OF KAVURRA", native="TAVARA O KAVURRA", code="KAV",
    accent=(14, 90, 90), accent2=(11, 60, 90), paper=(244, 241, 228),
    surname="VAITOA", given="SELENE MARA", sex="F",
    dob="02 JUN 1988", dob_mrz="880602", pob="PORT SELENE",
    docno="KV4829173", issue="14 MAR 2024", expiry="13 MAR 2034", exp_mrz="340313",
    authority="Registrar of Passports, Port Selene",
    personal="KV19880602SEL", portrait="media-generation-portrait-v1-kavurra-0-4e4601a0-05e6-470e-bae8-8e3d49f0b221.jpg",
    emblem="wave",
    stamps=[("PORT SELENE", "DEPARTURE", "27 AUG 2024", -4, (150, 60, 60)),
            ("MERIDIA", "ARRIVAL", "02 SEP 2024", 3, (40, 90, 140)),
            ("MERIDIA", "DEPARTURE", "09 SEP 2024", -2, (150, 60, 60)),
            ("PORT SELENE", "ARRIVAL", "21 NOV 2024", 5, (40, 90, 140))],
    visa=("ENTRY PERMIT", "MERIDIA  •  90 DAYS  •  MULTIPLE ENTRIES",
          "Issued 26 AUG 2024, Meridia Consulate, Port Selene"),
    detail_title="PEARL-DIVING LICENCE",
    detail=("Holder is licensed to dive the reef beds of Atuona for 90 days. "
            "Ferry fee 12 KVR paid — stamp 4417."),
    motto="THE SEA PROVIDES",
 ),
 "v2": dict(
    country="REPUBLIC OF VOSTRAN", native="REPUBLIKA VOSTRAN", code="VOS",
    accent=(110, 20, 35), accent2=(140, 110, 40), paper=(245, 240, 230),
    surname="KOVAC", given="MILAN DORIN", sex="M",
    dob="11 NOV 1979", dob_mrz="791111", pob="DRAVENMOOR",
    docno="VS7104582", issue="14 MAR 2024", expiry="13 MAR 2034", exp_mrz="340313",
    authority="Ministry of the Interior, Dravenmoor",
    personal="VS19791111KOV", portrait="media-generation-portrait-v2-vostran-0-71a5c0ed-f8c3-421e-a3b3-fe96fc56c5ce.jpg",
    emblem="mountain",
    stamps=[("DRAVENMOOR", "DEPARTURE", "05 JUL 2024", 4, (150, 60, 60)),
            ("ALBERIN", "ARRIVAL", "07 JUL 2024", -3, (40, 90, 140)),
            ("ALBERIN", "DEPARTURE", "18 JUL 2024", 2, (150, 60, 60)),
            ("DRAVENMOOR", "ARRIVAL", "02 OCT 2024", -5, (40, 90, 140))],
    visa=("MOUNTAIN PASS PERMIT", "ZORYA PASS  •  ON FOOT  •  MAY–OCT ONLY",
          "Issued 04 JUL 2024, Border Service, Dravenmoor"),
    detail_title="TIMBER LEVY — PAID 40 VSD",
    detail=("Holder may carry one felled larch across the Zorya Pass per season. "
            "Levy receipt 8812 attached at the border post."),
    motto="STONE STANDS  •  THE PASS ENDURES",
 ),
 "v3": dict(
    country="REPUBLIC OF TALAMAR", native="JUMHURIYYA TALAMAR", code="TAL",
    accent=(20, 83, 45), accent2=(150, 110, 30), paper=(246, 242, 230),
    surname="AL-HADDAD", given="LAYLA NOOR", sex="F",
    dob="23 APR 1995", dob_mrz="950423", pob="AL-MINA",
    docno="TL3061948", issue="14 MAR 2024", expiry="13 MAR 2034", exp_mrz="340313",
    authority="Directorate of Passports, Al-Mina",
    personal="TL19950423ALH", portrait="media-generation-portrait-v3-talamar-0-e2f35255-5ca2-4120-a1ff-2d6012f10332.jpg",
    emblem="sun",
    stamps=[("AL-MINA", "DEPARTURE", "19 JUN 2024", -3, (150, 60, 60)),
            ("SUHAIL", "ARRIVAL", "21 JUN 2024", 4, (40, 90, 140)),
            ("SUHAIL", "DEPARTURE", "30 JUN 2024", -4, (150, 60, 60)),
            ("AL-MINA", "ARRIVAL", "12 AUG 2024", 3, (40, 90, 140))],
    visa=("CARAVAN PERMIT", "DATE CARAVAN  •  BEYOND THE WADI RIM",
          "Issued 18 JUN 2024, Caravan Office, Al-Mina"),
    detail_title="WATER RATION — 4 LITRES / DAY",
    detail=("Holder travels with the date caravan beyond the Wadi Rim. "
            "Port due 25 TLD paid — stamp 2093."),
    motto="THE WELL REMEMBERS  •  THE ROAD PROVIDES",
 ),
}

def paper_base(cfg):
    img = Image.new("RGB", (W, H), (38, 34, 28))
    d = ImageDraw.Draw(img)
    # outer cover edge
    d.rectangle([0, 0, W - 1, H - 1], fill=(52, 44, 34))
    # two pages
    for x0 in (14, 514):
        d.rectangle([x0, 14, x0 + 496, H - 14], fill=cfg["paper"])
    # gutter shadow
    for i in range(12):
        a = 60 - i * 5
        d.line([(512 - i, 14), (512 - i, H - 14)], fill=(0, 0, 0))
        d.line([(512 + i, 14), (512 + i, H - 14)], fill=(0, 0, 0))
    # noise
    rnd = random.Random(7)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for _ in range(5200):
        x = rnd.randint(16, W - 16); y = rnd.randint(16, H - 16)
        od.point((x, y), fill=(60, 50, 30, rnd.randint(4, 12)))
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    return img

def guilloche(img, box, color):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r in range(14, 260, 9):
        d.ellipse([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62],
                  outline=color + (16,), width=1)
    img.alpha_composite(ov)

def emblem(d, cx, cy, r, cfg, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], outline=color, width=1)
    if cfg["emblem"] == "wave":
        for k, yy in enumerate((-6, 0, 6)):
            pts = []
            for x in range(cx - r + 8, cx + r - 7, 4):
                pts.append((x, cy + yy + 3 * math.sin((x - cx) / 9.0)))
            d.line(pts, fill=color, width=2)
        d.polygon([(cx, cy - r + 6), (cx - 6, cy - r + 16), (cx + 6, cy - r + 16)], fill=color)
    elif cfg["emblem"] == "mountain":
        d.polygon([(cx - r + 9, cy + 8), (cx - 8, cy - r + 12), (cx + 2, cy + 2),
                   (cx + 9, cy - r + 18), (cx + r - 9, cy + 8)], outline=color, width=2)
        d.line([(cx - r + 9, cy + 8), (cx + r - 9, cy + 8)], fill=color, width=2)
    else:  # sun
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=color)
        for a in range(0, 360, 30):
            x1 = cx + 13 * math.cos(math.radians(a)); y1 = cy + 13 * math.sin(math.radians(a))
            x2 = cx + (r - 6) * math.cos(math.radians(a)); y2 = cy + (r - 6) * math.sin(math.radians(a))
            d.line([(x1, y1), (x2, y2)], fill=color, width=2)

def stamp(img, cx, cy, w, h, color, top, mid, date, angle):
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = color + (215,)
    d.rounded_rectangle([6, 6, w + 33, h + 33], radius=10, outline=c, width=3)
    d.rounded_rectangle([11, 11, w + 28, h + 28], radius=7, outline=c, width=1)
    d.text((w // 2 + 20, 16), top, font=F(SANSB, 15), fill=c, anchor="mt")
    d.line([(16, 34), (w + 24, 34)], fill=c, width=1)
    d.text((w // 2 + 20, 40), mid, font=F(SERIFB, 19), fill=c, anchor="mt")
    d.text((w // 2 + 20, 64), date, font=F(SANSB, 14), fill=c, anchor="mt")
    d.text((20, h + 12), "*", font=F(SANSB, 12), fill=c)
    d.text((w + 20, h + 12), "*", font=F(SANSB, 12), fill=c, anchor="rt")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.alpha_composite(layer, (int(cx - layer.width // 2), int(cy - layer.height // 2)))

def render(cfg, out_path):
    img = paper_base(cfg)
    d = ImageDraw.Draw(img)
    A = cfg["accent"]; A2 = cfg["accent2"]
    guilloche(img, (14, 14, 510, 686), A)
    guilloche(img, (514, 14, 1010, 686), A)

    # ---------- LEFT PAGE: data page ----------
    x0, y0 = 14, 14
    d.rectangle([x0, y0, x0 + 496, y0 + 672], outline=(90, 78, 60), width=1)
    d.rectangle([x0 + 6, y0 + 6, x0 + 490, y0 + 666], outline=A, width=1)
    emblem(d, x0 + 52, y0 + 52, 30, cfg, A)
    d.text((x0 + 92, y0 + 26), cfg["country"], font=F(SERIFB, 25), fill=A)
    d.text((x0 + 92, y0 + 56), cfg["native"], font=F(SANS, 12), fill=(90, 78, 60))
    d.text((x0 + 92, y0 + 74), "PASSPORT  •  PASSEPORT", font=F(SANSB, 11), fill=(60, 52, 40))
    d.line([(x0 + 24, y0 + 104), (x0 + 472, y0 + 104)], fill=A, width=2)
    d.text((x0 + 24, y0 + 112), "Type / Type", font=F(SANS, 9), fill=(110, 100, 80))
    d.text((x0 + 24, y0 + 124), "P", font=F(SANSB, 15), fill=(20, 20, 20))
    d.text((x0 + 120, y0 + 112), "Code / Code", font=F(SANS, 9), fill=(110, 100, 80))
    d.text((x0 + 120, y0 + 124), cfg["code"], font=F(SANSB, 15), fill=(20, 20, 20))
    d.text((x0 + 230, y0 + 112), "Passport No. / No. du passeport", font=F(SANS, 9), fill=(110, 100, 80))
    d.text((x0 + 230, y0 + 124), cfg["docno"], font=F(SANSB, 15), fill=(20, 20, 20))
    d.text((x0 + 400, y0 + 112), "Sexe", font=F(SANS, 9), fill=(110, 100, 80))
    d.text((x0 + 400, y0 + 124), cfg["sex"], font=F(SANSB, 15), fill=(20, 20, 20))

    # portrait
    px, py, pw, ph = x0 + 24, y0 + 158, 148, 196
    por = Image.open(cfg["portrait"]).convert("RGB")
    cw, ch = por.size
    tw = int(cw * 0.72); th = int(tw / 0.755)
    left = (cw - tw) // 2; top = int(ch * 0.05)
    por = por.crop((left, top, left + tw, min(top + th, ch))).resize((pw, ph), Image.LANCZOS)
    img.paste(por, (px, py))
    d.rectangle([px, py, px + pw, py + ph], outline=A, width=2)
    d.rectangle([px + 3, py + 3, px + pw - 3, py + ph - 3], outline=(255, 255, 255), width=1)
    # ghost watermark of portrait on right page handled later; small foil circle
    d.ellipse([px + pw - 34, py + ph - 34, px + pw - 4, py + ph - 4], fill=A2, outline=(255, 255, 255), width=1)
    d.text((px + pw - 19, py + ph - 30), cfg["code"], font=F(SANSB, 8), fill=(255, 255, 255), anchor="mt")

    # data fields, right of portrait
    fx = x0 + 196
    fields = [
        ("Surname / Nom", cfg["surname"]),
        ("Given names / Prenoms", cfg["given"]),
        ("Nationality / Nationalite", cfg["country"].title().replace("Republic Of ", "")),
        ("Date of birth / Date de naissance", cfg["dob"]),
        ("Place of birth / Lieu de naissance", cfg["pob"]),
        ("Date of issue / Date de delivrance", cfg["issue"]),
        ("Date of expiry / Date d'expiration", cfg["expiry"]),
    ]
    yy = y0 + 158
    for label, val in fields:
        d.text((fx, yy), label, font=F(SANS, 9), fill=(110, 100, 80))
        d.text((fx, yy + 11), val, font=F(SANSB, 14), fill=(20, 20, 20))
        yy += 30
    d.text((x0 + 24, y0 + 368), "Authority / Autorite", font=F(SANS, 9), fill=(110, 100, 80))
    d.text((x0 + 24, y0 + 379), cfg["authority"], font=F(SANSB, 13), fill=(20, 20, 20))
    d.text((x0 + 24, y0 + 404), "Holder's signature / Signature du titulaire", font=F(SANS, 9), fill=(110, 100, 80))
    d.line([(x0 + 24, y0 + 436), (x0 + 300, y0 + 436)], fill=(120, 110, 90), width=1)
    d.text((x0 + 30, y0 + 410), cfg["surname"].title() + " " + cfg["given"].title(),
           font=F(ITALIC, 17), fill=(40, 40, 70))
    d.text((x0 + 330, y0 + 404), "Personal No.", font=F(SANS, 9), fill=(110, 100, 80))
    d.text((x0 + 330, y0 + 415), cfg["personal"], font=F(SANSB, 11), fill=(20, 20, 20))
    d.text((x0 + 330, y0 + 434), cfg["motto"], font=F(SANS, 8), fill=A)

    # MRZ
    l1, l2 = mrz_lines(cfg["code"], cfg["surname"], cfg["given"], cfg["docno"],
                       cfg["dob_mrz"], cfg["sex"], cfg["exp_mrz"], cfg["personal"])
    d.rectangle([x0 + 14, y0 + 470, x0 + 482, y0 + 540], fill=(255, 255, 255))
    d.rectangle([x0 + 14, y0 + 470, x0 + 482, y0 + 540], outline=A, width=1)
    d.text((x0 + 24, y0 + 478), l1, font=F(MONO, 15), fill=(10, 10, 10))
    d.text((x0 + 24, y0 + 500), l2, font=F(MONO, 15), fill=(10, 10, 10))
    d.text((x0 + 24, y0 + 528), "Machine readable zone — ICAO Doc 9303", font=F(SANS, 8), fill=(110, 100, 80))
    d.text((x0 + 24, y0 + 600), "This passport is the property of the " + cfg["country"].title() +
           " and must be returned on demand.", font=F(SANS, 9), fill=(90, 78, 60))
    d.text((x0 + 24, y0 + 622), "Ce passeport est la propriete de l'Etat et doit etre restitue sur demande.",
           font=F(SANS, 9), fill=(90, 78, 60))

    # ---------- RIGHT PAGE: visas & stamps ----------
    x0 = 514
    d.rectangle([x0, y0, x0 + 496, y0 + 672], outline=(90, 78, 60), width=1)
    d.rectangle([x0 + 6, y0 + 6, x0 + 490, y0 + 666], outline=A, width=1)
    d.text((x0 + 24, y0 + 26), "VISAS", font=F(SERIFB, 24), fill=A)
    d.text((x0 + 120, y0 + 34), "—  ENDORSEMENTS  •  STAMPS", font=F(SANS, 11), fill=(90, 78, 60))
    d.line([(x0 + 24, y0 + 62), (x0 + 472, y0 + 62)], fill=A, width=2)

    # visa sticker
    vx, vy, vw, vh = x0 + 24, y0 + 78, 448, 108
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle([vx, vy, vx + vw, vy + vh], radius=6, fill=A + (255,))
    od.rounded_rectangle([vx + 4, vy + 4, vx + vw - 4, vy + vh - 4], radius=4, outline=(255, 255, 255, 200), width=1)
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    d.text((vx + 16, vy + 10), cfg["visa"][0], font=F(SERIFB, 20), fill=(255, 255, 255))
    d.text((vx + 16, vy + 38), cfg["visa"][1], font=F(SANSB, 13), fill=(255, 255, 255))
    d.text((vx + 16, vy + 62), cfg["visa"][2], font=F(SANS, 11), fill=(235, 235, 235))
    d.text((vx + vw - 16, vy + 10), "No. 004417", font=F(SANSB, 12), fill=(255, 255, 255), anchor="rt")
    d.text((vx + vw - 16, vy + 78), "VALID WITH PASSPORT ONLY", font=F(SANS, 9), fill=(235, 235, 235), anchor="rt")

    # stamps: 2x2 grid, slight overlap
    positions = [(x0 + 128, y0 + 258), (x0 + 368, y0 + 258),
                 (x0 + 128, y0 + 372), (x0 + 368, y0 + 372)]
    for (top, mid, date, ang, col), (cx, cy) in zip(cfg["stamps"], positions):
        stamp(img, cx, cy, 196, 92, col, top, mid, date, ang)
    d = ImageDraw.Draw(img)

    # telling-detail box
    bx, by, bw, bh = x0 + 24, y0 + 452, 448, 96
    d.rectangle([bx, by, bx + bw, by + bh], outline=A, width=2)
    d.rectangle([bx + 3, by + 3, bx + bw - 3, by + bh - 3], outline=A2, width=1)
    d.text((bx + 14, by + 10), "CONDITIONS  •  " + cfg["detail_title"], font=F(SANSB, 13), fill=A)
    # wrap detail text
    words = cfg["detail"].split(); lines = []; cur = ""
    for w_ in words:
        if d.textlength(cur + " " + w_, font=F(SANS, 12)) < bw - 28:
            cur = (cur + " " + w_).strip()
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    yy = by + 32
    for ln in lines:
        d.text((bx + 14, yy), ln, font=F(SANS, 12), fill=(30, 30, 30)); yy += 17
    d.text((x0 + 24, y0 + 566), "The bearer is requested to allow the holder to pass freely",
           font=F(ITALIC, 12), fill=(70, 60, 45))
    d.text((x0 + 24, y0 + 584), "and to afford such assistance and protection as may be necessary.",
           font=F(ITALIC, 12), fill=(70, 60, 45))
    d.text((x0 + 24, y0 + 616), "Page 14  •  " + cfg["code"] + "  •  " + cfg["docno"],
           font=F(SANS, 9), fill=(110, 100, 80))

    img.convert("RGB").save(out_path, "PNG", optimize=True)
    return out_path

if __name__ == "__main__":
    key = sys.argv[1]; out = sys.argv[2]
    render(VARIANTS[key], out)
    print("wrote", out)
