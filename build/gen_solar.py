#!/usr/bin/env python3
"""Generates solar_system.html (text + inline SVG infographics)."""
import math, random

random.seed(11)

def shade(h, f):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    if f >= 0: r, g, b = [int(c + (255 - c) * f) for c in (r, g, b)]
    else: r, g, b = [int(c * (1 + f)) for c in (r, g, b)]
    return '#%02x%02x%02x' % (r, g, b)

COL = dict(mercury='#9c9a97', venus='#e6b86a', earth='#3a7fc8', mars='#c4522f',
           jupiter='#d6a06b', saturn='#e4cf8e', uranus='#8ad3da', neptune='#3d5fd1', sun='#f9a61a')
NAMES = dict(mercury='عطارد', venus='الزهرة', earth='الأرض', mars='المريخ',
             jupiter='المشتري', saturn='زحل', uranus='أورانوس', neptune='نبتون')
ORDER = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

def defs(sfx):
    out = '<defs>'
    for k, c in COL.items():
        out += (f'<radialGradient id="g_{k}_{sfx}" cx="0.68" cy="0.38" r="0.85">'
                f'<stop offset="0" stop-color="{shade(c,0.45)}"/><stop offset="0.55" stop-color="{c}"/>'
                f'<stop offset="1" stop-color="{shade(c,-0.55)}"/></radialGradient>')
    out += '</defs>'
    return out

def stars(w, h, n, rmax=1.4):
    s = ''
    for _ in range(n):
        s += f'<circle cx="{random.uniform(0,w):.0f}" cy="{random.uniform(0,h):.0f}" r="{random.uniform(.4,rmax):.1f}" fill="#fff" opacity="{random.uniform(.3,.9):.2f}"/>'
    return s

def planet(k, cx, cy, r, sfx):
    out = ''
    if k == 'saturn':
        out += (f'<g transform="rotate(-18 {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{r*2.0:.1f}" ry="{r*.55:.1f}" '
                f'fill="none" stroke="#cdb77a" stroke-width="{r*.32:.1f}" opacity=".9"/></g>')
    out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g_{k}_{sfx})"/>'
    cid = f'cp_{k}_{sfx}_{int(cx)}_{int(cy)}'
    if k == 'jupiter':
        out += f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><g clip-path="url(#{cid})" opacity=".55">'
        for dy, hh, c in [(-.55, .16, '#9b6a3f'), (-.15, .2, '#c98c55'), (.3, .16, '#9b6a3f'), (.62, .12, '#b87d4b')]:
            out += f'<rect x="{cx-r}" y="{cy+dy*r-hh*r/2:.1f}" width="{2*r}" height="{hh*r:.1f}" fill="{c}"/>'
        out += f'</g><ellipse cx="{cx+r*.28:.1f}" cy="{cy+r*.3:.1f}" rx="{r*.17:.1f}" ry="{r*.1:.1f}" fill="#b5442b"/>'
    if k == 'earth':
        out += (f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><g clip-path="url(#{cid})" fill="#4aa05a" opacity=".9">'
                f'<ellipse cx="{cx-r*.3:.1f}" cy="{cy-r*.2:.1f}" rx="{r*.35:.1f}" ry="{r*.28:.1f}"/>'
                f'<ellipse cx="{cx+r*.35:.1f}" cy="{cy+r*.3:.1f}" rx="{r*.28:.1f}" ry="{r*.34:.1f}"/></g>')
    if k == 'saturn':
        out += (f'<clipPath id="{cid}"><rect x="{cx-r*3}" y="{cy}" width="{r*6}" height="{r*3}"/></clipPath>'
                f'<g transform="rotate(-18 {cx} {cy})"><g clip-path="url(#{cid})"><ellipse cx="{cx}" cy="{cy}" rx="{r*2.0:.1f}" ry="{r*.55:.1f}" '
                f'fill="none" stroke="#cdb77a" stroke-width="{r*.32:.1f}"/></g></g>')
    return out

def sun_disc(cx, cy, r, sfx):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r*1.25:.0f}" fill="#ffb300" opacity=".16"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*1.1:.0f}" fill="#ffb300" opacity=".25"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g_sun_{sfx})"/>')

# ------------------------------------------------------------- SVG 1: overview
def svg_overview():
    W, H = 900, 430
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("ov")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 130)
    s += sun_disc(880, 190, 150, 'ov')
    s += '<text x="770" y="60" fill="#ffd36b" font-size="26" font-weight="700" text-anchor="middle">الشمس</text>'
    xs = dict(mercury=668, venus=622, earth=572, mars=525, jupiter=432, saturn=290, uranus=170, neptune=82)
    rs = dict(mercury=6, venus=11, earth=12, mars=8, jupiter=50, saturn=38, uranus=24, neptune=23)
    s += '<line x1="40" y1="190" x2="700" y2="190" stroke="#fff" stroke-opacity=".18" stroke-dasharray="4 6"/>'
    for i, k in enumerate(ORDER):
        x, r = xs[k], rs[k]
        s += planet(k, x, 190, r, 'ov')
        s += f'<circle cx="{x}" cy="95" r="14" fill="#ffd36b"/><text x="{x}" y="101" font-size="17" font-weight="700" fill="#0b1030" text-anchor="middle">{i+1}</text>'
        s += f'<line x1="{x}" y1="109" x2="{x}" y2="{190-r-6}" stroke="#ffd36b" stroke-opacity=".35"/>'
        s += f'<text x="{x}" y="{290 if k in ("jupiter","saturn") else 270}" font-size="21" font-weight="700" fill="#fff" text-anchor="middle">{NAMES[k]}</text>'
    # grouping brackets
    s += '<path d="M700 330 H510 M700 322 V338 M510 322 V338" stroke="#7fd1ff" stroke-width="2" fill="none"/>'
    s += '<text x="605" y="362" font-size="19" fill="#7fd1ff" text-anchor="middle" font-weight="700">كواكب صخرية (داخلية)</text>'
    s += '<path d="M495 330 H210 M495 322 V338 M210 322 V338" stroke="#ffcf8a" stroke-width="2" fill="none"/>'
    s += '<text x="352" y="362" font-size="19" fill="#ffcf8a" text-anchor="middle" font-weight="700">عملاقان غازيان</text>'
    s += '<path d="M195 330 H55 M195 322 V338 M55 322 V338" stroke="#a6e8ee" stroke-width="2" fill="none"/>'
    s += '<text x="125" y="362" font-size="19" fill="#a6e8ee" text-anchor="middle" font-weight="700">عملاقان جليديان</text>'
    s += '<text x="450" y="412" font-size="15" fill="#9aa4d6" text-anchor="middle">الأحجام مقرّبة للتوضيح، والمسافات بين الكواكب في الحقيقة أكبر بكثير جدًّا</text>'
    return s + '</svg>'

