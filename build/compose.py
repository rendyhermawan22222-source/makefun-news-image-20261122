#!/usr/bin/env python3
"""Compose 'The World at Midnight' - a final-edition front page for Sunday 22 November 2026."""
import glob, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, '..', 'art')
OUT = os.path.join(HERE, 'entry.png')
F = '/usr/share/fonts/truetype/noto/'

def font(name, size):
    return ImageFont.truetype(F + name + '.ttf', size)

W = H = 1024
PAPER = (244, 238, 226)
INK = (24, 22, 20)
MUTED = (92, 86, 78)
RED = (178, 34, 34)
NAVY = (22, 40, 74)
RULE = (60, 54, 48)
TINT = (232, 224, 208)

img = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(img)

def art(key):
    return Image.open(glob.glob(os.path.join(ART, f'*{key}*.png'))[0]).convert('RGB')

def fit(im, w, h, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * fx); y = round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))

def text_w(t, f):
    return d.textlength(t, font=f)

def wrap(t, f, maxw):
    out, line = [], ''
    for wd in t.split():
        cand = (line + ' ' + wd).strip()
        if text_w(cand, f) <= maxw:
            line = cand
        else:
            out.append(line); line = wd
    if line: out.append(line)
    return out

def para(x, y, t, f, maxw, fill=INK, lh=None):
    lh = lh or round(f.size * 1.22)
    for ln in wrap(t, f, maxw):
        d.text((x, y), ln, font=f, fill=fill); y += lh
    return y

def tag(x, y, label, bg, f=None, fg=(255, 255, 255)):
    f = f or font('NotoSans-CondensedBold', 11)
    tw = text_w(label, f)
    d.rectangle((x, y, x + tw + 10, y + 15), fill=bg)
    d.text((x + 5, y + 1), label, font=f, fill=fg)
    return x + tw + 14

# ---------------- masthead ----------------
d.rectangle((0, 0, W, 6), fill=INK)
mf = font('NotoSerif-ExtraCondensedBlack', 54)
d.text((18, 8), 'THE WORLD AT MIDNIGHT', font=mf, fill=INK)
mw = text_w('THE WORLD AT MIDNIGHT', mf)
# right date block
db1 = font('NotoSans-CondensedBlack', 22); db2 = font('NotoSans-CondensedSemiBold', 13)
d.rectangle((W - 238, 14, W - 16, 70), fill=INK)
d.text((W - 228, 16), 'SUNDAY 22 NOV 2026', font=db1, fill=PAPER)
d.text((W - 228, 46), 'FINAL EDITION · 23:59 UTC', font=db2, fill=(240, 190, 90))
sub = font('NotoSerif-CondensedSemiBoldItalic', 15)
d.text((20, 72), 'How the day actually ended: one page, every outcome, checked against the wires.', font=sub, fill=RED)
d.line((16, 96, W - 16, 96), fill=INK, width=3)
d.line((16, 100, W - 16, 100), fill=INK, width=1)

# ---------------- hero ----------------
HY = 108; HH = 330; HW = 612
hero = fit(art('cop31'), HW, HH, 0.5, 0.62)
img.paste(hero, (16, HY))
# gradient for headline legibility
grad = Image.new('L', (HW, 150))
gd = ImageDraw.Draw(grad)
for i in range(150):
    gd.line((0, i, HW, i), fill=int(220 * (i / 150) ** 1.3))
dark = Image.new('RGB', (HW, 150), (14, 12, 10))
img.paste(dark, (16, HY + HH - 150), grad)
tag(26, HY + 10, 'LEAD · ANTALYA, TÜRKIYE', RED, font('NotoSans-CondensedBold', 13))
hf = font('NotoSerif-ExtraCondensedBlack', 62)
d.text((26, HY + HH - 128), 'COP31 COLLAPSES', font=hf, fill=(255, 250, 240))
hf2 = font('NotoSerif-CondensedBold', 25)
d.text((28, HY + HH - 58), 'UN climate summit ends with no deal', font=hf2, fill=(250, 214, 140))
d.text((28, HY + HH - 30), 'First COP to fail outright since The Hague in 2000', font=font('NotoSans-CondensedMedium', 16), fill=(235, 230, 220))

