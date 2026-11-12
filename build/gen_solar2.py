import sys, re
sys.path.insert(0, '/home/user/-/build')
import gen_solar as g   # reuses the SVG builders (re-writes the long version's html, harmless)

ov = g.svg_overview()
ov = ov.replace('viewBox="0 0 900 440"', 'viewBox="0 70 900 330"')
ov = re.sub(r'<text x="450" y="425".*?</text>', '', ov)
ov = g.flip(ov) if hasattr(g, 'flip') else ov

rows = [('mercury', 'صخري', 'أصغرها وأقربها للشمس، سنته 88 يومًا'),
        ('venus', 'صخري', 'أسخنها (465°م) بسبب غلافه الكثيف'),
        ('earth', 'صخري', 'كوكبنا، فيه الماء والحياة، وله قمر واحد'),
        ('mars', 'صخري', 'الكوكب الأحمر، له قمران'),
        ('jupiter', 'غازي عملاق', 'أكبرها؛ يتّسع لأكثر من 1300 أرض'),
        ('saturn', 'غازي عملاق', 'صاحب الحلقات الجليدية الجميلة'),
        ('uranus', 'جليدي عملاق', 'أزرق مخضر، يدور مستلقيًا على جنبه'),
        ('neptune', 'جليدي عملاق', 'أبعدها، سنته 165 سنة أرضية')]
tbl = '<table><tr><th>#</th><th>الكوكب</th><th>نوعه</th><th>أهم معلومة</th></tr>'
for i, (k, t, d) in enumerate(rows):
    tbl += f'<tr><td>{i+1}</td><td><b>{g.NAMES[k]}</b></td><td>{t}</td><td style="text-align:right">{d}</td></tr>'
tbl += '</table>'

