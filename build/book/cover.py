# -*- coding: utf-8 -*-
"""Full-page cover (A4 ratio): layered landscape in the Knowledge Center palette, official white lockup, Lucide icons."""
import os, math, random, base64
import pics as I

B = os.path.dirname(os.path.abspath(__file__))

def _img(name):
    p = os.path.join(B, 'assets', name)
    if not os.path.exists(p): return None
    return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

def t(x, y, s, size, fill='#fff', w=700, op=1):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="middle" font-weight="{w}" opacity="{op}">{s}</text>'

def cover_svg():
    W, H = 794, 1123
    random.seed(7)
    s = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice"><defs>'
         '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#032a45"/><stop offset=".42" stop-color="#054473"/><stop offset=".72" stop-color="#0a5f6a"/><stop offset="1" stop-color="#063a41"/></linearGradient>'
         '<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff"/><stop offset=".62" stop-color="#f3eeec"/><stop offset="1" stop-color="#d2e3e5"/></radialGradient>'
         '<linearGradient id="m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3e8086" stop-opacity=".95"/><stop offset="1" stop-color="#0a5f6a"/></linearGradient>'
         '<linearGradient id="m2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b6974"/><stop offset="1" stop-color="#084c55"/></linearGradient>'
         '<linearGradient id="m3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a5f6a"/><stop offset="1" stop-color="#063a41"/></linearGradient>'
         '</defs>')
    s += f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
    for _ in range(70):
        s += f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,560):.0f}" r="{random.uniform(.6,1.8):.1f}" fill="#fff" opacity="{random.uniform(.25,.7):.2f}"/>'
    sx, sy = 690, 632
    for r, o in [(190, .10), (150, .14), (115, .20)]:
        s += f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="none" stroke="#d2e3e5" stroke-width="1.4" opacity="{o:.2f}"/>'
    s += f'<circle cx="{sx}" cy="{sy}" r="74" fill="#f3eeec" opacity=".18"/><circle cx="{sx}" cy="{sy}" r="54" fill="url(#sun)"/>'
    for bx, by, sc in [(610, 560, 1), (650, 535, .75), (575, 530, .6)]:
        s += f'<path d="M{bx-14*sc} {by} Q{bx-7*sc} {by-9*sc} {bx} {by} Q{bx+7*sc} {by-9*sc} {bx+14*sc} {by}" fill="none" stroke="#d2e3e5" stroke-width="2.4" stroke-linecap="round" opacity=".85"/>'
    s += '<path d="M0 700 L90 610 L170 665 L290 560 L400 650 L500 600 L610 680 L700 620 L794 690 V900 H0Z" fill="url(#m1)"/>'
    s += '<path d="M290 560 L262 592 L292 584 L318 596Z M500 600 L478 626 L502 620 L524 630Z M90 610 L72 630 L92 624 L110 634Z" fill="#f3eeec" opacity=".75"/>'
    s += '<path d="M0 790 Q150 700 330 770 T640 760 T794 780 V960 H0Z" fill="url(#m2)"/>'
    s += '<path d="M0 880 Q200 800 410 870 T794 850 V1123 H0Z" fill="url(#m3)"/>'
    s += '<path d="M330 1123 C310 1030 500 1000 450 930 C410 875 480 845 510 805 L546 808 C520 850 470 880 505 930 C560 1010 410 1050 490 1123Z" fill="#98babd" opacity=".55"/>'
    s += '<path d="M360 1123 C340 1040 520 1010 480 940 C446 886 500 860 522 826" fill="none" stroke="#f3eeec" stroke-width="2" opacity=".5"/>'
    def pine(x, y, h, c='#042f36'):
        w = h * .42
        return (f'<path d="M{x} {y-h} L{x-w*.55} {y-h*.55} L{x-w*.25} {y-h*.55} L{x-w*.8} {y-h*.2} L{x-w*.3} {y-h*.2} L{x-w} {y} L{x+w} {y} L{x+w*.3} {y-h*.2} L{x+w*.8} {y-h*.2} L{x+w*.25} {y-h*.55} L{x+w*.55} {y-h*.55} Z" fill="{c}"/>'
                f'<rect x="{x-3}" y="{y}" width="6" height="{h*.1}" fill="{c}"/>')
    for x, y, h in [(70, 960, 190), (140, 990, 140), (30, 1010, 120), (715, 950, 200), (650, 985, 150), (765, 1000, 130), (210, 1010, 90)]:
        s += pine(x, y, h)
    for x in range(20, 780, 26):
        if 300 < x < 540: continue
        h = random.uniform(40, 80); lean = random.uniform(-6, 6)
        s += f'<path d="M{x} 1123 Q{x+lean/2:.0f} {1123-h/2:.0f} {x+lean:.0f} {1123-h:.0f}" stroke="#98babd" stroke-width="2" fill="none" opacity=".55" stroke-linecap="round"/>'
    lk = _img('lockup-white.png')
    if lk: s += f'<image href="{lk}" x="456" y="48" width="290" height="98" preserveAspectRatio="xMidYMid meet"/>'
    s += '<line x1="48" y1="168" x2="746" y2="168" stroke="#d2e3e5" stroke-width="1.4" opacity=".6"/>'
    s += t(397, 360, 'العلوم', 190, '#fff', 900)
    s += '<line x1="297" y1="400" x2="497" y2="400" stroke="#98babd" stroke-width="2"/>'
    s += t(397, 462, 'السنة الثانية', 46, '#fff', 700)
    s += t(397, 506, 'الفصل الدراسي الأول', 28, '#d2e3e5', 300)
    for i, n in enumerate(['seedling', 'droplet', 'snowmtn', 'bee', 'wheat']):
        cx = 397 + (i - 2) * 94 - 40
        s += f'<circle cx="{cx}" cy="620" r="36" fill="#f3eeec" opacity=".92" stroke="#d2e3e5" stroke-width="1.6"/>' + I.nested(n, cx, 620, 48)
    s += '<rect x="48" y="1044" width="698" height="58" rx="10" fill="#032a45" opacity=".78" stroke="#98babd" stroke-width="1.4"/>'
    s += t(397, 1081, 'اسم الطالب: ..........................................   الفوج: ............', 21, '#f3eeec', 400)
    return s + '</svg>'
