# -*- coding: utf-8 -*-
"""Sober vector figures in the Knowledge Center palette. Text uses text-anchor=middle only (safe in RTL). Icons: Lucide."""
import math, random
import icons as I

TEAL, NAVY, TEAL4, TEAL2, TEAL1, TEAL0 = '#0a5f6a', '#054473', '#3e8086', '#98babd', '#d2e3e5', '#e8f1f2'
CANVAS, MUTED, LINE, INK, SOFT, FAINT = '#f3eeec', '#eeeded', '#e7e2df', '#303336', '#5d656e', '#8a9199'

def _t(x, y, s, size=20, fill=INK, bold=False, w=None):
    wt = w or (700 if bold else 400)
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="middle" font-weight="{wt}">{s}</text>'

def _pill(cx, cy, w, s, fill='#fff', stroke=TEAL, size=18, color=INK, bold=True, h=32):
    return (f'<rect x="{cx-w/2:.0f}" y="{cy-h/2:.0f}" width="{w}" height="{h}" rx="{h/2:.0f}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
            + _t(cx, cy + size * 0.34, s, size, color, bold))

def _arrow_def(i, c):
    return (f'<marker id="b{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>')

def _wrap(w, h, inner, defs=''):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>{inner}</svg>'

# ---------------------------------------------------------------- generic tree (children: title, colour, icon, subs)
def tree(root, children, color=TEAL, W=900):
    n = len(children); gap = 14
    cw = (W - 24 - (n - 1) * gap) / n
    maxsub = max(len(c[3]) for c in children)
    H = 96 + 70 + maxsub * 42 + 20
    s = f'<rect width="{W}" height="{H}" rx="10" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
    s += f'<rect x="{W/2-150}" y="14" width="300" height="52" rx="8" fill="{color}"/>' + _t(W / 2, 49, root, 26, '#fff', True)
    for i, (title, c, ico, subs) in enumerate(children):
        x = W - 12 - cw * (i + 1) - gap * i
        cx = x + cw / 2
        s += f'<path d="M{W/2} 66 V92 H{cx} V108" fill="none" stroke="{c}" stroke-width="2.5"/>'
        s += f'<rect x="{x:.0f}" y="108" width="{cw:.0f}" height="62" rx="8" fill="{c}"/>'
        s += _t(cx, 148, title, 22, '#fff', True)
        if ico: s += I.nested(ico, x + cw - 26, 139, 26, '#fff')
        for j, sub in enumerate(subs):
            y = 196 + j * 42
            s += f'<rect x="{x+10:.0f}" y="{y-17}" width="{cw-20:.0f}" height="34" rx="6" fill="#fff" stroke="{c}" stroke-width="1.6"/>'
            s += _t(cx, y + 6, sub, 17, INK)
    return _wrap(W, H, s)

# ---------------------------------------------------------------- generic flow (steps run right -> left)
def flow(steps, W=900, H=210, color=TEAL, arrow=NAVY):
    n = len(steps); gap = 56
    bw = (W - 20 - (n - 1) * gap) / n
    s = f'<rect width="{W}" height="{H}" rx="10" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
    for i, st in enumerate(steps):
        x = W - 10 - bw * (i + 1) - gap * i
        c = st.get('c', color); f = st.get('f', TEAL0)
        s += f'<rect x="{x:.0f}" y="16" width="{bw:.0f}" height="{H-32}" rx="10" fill="{f}" stroke="{c}" stroke-width="2"/>'
        s += f'<circle cx="{x+bw/2:.0f}" cy="68" r="34" fill="#fff" stroke="{c}" stroke-width="1.6"/>'
        s += I.nested(st.get('e', 'leaf'), x + bw / 2, 68, 38, c)
        s += _t(x + bw / 2, 132, st['t'], 21, INK, True)
        if st.get('s'): s += _t(x + bw / 2, 160, st['s'], 15, SOFT)
        if i < n - 1:
            s += f'<line x1="{x-6:.0f}" y1="{H/2:.0f}" x2="{x-gap+8:.0f}" y2="{H/2:.0f}" stroke="{arrow}" stroke-width="4" marker-end="url(#b1)"/>'
    return _wrap(W, H, s, _arrow_def(1, arrow))

