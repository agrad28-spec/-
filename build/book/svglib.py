# -*- coding: utf-8 -*-
"""Vector illustrations for the science book (inline SVG; text uses only text-anchor=middle)."""
import math, random

def _t(x, y, s, size=20, fill='#222', bold=False, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="middle"{" font-weight=\"700\"" if bold else ""} {extra}>{s}</text>'

def _pill(cx, cy, w, s, fill='#fff', stroke='#888', size=18, color='#222', bold=True, h=32):
    return (f'<rect x="{cx-w/2:.0f}" y="{cy-h/2:.0f}" width="{w}" height="{h}" rx="{h/2:.0f}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            + _t(cx, cy + size*0.34, s, size, color, bold))

def _arrow_def(i, c):
    return (f'<marker id="b{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>')

def _wrap(w, h, inner, defs=''):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>{inner}</svg>'

# ---------------------------------------------------------------- generic tree
def tree(root, children, color='#0a5f6a', W=900):
    n = len(children)
    gap = 14
    cw = (W - 24 - (n - 1) * gap) / n
    maxsub = max(len(c[3]) for c in children)
    H = 96 + 70 + maxsub * 42 + 20
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#fafbfc" stroke="#d9dee6"/>'
    s += f'<rect x="{W/2-150}" y="14" width="300" height="52" rx="14" fill="{color}"/>' + _t(W/2, 49, root, 26, '#fff', True)
    for i, (title, c, e, subs) in enumerate(children):
        x = W - 12 - cw * (i + 1) - gap * i
        cx = x + cw / 2
        s += f'<path d="M{W/2} 66 V92 H{cx} V108" fill="none" stroke="{c}" stroke-width="3"/>'
        s += f'<rect x="{x:.0f}" y="108" width="{cw:.0f}" height="62" rx="14" fill="{c}"/>'
        s += _t(cx, 150, f'{e} {title}', 22, '#fff', True)
        for j, sub in enumerate(subs):
            y = 196 + j * 42
            s += f'<rect x="{x+10:.0f}" y="{y-17}" width="{cw-20:.0f}" height="34" rx="17" fill="#fff" stroke="{c}" stroke-width="2"/>'
            s += _t(cx, y + 6, sub, 17, '#222')
    return _wrap(W, H, s)

# ---------------------------------------------------------------- generic flow (steps go right -> left)
def flow(steps, W=900, H=210, color='#0a5f6a', arrow='#054473'):
    n = len(steps)
    gap = 56
    bw = (W - 20 - (n - 1) * gap) / n
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#fafbfc" stroke="#d9dee6"/>'
    for i, st in enumerate(steps):
        x = W - 10 - bw * (i + 1) - gap * i
        c = st.get('c', color); f = st.get('f', '#fff')
        s += f'<rect x="{x:.0f}" y="16" width="{bw:.0f}" height="{H-32}" rx="16" fill="{f}" stroke="{c}" stroke-width="3"/>'
        s += _t(x + bw / 2, 90, st.get('e', ''), 56)
        s += _t(x + bw / 2, 132, st['t'], 21, '#222', True)
        if st.get('s'):
            s += _t(x + bw / 2, 160, st['s'], 15, '#555')
        if i < n - 1:
            s += f'<line x1="{x-6:.0f}" y1="{H/2:.0f}" x2="{x-gap+8:.0f}" y2="{H/2:.0f}" stroke="{arrow}" stroke-width="5" marker-end="url(#b1)"/>'
    return _wrap(W, H, s, _arrow_def(1, arrow))

# ---------------------------------------------------------------- environment panorama
def env_panorama():
    W, H = 900, 380
    zones = [('بحر', 'ماء مالح', '#3d9be9', ['🌊', '🐬', '🚢', '🐟'], 0), ('نهر', 'ماء عذب', '#74c0fc', ['🏞️', '🦆', '🐠', '🌿'], 0),
             ('غابة', 'يابسة', '#69b36d', ['🌲', '🌳', '🦌', '🌲'], 1), ('صحراء', 'يابسة', '#f2d78f', ['🏜️', '🌵', '🐪', '☀️'], 1),
             ('مزرعة', 'يابسة', '#b8dd7a', ['🌾', '🚜', '🐄', '🌴'], 1), ('مدينة', 'مشيّدة', '#ced4da', ['🏢', '🏫', '🏠', '🚗'], 2)]
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#fff" stroke="#d9dee6"/>'
    zw = (W - 20) / 6
    for i, (n, sub, c, ems, g) in enumerate(zones):
        x = W - 10 - zw * (i + 1)
        s += f'<rect x="{x:.0f}" y="66" width="{zw:.0f}" height="262" fill="{c}" opacity=".85" {"rx=\"10\"" if i in (0,5) else ""}/>'
        pos = [(0.5, 120), (0.28, 190), (0.72, 215), (0.5, 270)]
        for (fx, y), e in zip(pos, ems):
            s += _t(x + zw * fx, y, e, 46)
        s += _pill(x + zw / 2, 346, zw - 10, f'{n}', '#fff', '#555', 20)
    # brackets
    def br(i0, i1, label, col):
        xr = W - 10 - zw * i0; xl = W - 10 - zw * (i1 + 1)
        return (f'<path d="M{xr-4:.0f} 56 H{xl+4:.0f} M{xr-4:.0f} 50 V62 M{xl+4:.0f} 50 V62" stroke="{col}" stroke-width="3" fill="none"/>'
                + _t((xr + xl) / 2, 34, label, 21, col, True))
    s += br(0, 1, 'بيئة مائية', '#1c7ed6') + br(2, 4, 'بيئة يابسة', '#2b8a3e') + br(5, 5, 'بيئة مشيّدة', '#495057')
    return _wrap(W, H, s)

# ---------------------------------------------------------------- insect body
def insect():
    W, H = 900, 330
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#f7fbf2" stroke="#d9dee6"/>'
    # legs
    for x0, dx in [(520, -40), (550, 0), (580, 40)]:
        for side in (1, -1):
            s += f'<path d="M{x0} 190 L{x0+dx*0.8:.0f} {190+side*60} L{x0+dx*1.3:.0f} {190+side*105}" stroke="#5c3d10" stroke-width="7" fill="none" stroke-linecap="round"/>'
    # antennae
    s += '<path d="M730 170 Q760 120 800 110 M730 190 Q770 150 820 150" stroke="#5c3d10" stroke-width="5" fill="none"/>'
    # wings
    s += '<ellipse cx="540" cy="140" rx="95" ry="38" fill="#cfe8ff" opacity=".75" stroke="#74b9f5" transform="rotate(-18 540 140)"/>'
    s += '<ellipse cx="540" cy="240" rx="95" ry="38" fill="#cfe8ff" opacity=".75" stroke="#74b9f5" transform="rotate(18 540 240)"/>'
    # body
    s += '<ellipse cx="340" cy="190" rx="115" ry="50" fill="#ffd43b" stroke="#5c3d10" stroke-width="3"/>'
    for x in (290, 340, 390):
        s += f'<path d="M{x} 142 Q{x+14} 190 {x} 238" stroke="#5c3d10" stroke-width="12" fill="none" opacity=".75"/>'
    s += '<ellipse cx="545" cy="190" rx="70" ry="48" fill="#f59f00" stroke="#5c3d10" stroke-width="3"/>'
    s += '<circle cx="685" cy="190" r="48" fill="#e8590c" stroke="#5c3d10" stroke-width="3"/><circle cx="700" cy="177" r="9" fill="#fff"/><circle cx="702" cy="177" r="4" fill="#222"/>'
    # labels (above)
    for cx, ty, lab, tx in [(685, 50, 'الرأس', 685), (545, 50, 'الصدر', 545), (340, 50, 'البطن', 340)]:
        s += _pill(tx, ty, 120, lab, '#fff', '#e8590c', 22)
    s += '<path d="M685 66 V138 M545 66 V142 M340 66 V140" stroke="#e8590c" stroke-width="2" stroke-dasharray="5 4"/>'
    s += _pill(450, 308, 480, 'ثلاثة أزواج من الأرجل = 6 أرجل', '#fff', '#5c3d10', 20)
    return _wrap(W, H, s)

# ---------------------------------------------------------------- plant diagram
def plant():
    W, H = 900, 430
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#eaf7ff" stroke="#d9dee6"/>'
    s += '<rect x="0" y="290" width="900" height="140" rx="0" fill="#8b5a2b"/><path d="M0 290 H900" stroke="#3b8f3f" stroke-width="8"/>'
    # roots
    for dx in (-70, -35, 0, 35, 70):
        s += f'<path d="M450 292 Q{450+dx*0.9} 340 {450+dx*1.5} 395" stroke="#e6c9a0" stroke-width="6" fill="none"/>'
    s += '<path d="M450 292 V380" stroke="#e6c9a0" stroke-width="8"/>'
    # stem
    s += '<rect x="441" y="130" width="18" height="164" rx="6" fill="#3b8f3f"/>'
    # leaves
    s += '<ellipse cx="520" cy="215" rx="66" ry="25" fill="#51b155" transform="rotate(-24 520 215)"/><ellipse cx="380" cy="235" rx="66" ry="25" fill="#51b155" transform="rotate(24 380 235)"/>'
    # flower
    for a in range(0, 360, 60):
        s += f'<ellipse cx="{450+34*math.cos(math.radians(a)):.0f}" cy="{104+34*math.sin(math.radians(a)):.0f}" rx="20" ry="13" fill="#ff8fab" transform="rotate({a} {450+34*math.cos(math.radians(a)):.0f} {104+34*math.sin(math.radians(a)):.0f})"/>'
    s += '<circle cx="450" cy="104" r="16" fill="#ffd43b"/>'
    # fruit on a branch
    s += '<path d="M455 170 Q520 150 560 172" stroke="#3b8f3f" stroke-width="6" fill="none"/><circle cx="570" cy="190" r="26" fill="#e03131"/><path d="M570 164 q8 -10 16 -8" stroke="#2b8a3e" stroke-width="4" fill="none"/>'
    # labels
    lab = [(190, 80, 'الزهرة: عضو التكاثر', 450, 104, 'L'), (190, 160, 'الورقة: مصنع الغذاء', 385, 232, 'L'),
           (190, 240, 'الساق: تحمل النبات', 441, 250, 'L'), (190, 360, 'الجذر: يثبّت النبات', 440, 360, 'L'),
           (710, 130, 'الثمرة: تحمي البذور', 592, 188, 'R')]
    for x, y, t, tx, ty, side in lab:
        s += f'<line x1="{x+105 if side=="L" else x-105}" y1="{y}" x2="{tx}" y2="{ty}" stroke="#444" stroke-width="2"/><circle cx="{tx}" cy="{ty}" r="4" fill="#444"/>'
        s += _pill(x, y, 210, t, '#fff', '#2b8a3e', 18)
    return _wrap(W, H, s)

# ---------------------------------------------------------------- seeds
def seeds():
    W, H = 900, 300
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#fffaf0" stroke="#d9dee6"/>'
    # monocot (right)
    s += '<ellipse cx="680" cy="130" rx="110" ry="68" fill="#e8c27c" stroke="#8a6a2a" stroke-width="3"/>'
    s += '<path d="M610 130 Q680 60 750 130 Q680 195 610 130 Z" fill="#f4e2b8" stroke="#8a6a2a" stroke-width="2"/><ellipse cx="740" cy="150" rx="20" ry="12" fill="#6fae4a"/>'
    s += _t(680, 232, 'فلقة واحدة', 24, '#8a5a00', True) + _t(680, 262, 'القمح • الشعير • الأرز • التمر', 17, '#444')
    s += '<line x1="450" y1="30" x2="450" y2="270" stroke="#bbb" stroke-dasharray="6 6"/>'
    # dicot (left): two halves
    s += '<path d="M180 135 Q160 60 240 70 Q300 90 280 150 Q250 195 200 175 Z" fill="#d9a066" stroke="#7a4a1a" stroke-width="3"/>'
    s += '<path d="M330 135 Q310 60 390 70 Q445 90 425 150 Q395 195 350 175 Z" fill="#d9a066" stroke="#7a4a1a" stroke-width="3" transform="translate(-30 0)"/>'
    s += '<ellipse cx="300" cy="150" rx="20" ry="11" fill="#6fae4a"/>'
    s += _t(300, 232, 'فلقتان', 24, '#8a5a00', True) + _t(300, 262, 'الفاصولياء • الحمص • العدس', 17, '#444')
    return _wrap(W, H, s)

# ---------------------------------------------------------------- earth
def earth():
    W, H = 900, 380
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>'
    random.seed(3)
    for _ in range(60):
        s += f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,H):.0f}" r="{random.uniform(.5,1.6):.1f}" fill="#fff" opacity=".6"/>'
    cx, cy = 660, 190
    s += f'<circle cx="{cx}" cy="{cy}" r="172" fill="#8fd3ff" opacity=".28"/><circle cx="{cx}" cy="{cy}" r="150" fill="#2f78d4"/>'
    s += '<clipPath id="ec"><circle cx="660" cy="190" r="150"/></clipPath><g clip-path="url(#ec)" fill="#52b058">'
    s += '<path d="M560 120 Q600 80 650 110 Q680 150 640 190 Q600 200 570 170 Z"/><path d="M680 220 Q740 190 790 230 Q780 290 720 320 Q690 280 680 220 Z"/><path d="M590 250 Q620 240 640 270 Q630 320 600 320 Z"/></g>'
    for y, lab, c, ty, tx in [(80, 'الهواء يحيط بالأرض', '#8fd3ff', 70, 520), (170, 'اليابسة: تربة وصخور', '#52b058', 160, 600), (260, 'الماء: بحار وأنهار', '#2f78d4', 250, 610)]:
        pass
    s += _pill(210, 80, 340, 'الهواء يحيط بالأرض', '#fff', '#8fd3ff', 20)
    s += f'<line x1="380" y1="80" x2="{cx-130}" y2="70" stroke="#8fd3ff" stroke-width="2.5"/>'
    s += _pill(210, 190, 340, 'اليابسة: تربة وصخور', '#fff', '#52b058', 20)
    s += f'<line x1="380" y1="190" x2="{cx-90}" y2="150" stroke="#52b058" stroke-width="2.5"/>'
    s += _pill(210, 300, 340, 'الماء: بحار وأنهار', '#fff', '#2f78d4', 20)
    s += f'<line x1="380" y1="300" x2="{cx-50}" y2="230" stroke="#2f78d4" stroke-width="2.5"/>'
    return _wrap(W, H, s)