# hero side column
SX = 16 + HW + 16; SW = W - 16 - SX
y = HY
d.text((SX, y - 2), 'THE ANTALYA PACT, REJECTED', font=font('NotoSans-CondensedBlack', 15), fill=RED); y += 20
pb = font('NotoSerif-Condensed', 15)
y = para(SX, y, 'After the longest COP on record, about 44 hours into overtime, COP31 president Murat Kurum conceded there was “no agreement on this text”.', pb, SW, lh=18) + 6
# stat boxes
def stat(x, y, w, big, small, col):
    d.rectangle((x, y, x + w, y + 58), fill=TINT)
    d.rectangle((x, y, x + 4, y + 58), fill=col)
    d.text((x + 10, y - 2), big, font=font('NotoSans-CondensedBlack', 34), fill=col)
    para(x + 10, y + 38, small, font('NotoSans-CondensedSemiBold', 12), w - 14, fill=MUTED, lh=13)
bw = (SW - 8) // 2
stat(SX, y, bw, '0', 'fossil fuels named in final text', RED)
stat(SX + bw + 8, y, bw, '44 h', 'of overtime, a record', NAVY)
y += 66
bl = font('NotoSans-Condensed', 14)
for b in ['EU, Norway, Panama and the Marshall Islands refused the weak draft',
          'Draft kept 35% clean power by 2035; dropped a $120bn adaptation figure',
          'Open issues roll over to COP32, Addis Ababa, November 2027']:
    d.ellipse((SX, y + 6, SX + 6, y + 12), fill=RED)
    y = para(SX + 12, y, b, bl, SW - 12, lh=17) + 3
y += 4
d.line((SX, y, SX + SW, y), fill=RULE, width=1); y += 6
# numbers of the day
d.text((SX, y), 'NUMBERS OF THE DAY', font=font('NotoSans-CondensedBlack', 13), fill=INK); y += 18
nums = [('186', 'Russian drones at Ukraine overnight'), ('258', 'House seats now held by Democrats'),
        ('98.79%', 'record Hong Kong Election Committee turnout'), ]
nf = font('NotoSans-CondensedBlack', 21); nl = font('NotoSans-Condensed', 13)
for n, l in nums:
    d.text((SX, y - 3), n, font=nf, fill=NAVY)
    d.text((SX + 82, y + 4), l, font=nl, fill=INK)
    y += 23

# ---------------- second row: three illustrated stories ----------------
RY = HY + HH + 12
d.line((16, RY - 5, W - 16, RY - 5), fill=INK, width=2)
CW = (W - 32 - 24) // 3; IH = 138
cards = [
    ('dymer', 0.5, 0.55, 'UKRAINE · DYMER', RED, 'Nine dead in Kyiv-region block',
     'A drone tore through an apartment block before dawn. A boy, 7, was pulled out alive after about 14 hours. 186 drones launched; 161 downed (Ukrainian Air Force).'),
    ('benghazi', 0.4, 0.5, 'LIBYA · BENGHAZI', NAVY, 'Russian warship sunk in port',
     'Corvette Merkury capsized after suspected Ukrainian sea-drone strikes: two hit, at least four shot down. About 10 hurt; Libya asks UN to investigate.'),
    ('house', 0.5, 0.4, 'UNITED STATES', (30, 70, 150), 'Democrats reach 258 House seats',
     'Largest majority since 1992, clinched as Chuck Hubbard ousted Rep. Virginia Foxx in North Carolina. Republicans hold at least 173; four races uncalled.'),
]
cf = font('NotoSerif-CondensedBlack', 21); cb = font('NotoSerif-Condensed', 14)
for i, (k, fx, fy, lab, col, head, body) in enumerate(cards):
    x = 16 + i * (CW + 12)
    img.paste(fit(art(k), CW, IH, fx, fy), (x, RY))
    tag(x + 6, RY + 6, lab, col)
    yy = RY + IH + 4
    for ln in wrap(head, cf, CW):
        d.text((x, yy), ln, font=cf, fill=INK); yy += 24
    para(x, yy + 1, body, cb, CW, fill=(50, 46, 42), lh=17)
    if i: d.line((x - 6, RY, x - 6, RY + 262), fill=(190, 180, 165), width=1)