# ------------------------------------------------------------- SVG 2: orbits
def svg_orbits():
    W = H = 700; cx = cy = 350
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("or")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 110)
    orb = dict(mercury=48, venus=78, earth=108, mars=138, jupiter=232, saturn=272, uranus=307, neptune=334)
    ang = dict(mercury=200, venus=300, earth=40, mars=130, jupiter=330, saturn=210, uranus=95, neptune=265)
    rp = dict(mercury=4, venus=7, earth=8, mars=5.5, jupiter=18, saturn=14, uranus=10, neptune=10)
    for k in ORDER:
        s += f'<circle cx="{cx}" cy="{cy}" r="{orb[k]}" fill="none" stroke="#fff" stroke-opacity=".28" stroke-dasharray="3 5"/>'
    # asteroid belt
    for _ in range(230):
        a = random.uniform(0, 2*math.pi); r = random.uniform(172, 200)
        s += f'<circle cx="{cx+r*math.cos(a):.1f}" cy="{cy+r*math.sin(a):.1f}" r="{random.uniform(.6,1.6):.1f}" fill="#b9a68f" opacity=".85"/>'
    s += sun_disc(cx, cy, 22, 'or')
    for k in ORDER:
        a = math.radians(ang[k]); x = cx + orb[k]*math.cos(a); y = cy + orb[k]*math.sin(a)
        s += planet(k, round(x, 1), round(y, 1), rp[k], 'or')
        dx = 14 + rp[k]*(2.2 if k == 'saturn' else 1) ; ox = x + (dx if math.cos(a) >= 0 else -dx)
        anchor = 'start' if math.cos(a) >= 0 else 'end'
        s += f'<text x="{ox:.0f}" y="{y+5:.0f}" font-size="17" fill="#fff" font-weight="700" text-anchor="{anchor}">{NAMES[k]}</text>'
    s += f'<text x="{cx}" y="{cy-205}" font-size="16" fill="#e2c9a6" text-anchor="middle">حزام الكويكبات</text>'
    s += f'<line x1="{cx}" y1="{cy-200}" x2="{cx}" y2="{cy-190}" stroke="#e2c9a6"/>'
    s += f'<text x="{cx+30}" y="{cy+8}" font-size="17" fill="#ffd36b" font-weight="700">الشمس</text>'
    s += '<text x="350" y="684" font-size="14" fill="#9aa4d6" text-anchor="middle">منظر من الأعلى — المدارات مقرّبة وغير مرسومة بمقياس حقيقي</text>'
    return s + '</svg>'

# ------------------------------------------------------------- SVG 3: sizes
def svg_sizes():
    W, H = 900, 330
    d = dict(mercury=4879, venus=12104, earth=12742, mars=6779, jupiter=139820, saturn=116460, uranus=50724, neptune=49244)
    k_ = 0.00052  # px per km (radius)
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("sz")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#f4f6fb" stroke="#cfd6ea"/>'
    # layout right->left
    xs = dict(mercury=856, venus=806, earth=756, mars=706, jupiter=600, saturn=385, uranus=215, neptune=105)
    base = 200
    for k in ORDER:
        r = d[k]/2*k_*1.0
        r = max(r*1.0, 3)
        r_ = d[k]/2*0.0011
        s += planet(k, xs[k], base, round(r_, 1), 'sz')
        s += f'<text x="{xs[k]}" y="{base+r_+(26 if k not in ("jupiter","saturn") else 24)}" font-size="19" font-weight="700" fill="#1d2a52" text-anchor="middle">{NAMES[k]}</text>'
        s += f'<text x="{xs[k]}" y="{base+r_+(47 if k not in ("jupiter","saturn") else 45)}" font-size="13" fill="#555" text-anchor="middle">{d[k]:,}</text>'
    s += '<text x="450" y="38" font-size="20" font-weight="700" fill="#0b5d3b" text-anchor="middle">مقارنة أحجام الكواكب (الأقطار بالكيلومتر، ومرسومة بنسبتها الحقيقية)</text>'
    s += '<text x="450" y="64" font-size="15" fill="#555" text-anchor="middle">المشتري يتّسع لأكثر من 1300 كرة بحجم الأرض! أما الشمس فقطرها يساوي 109 أمثال قطر الأرض.</text>'
    s += '<text x="450" y="312" font-size="14" fill="#777" text-anchor="middle">رسم تقريبي — سيارتك الصغيرة بحجم الأرض لن تقارن بحجم المشتري</text>'
    return s + '</svg>'

# ------------------------------------------------------------- SVG 4: cosmic address
def svg_address():
    W, H = 900, 470
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 120)
    cx, cy = 640, 235
    rings = [(215, '#2b3a8c', 'الكون'), (170, '#3b4cb0', 'العنقود المحلي للمجرات'), (125, '#5a6ad0', 'مجرة درب التبانة'),
             (78, '#f0a830', 'النظام الشمسي'), (32, '#3a7fc8', 'الأرض')]
    for r, c, _ in rings:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" fill-opacity=".55" stroke="#fff" stroke-opacity=".5"/>'
    ys = [60, 130, 200, 270, 340]
    for (r, c, t), y in zip(rings, ys):
        px, py = cx - r + (14 if r > 40 else 6), cy - (0 if r < 40 else 0)
        # leader to the ring's top-left edge
        ex = cx - r*0.6; ey = cy - r*0.8 if r > 40 else cy - r
        s += f'<line x1="380" y1="{y}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="#ffd36b" stroke-opacity=".7"/>'
        s += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="4" fill="#ffd36b"/>'
        s += f'<text x="372" y="{y+6}" font-size="22" font-weight="700" fill="#fff" text-anchor="end">{t}</text>'
    s += '<text x="450" y="440" font-size="18" fill="#ffd36b" text-anchor="middle" font-weight="700">عنوانك الكامل في الكون: الأرض ← النظام الشمسي ← درب التبانة ← العنقود المحلي ← الكون</text>'
    return s + '</svg>'