# ---------------------------------------------------------------- soil
def soil():
    W, H = 900, 380
    random.seed(8)
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#eaf7ff" stroke="#d9dee6"/>'
    # cross section (right)
    s += '<rect x="480" y="190" width="400" height="170" fill="#8b5a2b"/><path d="M480 190 H880" stroke="#3b8f3f" stroke-width="8"/>'
    s += '<rect x="670" y="110" width="12" height="82" fill="#3b8f3f"/><ellipse cx="702" cy="130" rx="26" ry="11" fill="#51b155" transform="rotate(-24 702 130)"/><ellipse cx="650" cy="140" rx="26" ry="11" fill="#51b155" transform="rotate(24 650 140)"/>'
    for dx in (-50, -25, 0, 25, 50):
        s += f'<path d="M676 192 Q{676+dx*0.8} 240 {676+dx*1.4} 300" stroke="#f0d4a8" stroke-width="4" fill="none"/>'
    s += _pill(680, 340, 330, 'الجذور تثبّت النبات وتمتصّ الماء والأملاح', '#fff', '#8b5a2b', 16)
    # magnified circle (left)
    cx, cy, r = 230, 190, 150
    s += f'<clipPath id="mc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><circle cx="{cx}" cy="{cy}" r="{r}" fill="#a97c50" stroke="#5c3d10" stroke-width="4"/><g clip-path="url(#mc)">'
    for _ in range(46):
        x = cx + random.uniform(-r, r); y = cy + random.uniform(-r, r)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(8,14):.0f}" fill="#e8cf9a" stroke="#b89960" stroke-width="1.5"/>'
    for _ in range(160):
        x = cx + random.uniform(-r, r); y = cy + random.uniform(-r, r)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(2,3.5):.1f}" fill="#8a8f96"/>'
    for _ in range(18):
        x = cx + random.uniform(-r, r); y = cy + random.uniform(-r, r)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(8,15):.0f}" ry="{random.uniform(5,8):.0f}" fill="#3b2a14" transform="rotate({random.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    s += '</g>'
    s += _t(230, 30, 'تكبير حبيبات التربة', 20, '#444', True)
    s += _pill(405, 130, 130, 'رمل', '#e8cf9a', '#b89960', 19) + _pill(405, 190, 130, 'طين', '#8a8f96', '#555', 19, '#fff') + _pill(405, 250, 130, 'دبال', '#3b2a14', '#000', 19, '#fff')
    return _wrap(W, H, s)

