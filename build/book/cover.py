# -*- coding: utf-8 -*-
"""Full-page illustrated cover (A4 ratio) with optional logo slots (assets/logo_right.* , assets/logo_left.*)."""
import os, math, random, base64, glob

B = os.path.dirname(os.path.abspath(__file__))

def _logo(name):
    for ext in ('png', 'svg', 'jpg', 'jpeg', 'webp'):
        p = os.path.join(B, 'assets', f'{name}.{ext}')
        if os.path.exists(p):
            mime = {'png': 'image/png', 'svg': 'image/svg+xml', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'webp': 'image/webp'}[ext]
            return f'data:{mime};base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    return None

def t(x, y, s, size, fill='#222', bold=False, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="middle"{" font-weight=\"700\"" if bold else ""} {extra}>{s}</text>'

def cover_svg():
    W, H = 794, 1123
    random.seed(21)
    s = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice"><defs>'
         '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f8fe0"/><stop offset=".45" stop-color="#8fd0ff"/><stop offset=".8" stop-color="#fff1c7"/></linearGradient>'
         '<radialGradient id="sunG"><stop offset="0" stop-color="#fff7c2"/><stop offset=".55" stop-color="#ffd43b"/><stop offset="1" stop-color="#ffa94d"/></radialGradient>'
         '<linearGradient id="riv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7cc7ff"/><stop offset="1" stop-color="#2d7fd4"/></linearGradient>'
         '<linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ad66e"/><stop offset="1" stop-color="#4aa84c"/></linearGradient>'
         '<linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fbf5a"/><stop offset="1" stop-color="#2f8a3c"/></linearGradient>'
         '</defs>')
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    # sun + rays
    sx, sy = 650, 215
    for i in range(24):
        a = math.radians(i * 15)
        s += f'<line x1="{sx+92*math.cos(a):.0f}" y1="{sy+92*math.sin(a):.0f}" x2="{sx+(150 if i%2 else 130)*math.cos(a):.0f}" y2="{sy+(150 if i%2 else 130)*math.sin(a):.0f}" stroke="#ffe066" stroke-width="7" stroke-linecap="round" opacity=".75"/>'
    s += f'<circle cx="{sx}" cy="{sy}" r="120" fill="#fff3b0" opacity=".35"/><circle cx="{sx}" cy="{sy}" r="78" fill="url(#sunG)"/>'
    # stars-ish sparkles at top and clouds
    for _ in range(30):
        s += f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,330):.0f}" r="{random.uniform(1,2.6):.1f}" fill="#fff" opacity=".55"/>'
    for cx, cy, sc in [(120, 430, 1.1), (420, 395, .9), (700, 470, .8)]:
        s += (f'<g fill="#fff" opacity=".93"><ellipse cx="{cx}" cy="{cy}" rx="{80*sc:.0f}" ry="{28*sc:.0f}"/><ellipse cx="{cx-40*sc:.0f}" cy="{cy+8*sc:.0f}" rx="{46*sc:.0f}" ry="{22*sc:.0f}"/>'
              f'<ellipse cx="{cx+46*sc:.0f}" cy="{cy+10*sc:.0f}" rx="{52*sc:.0f}" ry="{22*sc:.0f}"/></g>')
    # mountains
    s += '<path d="M0 700 L110 590 L200 660 L330 540 L450 665 L575 575 L690 670 L794 610 V820 H0Z" fill="#9db6e8"/>'
    s += '<path d="M330 540 L300 575 L330 565 L355 578Z M110 590 L90 612 L112 604 L130 616Z M575 575 L550 605 L575 596 L598 610Z" fill="#fff" opacity=".9"/>'
    s += '<path d="M0 760 Q140 670 300 740 T600 720 T794 735 V900 H0Z" fill="#7fd06b"/>'
    s += '<path d="M0 840 Q220 760 430 835 T794 815 V1123 H0Z" fill="url(#g1)"/>'
    # river
    s += '<path d="M330 1123 C300 1010 520 985 470 905 C430 845 505 800 540 765 L580 770 C545 815 485 850 530 905 C590 985 430 1030 520 1123Z" fill="url(#riv)"/>'
    for (x1, y1, x2, y2) in [(430, 1060, 480, 1048), (470, 985, 520, 975), (500, 925, 540, 915), (520, 880, 548, 872)]:
        s += f'<path d="M{x1} {y1} q15 -10 30 0 t30 0" stroke="#fff" stroke-width="3.5" fill="none" opacity=".85"/>'
    s += '<path d="M0 960 Q200 905 340 975 L330 1123 H0Z" fill="url(#g2)"/><path d="M794 950 Q640 900 560 985 L520 1123 H794Z" fill="url(#g2)"/>'
    # flowers
    cols = ['#ff6b8a', '#ffd43b', '#fff', '#ff922b', '#b197fc']
    for _ in range(150):
        x = random.uniform(0, W); y = random.uniform(900, 1123)
        if 330 < x < 560 and y > 900:  # river zone approx
            continue
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(2.5,5):.1f}" fill="{random.choice(cols)}"/>'
    # emoji scene
    for e, x, y, fs in [('🌳', 105, 835, 170), ('🌴', 705, 800, 150), ('🌳', 635, 860, 110), ('🐄', 190, 990, 105), ('🐑', 285, 1040, 80), ('🚜', 650, 975, 105),
                        ('🪨', 95, 1075, 85), ('🌾', 720, 1050, 90), ('🌱', 610, 1075, 70), ('🦋', 165, 700, 58), ('🐝', 590, 705, 50), ('🐦', 290, 610, 52), ('🐦', 340, 585, 38), ('🐟', 505, 985, 42), ('💧', 395, 905, 40)]:
        s += t(x, y, e, fs)
    # top bar (logo slots)
    s += '<rect x="30" y="26" width="734" height="92" rx="24" fill="#fff" opacity=".95" stroke="#0b2a6b" stroke-width="3"/>'
    s += t(397, 66, 'الصف الرابع الابتدائي', 38, '#0b2a6b', True) + t(397, 100, 'الفصل الدراسي الأول', 26, '#1c7ed6', True)
    lr, ll = _logo('logo_right'), _logo('logo_left')
    if lr: s += f'<image href="{lr}" x="46" y="34" width="150" height="76" preserveAspectRatio="xMidYMid meet" transform="translate(548 0)"/>'
    if ll: s += f'<image href="{ll}" x="46" y="34" width="150" height="76" preserveAspectRatio="xMidYMid meet"/>'
    # ribbon title
    s += '<path d="M60 250 L110 290 L110 330 L60 330 L90 290Z" fill="#0b2a6b" opacity=".85"/><path d="M734 250 L684 290 L684 330 L734 330 L704 290Z" fill="#0b2a6b" opacity=".85"/>'
    s += '<rect x="106" y="178" width="586" height="170" rx="40" fill="#0b2a6b" opacity=".25" transform="translate(7 9)"/>'
    s += '<rect x="106" y="178" width="586" height="170" rx="40" fill="#fff" stroke="#0b2a6b" stroke-width="7"/>'
    s += '<rect x="122" y="194" width="554" height="138" rx="28" fill="none" stroke="#f0a830" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round"/>'
    s += t(397, 298, 'العلوم', 138, '#0b2a6b', True, 'style="paint-order:stroke" stroke="#f0a830" stroke-width="5"')
    # unit medallions
    units = [('🌍', ['الإنسان', 'والبيئة'], '#2b8a3e', 600), ('🐝', ['الكائنات', 'الحية'], '#e8590c', 397), ('🌱', ['الأرض والتربة', 'والزراعة'], '#8d5a2b', 194)]
    for e, lines, c, x in units:
        s += f'<circle cx="{x}" cy="500" r="66" fill="#000" opacity=".12" transform="translate(4 6)"/><circle cx="{x}" cy="500" r="66" fill="#fff" stroke="{c}" stroke-width="8"/>'
        s += t(x, 523, e, 66)
        w = 28 + max(len(l) for l in lines) * 12.5
        h = 16 + 27 * len(lines)
        s += f'<rect x="{x-w/2:.0f}" y="582" width="{w:.0f}" height="{h}" rx="22" fill="{c}"/>'
        for i, l in enumerate(lines):
            s += t(x, 610 + i * 27, l, 21, '#fff', True)
    # bottom band
    s += '<rect x="60" y="1056" width="674" height="52" rx="26" fill="#fff" opacity=".95" stroke="#0b2a6b" stroke-width="3"/>'
    s += t(397, 1090, 'اسم التلميذ: ............................................  الفصل: ..........', 22, '#0b2a6b', True)
    return s + '</svg>'
