#!/usr/bin/env python3
"""Generates living.html: environment intro + classification of living things (kingdoms)."""
import random, math
random.seed(5)

def arrow_defs(i, color):
    return (f'<marker id="ar{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{color}"/></marker>')

def arrow(x1, y1, x2, y2, color, i, w=3, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" marker-end="url(#ar{i})"{d}/>'

def pill(cx, cy, w, text, fill, stroke, color='#222', fs=18, bold=True):
    return (f'<rect x="{cx-w/2}" y="{cy-16}" width="{w}" height="32" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<text x="{cx}" y="{cy+6}" font-size="{fs}" text-anchor="middle" fill="{color}" {"font-weight=\"700\"" if bold else ""}>{text}</text>')

# ---------------------------------------------------------------- 1: ecosystem scene
def svg_eco():
    W, H = 900, 440
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs>'
    s += '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9dcff"/><stop offset="1" stop-color="#e9f7ff"/></linearGradient>'
    s += '<linearGradient id="soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5a2b"/><stop offset="1" stop-color="#5e3a1a"/></linearGradient></defs>'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="url(#sky)"/>'
    # sun
    s += '<circle cx="790" cy="75" r="46" fill="#ffc933"/><circle cx="790" cy="75" r="62" fill="#ffc933" opacity=".25"/>'
    # clouds
    for cx, cy in [(300, 70), (520, 110)]:
        s += f'<g fill="#fff" opacity=".95"><ellipse cx="{cx}" cy="{cy}" rx="60" ry="22"/><ellipse cx="{cx-30}" cy="{cy+6}" rx="34" ry="18"/><ellipse cx="{cx+34}" cy="{cy+8}" rx="38" ry="18"/></g>'
    # ground
    s += '<path d="M0 262 Q200 232 420 258 T900 250 V440 H0 Z" fill="#4caf50"/>'
    s += '<rect x="0" y="330" width="900" height="110" rx="0" fill="url(#soil)"/>'
    s += '<path d="M0 330 Q200 318 420 330 T900 326" fill="none" stroke="#3b8f3f" stroke-width="6"/>'
    # pond
    s += '<ellipse cx="170" cy="318" rx="130" ry="38" fill="#3d9be9"/><ellipse cx="170" cy="312" rx="110" ry="26" fill="#6bb7f2" opacity=".6"/>'
    # emoji
    em = [('🌳', 600, 275, 84), ('🌳', 700, 285, 66), ('🌸', 520, 290, 38), ('🌿', 470, 292, 38), ('🐇', 405, 290, 52),
          ('🐟', 150, 330, 46), ('🐦', 600, 130, 50), ('🍄', 790, 300, 44), ('🦊', 300, 288, 50), ('🐛', 560, 300, 30)]
    for e, x, y, fs in em:
        s += f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="middle">{e}</text>'
    # bacteria in soil
    for _ in range(26):
        x, y = random.uniform(30, 870), random.uniform(350, 425)
        a = random.uniform(0, 180)
        s += f'<rect x="{x-7:.0f}" y="{y-3:.0f}" width="14" height="6" rx="3" fill="#7fd1ff" transform="rotate({a:.0f} {x:.0f} {y:.0f})" opacity=".9"/>'
    s += '<text x="450" y="392" font-size="34" text-anchor="middle">🦠</text>'
    # labels
    live = ('#e7f6e7', '#2b8a3e'); dead = ('#f1f1f1', '#777')
    L = [(790, 148, 'الشمس', dead, 90), (330, 140, 'الهواء', dead, 80), (170, 280, 'الماء', dead, 70),
         (450, 420, 'التربة', dead, 80), (610, 228, 'نبات', live, 70), (405, 232, 'حيوان', live, 80),
         (790, 262, 'فطريات', live, 90), (300, 232, 'حيوان', live, 80), (470, 372, 'بكتيريا', live, 90), (150, 375, 'حيوان مائي', live, 130)]
    seen = set()
    for x, y, t, (f, st), w in L:
        if (t, x) in seen: continue
        seen.add((t, x))
        s += pill(x, y, w, t, f, st, fs=18)
    s += pill(120, 28, 190, 'كائنات حيّة', '#e7f6e7', '#2b8a3e')
    s += pill(330, 28, 230, 'مكوّنات غير حيّة', '#f1f1f1', '#777')
    return s + '</svg>'

# ---------------------------------------------------------------- 2: food chain
def svg_chain():
    W, H = 900, 330
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs>{arrow_defs(1, "#e8590c")}{arrow_defs(2, "#7a5a2b")}</defs>'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#f4faf1" stroke="#cfe3c8"/>'
    boxes = [('☀️', 'الشمس', 'مصدر الطاقة', '#fff3bf', '#f59f00'),
             ('🌿', 'النبات', 'منتِج (يصنع غذاءه)', '#d3f9d8', '#2b8a3e'),
             ('🐇', 'الأرنب', 'مستهلِك أول (آكل أعشاب)', '#ffe8cc', '#e8590c'),
             ('🦊', 'الثعلب', 'مستهلِك ثانٍ (آكل لحوم)', '#ffd8d8', '#c92a2a')]
    xs = [735, 555, 375, 195]
    for (e, n, r, f, st), x in zip(boxes, xs):
        s += f'<rect x="{x}" y="30" width="150" height="150" rx="16" fill="{f}" stroke="{st}" stroke-width="3"/>'
        s += f'<text x="{x+75}" y="98" font-size="58" text-anchor="middle">{e}</text>'
        s += f'<text x="{x+75}" y="132" font-size="22" font-weight="700" text-anchor="middle" fill="#222">{n}</text>'
        s += f'<text x="{x+75}" y="160" font-size="14" text-anchor="middle" fill="#444">{r}</text>'
    for x in xs[:-1]:
        s += arrow(x - 4, 105, x - 38, 105, '#e8590c', 1, 4)
    # decomposers
    s += '<rect x="330" y="235" width="240" height="78" rx="16" fill="#efe3d3" stroke="#7a5a2b" stroke-width="3"/>'
    s += '<text x="450" y="268" font-size="30" text-anchor="middle">🍄 🦠</text>'
    s += '<text x="450" y="300" font-size="19" font-weight="700" text-anchor="middle" fill="#3b2a14">المحلِّلات: فطريات وبكتيريا</text>'
    for x in (630, 450, 270):
        s += arrow(x, 184, 450 if x != 450 else 450, 233, '#7a5a2b', 2, 2.5, '6 5')
    s += '<text x="780" y="270" font-size="16" fill="#555" text-anchor="middle">الأسهم تدلّ على انتقال الطاقة والغذاء</text>'
    s += '<text x="780" y="292" font-size="16" fill="#7a5a2b" text-anchor="middle">والمحلِّلات تُعيد المواد إلى التربة</text>'
    return s + '</svg>'

# ---------------------------------------------------------------- 3: classification tree
def svg_tree():
    W, H = 900, 450
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#f7f9fc" stroke="#d6dcea"/>'
    s += '<rect x="300" y="14" width="300" height="52" rx="14" fill="#0b2a6b"/><text x="450" y="50" font-size="26" font-weight="700" fill="#fff" text-anchor="middle">الكائنات الحية</text>'
    kings = [('🐱', 'مملكة الحيوان', '#d9480f', ['تتحرّك', 'تأكل الطعام جاهزًا', '(لا تصنعه)'], 'الإنسان • القط • السمكة'),
             ('🌳', 'مملكة النبات', '#2b8a3e', ['تصنع طعامها بنفسها', 'بضوء الشمس', 'ثابتة في مكانها'], 'الأشجار • الأزهار • الأعشاب'),
             ('🍄', 'مملكة الفطريات', '#8d5a2b', ['لا تصنع طعامها', 'تمتصّه من النبات أو', 'الحيوان أو الأطعمة الفاسدة'], 'الفطر • العفن • الخميرة'),
             ('🦠', 'مملكة البكتيريا', '#1c7ed6', ['صغيرة جدًّا', 'لا تُرى بالعين المجرّدة', 'تُرى بالمجهر فقط'], 'نافعة • ضارّة')]
    xs = [678, 458, 238, 18]
    for (e, n, c, lines, ex), x in zip(kings, xs):
        cx = x + 102
        s += f'<path d="M450 66 V100 H{cx} V130" fill="none" stroke="{c}" stroke-width="3"/>'
        s += f'<rect x="{x}" y="130" width="205" height="296" rx="14" fill="#fff" stroke="{c}" stroke-width="3"/>'
        s += f'<rect x="{x}" y="130" width="205" height="48" rx="14" fill="{c}"/><rect x="{x}" y="160" width="205" height="18" fill="{c}"/>'
        s += f'<text x="{cx}" y="163" font-size="21" font-weight="700" fill="#fff" text-anchor="middle">{n}</text>'
        s += f'<text x="{cx}" y="250" font-size="64" text-anchor="middle">{e}</text>'
        for i, l in enumerate(lines):
            s += f'<text x="{cx}" y="{288+i*27}" font-size="17.5" text-anchor="middle" fill="#222">{l}</text>'
        s += f'<line x1="{x+20}" y1="372" x2="{x+185}" y2="372" stroke="{c}" stroke-dasharray="4 4"/>'
        s += f'<text x="{cx}" y="400" font-size="16" text-anchor="middle" fill="{c}" font-weight="700">{ex}</text>'
    return s + '</svg>'

# ---------------------------------------------------------------- 4: photosynthesis
def svg_photo():
    W, H = 900, 420
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs>{arrow_defs(3, "#f08c00")}{arrow_defs(4, "#228be6")}{arrow_defs(5, "#495057")}{arrow_defs(6, "#2b8a3e")}</defs>'
    s += '<rect width="900" height="420" rx="18" fill="#eaf7ff"/>'
    s += '<rect x="0" y="300" width="900" height="120" fill="#8b5a2b"/><path d="M0 300 H900" stroke="#3b8f3f" stroke-width="8"/>'
    # plant
    s += '<rect x="440" y="140" width="14" height="165" fill="#3b8f3f"/>'
    s += '<ellipse cx="500" cy="170" rx="62" ry="26" fill="#43a047" transform="rotate(-20 500 170)"/><ellipse cx="395" cy="190" rx="62" ry="26" fill="#43a047" transform="rotate(20 395 190)"/>'
    s += '<ellipse cx="447" cy="130" rx="30" ry="40" fill="#66bb6a"/>'
    for dx in (-60, -30, 0, 30, 60):
        s += f'<path d="M{447+dx} 305 Q{447+dx*1.3} 340 {447+dx*1.7} 375" stroke="#d9b38c" stroke-width="4" fill="none"/>'
    # sun
    s += '<circle cx="790" cy="70" r="42" fill="#ffc933"/>'
    s += arrow(750, 98, 520, 150, '#f08c00', 3, 4)
    s += '<text x="760" y="150" font-size="20" font-weight="700" fill="#e67700" text-anchor="middle">ضوء الشمس</text>'
    # CO2
    s += arrow(190, 100, 380, 160, '#495057', 5, 4)
    s += '<text x="190" y="75" font-size="20" font-weight="700" fill="#343a40" text-anchor="middle">ثاني أكسيد الكربون</text><text x="190" y="98" font-size="15" fill="#555" text-anchor="middle">من الهواء</text>'
    # water
    s += arrow(190, 360, 380, 350, '#228be6', 4, 4)
    s += '<text x="150" y="350" font-size="20" font-weight="700" fill="#e7f5ff" text-anchor="middle">الماء</text><text x="150" y="372" font-size="15" fill="#d0ebff" text-anchor="middle">تمتصّه الجذور</text>'
    # outputs
    s += arrow(500, 120, 640, 40, '#2b8a3e', 6, 4)
    s += '<text x="610" y="24" font-size="20" font-weight="700" fill="#2b8a3e" text-anchor="middle">الأكسجين (O₂)</text>'
    s += arrow(520, 190, 700, 230, '#2b8a3e', 6, 4)
    s += '<text x="760" y="226" font-size="20" font-weight="700" fill="#2b8a3e" text-anchor="middle">الغذاء (سكّر)</text>'
    s += '<rect x="170" y="238" width="560" height="40" rx="20" fill="#fff" stroke="#2b8a3e" stroke-width="2"/>'
    s += '<text x="450" y="265" font-size="19" font-weight="700" text-anchor="middle" fill="#1b5e20">ماء + ثاني أكسيد الكربون + ضوء الشمس  ←  غذاء + أكسجين</text>'
    return s + '</svg>'

# ---------------------------------------------------------------- 5: bacteria shapes + doubling
def svg_bact():
    W, H = 900, 340
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#0d2b45"/>'
    for _ in range(60):
        s += f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,H):.0f}" r="{random.uniform(1,3):.1f}" fill="#7fd1ff" opacity=".18"/>'
    # three shapes (right panel)
    s += '<text x="680" y="40" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">ثلاثة أشكال للبكتيريا</text>'
    # cocci
    for dx, dy in [(0, 0), (30, 0), (15, 26), (45, 26), (-15, 26)]:
        s += f'<circle cx="{800+dx}" cy="{110+dy}" r="16" fill="#51cf66" stroke="#2b8a3e" stroke-width="2"/>'
    s += '<text x="815" y="190" font-size="18" fill="#fff" text-anchor="middle">كروية</text>'
    # bacilli
    for x, y, a in [(650, 100, 20), (690, 118, -15), (660, 140, 70), (700, 90, 50)]:
        s += f'<rect x="{x-26}" y="{y-9}" width="52" height="18" rx="9" fill="#ff922b" stroke="#d9480f" stroke-width="2" transform="rotate({a} {x} {y})"/>'
    s += '<text x="675" y="190" font-size="18" fill="#fff" text-anchor="middle">عُصَيّة (عصويّة)</text>'
    # spiral
    s += '<path d="M520 90 q15 -22 30 0 t30 0 t30 0 t30 0" fill="none" stroke="#da77f2" stroke-width="9" stroke-linecap="round"/>'
    s += '<path d="M520 135 q15 -22 30 0 t30 0 t30 0 t30 0" fill="none" stroke="#da77f2" stroke-width="9" stroke-linecap="round"/>'
    s += '<text x="570" y="190" font-size="18" fill="#fff" text-anchor="middle">حلزونية</text>'
    s += '<line x1="470" y1="20" x2="470" y2="320" stroke="#fff" stroke-opacity=".3" stroke-dasharray="5 6"/>'
    # doubling (left panel)
    s += '<text x="240" y="40" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">كيف تتكاثر؟ تنقسم إلى اثنتين</text>'
    rows = [(1, 'بعد 0 دقيقة', 330), (2, 'بعد 20 دقيقة', 250), (4, 'بعد 40 دقيقة', 170), (8, 'بعد ساعة', 90)]
    for n, lab, _ in rows:
        pass
    ys = [90, 140, 190, 240]
    for (n, lab, _), y in zip(rows, ys):
        gap = 40
        x0 = 340 - (n - 1) * gap / 2
        for i in range(n):
            s += f'<circle cx="{x0+i*gap:.0f}" cy="{y}" r="15" fill="#51cf66" stroke="#2b8a3e" stroke-width="2"/>'
        s += f'<text x="440" y="{y+6}" font-size="17" fill="#cfe9ff" text-anchor="end">{lab}</text>'
    s += '<text x="240" y="296" font-size="17" fill="#ffe066" text-anchor="middle">في الظروف المناسبة تتضاعف أعدادها بسرعة هائلة!</text>'
    s += '<text x="450" y="326" font-size="15" fill="#9ec9e8" text-anchor="middle">حجم البكتيريا نحو 1 إلى 5 ميكرومتر؛ أي أصغر من المليمتر بنحو ألف مرة</text>'
    return s + '</svg>'