# ---------------------------------------------------------------- before / after desertification
def desertification():
    W, H = 900, 360
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#fff" stroke="#d9dee6"/>'
    # before (right)
    s += '<rect x="470" y="40" width="420" height="270" rx="12" fill="#bfe6ff"/><rect x="470" y="180" width="420" height="130" fill="#6fbf5a"/>'
    for i in range(5):
        s += f'<path d="M{480+i*84} 190 H{540+i*84}" stroke="#3b8f3f" stroke-width="3" opacity=".7"/>'
    for x in (500, 590, 690, 790, 850):
        s += _t(x, 250, '🌾', 40)
    s += _t(560, 160, '🌴', 52) + _t(790, 160, '🌴', 52) + _t(680, 90, '☀️', 44)
    s += _pill(680, 336, 300, 'قبل: أرض زراعية خضراء', '#fff', '#2b8a3e', 19)
    # after (left)
    s += '<rect x="10" y="40" width="420" height="270" rx="12" fill="#f6e2b3"/><rect x="10" y="180" width="420" height="130" fill="#6fbf5a"/>'
    s += '<path d="M10 300 Q100 190 190 250 Q280 170 430 240 V310 H10 Z" fill="#e7c36e"/><path d="M10 310 Q120 235 230 285 Q330 230 430 280 V310 Z" fill="#d6ac52"/>'
    s += _t(60, 235, '🥀', 36) + _t(140, 205, '🌴', 40)
    s += _t(330, 120, '💨', 48) + _t(260, 90, '💨', 36) + _t(380, 70, '☀️', 44)
    s += _pill(220, 336, 340, 'بعد: زحف الرمال على الأرض', '#fff', '#c92a2a', 19)
    s += '<path d="M455 190 H440" stroke="#444" stroke-width="3" marker-end="url(#b5)"/>'
    return _wrap(W, H, s, _arrow_def(5, '#444'))