# ------------------------------------------------------------- SVG 5: Milky Way
def svg_milkyway():
    W, H = 900, 560
    cx, cy = 450, 285
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += ('<defs><radialGradient id="bulge"><stop offset="0" stop-color="#fff6c8"/><stop offset=".5" stop-color="#f3b94a" stop-opacity=".8"/>'
          '<stop offset="1" stop-color="#f3b94a" stop-opacity="0"/></radialGradient></defs>')
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#070a22"/>' + stars(W, H, 160)
    for arm in range(4):
        for i in range(260):
            t = i / 260
            r = 30 + t * 215
            th = arm * math.pi/2 + t * 3.7
            for _ in range(3):
                jr = random.gauss(0, 7 + 10*t)
                jt = random.gauss(0, .05)
                x = cx + (r + jr) * math.cos(th + jt) * 1.5
                y = cy + (r + jr) * math.sin(th + jt) * .93
                col = '#9fc0ff' if random.random() < .6 else '#ffe9b0'
                s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(.6,1.7):.1f}" fill="{col}" opacity="{random.uniform(.35,.95):.2f}"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="95" ry="52" fill="url(#bulge)"/>'
    # sun marker
    t = 0.60; r = 30 + t*215; th = 1*math.pi/2 + t*3.7
    sx = cx + r*math.cos(th)*1.5; sy = cy + r*math.sin(th)*.93
    s += f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="9" fill="#ffb300" stroke="#fff" stroke-width="2"/>'
    lx, ly = sx - 150, sy + 55
    s += f'<line x1="{sx-8:.0f}" y1="{sy+7:.0f}" x2="{lx+20:.0f}" y2="{ly-18:.0f}" stroke="#ffd36b" stroke-width="2"/>'
    s += f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="22" fill="#ffd36b" font-weight="700" text-anchor="middle">نحن هنا (النظام الشمسي)</text>'
    s += f'<text x="{cx}" y="{cy+6}" font-size="17" fill="#3a2a00" font-weight="700" text-anchor="middle">مركز المجرة</text>'
    s += f'<line x1="130" y1="528" x2="770" y2="528" stroke="#7fd1ff" stroke-width="2"/><path d="M130 520 V536 M770 520 V536" stroke="#7fd1ff" stroke-width="2"/>'
    s += '<text x="450" y="520" font-size="17" fill="#7fd1ff" text-anchor="middle" font-weight="700">قطر المجرة نحو 100,000 سنة ضوئية</text>'
    s += '<text x="450" y="38" font-size="24" fill="#fff" text-anchor="middle" font-weight="700">مجرة درب التبانة (منظر تخيّلي من الأعلى)</text>'
    return s + '</svg>'

# ------------------------------------------------------------- SVG 6: sun anatomy
def svg_sun():
    W, H = 900, 420
    cx, cy = 650, 210
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("sn")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 90)
    s += f'<circle cx="{cx}" cy="{cy}" r="190" fill="#ffb300" opacity=".12"/><circle cx="{cx}" cy="{cy}" r="165" fill="#ffb300" opacity=".2"/>'
    for r, c in [(140, '#ff8f1f'), (112, '#ffb02e'), (80, '#ffd04a'), (38, '#fff3b0')]:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>'
    lay = [(70, 'الإكليل (الغلاف الخارجي)', 'طبقة حارقة رقيقة تظهر عند كسوف الشمس', cx-178, cy-70),
           (135, 'سطح الشمس (الفوتوسفير)', 'حرارته نحو 5500 درجة مئوية — منه يصلنا الضوء', cx-125, cy-62),
           (200, 'منطقة الحمل', 'الغاز الساخن يصعد ويهبط مثل الماء الذي يغلي', cx-96, cy-30),
           (265, 'منطقة الإشعاع', 'الطاقة تنتقل فيها ببطء شديد', cx-60, cy+8),
           (330, 'النواة (قلب الشمس)', 'حرارتها نحو 15 مليون درجة؛ فيها يتحول الهيدروجين إلى هيليوم فتنتج الطاقة', cx-12, cy+16)]
    for y, t, d, px, py in lay:
        s += f'<line x1="400" y1="{y-6}" x2="{px}" y2="{py}" stroke="#ffd36b" stroke-opacity=".8"/><circle cx="{px}" cy="{py}" r="4" fill="#fff"/>'
        s += f'<text x="392" y="{y}" font-size="19" font-weight="700" fill="#ffd36b" text-anchor="end">{t}</text>'
        s += f'<text x="392" y="{y+22}" font-size="14" fill="#dfe4ff" text-anchor="end">{d}</text>'
    return s + '</svg>'

# ------------------------------------------------------------- SVG 7: Earth day/night + seasons
def svg_earth():
    W, H = 900, 330
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("ea")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 80)
    # panel A (right half): rotation
    ax, ay, r = 650, 175, 78
    s += sun_disc(880, 175, 48, 'ea')
    for dy in (-50, 0, 50):
        s += f'<line x1="835" y1="{ay+dy}" x2="{ax+r+14}" y2="{ay+dy}" stroke="#ffd36b" stroke-width="2.5" stroke-dasharray="7 5"/>'
    s += planet('earth', ax, ay, r, 'ea')
    s += (f'<clipPath id="nightc"><circle cx="{ax}" cy="{ay}" r="{r}"/></clipPath>'
          f'<rect x="{ax-r}" y="{ay-r}" width="{r}" height="{2*r}" fill="#000" opacity=".6" clip-path="url(#nightc)"/>')
    tx, ty = math.sin(math.radians(23.5))*(r+30), math.cos(math.radians(23.5))*(r+30)
    s += f'<line x1="{ax+tx:.0f}" y1="{ay-ty:.0f}" x2="{ax-tx:.0f}" y2="{ay+ty:.0f}" stroke="#fff" stroke-width="2" stroke-dasharray="3 4"/>'
    s += f'<text x="{ax+tx+8:.0f}" y="{ay-ty+4:.0f}" font-size="13" fill="#fff">محور الأرض</text>'
    s += f'<text x="{ax+r*.5:.0f}" y="{ay+8}" font-size="23" font-weight="700" fill="#fff" text-anchor="middle">نهار</text>'
    s += f'<text x="{ax-r*.5:.0f}" y="{ay+8}" font-size="23" font-weight="700" fill="#cfd8ff" text-anchor="middle">ليل</text>'
    s += '<text x="700" y="285" font-size="19" fill="#ffd36b" text-anchor="middle" font-weight="700">دوران الأرض حول نفسها = ليل ونهار (24 ساعة)</text>'
    s += '<text x="700" y="35" font-size="20" fill="#fff" text-anchor="middle" font-weight="700">أولًا: الدوران حول المحور</text>'
    # panel B (left half): revolution
    ox, oy, rx, ry = 230, 175, 170, 82
    s += f'<ellipse cx="{ox}" cy="{oy}" rx="{rx}" ry="{ry}" fill="none" stroke="#fff" stroke-opacity=".4" stroke-dasharray="4 6" stroke-width="2"/>'
    s += sun_disc(ox, oy, 24, 'ea')
    pos = [(ox - rx, oy, 'يونيو', 'صيف في الشمال'), (ox + rx, oy, 'ديسمبر', 'شتاء في الشمال'),
           (ox, oy - ry, 'مارس', 'ربيع في الشمال'), (ox, oy + ry, 'سبتمبر', 'خريف في الشمال')]
    for x, y, m, ss in pos:
        s += planet('earth', x, y, 15, 'ea')
        s += f'<line x1="{x+11:.0f}" y1="{y-26:.0f}" x2="{x-11:.0f}" y2="{y+26:.0f}" stroke="#fff" stroke-width="1.6"/>'
    s += f'<text x="{ox-rx+8}" y="{oy+50}" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">يونيو</text><text x="{ox-rx+8}" y="{oy+68}" font-size="12.5" fill="#cfd8ff" text-anchor="middle">صيف في الشمال</text>'
    s += f'<text x="{ox+rx-8}" y="{oy+50}" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">ديسمبر</text><text x="{ox+rx-8}" y="{oy+68}" font-size="12.5" fill="#cfd8ff" text-anchor="middle">شتاء في الشمال</text>'
    s += f'<text x="{ox}" y="{oy-ry-28}" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">مارس <tspan font-size="12.5" fill="#cfd8ff" font-weight="400">(ربيع في الشمال)</tspan></text>'
    s += f'<text x="{ox}" y="{oy+ry+42}" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">سبتمبر <tspan font-size="12.5" fill="#cfd8ff" font-weight="400">(خريف في الشمال)</tspan></text>'
    s += '<text x="230" y="35" font-size="20" fill="#fff" text-anchor="middle" font-weight="700">ثانيًا: الدوران حول الشمس</text>'
    s += '<text x="230" y="312" font-size="19" fill="#ffd36b" text-anchor="middle" font-weight="700">دورة كاملة = سنة (365 يومًا وربع)</text>'
    return s + '</svg>'