# ---------------------------------------------------------------- environment panorama (six panels with icons)
def env_panorama():
    W, H = 900, 330
    zones = [('بحر', '#cfe0ee', NAVY, ['waves', 'fish']), ('نهر', '#dbe9f1', NAVY, ['droplets', 'bird']),
             ('غابة', TEAL1, TEAL, ['trees', 'leaf']), ('صحراء', '#ece3d2', '#7a6a4a', ['sun', 'mountain']),
             ('مزرعة', TEAL0, TEAL, ['wheat', 'tractor']), ('مدينة', MUTED, SOFT, ['building-2', 'school'])]
    s = f'<rect width="{W}" height="{H}" rx="10" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
    zw = (W - 20) / 6
    for i, (n, bg, c, ics) in enumerate(zones):
        x = W - 10 - zw * (i + 1)
        s += f'<rect x="{x+3:.0f}" y="64" width="{zw-6:.0f}" height="212" rx="8" fill="{bg}"/>'
        s += I.nested(ics[0], x + zw / 2, 130, 62, c, 1.5)
        s += I.nested(ics[1], x + zw / 2, 208, 40, c, 1.5)
        s += _pill(x + zw / 2, 300, zw - 14, n, '#fff', c, 19, INK)
    def br(i0, i1, label, col):
        xr = W - 10 - zw * i0 - 3; xl = W - 10 - zw * (i1 + 1) + 3
        return (f'<path d="M{xr:.0f} 54 H{xl:.0f} M{xr:.0f} 48 V60 M{xl:.0f} 48 V60" stroke="{col}" stroke-width="2.4" fill="none"/>'
                + _t((xr + xl) / 2, 32, label, 21, col, True))
    s += br(0, 1, 'بيئة مائية', NAVY) + br(2, 4, 'بيئة يابسة', TEAL) + br(5, 5, 'بيئة مشيّدة', SOFT)
    return _wrap(W, H, s)

# ---------------------------------------------------------------- insect
def insect():
    W, H = 900, 330
    s = f'<rect width="{W}" height="{H}" rx="10" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
    for x0, dx in [(520, -40), (550, 0), (580, 40)]:
        for side in (1, -1):
            s += f'<path d="M{x0} 190 L{x0+dx*0.8:.0f} {190+side*60} L{x0+dx*1.3:.0f} {190+side*105}" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="M730 170 Q760 120 800 110 M730 190 Q770 150 820 150" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    s += f'<ellipse cx="540" cy="140" rx="95" ry="38" fill="{TEAL1}" opacity=".8" stroke="{TEAL4}" stroke-width="1.6" transform="rotate(-18 540 140)"/>'
    s += f'<ellipse cx="540" cy="240" rx="95" ry="38" fill="{TEAL1}" opacity=".8" stroke="{TEAL4}" stroke-width="1.6" transform="rotate(18 540 240)"/>'
    s += f'<ellipse cx="340" cy="190" rx="115" ry="50" fill="{TEAL4}" stroke="{INK}" stroke-width="2.5"/>'
    for x in (290, 340, 390):
        s += f'<path d="M{x} 142 Q{x+14} 190 {x} 238" stroke="{NAVY}" stroke-width="10" fill="none" opacity=".55"/>'
    s += f'<ellipse cx="545" cy="190" rx="70" ry="48" fill="{TEAL}" stroke="{INK}" stroke-width="2.5"/>'
    s += f'<circle cx="685" cy="190" r="48" fill="{NAVY}" stroke="{INK}" stroke-width="2.5"/><circle cx="702" cy="177" r="9" fill="#fff"/><circle cx="704" cy="177" r="4" fill="{INK}"/>'
    for cx, ty, lab in [(685, 50, 'الرأس'), (545, 50, 'الصدر'), (340, 50, 'البطن')]:
        s += _pill(cx, ty, 120, lab, '#fff', TEAL, 22)
    s += f'<path d="M685 66 V138 M545 66 V142 M340 66 V140" stroke="{TEAL}" stroke-width="1.6" stroke-dasharray="5 4"/>'
    s += _pill(450, 304, 480, 'ثلاثة أزواج من الأرجل (ست أرجل)', '#fff', SOFT, 20)
    return _wrap(W, H, s)