# ---------------------------------------------------------------- clean vs polluted
def clean_vs_polluted():
    W, H = 900, 340
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#fff" stroke="#d9dee6"/>'
    # clean right
    s += '<rect x="470" y="30" width="420" height="260" rx="12" fill="#bfe6ff"/><rect x="470" y="190" width="420" height="100" fill="#74c0fc"/><path d="M470 190 Q600 175 700 190 T890 188 V210 H470Z" fill="#69b36d"/>'
    s += _t(520, 110, '☀️', 46) + _t(640, 170, '🌳', 60) + _t(760, 170, '🌳', 54) + _t(840, 100, '🐦', 36) + _t(700, 255, '🐟', 34) + _t(580, 245, '🐠', 30)
    s += _pill(680, 316, 260, 'بيئة نظيفة', '#fff', '#2b8a3e', 19)
    # polluted left
    s += '<rect x="10" y="30" width="420" height="260" rx="12" fill="#b9b3a8"/><rect x="10" y="190" width="420" height="100" fill="#8a7a52"/><path d="M10 190 Q140 178 240 190 T430 186 V210 H10Z" fill="#7c8a6a"/>'
    s += _t(120, 150, '🏭', 66) + _t(130, 90, '☁️', 48) + _t(200, 70, '☁️', 36) + _t(300, 160, '🚗', 40) + _t(250, 262, '🗑️', 36) + _t(350, 250, '🛢️', 34) + _t(70, 262, '🥫', 28)
    s += _pill(220, 316, 260, 'بيئة ملوّثة', '#fff', '#c92a2a', 19)
    return _wrap(W, H, s)