# ------------------------------------------------------------- SVG 8: year length bars
def svg_year():
    W, H = 900, 400
    data = [('mercury', 0.241, '88 يومًا'), ('venus', 0.615, '225 يومًا'), ('earth', 1.0, '365 يومًا (سنة)'),
            ('mars', 1.881, '687 يومًا'), ('jupiter', 11.86, '12 سنة تقريبًا'), ('saturn', 29.46, '29.5 سنة'),
            ('uranus', 84.0, '84 سنة'), ('neptune', 164.8, '165 سنة')]
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("yr")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#f4f6fb" stroke="#cfd6ea"/>'
    s += '<text x="450" y="34" font-size="21" font-weight="700" fill="#0b5d3b" text-anchor="middle">كم تستغرق «سنة» كل كوكب؟ (زمن دورته حول الشمس)</text>'
    for i, (k, y, lab) in enumerate(data):
        yy = 66 + i*38
        w = max(math.sqrt(y) * 46, 8)
        s += planet(k, 860, yy+10, 12 if k not in ('saturn',) else 9, 'yr')
        s += f'<text x="832" y="{yy+16}" font-size="19" font-weight="700" fill="#1d2a52" text-anchor="end">{NAMES[k]}</text>'
        s += f'<rect x="{745-w:.0f}" y="{yy}" width="{w:.0f}" height="22" rx="6" fill="{shade(COL[k], -0.1)}"/>'
        s += f'<text x="{745-w-8:.0f}" y="{yy+17}" font-size="16" fill="#333" text-anchor="end">{lab}</text>'
    s += '<text x="450" y="384" font-size="13.5" fill="#777" text-anchor="middle">كلما ابتعد الكوكب عن الشمس صارت دورته أطول وأبطأ (الأطوال مرسومة بمقياس تقريبي)</text>'
    return s + '</svg>'

# ------------------------------------------------------------- SVG 9: asteroid/comet/moon mini row
def svg_small():
    W, H = 900, 300
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("sm")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 90)
    # moon
    s += f'<circle cx="780" cy="120" r="48" fill="#cfcfd6"/><circle cx="765" cy="105" r="9" fill="#a8a8b2"/><circle cx="795" cy="135" r="12" fill="#a8a8b2"/><circle cx="800" cy="100" r="6" fill="#b8b8c2"/>'
    s += '<text x="780" y="205" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">القمر</text><text x="780" y="230" font-size="16" fill="#cfd8ff" text-anchor="middle">يدور حول كوكب</text><text x="780" y="250" font-size="16" fill="#cfd8ff" text-anchor="middle">(قمر الأرض واحد)</text>'
    # asteroids
    for x, y, rx, ry, rot in [(560, 90, 26, 18, 20), (620, 150, 18, 12, -30), (520, 140, 14, 10, 40), (600, 80, 10, 8, 0), (565, 175, 12, 9, 10)]:
        s += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#9b8a77" transform="rotate({rot} {x} {y})"/>'
    s += '<text x="575" y="205" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">الكويكبات</text><text x="575" y="230" font-size="16" fill="#cfd8ff" text-anchor="middle">صخور صغيرة بين</text><text x="575" y="250" font-size="16" fill="#cfd8ff" text-anchor="middle">المريخ والمشتري</text>'
    # comet
    s += '<defs><linearGradient id="tail" x1="1" x2="0"><stop offset="0" stop-color="#bfe9ff" stop-opacity=".9"/><stop offset="1" stop-color="#bfe9ff" stop-opacity="0"/></linearGradient></defs>'
    s += '<path d="M380 110 L170 70 L170 150 Z" fill="url(#tail)"/><circle cx="385" cy="110" r="17" fill="#e8f6ff"/>'
    s += '<text x="300" y="205" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">المذنّب</text><text x="300" y="230" font-size="16" fill="#cfd8ff" text-anchor="middle">جليد وغبار، له ذيل</text><text x="300" y="250" font-size="16" fill="#cfd8ff" text-anchor="middle">يتجه بعيدًا عن الشمس</text>'
    # dwarf planet
    s += f'<circle cx="95" cy="120" r="22" fill="url(#g_mercury_sm)"/>'
    s += '<text x="95" y="205" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">كوكب قزم</text><text x="95" y="230" font-size="16" fill="#cfd8ff" text-anchor="middle">مثل بلوتو، أصغر من</text><text x="95" y="250" font-size="16" fill="#cfd8ff" text-anchor="middle">الكواكب الثمانية</text>'
    return s + '</svg>'