# ---------------------------------------------------------------- plant
def plant():
    W, H = 900, 430
    s = f'<rect width="{W}" height="{H}" rx="10" fill="{TEAL0}" stroke="{LINE}" stroke-width="1.5"/>'
    s += f'<rect x="1" y="290" width="898" height="139" rx="0" fill="#8b7765"/><path d="M1 290 H899" stroke="{TEAL}" stroke-width="6"/>'
    for dx in (-70, -35, 0, 35, 70):
        s += f'<path d="M450 292 Q{450+dx*0.9} 340 {450+dx*1.5} 395" stroke="{CANVAS}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M450 292 V380" stroke="{CANVAS}" stroke-width="7" stroke-linecap="round"/>'
    s += f'<rect x="441" y="130" width="18" height="164" rx="6" fill="{TEAL}"/>'
    s += f'<ellipse cx="520" cy="215" rx="66" ry="25" fill="{TEAL4}" transform="rotate(-24 520 215)"/><ellipse cx="380" cy="235" rx="66" ry="25" fill="{TEAL4}" transform="rotate(24 380 235)"/>'
    for a in range(0, 360, 60):
        px, py = 450 + 34 * math.cos(math.radians(a)), 104 + 34 * math.sin(math.radians(a))
        s += f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="20" ry="13" fill="#fff" stroke="{TEAL2}" stroke-width="1.5" transform="rotate({a} {px:.0f} {py:.0f})"/>'
    s += f'<circle cx="450" cy="104" r="15" fill="{NAVY}"/>'
    s += f'<path d="M455 170 Q520 150 560 172" stroke="{TEAL}" stroke-width="5" fill="none"/><circle cx="570" cy="192" r="26" fill="{NAVY}"/><circle cx="562" cy="186" r="5" fill="{TEAL2}" opacity=".7"/>'
    lab = [(190, 80, 'الزهرة: عضو التكاثر', 450, 104, 'L'), (190, 160, 'الورقة: مصنع الغذاء', 385, 232, 'L'),
           (190, 240, 'الساق: تحمل النبات', 441, 250, 'L'), (190, 360, 'الجذر: يثبّت النبات', 440, 360, 'L'),
           (710, 130, 'الثمرة: تحمي البذور', 592, 190, 'R')]
    for x, y, t, tx, ty, side in lab:
        s += f'<line x1="{x+105 if side=="L" else x-105}" y1="{y}" x2="{tx}" y2="{ty}" stroke="{INK}" stroke-width="1.6"/><circle cx="{tx}" cy="{ty}" r="3.5" fill="{INK}"/>'
        s += _pill(x, y, 210, t, '#fff', TEAL, 18)
    return _wrap(W, H, s)

# ---------------------------------------------------------------- seeds
def seeds():
    W, H = 900, 300
    s = f'<rect width="{W}" height="{H}" rx="10" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
    s += f'<ellipse cx="680" cy="130" rx="110" ry="68" fill="{CANVAS}" stroke="{SOFT}" stroke-width="2.5"/>'
    s += f'<path d="M610 130 Q680 60 750 130 Q680 195 610 130 Z" fill="{TEAL1}" stroke="{SOFT}" stroke-width="1.6"/><ellipse cx="740" cy="150" rx="20" ry="12" fill="{TEAL}"/>'
    s += _t(680, 232, 'فلقة واحدة', 24, NAVY, True) + _t(680, 262, 'القمح • الشعير • الأرز • التمر', 17, SOFT)
    s += f'<line x1="450" y1="30" x2="450" y2="270" stroke="{LINE}" stroke-width="2" stroke-dasharray="6 6"/>'
    s += f'<path d="M180 135 Q160 60 240 70 Q300 90 280 150 Q250 195 200 175 Z" fill="{CANVAS}" stroke="{SOFT}" stroke-width="2.5"/>'
    s += f'<path d="M330 135 Q310 60 390 70 Q445 90 425 150 Q395 195 350 175 Z" fill="{CANVAS}" stroke="{SOFT}" stroke-width="2.5" transform="translate(-30 0)"/>'
    s += f'<ellipse cx="300" cy="150" rx="20" ry="11" fill="{TEAL}"/>'
    s += _t(300, 232, 'فلقتان', 24, NAVY, True) + _t(300, 262, 'الفاصولياء • الحمص • العدس', 17, SOFT)
    return _wrap(W, H, s)