# ---------------------------------------------------------------- food chain pictures are produced with flow(); plant needs:
def plant_needs():
    W, H = 900, 360
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#eaf7ff" stroke="#d9dee6"/>'
    s += '<rect x="0" y="250" width="900" height="110" fill="#8b5a2b"/><path d="M0 250 H900" stroke="#3b8f3f" stroke-width="8"/>'
    s += '<rect x="441" y="120" width="16" height="132" rx="6" fill="#3b8f3f"/><ellipse cx="515" cy="160" rx="62" ry="24" fill="#51b155" transform="rotate(-20 515 160)"/><ellipse cx="385" cy="175" rx="62" ry="24" fill="#51b155" transform="rotate(20 385 175)"/><ellipse cx="450" cy="118" rx="28" ry="38" fill="#66bb6a"/>'
    for dx in (-50, 0, 50):
        s += f'<path d="M450 252 Q{450+dx*0.9} 292 {450+dx*1.4} 335" stroke="#e6c9a0" stroke-width="5" fill="none"/>'
    s += _t(790, 70, '☀️', 66) + _pill(790, 132, 200, 'ضوء الشمس', '#fff7d6', '#f08c00', 19)
    s += '<line x1="740" y1="95" x2="540" y2="140" stroke="#f08c00" stroke-width="4" marker-end="url(#b2)"/>'
    s += _pill(160, 70, 260, 'ثاني أكسيد الكربون', '#fff', '#495057', 19) + '<line x1="270" y1="86" x2="385" y2="150" stroke="#495057" stroke-width="4" marker-end="url(#b3)"/>'
    s += _pill(160, 300, 200, 'الماء', '#e7f5ff', '#1c7ed6', 19) + '<line x1="250" y1="300" x2="385" y2="300" stroke="#1c7ed6" stroke-width="4" marker-end="url(#b4)"/>'
    s += _pill(720, 250, 300, 'المادة الخضراء في الأوراق', '#fff', '#2b8a3e', 18) + '<line x1="590" y1="250" x2="510" y2="175" stroke="#2b8a3e" stroke-width="3" marker-end="url(#b6)"/>'
    s += _pill(450, 22, 360, 'ينتج النبات غذاءه بنفسه', '#d3f9d8', '#2b8a3e', 19)
    return _wrap(W, H, s, _arrow_def(2, '#f08c00') + _arrow_def(3, '#495057') + _arrow_def(4, '#1c7ed6') + _arrow_def(6, '#2b8a3e'))