# ---------------------------------------------------------------- HTML helpers
CARDS = [('🔬', 'تتكوّن من خلايا', 'الخلية وحدة بناء كل كائن حي'),
         ('🍽️', 'تتغذّى', 'تحصل على الغذاء لتنتج الطاقة'),
         ('🌬️', 'تتنفّس', 'تأخذ الأكسجين أو الغازات التي تحتاجها'),
         ('📏', 'تنمو', 'يكبر حجمها وتتغيّر مع الوقت'),
         ('🐣', 'تتكاثر', 'تُنتج أفرادًا جددًا من نوعها'),
         ('🌻', 'تستجيب', 'تتأثّر بما حولها: كاتجاه النبات للضوء'),
         ('💧', 'تُخرج الفضلات', 'تتخلّص من المواد الضارّة أو الزائدة'),
         ('🏃', 'تتحرّك', 'بعضها ينتقل، وبعضها يحرّك أجزاءه')]

def cards():
    s = '<div class="grid4">'
    for e, t, d in CARDS:
        s += f'<div class="mini"><div class="e">{e}</div><b>{t}</b><br><span>{d}</span></div>'
    return s + '</div>'

CSS = open('/home/user/-/build/living.css', encoding='utf-8').read()
BODY = open('/home/user/-/build/living_body.html', encoding='utf-8').read()

def flip(v):
    return v.replace('text-anchor="start"', '@@S@@').replace('text-anchor="end"', 'text-anchor="start"').replace('@@S@@', 'text-anchor="end"')

vals = dict(SVG_ECO=svg_eco(), SVG_CHAIN=svg_chain(), SVG_TREE=svg_tree(), SVG_PHOTO=svg_photo(), SVG_BACT=svg_bact(), CARDS=cards())
for k, v in vals.items():
    assert '{{' + k + '}}' in BODY, k
    BODY = BODY.replace('{{' + k + '}}', flip(v) if k.startswith('SVG') else v)

html = f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>تصنيف الكائنات الحية</title><style>{CSS}</style></head><body>{BODY}</body></html>'
open('/home/user/-/build/living.html', 'w', encoding='utf-8').write(html)
print('ok')