# ---------------------------------------------------------------- earth
def earth():
    W, H = 900, 380
    random.seed(3)
    s = f'<rect width="{W}" height="{H}" rx="10" fill="{NAVY}"/>'
    for _ in range(60):
        s += f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,H):.0f}" r="{random.uniform(.5,1.6):.1f}" fill="#fff" opacity=".5"/>'
    cx, cy = 660, 190
    s += f'<circle cx="{cx}" cy="{cy}" r="172" fill="{TEAL2}" opacity=".22"/><circle cx="{cx}" cy="{cy}" r="150" fill="#1f6291"/>'
    s += '<clipPath id="ec"><circle cx="660" cy="190" r="150"/></clipPath><g clip-path="url(#ec)" fill="#98babd">'
    s += '<path d="M560 120 Q600 80 650 110 Q680 150 640 190 Q600 200 570 170 Z"/><path d="M680 220 Q740 190 790 230 Q780 290 720 320 Q690 280 680 220 Z"/><path d="M590 250 Q620 240 640 270 Q630 320 600 320 Z"/></g>'
    for y, lab, c, ex, ey in [(80, 'الهواء يحيط بالأرض', TEAL2, cx - 130, 70), (190, 'اليابسة: تربة وصخور', TEAL2, cx - 90, 150), (300, 'الماء: بحار وأنهار', '#1f6291', cx - 50, 230)]:
        s += _pill(210, y, 340, lab, '#fff', c, 20)
        s += f'<line x1="380" y1="{y}" x2="{ex}" y2="{ey}" stroke="{c if c != "#1f6291" else "#6a9fc4"}" stroke-width="2.2"/>'
    return _wrap(W, H, s)

# ---------------------------------------------------------------- soil
def soil():
    W, H = 900, 380
    random.seed(8)
    s = f'<rect width="{W}" height="{H}" rx="10" fill="{TEAL0}" stroke="{LINE}" stroke-width="1.5"/>'
    s += f'<rect x="481" y="190" width="418" height="189" fill="#8b7765"/><path d="M481 190 H899" stroke="{TEAL}" stroke-width="6"/>'
    s += f'<rect x="670" y="110" width="12" height="82" fill="{TEAL}"/><ellipse cx="702" cy="130" rx="26" ry="11" fill="{TEAL4}" transform="rotate(-24 702 130)"/><ellipse cx="650" cy="140" rx="26" ry="11" fill="{TEAL4}" transform="rotate(24 650 140)"/>'
    for dx in (-50, -25, 0, 25, 50):
        s += f'<path d="M676 192 Q{676+dx*0.8} 240 {676+dx*1.4} 300" stroke="{CANVAS}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    s += _pill(690, 340, 340, 'الجذور تثبّت النبات وتمتصّ الماء والأملاح', '#fff', '#8b7765', 16)
    cx, cy, r = 230, 190, 150
    s += f'<clipPath id="mc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><circle cx="{cx}" cy="{cy}" r="{r}" fill="#9a8672" stroke="{INK}" stroke-width="3"/><g clip-path="url(#mc)">'
    for _ in range(46):
        x = cx + random.uniform(-r, r); y = cy + random.uniform(-r, r)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(8,14):.0f}" fill="#e7dcc3" stroke="#bfae8a" stroke-width="1.5"/>'
    for _ in range(160):
        x = cx + random.uniform(-r, r); y = cy + random.uniform(-r, r)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(2,3.5):.1f}" fill="#8a9199"/>'
    for _ in range(18):
        x = cx + random.uniform(-r, r); y = cy + random.uniform(-r, r)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(8,15):.0f}" ry="{random.uniform(5,8):.0f}" fill="#2c241c" transform="rotate({random.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    s += '</g>'
    s += _t(230, 30, 'تكبير حبيبات التربة', 20, SOFT, True)
    s += _pill(405, 130, 130, 'رمل', '#e7dcc3', '#bfae8a', 19) + _pill(405, 190, 130, 'طين', '#8a9199', SOFT, 19, '#fff') + _pill(405, 250, 130, 'دبال', '#2c241c', INK, 19, '#fff')
    return _wrap(W, H, s)