# ------------------------------------------------------------- planet cards
CARDS = [
 ('mercury', 'أصغر الكواكب وأقربها إلى الشمس.', 'لا غلاف جوي له تقريبًا، فنهاره شديد الحرارة (حتى 430°م) وليله شديد البرودة (حتى -170°م).', 'سنته 88 يومًا فقط.'),
 ('venus', 'أسخن الكواكب (نحو 465°م).', 'غلافه كثيف من ثاني أكسيد الكربون يحبس الحرارة كالبطانية، فهو أسخن من عطارد رغم أنه أبعد.', 'يُسمّى «نجمة الصباح» لشدة لمعانه، ويدور حول نفسه ببطء شديد وفي اتجاه معاكس لمعظم الكواكب.'),
 ('earth', 'كوكبنا، والوحيد المعروف بوجود الحياة عليه.', 'نحو 71% من سطحه ماء، وغلافه الجوي (نيتروجين وأكسجين) يحمينا ويمنحنا الهواء. له قمر واحد.', 'بُعده عن الشمس مناسب تمامًا: لا حارّ يحرق ولا بارد يجمّد.'),
 ('mars', 'الكوكب الأحمر بسبب صدأ الحديد في تربته.', 'غلافه الجوي رقيق وبارد جدًّا (متوسط -65°م). له قمران صغيران: فوبوس وديموس.', 'فيه أعلى بركان معروف في المجموعة الشمسية: «أوليمبوس» (نحو 22 كم ارتفاعًا).'),
 ('jupiter', 'أكبر الكواكب بلا منازع.', 'كوكب غازي (هيدروجين وهيليوم) بلا سطح صلب. يتسع لأكثر من 1300 أرض. له عشرات الأقمار (أكثر من 90).', '«البقعة الحمراء العظمى» عاصفة هائلة مستمرة منذ مئات السنين.'),
 ('saturn', 'سيّد الحلقات الجميلة.', 'غازي أيضًا، وحلقاته مكوّنة من قطع جليد وصخور لا تُحصى. له أكثر من 270 قمرًا.', 'كثافته أقل من الماء! لو وُجد حوض ماء ضخم بما يكفي لطفا فوقه.'),
 ('uranus', 'عملاق جليدي أزرق مخضر.', 'لونه من غاز الميثان في غلافه. حرارته نحو -195°م. له حلقات خافتة و28 قمرًا معروفًا.', 'يدور «مستلقيًا على جنبه» تقريبًا، كأنه كرة تتدحرج في مداره.'),
 ('neptune', 'أبعد الكواكب عن الشمس.', 'عملاق جليدي أزرق داكن، رياحه من أسرع الرياح في المجموعة (أكثر من 2000 كم/ساعة).', 'اكتُشف بالحساب الرياضي قبل رؤيته (1846)، وسنته 165 سنة أرضية.'),
]

def card_icon(k):
    r = {'mercury': 9, 'venus': 15, 'earth': 16, 'mars': 11, 'jupiter': 27, 'saturn': 21, 'uranus': 20, 'neptune': 20}[k]
    return (f'<svg viewBox="0 0 90 70" width="90" height="70" xmlns="http://www.w3.org/2000/svg">{defs("c"+k)}'
            f'{planet(k, 45, 35, r, "c"+k)}</svg>')

def cards_html():
    out = '<div class="cards">'
    for i, (k, t, d, f) in enumerate(CARDS):
        out += (f'<div class="card"><div class="ic">{card_icon(k)}<div class="num">{i+1}</div></div>'
                f'<div class="ct"><h4>{NAMES[k]}</h4><p><b>{t}</b> {d}</p><p class="fun">💡 {f}</p></div></div>')
    return out + '</div>'

# ------------------------------------------------------------- stat cards
def stats_html():
    items = [('8', 'كواكب تدور حول الشمس'), ('99.86%', 'من كتلة المجموعة الشمسية في الشمس وحدها'),
             ('109 ×', 'قطر الشمس مقارنة بقطر الأرض'), ('8 د 20 ث', 'زمن وصول ضوء الشمس إلى الأرض'),
             ('4.6 مليار', 'سنة: عمر الشمس التقريبي'), ('150 مليون كم', 'المسافة بين الأرض والشمس')]
    out = '<div class="stats">'
    for n, t in items:
        out += f'<div class="stat"><div class="n">{n}</div><div class="t">{t}</div></div>'
    return out + '</div>'

# ------------------------------------------------------------- facts table
def table_html():
    rows = [
     ('mercury', '58', '3 د', '88 يومًا', '59 يومًا', '0', '−170 إلى 430'),
     ('venus', '108', '6 د', '225 يومًا', '243 يومًا', '0', '465'),
     ('earth', '150', '8 د 20 ث', '365 يومًا', '24 ساعة', '1', '15 (متوسط)'),
     ('mars', '228', '12.7 د', '687 يومًا', '24.6 ساعة', '2', '−65 (متوسط)'),
     ('jupiter', '778', '43 د', '11.9 سنة', '10 ساعات', '90+', '−110 (قمة السحب)'),
     ('saturn', '1434', '1 س 20 د', '29.5 سنة', '10.7 ساعة', '270+', '−140 (قمة السحب)'),
     ('uranus', '2871', '2 س 40 د', '84 سنة', '17 ساعة', '28', '−195'),
     ('neptune', '4495', '4 س 10 د', '165 سنة', '16 ساعة', '16', '−200')]
    t = ('<table class="ptable"><tr><th>الكوكب</th><th>البعد عن الشمس<br>(مليون كم)</th><th>وصول الضوء<br>إليه</th>'
         '<th>طول السنة</th><th>طول اليوم<br>(دورة حول نفسه)</th><th>عدد<br>الأقمار</th><th>الحرارة (°م)</th></tr>')
    for k, *rest in rows:
        t += f'<tr><td><b>{NAMES[k]}</b></td>' + ''.join(f'<td>{x}</td>' for x in rest) + '</tr>'
    return t + '</table>'


# ======================= overrides (v2) =======================
def svg_overview():
    W, H = 900, 440
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("ov")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 130)
    s += sun_disc(880, 190, 150, 'ov')
    s += '<text x="772" y="58" fill="#ffd36b" font-size="28" font-weight="700" text-anchor="middle">الشمس</text>'
    xs = dict(mercury=668, venus=622, earth=572, mars=525, jupiter=432, saturn=290, uranus=170, neptune=82)
    rs = dict(mercury=6, venus=11, earth=12, mars=8, jupiter=50, saturn=38, uranus=24, neptune=23)
    s += '<line x1="40" y1="190" x2="700" y2="190" stroke="#fff" stroke-opacity=".18" stroke-dasharray="4 6"/>'
    ly = dict(mercury=256, venus=292, earth=256, mars=292, jupiter=275, saturn=275, uranus=275, neptune=275)
    for i, k in enumerate(ORDER):
        x, r = xs[k], rs[k]
        s += planet(k, x, 190, r, 'ov')
        s += f'<circle cx="{x}" cy="95" r="14" fill="#ffd36b"/><text x="{x}" y="101" font-size="17" font-weight="700" fill="#0b1030" text-anchor="middle">{i+1}</text>'
        s += f'<line x1="{x}" y1="109" x2="{x}" y2="{190-r-6}" stroke="#ffd36b" stroke-opacity=".35"/>'
        if k in ('mercury', 'venus', 'earth', 'mars'):
            s += f'<line x1="{x}" y1="{190+r+6}" x2="{x}" y2="{ly[k]-20}" stroke="#fff" stroke-opacity=".3"/>'
        s += f'<text x="{x}" y="{ly[k]}" font-size="21" font-weight="700" fill="#fff" text-anchor="middle">{NAMES[k]}</text>'
    for x1, x2, c, t in [(700, 510, '#7fd1ff', 'كواكب صخرية (داخلية)'), (495, 210, '#ffcf8a', 'عملاقان غازيان'), (195, 55, '#a6e8ee', 'عملاقان جليديان')]:
        s += f'<path d="M{x1} 345 H{x2} M{x1} 337 V353 M{x2} 337 V353" stroke="{c}" stroke-width="2" fill="none"/>'
        s += f'<text x="{(x1+x2)/2}" y="383" font-size="20" fill="{c}" text-anchor="middle" font-weight="700">{t}</text>'
    s += '<text x="450" y="425" font-size="15" fill="#9aa4d6" text-anchor="middle">الأحجام مقرّبة للتوضيح، والمسافات بين الكواكب في الحقيقة أكبر بكثير جدًّا</text>'
    return s + '</svg>'