# ---------------------------------------------------------------- dunes
def dunes():
    W, H = 900, 300
    s = f'<rect width="{W}" height="{H}" rx="18" fill="#cfeaff"/>'
    s += _t(780, 70, '☀️', 56)
    s += '<path d="M0 300 V210 Q120 120 250 200 Q360 120 520 210 Q660 110 900 220 V300Z" fill="#e8c66b"/><path d="M0 300 V250 Q160 190 320 250 Q500 190 680 255 Q800 220 900 250 V300Z" fill="#d6ab4c"/>'
    s += '<line x1="60" y1="90" x2="250" y2="90" stroke="#5c7080" stroke-width="5" marker-end="url(#b7)"/><line x1="100" y1="125" x2="300" y2="125" stroke="#5c7080" stroke-width="5" marker-end="url(#b7)"/>'
    s += _pill(160, 60, 200, 'الرياح تنقل الرمال', '#fff', '#5c7080', 18)
    s += _pill(450, 276, 300, 'الكثبان الرملية', '#fff', '#a7791e', 20)
    return _wrap(W, H, s, _arrow_def(7, '#5c7080'))

# ---------------------------------------------------------------- cover
def cover():
    W, H = 900, 560
    s = ('<defs><linearGradient id="cs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fb4f5"/><stop offset="1" stop-color="#d7f0ff"/></linearGradient></defs>'
         f'<rect width="{W}" height="{H}" rx="26" fill="url(#cs)"/>')
    s += '<circle cx="770" cy="110" r="64" fill="#ffd43b"/><circle cx="770" cy="110" r="86" fill="#ffd43b" opacity=".25"/>'
    s += '<ellipse cx="220" cy="100" rx="90" ry="30" fill="#fff" opacity=".9"/><ellipse cx="300" cy="120" rx="70" ry="26" fill="#fff" opacity=".9"/>'
    s += '<path d="M0 430 Q200 320 420 400 T900 380 V560 H0Z" fill="#7cc361"/><path d="M0 500 Q250 430 520 480 T900 470 V560 H0Z" fill="#5aa845"/>'
    s += '<ellipse cx="640" cy="470" rx="150" ry="36" fill="#4aa3ec"/>'
    for e, x, y, fs in [('🌳', 120, 420, 120), ('🌴', 250, 400, 100), ('🐄', 430, 450, 90), ('🐑', 520, 460, 70), ('🪨', 800, 500, 70), ('🌾', 330, 500, 70), ('🐦', 480, 200, 56), ('🦋', 200, 250, 52), ('🐟', 650, 480, 44), ('💧', 600, 330, 52)]:
        s += _t(x, y, e, fs)
    return _wrap(W, H, s)