# ---------------------------------------------------------------- desertification before/after
def desertification():
    W, H = 900, 360
    s = f'<rect width="{W}" height="{H}" rx="10" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
    s += f'<rect x="470" y="40" width="420" height="270" rx="8" fill="#d6e6f0"/><rect x="470" y="180" width="420" height="130" fill="{TEAL4}"/>'
    for i in range(5):
        s += f'<path d="M{480+i*84} 196 H{540+i*84}" stroke="{TEAL0}" stroke-width="3" opacity=".8"/><path d="M{480+i*84} 236 H{540+i*84}" stroke="{TEAL0}" stroke-width="3" opacity=".8"/>'
    for x in (500, 590, 690, 790, 850):
        s += I.nested('wheat', x, 258, 46, TEAL0, 1.6)
    s += I.nested('tree-palm', 560, 140, 70, TEAL, 1.6) + I.nested('tree-palm', 800, 140, 70, TEAL, 1.6) + I.nested('sun', 690, 86, 46, '#7a6a4a', 1.6)
    s += _pill(680, 336, 300, 'قبل: أرض زراعية', '#fff', TEAL, 19)
    s += f'<rect x="10" y="40" width="420" height="270" rx="8" fill="#ece3d2"/><rect x="10" y="180" width="420" height="130" fill="{TEAL4}"/>'
    s += '<path d="M10 300 Q100 190 190 250 Q280 170 430 240 V310 H10 Z" fill="#dcc99f"/><path d="M10 310 Q120 235 230 285 Q330 230 430 280 V310 Z" fill="#c9b080"/>'
    s += I.nested('tree-palm', 140, 190, 56, TEAL, 1.6) + I.nested('wind', 330, 110, 56, SOFT, 1.6) + I.nested('wind', 250, 80, 40, SOFT, 1.6) + I.nested('sun', 380, 80, 44, '#7a6a4a', 1.6)
    s += _pill(220, 336, 340, 'بعد: زحف الرمال على الأرض', '#fff', NAVY, 19)
    s += f'<path d="M455 190 H440" stroke="{INK}" stroke-width="3" marker-end="url(#b5)"/>'
    return _wrap(W, H, s, _arrow_def(5, INK))

# ---------------------------------------------------------------- clean vs polluted
def clean_vs_polluted():
    W, H = 900, 340
    s = f'<rect width="{W}" height="{H}" rx="10" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
    s += f'<rect x="470" y="30" width="420" height="260" rx="8" fill="#d6e6f0"/><rect x="470" y="190" width="420" height="100" fill="#a9c9d9"/><path d="M470 190 Q600 175 700 190 T890 188 V212 H470Z" fill="{TEAL4}"/>'
    s += I.nested('sun', 530, 96, 56, '#7a6a4a', 1.6) + I.nested('trees', 650, 150, 90, TEAL, 1.5) + I.nested('bird', 830, 100, 44, NAVY, 1.6) + I.nested('fish', 700, 250, 44, NAVY, 1.6)
    s += _pill(680, 316, 260, 'بيئة نظيفة', '#fff', TEAL, 19)
    s += f'<rect x="10" y="30" width="420" height="260" rx="8" fill="#c9c6c0"/><rect x="10" y="190" width="420" height="100" fill="#8e8672"/><path d="M10 190 Q140 178 240 190 T430 186 V210 H10Z" fill="#7a7766"/>'
    s += I.nested('factory', 120, 150, 90, INK, 1.5) + I.nested('cloud', 150, 80, 60, SOFT, 1.6) + I.nested('cloud', 230, 60, 44, SOFT, 1.6) + I.nested('truck', 310, 160, 56, INK, 1.6) + I.nested('trash-2', 250, 250, 44, INK, 1.6) + I.nested('fuel', 350, 250, 40, INK, 1.6)
    s += _pill(220, 316, 260, 'بيئة ملوّثة', '#fff', '#b42d26', 19)
    return _wrap(W, H, s)