def svg_orbits():
    W = H = 700; cx = cy = 350
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("or")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 110)
    orb = dict(mercury=44, venus=70, earth=96, mars=122, jupiter=205, saturn=240, uranus=270, neptune=297)
    ang = dict(mercury=200, venus=300, earth=40, mars=130, jupiter=335, saturn=205, uranus=100, neptune=262)
    rp = dict(mercury=4, venus=7, earth=8, mars=5.5, jupiter=17, saturn=13, uranus=10, neptune=10)
    for k in ORDER:
        s += f'<circle cx="{cx}" cy="{cy}" r="{orb[k]}" fill="none" stroke="#fff" stroke-opacity=".28" stroke-dasharray="3 5"/>'
    for _ in range(230):
        a = random.uniform(0, 2*math.pi); r = random.uniform(148, 176)
        s += f'<circle cx="{cx+r*math.cos(a):.1f}" cy="{cy+r*math.sin(a):.1f}" r="{random.uniform(.6,1.6):.1f}" fill="#b9a68f" opacity=".85"/>'
    s += sun_disc(cx, cy, 20, 'or')
    for k in ORDER:
        a = math.radians(ang[k]); x = cx + orb[k]*math.cos(a); y = cy + orb[k]*math.sin(a)
        s += planet(k, round(x, 1), round(y, 1), rp[k], 'or')
        dx = 14 + rp[k]*(2.2 if k == 'saturn' else 1); right = math.cos(a) >= 0
        ox = x + (dx if right else -dx)
        s += f'<text x="{ox:.0f}" y="{y+6:.0f}" font-size="19" fill="#fff" font-weight="700" text-anchor="{"start" if right else "end"}">{NAMES[k]}</text>'
    s += f'<text x="{cx+118}" y="{cy-122}" font-size="16" fill="#e2c9a6" text-anchor="start">حزام الكويكبات</text>'
    s += f'<line x1="{cx+90}" y1="{cy-112}" x2="{cx+116}" y2="{cy-118}" stroke="#e2c9a6"/>'
    s += f'<text x="{cx}" y="{cy+44}" font-size="18" fill="#ffd36b" font-weight="700" text-anchor="middle">الشمس</text>'
    s += '<text x="350" y="688" font-size="14" fill="#9aa4d6" text-anchor="middle">منظر من الأعلى — المدارات مقرّبة وغير مرسومة بمقياس حقيقي</text>'
    return s + '</svg>'

def svg_sizes():
    W, H = 900, 340
    d = dict(mercury=4879, venus=12104, earth=12742, mars=6779, jupiter=139820, saturn=116460, uranus=50724, neptune=49244)
    sc = 0.0009
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("sz")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#f4f6fb" stroke="#cfd6ea"/>'
    xs = dict(mercury=858, venus=806, earth=754, mars=702, jupiter=600, saturn=400, uranus=245, neptune=130)
    ys = dict(mercury=0, venus=34, earth=0, mars=34)
    base = 185
    for k in ORDER:
        r_ = round(d[k]/2*sc, 1)
        s += planet(k, xs[k], base, r_, 'sz')
        ex = ys.get(k, 0) if k in ys else 0
        by = base + max(r_, 6) + 30 + (ex if k in ys else 0)
        if k in ys and ex: s += f'<line x1="{xs[k]}" y1="{base+r_+4}" x2="{xs[k]}" y2="{by-20}" stroke="#aab" />'
        by = base + max(r_, 6) + 30 + (34 if (k in ys and ex) else 0)
        if k in ('jupiter', 'saturn'): by = base + 80 + 28
        if k in ('uranus', 'neptune'): by = base + 80 + 28
        s += f'<text x="{xs[k]}" y="{by}" font-size="20" font-weight="700" fill="#1d2a52" text-anchor="middle">{NAMES[k]}</text>'
        s += f'<text x="{xs[k]}" y="{by+22}" font-size="14" fill="#555" text-anchor="middle">{d[k]:,}</text>'
    s += '<text x="450" y="38" font-size="22" font-weight="700" fill="#0b5d3b" text-anchor="middle">مقارنة أحجام الكواكب (الأقطار بالكيلومتر، بنسبتها الحقيقية)</text>'
    s += '<text x="450" y="66" font-size="16" fill="#555" text-anchor="middle">المشتري يتّسع لأكثر من 1300 كرة بحجم الأرض! أما قطر الشمس فيساوي 109 أمثال قطر الأرض.</text>'
    return s + '</svg>'

def svg_address():
    W, H = 900, 470
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 120)
    cx, cy = 650, 225
    rings = [(205, '#2b3a8c', 'الكون'), (162, '#3b4cb0', 'العنقود المحلي للمجرّات'), (120, '#5a6ad0', 'مجرّة درب التبانة'),
             (78, '#f0a830', 'النظام الشمسي'), (34, '#3a7fc8', 'الأرض')]
    for r, c, _ in rings:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" fill-opacity=".6" stroke="#fff" stroke-opacity=".5"/>'
    ys = [60, 135, 210, 285, 360]
    for (r, c, t), y in zip(rings, ys):
        ang = math.radians(215)
        rr = r - 8 if r > 40 else 0
        ex = cx + rr*math.cos(ang); ey = cy + rr*math.sin(ang)
        s += f'<line x1="410" y1="{y}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="#ffd36b" stroke-opacity=".8"/>'
        s += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="4.5" fill="#ffd36b"/>'
        s += f'<text x="400" y="{y+7}" font-size="24" font-weight="700" fill="#fff" text-anchor="end">{t}</text>'
    s += '<text x="450" y="448" font-size="18" fill="#ffd36b" text-anchor="middle" font-weight="700">الأرض ← النظام الشمسي ← درب التبانة ← العنقود المحلي ← الكون</text>'
    return s + '</svg>'