# ---------------- third row: briefs grid ----------------
BY = RY + 270
d.rectangle((16, BY, W - 16, BY + 22), fill=INK)
d.text((24, BY + 2), 'ALSO ON SUNDAY', font=font('NotoSans-CondensedBlack', 15), fill=PAPER)
d.text((160, BY + 4), 'claims are marked as claims', font=font('NotoSans-CondensedMediumItalic', 13), fill=(200, 190, 170))
briefs = [
    ('GULF', 'CLAIM', 'Iran says it hit US radars in Bahrain; Bahrain says debris fell on an industrial site, US says no damage.'),
    ('SAUDI', 'CLAIM', 'Houthis claim a direct hit on the Rabigh refinery; coalition says a missile was intercepted.'),
    ('IRAN', 'CONFIRMED', 'Rolling power cuts begin nationwide, up to two hours a day, as war damage hits fuel supply.'),
    ('WEST BANK', 'REPORTED', 'Settlers torch cars in villages near Ramallah; Israeli police open inquiry; Eisenkot: “Jewish terrorism”.'),
    ('HONG KONG', 'CONFIRMED', 'Election Committee polls: 98.79% turnout, 5,640 of 5,709 voters; 723 seats filled.'),
    ('INDONESIA', 'REPORTED', 'Cikande candy-factory fire, Banten: 24 body bags recovered, around 30 workers missing.'),
    ('UKRAINE', 'REPORTED', 'At least 12 killed across Kyiv region; Zelensky says about 2,700 drones hit Ukraine this week.'),
    ('VATICAN', 'CONFIRMED', 'Pope Leo XIV lunches with 1,300 guests on the World Day of the Poor.'),
]
TAGC = {'CLAIM': (196, 120, 20), 'CONFIRMED': (40, 120, 70), 'REPORTED': (90, 90, 120)}
cols = 4; bw4 = (W - 32 - 3 * 10) // cols; by0 = BY + 28
bf = font('NotoSans-Condensed', 14); kf = font('NotoSans-CondensedBlack', 13)
for i, (place, kind, t) in enumerate(briefs):
    cx = 16 + (i % cols) * (bw4 + 10); cy = by0 + (i // cols) * 86
    d.text((cx, cy), place, font=kf, fill=RED)
    tag(cx + text_w(place, kf) + 6, cy + 1, kind, TAGC[kind], font('NotoSans-CondensedBold', 10))
    para(cx, cy + 19, t, bf, bw4, fill=INK, lh=16)

# ---------------- sport strip ----------------
SY = by0 + 2 * 86 + 2
d.rectangle((16, SY, W - 16, SY + 54), fill=NAVY)
d.text((24, SY + 4), 'SPORT', font=font('NotoSans-CondensedBlack', 15), fill=(240, 190, 90))
sp = [('ATP FINALS, TURIN', 'Alcaraz beats No.1 Zverev 6-2 7-6'),
      ('PREMIER LEAGUE', 'Liverpool 4-0 Man Utd, Yoro sent off 8’'),
      ('F1 · LAS VEGAS', 'Verstappen wins by 0.639s, 75th win'),
      ('CRICKET · WELLINGTON', 'India 720/9 dec, a Test record in NZ')]
sw4 = (W - 32 - 80) // 4
for i, (a, b) in enumerate(sp):
    x = 92 + i * sw4
    d.text((x, SY + 5), a, font=font('NotoSans-CondensedBold', 11), fill=(170, 190, 225))
    para(x, SY + 20, b, font('NotoSans-CondensedSemiBold', 14), sw4 - 10, fill=(255, 255, 255), lh=16)

# ---------------- footer ----------------
FY = SY + 60
d.line((16, FY, W - 16, FY), fill=INK, width=1)
ff = font('NotoSans-Condensed', 11)
d.text((16, FY + 3), 'DATE CHECK: left out as not Sunday news: Trump–Xi–Putin Shenzhen summit (19-20 Nov), ICJ Rohingya ruling, EU–Indonesia trade deal (21 Nov).',
       font=ff, fill=MUTED)
d.text((16, FY + 17), 'Sources: AP, Reuters, AFP, CNN, Ukrainian Air Force, Kyiv regional administration, news.gov.hk, ATP, F1. Illustrations are artistic, not photographs.',
       font=ff, fill=MUTED)
d.rectangle((0, H - 4, W, H), fill=INK)

img.save(os.path.join(HERE, 'full.png'))
q = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
q.save(OUT, optimize=True)
print('bottom used', FY + 31, 'size', os.path.getsize(OUT))