# ---------------------------------------------------------------- what a plant needs
def plant_needs():
    W, H = 900, 360
    s = f'<rect width="{W}" height="{H}" rx="10" fill="{TEAL0}" stroke="{LINE}" stroke-width="1.5"/>'
    s += f'<rect x="1" y="250" width="898" height="109" fill="#8b7765"/><path d="M1 250 H899" stroke="{TEAL}" stroke-width="6"/>'
    s += f'<rect x="441" y="120" width="16" height="132" rx="6" fill="{TEAL}"/><ellipse cx="515" cy="160" rx="62" ry="24" fill="{TEAL4}" transform="rotate(-20 515 160)"/><ellipse cx="385" cy="175" rx="62" ry="24" fill="{TEAL4}" transform="rotate(20 385 175)"/><ellipse cx="450" cy="118" rx="28" ry="38" fill="{TEAL2}"/>'
    for dx in (-50, 0, 50):
        s += f'<path d="M450 252 Q{450+dx*0.9} 292 {450+dx*1.4} 335" stroke="{CANVAS}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
    s += I.nested('sun', 790, 70, 64, '#7a6a4a', 1.5) + _pill(790, 132, 200, 'ضوء الشمس', '#fff', '#7a6a4a', 19)
    s += f'<line x1="740" y1="100" x2="540" y2="140" stroke="#7a6a4a" stroke-width="3" marker-end="url(#b2)"/>'
    s += _pill(160, 70, 260, 'ثاني أكسيد الكربون', '#fff', SOFT, 19) + f'<line x1="270" y1="86" x2="385" y2="150" stroke="{SOFT}" stroke-width="3" marker-end="url(#b3)"/>'
    s += _pill(160, 300, 200, 'الماء', '#fff', NAVY, 19) + f'<line x1="250" y1="300" x2="385" y2="300" stroke="{NAVY}" stroke-width="3" marker-end="url(#b4)"/>'
    s += _pill(720, 250, 300, 'المادة الخضراء في الأوراق', '#fff', TEAL, 18) + f'<line x1="590" y1="250" x2="510" y2="175" stroke="{TEAL}" stroke-width="2.5" marker-end="url(#b6)"/>'
    s += _pill(450, 24, 360, 'ينتج النبات غذاءه بنفسه', TEAL1, TEAL, 19)
    return _wrap(W, H, s, _arrow_def(2, '#7a6a4a') + _arrow_def(3, SOFT) + _arrow_def(4, NAVY) + _arrow_def(6, TEAL))

# ---------------------------------------------------------------- dunes
def dunes():
    W, H = 900, 300
    s = f'<rect width="{W}" height="{H}" rx="10" fill="#e6eef2"/>'
    s += I.nested('sun', 790, 70, 60, '#7a6a4a', 1.5)
    s += '<path d="M0 300 V210 Q120 120 250 200 Q360 120 520 210 Q660 110 900 220 V300Z" fill="#dcc99f"/><path d="M0 300 V250 Q160 190 320 250 Q500 190 680 255 Q800 220 900 250 V300Z" fill="#c9b080"/>'
    s += f'<line x1="60" y1="90" x2="250" y2="90" stroke="{SOFT}" stroke-width="4" marker-end="url(#b7)"/><line x1="100" y1="125" x2="300" y2="125" stroke="{SOFT}" stroke-width="4" marker-end="url(#b7)"/>'
    s += _pill(160, 58, 200, 'الرياح تنقل الرمال', '#fff', SOFT, 18) + _pill(450, 276, 300, 'الكثبان الرملية', '#fff', '#7a6a4a', 20)
    return _wrap(W, H, s, _arrow_def(7, SOFT))