_old_milky = svg_milkyway
def svg_milkyway():
    return _old_milky().replace(
        'x1="252" y1="202"', 'x1="252" y1="202"')  # placeholder, replaced below

def svg_milkyway():
    W, H = 900, 560
    cx, cy = 450, 285
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += ('<defs><radialGradient id="bulge"><stop offset="0" stop-color="#fff6c8"/><stop offset=".5" stop-color="#f3b94a" stop-opacity=".8"/>'
          '<stop offset="1" stop-color="#f3b94a" stop-opacity="0"/></radialGradient></defs>')
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#070a22"/>' + stars(W, H, 160)
    for arm in range(4):
        for i in range(260):
            t = i / 260; r = 30 + t * 215; th = arm * math.pi/2 + t * 3.7
            for _ in range(3):
                jr = random.gauss(0, 7 + 10*t); jt = random.gauss(0, .05)
                x = cx + (r + jr) * math.cos(th + jt) * 1.5; y = cy + (r + jr) * math.sin(th + jt) * .93
                col = '#9fc0ff' if random.random() < .6 else '#ffe9b0'
                s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(.6,1.7):.1f}" fill="{col}" opacity="{random.uniform(.35,.95):.2f}"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="95" ry="52" fill="url(#bulge)"/>'
    t = 0.60; r = 30 + t*215; th = math.pi/2 + t*3.7
    sx = cx + r*math.cos(th)*1.5; sy = cy + r*math.sin(th)*.93
    s += f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="9" fill="#ffb300" stroke="#fff" stroke-width="2"/>'
    s += f'<line x1="{sx:.0f}" y1="{sy-10:.0f}" x2="{sx:.0f}" y2="{sy-52:.0f}" stroke="#ffd36b" stroke-width="2"/>'
    s += f'<rect x="{sx-135:.0f}" y="{sy-92:.0f}" width="270" height="40" rx="10" fill="#0b1030" stroke="#ffd36b"/>'
    s += f'<text x="{sx:.0f}" y="{sy-64:.0f}" font-size="21" fill="#ffd36b" font-weight="700" text-anchor="middle">نحن هنا (النظام الشمسي)</text>'
    s += f'<text x="{cx}" y="{cy+6}" font-size="18" fill="#3a2a00" font-weight="700" text-anchor="middle">مركز المجرّة</text>'
    s += '<line x1="130" y1="528" x2="770" y2="528" stroke="#7fd1ff" stroke-width="2"/><path d="M130 520 V536 M770 520 V536" stroke="#7fd1ff" stroke-width="2"/>'
    s += '<text x="450" y="516" font-size="18" fill="#7fd1ff" text-anchor="middle" font-weight="700">قطر المجرّة نحو 100,000 سنة ضوئية</text>'
    s += '<text x="450" y="40" font-size="24" fill="#fff" text-anchor="middle" font-weight="700">مجرّة درب التبانة (منظر تخيّلي من الأعلى)</text>'
    return s + '</svg>'

def svg_sun():
    W, H = 900, 440
    cx, cy = 690, 220
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 90)
    s += f'<circle cx="{cx}" cy="{cy}" r="195" fill="#ffb300" opacity=".12"/><circle cx="{cx}" cy="{cy}" r="172" fill="#ffb300" opacity=".22"/>'
    for r, c in [(145, '#ff8f1f'), (115, '#ffb02e'), (82, '#ffd04a'), (40, '#fff3b0')]:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>'
    lay = [(55,  'الإكليل (الغلاف الخارجي)', ['طبقة حارّة رقيقة، تظهر عند كسوف الشمس'], cx-165, cy-85),
           (125, 'سطح الشمس (الفوتوسفير)', ['حرارته نحو 5500°م — منه يصلنا الضوء'], cx-130, cy-62),
           (200, 'منطقة الحمل', ['الغاز الساخن يصعد ويهبط', 'مثل الماء الذي يغلي'], cx-100, cy-30),
           (275, 'منطقة الإشعاع', ['الطاقة تنتقل فيها ببطء شديد'], cx-62, cy+10),
           (345, 'النواة (قلب الشمس)', ['حرارتها نحو 15 مليون درجة', 'فيها يتحوّل الهيدروجين إلى هيليوم', 'فتنتج الطاقة'], cx-14, cy+18)]
    for y, t, ds, px, py in lay:
        s += f'<line x1="470" y1="{y-6}" x2="{px}" y2="{py}" stroke="#ffd36b" stroke-opacity=".8"/><circle cx="{px}" cy="{py}" r="4.5" fill="#fff"/>'
        s += f'<text x="462" y="{y}" font-size="21" font-weight="700" fill="#ffd36b" text-anchor="end">{t}</text>'
        for j, d in enumerate(ds):
            s += f'<text x="462" y="{y+22+j*20}" font-size="16" fill="#dfe4ff" text-anchor="end">{d}</text>'
    return s + '</svg>'

def svg_rotation():
    W, H = 900, 330
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("ea")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 80)
    ax, ay, r = 520, 175, 105
    s += sun_disc(905, 175, 70, 'ea')
    s += '<text x="820" y="60" font-size="22" fill="#ffd36b" font-weight="700" text-anchor="middle">الشمس</text>'
    for dy in (-70, 0, 70):
        s += f'<line x1="830" y1="{ay+dy}" x2="{ax+r+16}" y2="{ay+dy}" stroke="#ffd36b" stroke-width="3" stroke-dasharray="8 6"/>'
    s += planet('earth', ax, ay, r, 'ea')
    s += (f'<clipPath id="nightc"><circle cx="{ax}" cy="{ay}" r="{r}"/></clipPath>'
          f'<rect x="{ax-r}" y="{ay-r}" width="{r}" height="{2*r}" fill="#000" opacity=".6" clip-path="url(#nightc)"/>')
    tx, ty = math.sin(math.radians(23.5))*(r+32), math.cos(math.radians(23.5))*(r+32)
    s += f'<line x1="{ax+tx:.0f}" y1="{ay-ty:.0f}" x2="{ax-tx:.0f}" y2="{ay+ty:.0f}" stroke="#fff" stroke-width="2.5" stroke-dasharray="4 5"/>'
    s += f'<text x="{ax+tx+10:.0f}" y="{ay-ty+8:.0f}" font-size="17" fill="#fff">محور الأرض</text>'
    s += f'<text x="{ax+r*.5:.0f}" y="{ay+9}" font-size="28" font-weight="700" fill="#fff" text-anchor="middle">نهار</text>'
    s += f'<text x="{ax-r*.5:.0f}" y="{ay+9}" font-size="28" font-weight="700" fill="#cfd8ff" text-anchor="middle">ليل</text>'
    s += '<text x="255" y="90" font-size="26" fill="#fff" text-anchor="middle" font-weight="700">الدوران حول النفس</text>'
    s += '<text x="255" y="135" font-size="20" fill="#ffd36b" text-anchor="middle">دورة كاملة كل 24 ساعة</text>'
    s += '<text x="255" y="172" font-size="20" fill="#dfe4ff" text-anchor="middle">= تعاقب الليل والنهار</text>'
    s += '<text x="255" y="212" font-size="18" fill="#9aa4d6" text-anchor="middle">النصف المواجه للشمس: نهار</text>'
    s += '<text x="255" y="238" font-size="18" fill="#9aa4d6" text-anchor="middle">والنصف الآخر: ليل</text>'
    return s + '</svg>'