html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>المجموعة الشمسية — ملخص</title>
<style>
@font-face {{ font-family:"LoewNA"; src:url("fonts/LoewNextArabic-Regular.otf"); font-weight:400; }}
@font-face {{ font-family:"LoewNA"; src:url("fonts/LoewNextArabic-Bold.otf"); font-weight:700; }}
@page {{ size:A4; margin:11mm 12mm 11mm 12mm; }}
* {{ box-sizing:border-box; }}
body {{ font-family:"LoewNA","FreeSerif",serif; font-size:11.5pt; line-height:1.75; color:#1b1b1b; margin:0; }}
svg {{ width:100%; height:auto; display:block; }} svg text {{ font-family:"LoewNA","FreeSerif",sans-serif; }}
h1 {{ font-size:19pt; color:#fff; background:linear-gradient(90deg,#0b2a6b,#1e56c0); border-radius:8px; margin:0 0 6px; padding:0 14px; }}
h2 {{ font-size:13pt; color:#0b2a6b; border-bottom:2px solid #f0a830; margin:8px 0 3px; }}
p {{ margin:2px 0 4px; }}
.nb {{ border:2px solid #1e56c0; border-radius:10px; background:#f7faff; padding:3px 12px; font-size:11.5pt; line-height:1.9; }}
.ayah {{ color:#0b5d3b; font-weight:700; }} .cite {{ color:#8a5a00; font-size:9.5pt; }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; }}
.bx {{ border-right:5px solid #f0a830; background:#fff8e6; border-radius:6px; padding:2px 10px; }}
.bx.b {{ border-right-color:#1e56c0; background:#eaf2ff; }} .bx.g {{ border-right-color:#1b8a5a; background:#eaf8f0; }}
table {{ width:100%; border-collapse:collapse; font-size:10.5pt; line-height:1.55; margin:3px 0 6px; }}
th,td {{ border:1px solid #99a; padding:1px 6px; text-align:center; }} th {{ background:#dfe9ff; color:#0b2a6b; }}
.q {{ font-weight:700; color:#7a1020; }} .a {{ margin:0 0 3px; padding-right:8px; border-right:3px solid #1b8a5a; }}
.mn {{ text-align:center; font-weight:700; color:#7a1020; background:#fff3f3; border:2px dashed #c0111f; border-radius:8px; padding:1px 6px; margin:6px 0 0; }}
.pb {{ page-break-before:always; }}
.cap {{ text-align:center; font-size:9.5pt; color:#556; margin:0; }}
</style></head><body>

<h1>🌞 المجموعة الشمسية — العلوم</h1>
<div class="nb">
<p>تدور الأرضُ حول الشمس في النظام الشمسي داخل مجرّة درب التبانة، وهي إحدى مليارات المجرّات التي يتكوّن منها الكون، وتُعَدُّ الشمسُ أكبرَ جرمٍ في نظامنا الشمسي. <b>فما هي المجموعة الشمسية؟ وما خصائص كواكبها؟</b>
قال الله تعالى: <span class="ayah">﴿إِنَّ فِي خَلْقِ السَّمَاوَاتِ وَالْأَرْضِ وَاخْتِلَافِ اللَّيْلِ وَالنَّهَارِ لَآيَاتٍ لِّأُولِي الْأَلْبَابِ﴾</span> <span class="cite">[آل عمران: 190]</span>.
<b>ما هو الكون؟</b> يُطلَق اسم الكون على المكان الذي يضمُّ مخلوقات الله سبحانه، ولهذا فالكون هو ما يحيط بنا من نجوم ومجرّات ومخلوقات فيه، ويحتوي على عدد هائل من المجرّات.
<b>المجرّات:</b> مجموعات هائلة الحجم من النجوم والكواكب والأقمار والمذنّبات، ومن أشهرها مجرّة درب التبانة، تنتمي إليها مجموعتنا الشمسية ومنها الأرض.</p>
</div>

<h2>رسم 1: ترتيب الكواكب الثمانية من الشمس</h2>
{ov}

<h2>الشرح المبسّط</h2>
<div class="two">
<div class="bx b"><b>الكون:</b> أكبر مكان؛ فيه كل ما خلق الله من نجوم ومجرّات وكواكب. <b>عنواننا فيه:</b> الأرض ← النظام الشمسي ← درب التبانة ← الكون.</div>
<div class="bx b"><b>المجرّة:</b> «مدينة» ضخمة من مئات المليارات من النجوم تربطها الجاذبية. مجرّتنا <b>درب التبانة</b> (تظهر كشريط أبيض في السماء الصافية).</div>
<div class="bx g"><b>المجموعة الشمسية:</b> الشمس + ثمانية كواكب وأقمارها والكويكبات والمذنّبات، تدور حول الشمس في مسارات تسمى <b>المدارات</b> بفضل جاذبيتها.</div>
<div class="bx g"><b>الشمس:</b> <b>نجم</b> يصنع الضوء والحرارة بنفسه، وفيه 99.86% من كتلة النظام الشمسي. يصل ضوؤها إلى الأرض في 8 دقائق و20 ثانية.</div>
</div>

<!-- ======== الصفحة 2 ======== -->
<h2 class="pb" style="margin-top:0">الكواكب الثمانية</h2>
{tbl}
<p class="cap">الكوكب جرم يدور حول الشمس ولا يصدر ضوءًا من نفسه (يعكس ضوء الشمس). الكواكب الصخرية قريبة من الشمس وصغيرة، والعملاقة بعيدة وكبيرة.</p>

<h2>حركات الأرض</h2>
<div class="two" style="grid-template-columns:1fr 1fr 1fr">
<div class="bx"><b>الدوران حول نفسها</b> (24 ساعة) ← <b>الليل والنهار</b>.</div>
<div class="bx"><b>الدوران حول الشمس</b> (365 يومًا وربع) ← <b>السنة</b>.</div>
<div class="bx"><b>ميل محورها</b> (23.5°) ← <b>الفصول الأربعة</b>.</div>
</div>
<div class="bx g" style="margin-top:5px"><b>وقفة مع الآية:</b> «اختلاف الليل والنهار» أي تعاقبهما، وهو من آثار دوران الأرض. و«أولو الألباب» هم أصحاب العقول السليمة الذين يتأمّلون في خلق الله فيزداد إيمانهم.</div>

<h2>أسئلة سريعة مع الحل</h2>
<div class="two">
<div><p class="q">1) ما الكون؟</p><div class="a">المكان الذي يضمّ مخلوقات الله من نجوم ومجرّات وغيرها.</div>
<p class="q">2) ما اسم مجرّتنا؟</p><div class="a">درب التبانة.</div>
<p class="q">3) ما أكبر جرم في المجموعة الشمسية؟</p><div class="a">الشمس (وهي نجم).</div>
<p class="q">4) كم كوكبًا في المجموعة الشمسية؟ وما ترتيب الأرض؟</p><div class="a">ثمانية، والأرض الثالثة.</div></div>
<div><p class="q">5) صح أم خطأ: الأرض مركز المجموعة الشمسية.</p><div class="a">خطأ، المركز هو الشمس.</div>
<p class="q">6) لماذا الزهرة أسخن من عطارد رغم أنها أبعد؟</p><div class="a">لغلافها الكثيف الذي يحبس الحرارة.</div>
<p class="q">7) ما سبب تعاقب الليل والنهار؟</p><div class="a">دوران الأرض حول نفسها.</div>
<p class="q">8) أكمل: أكبر الكواكب …… وأبعدها ……</p><div class="a">المشتري — نبتون.</div></div>
</div>
<div class="mn">لحفظ الترتيب: «عُمرُ زرعَ أرضًا مُثمرةً، مَعَ زهورٍ أنيقةٍ نضرة» (ع ز أ م م ز أ ن)</div>
</body></html>'''
open('/home/user/-/build/solar_short.html', 'w', encoding='utf-8').write(html)