def svg_seasons():
    W, H = 900, 470
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("ea")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0b1030"/>' + stars(W, H, 80)
    ox, oy, rx, ry = 450, 262, 330, 105
    s += f'<ellipse cx="{ox}" cy="{oy}" rx="{rx}" ry="{ry}" fill="none" stroke="#fff" stroke-opacity=".4" stroke-dasharray="5 7" stroke-width="2"/>'
    s += sun_disc(ox, oy, 30, 'ea')
    s += f'<text x="{ox}" y="{oy+62}" font-size="19" fill="#ffd36b" font-weight="700" text-anchor="middle">الشمس</text>'
    pos = [(ox-rx, oy, 'يونيو', 'صيف في الشمال', 'شتاء في الجنوب', 'b'), (ox+rx, oy, 'ديسمبر', 'شتاء في الشمال', 'صيف في الجنوب', 'b'),
           (ox, oy-ry, 'مارس', 'ربيع في الشمال', '', 't'), (ox, oy+ry, 'سبتمبر', 'خريف في الشمال', '', 'b')]
    for x, y, m, a, b_, side in pos:
        s += planet('earth', x, y, 22, 'ea')
        s += f'<line x1="{x+15:.0f}" y1="{y-38:.0f}" x2="{x-15:.0f}" y2="{y+38:.0f}" stroke="#fff" stroke-width="2.2"/>'
        ty = y - 52 if side == 't' else y + 56
        if side == 't':
            s += f'<text x="{x}" y="{ty-22:.0f}" font-size="21" fill="#fff" text-anchor="middle" font-weight="700">{m}</text>'
            s += f'<text x="{x}" y="{ty:.0f}" font-size="16" fill="#cfd8ff" text-anchor="middle">{a}</text>'
        else:
            s += f'<text x="{x}" y="{ty:.0f}" font-size="21" fill="#fff" text-anchor="middle" font-weight="700">{m}</text>'
            s += f'<text x="{x}" y="{ty+22:.0f}" font-size="16" fill="#cfd8ff" text-anchor="middle">{a}</text>'
            if b_: s += f'<text x="{x}" y="{ty+42:.0f}" font-size="16" fill="#9fb0e8" text-anchor="middle">{b_}</text>'
    s += '<text x="450" y="34" font-size="22" fill="#fff" text-anchor="middle" font-weight="700">الدوران حول الشمس: سنة كاملة، والمحور المائل يصنع الفصول</text>'
    return s + '</svg>'

def svg_earth():
    return (svg_rotation() + '<div class="cap">رسم 9-أ: الدوران حول المحور يصنع الليل والنهار</div></div>'
            '<div class="fig">' + svg_seasons())

def svg_year():
    W, H = 900, 420
    data = [('mercury', 0.241, '88 يومًا'), ('venus', 0.615, '225 يومًا'), ('earth', 1.0, '365 يومًا (سنة)'),
            ('mars', 1.881, '687 يومًا'), ('jupiter', 11.86, '12 سنة تقريبًا'), ('saturn', 29.46, '29.5 سنة'),
            ('uranus', 84.0, '84 سنة'), ('neptune', 164.8, '165 سنة')]
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs("yr")}'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#f4f6fb" stroke="#cfd6ea"/>'
    s += '<text x="450" y="36" font-size="23" font-weight="700" fill="#0b5d3b" text-anchor="middle">كم تستغرق «سنة» كل كوكب؟ (زمن دورته حول الشمس)</text>'
    for i, (k, y, lab) in enumerate(data):
        yy = 62 + i*41
        w = max(math.sqrt(y) * 40, 8)
        s += planet(k, 858, yy+12, 13 if k != 'saturn' else 9, 'yr')
        s += f'<text x="828" y="{yy+19}" font-size="22" font-weight="700" fill="#1d2a52" text-anchor="end">{NAMES[k]}</text>'
        s += f'<rect x="{715-w:.0f}" y="{yy}" width="{w:.0f}" height="26" rx="7" fill="{shade(COL[k], -0.1)}"/>'
        s += f'<text x="{715-w-10:.0f}" y="{yy+20}" font-size="19" fill="#333" text-anchor="end">{lab}</text>'
    s += '<text x="450" y="408" font-size="15" fill="#777" text-anchor="middle">كلما ابتعد الكوكب عن الشمس صارت سنته أطول (الأطوال مرسومة بمقياس تقريبي)</text>'
    return s + '</svg>'

# =========================================================== HTML
CSS = open('/home/user/-/build/solar.css', encoding='utf-8').read()
BODY = open('/home/user/-/build/solar_body.html', encoding='utf-8').read()

vals = dict(SVG_OVERVIEW=svg_overview(), SVG_ORBITS=svg_orbits(), SVG_SIZES=svg_sizes(), SVG_ADDRESS=svg_address(),
            SVG_MILKY=svg_milkyway(), SVG_SUN=svg_sun(), SVG_EARTH=svg_earth(), SVG_YEAR=svg_year(),
            SVG_SMALL=svg_small(), CARDS=cards_html(), STATS=stats_html(), TABLE=table_html())
def flip(v):
    # in an RTL document SVG text-anchor start/end are mirrored; swap so that 'end' means right edge
    return v.replace('text-anchor="start"', '@@S@@').replace('text-anchor="end"', 'text-anchor="start"').replace('@@S@@', 'text-anchor="end"')
for k, v in vals.items():
    assert '{{'+k+'}}' in BODY, k
    BODY = BODY.replace('{{'+k+'}}', flip(v) if k.startswith('SVG') else v)

html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>المجموعة الشمسية — شرح مبسّط بالرسوم</title>
<style>{CSS}</style></head><body>{BODY}</body></html>'''
open('/home/user/-/build/solar_system.html', 'w', encoding='utf-8').write(html)
print('ok', len(html))
