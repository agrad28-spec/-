# -*- coding: utf-8 -*-
import sys, os, re, json, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svglib as S
import icons as I
import cover as COV
from qdata import L as LQ, R as RQ, FINAL

try:
    import pyarabic.araby as araby
except Exception:  # PyArabic (github.com/linuxscout/pyarabic) is only used for text hygiene
    araby = None

B = os.path.dirname(os.path.abspath(__file__))
LET = ['أ', 'ب', 'ج', 'د', 'هـ']
ORD = ['الأول', 'الثاني', 'الثالث', 'الرابع', 'الخامس', 'السادس', 'السابع', 'الثامن', 'التاسع']
STATS = {'tatweel': 0, 'punct': 0, 'spaces': 0}

# ------------------------------------------------------------------ Arabic text hygiene (PyArabic + punctuation rules)
AR = re.compile(r'[؀-ۿ]')
def clean_text(seg):
    if not AR.search(seg):
        return seg
    out = seg
    if araby is not None and 'ـ' in out:
        STATS['tatweel'] += out.count('ـ')
        out = araby.strip_tatweel(out)
    for a, b in ((',', '،'), (';', '؛'), ('?', '؟')):
        if a in out:
            STATS['punct'] += out.count(a)
            out = out.replace(a, b)
    STATS['spaces'] += len(re.findall(r'(?<!;) {2,}', out))
    return re.sub(r'(?<!&nbsp;) {2,}', ' ', out)

def arabic_clean(html):
    return re.sub(r'(?<=>)([^<>]+)(?=<)', lambda m: clean_text(m.group(1)), html)

# ------------------------------------------------------------------ icons in text
ICON_MAP = {'🎯': 'target', '📖': 'book-open', '📚': 'library', '⭐': 'list-checks', '🧪': 'pencil', '✅': 'circle-check', '💡': 'lightbulb',
            '⚠️': 'triangle-alert', '🧴': 'triangle-alert', '🧭': 'compass', '🔭': 'compass', '📌': 'map-pin',
            '🦴': 'bone', '🐛': 'bug', '💧': 'droplets', '🌬️': 'wind', '⛰️': 'mountain'}
EMOJI_RE = re.compile('[\U0001F000-\U0001FAFF\u2600-\u2712\u2715-\u27BF\u2B00-\u2BFF\uFE0F\u200D\u2705]+')   # keeps U+2713/2714 (check mark)

def iconify(html):
    html = re.sub(r'(<div class="tip">)(?:🌱|🌳|💡)\s*', lambda m: m.group(1) + I.html('lightbulb') + ' ', html)
    for e, n in ICON_MAP.items():
        html = html.replace(e, I.html(n))
    return EMOJI_RE.sub('', html)   # any other emoji left in running text is dropped (figures use vector icons only)

# ------------------------------------------------------------------ tone: a more mature, academic register
def tone(html):
    html = html.replace('🎯 في هذه الوحدة سأتعلّم:', 'ما تتناوله هذه الوحدة')
    html = html.replace('🎯 سأتعلّم:', 'أهداف الدرس <span class="gl">بعد دراسة هذا الدرس ينبغي أن يكون الطالب قادرًا على:</span>')
    html = re.sub(r'<li>أن أ', '<li>أن ي', html)
    html = html.replace('📖 مفرداتي:', '📖 مصطلحات الدرس:').replace('⭐ خلاصتي', '⭐ خلاصة الدرس').replace('✅ أقيّم نفسي', '✅ تقويم الدرس')
    html = html.replace('<b>هل تعلم؟</b>', '<b>معلومة:</b>')
    def lh(m):
        num, title, unit = m.group(1), m.group(2), m.group(3)
        label = {'✓': 'مراجعة', '★': 'تقويم', 'أ': 'ملحق'}.get(num) or ('الدرس ' + ORD[int(num) - 1])
        words = title.split(' '); words[-1] = '<b>' + words[-1] + '</b>'
        return f'<div class="lh"><div class="lno">{label}</div><div class="lt">{" ".join(words)}</div><div class="lu">{unit}</div></div>'
    html = re.sub(r'<div class="lh"[^>]*><div class="ln"[^>]*>([^<]+)</div><div><div class="lt">([^<]+)</div><div class="ls">([^<]+)</div></div></div>', lh, html)
    rows = {'u1': ['earth', 'trees', 'building-2'], 'u2': ['bug', 'leaf', 'fish'], 'u3': ['mountain', 'sprout', 'tractor']}
    for u, names in rows.items():
        html = re.sub(r'(<div class="unitopen %s">.*?)<div class="big">[^<]*</div>' % u,
                      lambda m, n=names: m.group(1) + '<div class="uicons">' + ''.join(f'<span class="uic">{I.html(x, "ui")}</span>' for x in n) + '</div>', html, count=1, flags=re.S)
    html = re.sub(r'<h1>([^<]+)</h1>', lambda m: '<h1>' + ' '.join(m.group(1).split(' ')[:-1]) + ' <b>' + m.group(1).split(' ')[-1] + '</b></h1>', html)
    return html

# ------------------------------------------------------------------ questions (Arabic-safe: badges instead of "1." / "أ)")
def bd(x): return f'<span class="bd">{x}</span>'
def fill_blanks(q): return q.replace('____', '<span class="blank">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>')
def shown(items, k=1): return items[k:] + items[:k]
def perm(n):
    k = 1 if n <= 3 else n // 2
    return [(i + k) % n for i in range(n)]

def table_classify(cols, rows, student, group=False, multi=False, first='العنصر'):
    t = f'<table class="cls"><tr><th>{first}</th>' + ''.join(f'<th>{c}</th>' for c in cols) + ('<th>المجموعة</th>' if group else '') + '</tr>'
    for name, a in rows:
        grp = ''
        if group: marks = {a[0]}; grp = a[1]
        elif multi: marks = set(a)
        else: marks = {a}
        t += f'<tr><td class="rt">{name}</td>'
        for i in range(len(cols)):
            t += '<td>' + ('✓' if (not student and i in marks) else '') + '</td>'
        if group: t += '<td>' + ('' if student else grp) + '</td>'
        t += '</tr>'
    return t + '</table>'

def render_q(q, n, student=True):
    k = q['k']; head = f'<span class="qn">{n}</span>'
    if k == 'mcq':
        if student:
            opts = ''.join(f'<span class="opt">{bd(LET[i])} {o}</span>' for i, o in enumerate(q['o']))
            return f'<div class="qb">{head}<b>{q["q"]}</b><div class="opts">{opts}</div></div>'
        return f'<div class="ab">{head}{bd(LET[q["a"]])} {q["o"][q["a"]]}</div>'
    if k == 'tf':
        if student:
            return f'<div class="qb">{head}<b>{q["q"]}</b> <span class="tfbox">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>'
        s = 'صحيحة' if q['a'] else 'خاطئة'
        if not q['a'] and q.get('fix'): s += f' — التصحيح: {q["fix"]}'
        return f'<div class="ab">{head}{s}</div>'
    if k == 'fill':
        if student: return f'<div class="qb">{head}<b>{fill_blanks(q["q"])}</b></div>'
        return f'<div class="ab">{head}' + ' ، '.join(q['a']) + '</div>'
    if k == 'open':
        if student: return f'<div class="qb">{head}<b>{q["q"]}</b><div class="ln"></div><div class="ln"></div></div>'
        return f'<div class="ab">{head}{q["a"]}</div>'
    if k == 'match':
        pairs = q['pairs']; m = len(pairs); p = perm(m)
        if student:
            t = f'<div class="qb">{head}<b>{q["q"]}</b><table class="mt">'
            for i in range(m):
                t += f'<tr><td class="rt">{bd(i + 1)} {pairs[i][0]}</td><td class="bx">&nbsp;</td><td class="rt">{bd(LET[i])} {pairs[p[i]][1]}</td></tr>'
            return t + '</table><div class="hint">اكتب في الخانة الوسطى حرف العبارة المناسبة.</div></div>'
        out = [f'{bd(i + 1)} ← {bd(LET[p.index(i)])}' for i in range(m)]
        return f'<div class="ab">{head}' + ' &nbsp; '.join(out) + '</div>'
    if k == 'order':
        items = q['items']
        if student:
            li = ''.join(f'<span class="ob"><span class="sq"></span> {x}</span>' for x in shown(items))
            return f'<div class="qb">{head}<b>{q["q"]}</b><div class="opts">{li}</div></div>'
        return f'<div class="ab">{head}' + ' ← '.join(items) + '</div>'
    if k == 'classify':
        if student: return f'<div class="qb">{head}<b>{q["q"]}</b>' + table_classify(q['cols'], q['rows'], True) + '</div>'
        return f'<div class="ab">{head}' + ' ؛ '.join(f'{r[0]} ← {q["cols"][r[1]]}' for r in q['rows']) + '</div>'
    return ''

def render_activity(a):
    s = f'<div class="act"><div class="act-t">{I.html("pencil")} {a["title"]}</div><p>{a["text"]}</p>'
    k = a['kind']
    if k == 'classify':
        s += table_classify(a['cols'], a['rows'], True, group=a.get('with_group', False), multi=a.get('multi', False))
    elif k == 'order':
        s += '<div class="opts">' + ''.join(f'<span class="ob"><span class="sq"></span> {x}</span>' for x in shown(a['items'])) + '</div><div class="ln"></div>'
    elif k == 'table':
        cols = a['cols']; rows = a.get('fixed') or [None] * a['n']
        t = '<table class="cls"><tr>' + ''.join(f'<th>{c}</th>' for c in cols) + '</tr>'
        for r in rows:
            t += '<tr>' + (f'<td class="rt">{r}</td>' if r else '<td>&nbsp;</td>') + '<td>&nbsp;</td>' * (len(cols) - 1) + '</tr>'
        s += t + '</table>'
    elif k == 'match':
        pairs = a['pairs']; m = len(pairs); p = perm(m)
        t = '<table class="mt">'
        for i in range(m):
            t += f'<tr><td class="rt">{bd(i + 1)} {pairs[i][0]}</td><td class="bx">&nbsp;</td><td class="rt">{bd(LET[i])} {pairs[p[i]][1]}</td></tr>'
        s += '<b>الجزء الأول:</b>' + t + '</table>'
        s += '<b>الجزء الثاني: رتِّب</b><div class="opts">' + ''.join(f'<span class="ob"><span class="sq"></span> {x}</span>' for x in shown(a['order'])) + '</div>'
    elif k == 'lines':
        s += ''.join(f'<div class="ln">{bd(i + 1)}</div>' for i in range(a['n']))
    return s + '</div>'

def render_activity_key(a):
    k = a['kind']; s = f'<div class="ab"><b>{a["title"]}:</b> '
    if k == 'classify':
        if a.get('with_group'): s += ' ؛ '.join(f'{r[0]} ← {a["cols"][r[1][0]]} ({r[1][1]})' for r in a['rows'])
        elif a.get('multi'): s += ' ؛ '.join(f'{r[0]} ← ' + ' و'.join(a['cols'][i] for i in r[1]) for r in a['rows'])
        else: s += ' ؛ '.join(f'{r[0]} ← {a["cols"][r[1]]}' for r in a['rows'])
    elif k == 'order': s += ' ← '.join(a['items']) + ' — ' + a.get('note', '')
    elif k == 'match': s += ' ؛ '.join(f'{x} ← {y}' for x, y in a['pairs']) + ' — الترتيب: ' + ' ← '.join(a['order'])
    else: s += a.get('note', '')
    return s + '</div>'

def assess_student(n):
    d = LQ[n]
    s = f'<div class="assess"><h3>{I.html("circle-check")} تقويم الدرس</h3>' + render_activity(d['activity'])
    for i, q in enumerate(d['qs']): s += render_q(q, i + 1, True)
    return s + '</div>'

def review_student(qs): return ''.join(render_q(q, i + 1, True) for i, q in enumerate(qs))

# ------------------------------------------------------------------ glossary
GLOSS = [
 ('البيئة', 'المكان الذي يعيش فيه الكائن الحي ويجد فيه حاجاته.'), ('المكوّنات الحية', 'الإنسان والحيوان والنبات.'),
 ('المكوّنات غير الحية', 'الماء والهواء واليابسة.'), ('البيئة الطبيعية', 'مكان لم يتدخّل الإنسان في تكوينه.'),
 ('البيئة المشيّدة', 'مكان تدخّل الإنسان في تكوينه.'), ('المنتِج', 'كائن يصنع غذاءه بنفسه، مثل النبات.'),
 ('المستهلِك', 'كائن يتغذّى على غيره، مثل الحيوان والإنسان.'), ('الحيوان العاشب', 'حيوان يتغذّى على النباتات.'),
 ('الحيوان اللاحم', 'حيوان يتغذّى على حيوانات أخرى.'), ('السلسلة الغذائية', 'ترتيب الكائنات الحية حسب من يتغذّى على من.'),
 ('الموارد', 'ما نحصل عليه من البيئة لسدّ حاجاتنا.'), ('التلوّث', 'وجود مواد أو مؤثرات ضارة في البيئة.'),
 ('الضوضاء', 'أصوات مرتفعة مزعجة.'), ('الفقاريات', 'حيوانات لها عمود فقري.'), ('اللافقاريات', 'حيوانات ليس لها عمود فقري.'),
 ('الحشرات', 'لافقاريات من المفصليات، لها ثلاثة أزواج من الأرجل.'), ('النبات الزهري', 'نبات يكوّن أزهارًا.'),
 ('الفلقة', 'جزء من البذرة؛ قد تكون واحدة أو اثنتين.'), ('الصخور', 'كتل طبيعية صلبة تتكوّن منها اليابسة.'),
 ('المعدن', 'مادة تدخل في تركيب الصخور.'), ('الكثبان الرملية', 'تلال من الرمال تتكوّن حين تترسّب الرمال التي تنقلها الرياح.'),
 ('التربة', 'الوسط الذي تنبت فيه النباتات وتثبّت جذورها فيه.'), ('الدبال', 'بقايا نباتات وحيوانات ميتة تحلّلت.'),
 ('التصحّر', 'زحف الرمال إلى الأراضي الزراعية ودفنها.'), ('الدورة الزراعية', 'تغيير المحاصيل المزروعة وفق خطة زراعية، كزراعة البقوليات أو البرسيم.'),
]
def glossary_html():
    return '<table class="gl"><tr><th style="width:26%">المصطلح</th><th>المعنى</th></tr>' + ''.join(f'<tr><td class="rt"><b>{a}</b></td><td class="rt">{b}</td></tr>' for a, b in GLOSS) + '</table>'

# ------------------------------------------------------------------ figures
T, N, G = S.TEAL, S.NAVY, S.SOFT
def mk_svgs():
    D = {'COVER': COV.cover_svg(), 'ENV': S.env_panorama()}
    D['TREE_WL'] = S.tree('البيئة', [('بيئة مائية', N, 'waves', ['مياه مالحة: البحار', 'مياه عذبة: الأنهار']), ('بيئة يابسة', T, 'mountain', ['الصحاري', 'الغابات', 'المزارع'])], N)
    D['TREE_LN'] = S.tree('مكوّنات البيئة', [('مكوّنات حية', T, 'leaf', ['الإنسان', 'الحيوان', 'النبات']), ('مكوّنات غير حية', G, 'droplets', ['الماء', 'الهواء', 'اليابسة'])], N)
    D['FOODCHAIN'] = S.flow([dict(e='sprout', t='نبات', s='منتِج', c=T), dict(e='rabbit', t='أرنب', s='مستهلِك (عاشب)', c=N), dict(e='paw-print', t='ثعلب', s='مستهلِك (لاحم)', c=G)])
    D['PLANTNEEDS'] = S.plant_needs()
    D['RES'] = S.tree('موارد البيئة', [('موارد حية', T, 'trees', ['نباتية: الحبوب، القطن، الأخشاب', 'حيوانية: الأبقار، الأغنام، الأسماك']),
                                    ('موارد غير حية', N, 'droplets', ['الماء', 'الهواء', 'اليابسة: التربة والصخور والنفط'])], N)
    D['CLEANPOL'] = S.clean_vs_polluted()
    D['VERTTREE'] = S.tree('الحيوانات', [('لافقاريات', N, 'bug', ['الإسفنجيات', 'الديدان', 'المفصليات', 'الرخويات', 'شوكيات الجلد']),
                                      ('فقاريات', T, 'bone', ['الثدييات', 'الطيور', 'الزواحف', 'البرمائيات', 'الأسماك'])], N)
    D['INSECT'] = S.insect(); D['PLANT'] = S.plant(); D['SEEDS'] = S.seeds()
    D['PLANTTREE'] = S.tree('النباتات', [('حسب مكان العيش', N, 'map-pin', ['مائية: عذبة / مالحة', 'يابسة: غابات / صحارى']),
                                      ('حسب البذور', T, 'sprout', ['بذرية', 'لا بذرية']), ('حسب الأزهار', G, 'flower', ['زهرية', 'لازهرية'])], N)
    D['EARTH'] = S.earth()
    D['ROCKS1'] = S.flow([dict(e='flame', t='مواد منصهرة', c=N), dict(e='snowflake', t='تبرد وتتصلّب', c=T), dict(e='mountain', t='صخر ناري', s='مثال: الجرانيت', c=G)], H=190)
    D['ROCKS2'] = S.flow([dict(e='waves', t='فتات ورواسب', c=N), dict(e='layers', t='تراكم والتحام', c=T), dict(e='mountain', t='صخر رسوبي', s='مثال: الحجر الجيري', c=G)], H=190)
    D['ROCKS3'] = S.flow([dict(e='mountain', t='صخر سابق', c=N), dict(e='flame', t='حرارة وضغط', c=T), dict(e='gem', t='صخر متحوّل', s='مثال: الرخام', c=G)], H=190)
    D['ERODE'] = S.flow([dict(e='wind', t='تفتيت', s='الرياح والمياه تفتّت الصخور', c=N), dict(e='truck', t='نقل', s='تنقل الفتات', c=T), dict(e='mountain', t='ترسيب', s='يترسّب حين تقلّ السرعة', c=G)], H=215)
    D['DUNES'] = S.dunes(); D['SOIL'] = S.soil(); D['DESERT'] = S.desertification()
    D['DESERTFLOW'] = S.flow([dict(e='triangle-alert', t='المشكلة', s='التصحّر', c=N), dict(e='wind', t='أسبابه', s='رمال، رياح، جفاف، حرارة', c=T), dict(e='sprout', t='وسائل الحدّ منه', s='حلول متعدّدة', c=G)], H=215)
    return D

def icon_cards(items, cols=3):
    s = f'<div class="ec" style="grid-template-columns:repeat({cols},1fr)">'
    for names, t, d in items:
        s += '<div class="ecard"><div class="ico">' + ''.join(I.html(n, 'ci') for n in names.split()) + f'</div><b>{t}</b><br><span>{d}</span></div>'
    return s + '</div>'

CARDS = {
 'ANIM': icon_cards([
    ('paw-print', 'الثدييات', 'ترضع صغارها الحليب. يغطي أجسام كثير منها الشعر أو الصوف.'),
    ('bird', 'الطيور', 'يغطي أجسامها الريش، ولها مناقير، وتتكاثر بالبيض. منها ما يطير ومنها ما لا يطير.'),
    ('turtle', 'الزواحف', 'يغطي أجسام كثير منها حراشف، وتتكاثر بالبيض. بعضها يزحف لقصر أطرافه أو لعدم وجودها.'),
    ('waves', 'البرمائيات', 'تقضي جزءًا من حياتها في الماء وجزءًا على اليابسة. جلد الضفدع رطب، وله أطراف تساعده على السباحة، ويتكاثر بالبيض.'),
    ('fish', 'الأسماك', 'تعيش في الماء، وتتنفّس بالخياشيم، ولها زعانف تساعدها على الحركة، ويغطي أجسام كثير منها القشور.'),
    ('bug snail', 'اللافقاريات', 'ليس لها عمود فقري؛ منها الإسفنجيات والديدان والمفصليات (ومنها الحشرات) والرخويات وشوكيات الجلد.')], 3),
 'INSECTS': icon_cards([
    ('flower-2', 'النحل', 'نافع: يلقّح الأزهار وينتج العسل.'), ('worm', 'دودة القزّ', 'نافعة: تعطينا الحرير.'),
    ('bug', 'الذباب', 'ضارّ: قد ينقل الأمراض.'), ('bug', 'البعوض', 'ضارّ: قد ينقل الأمراض.'), ('wheat', 'الجراد', 'ضارّ: يتلف المحاصيل.')], 5),
 'RESCARDS': icon_cards([
    ('wheat', 'الحبوب', 'غذاء'), ('shirt', 'القطن', 'ملابس'), ('tree-deciduous', 'الأخشاب', 'أثاث وبناء'), ('leaf', 'المطاط', 'أدوات وإطارات'),
    ('milk', 'الأبقار', 'لحم وحليب'), ('paw-print', 'الأغنام', 'لحم وصوف'), ('footprints', 'الجمال', 'نقل وحمل الأمتعة'), ('egg', 'الدجاج', 'لحم وبيض'),
    ('fish', 'الأسماك', 'غذاء'), ('droplets', 'الماء', 'شرب وغسل وري'), ('mountain', 'الصخور', 'بناء وصناعة'), ('fuel', 'النفط والغاز', 'وقود')], 6),
 'POLL': icon_cards([('factory', 'تلوّث الهواء', 'الغبار والدخان واحتراق الوقود.'), ('droplets', 'تلوّث الماء', 'مخلّفات المصانع ومياه المجاري وتسرّب النفط.'),
    ('trash-2', 'تلوّث اليابسة', 'تراكم النفايات والقمامة.'), ('volume-2', 'الضوضاء', 'أصوات مرتفعة مزعجة: المنبّهات والآلات والمركبات.')], 4),
 'SOLUTIONS': icon_cards([
    ('sprout', 'زراعة الأراضي الصالحة', 'نزرع الأراضي الصالحة ونحسّنها.'), ('trees', 'مصدّات الرياح', 'أحزمة من الأشجار حول الحقول.'),
    ('shovel', 'السماد والدبال', 'نضيف الدبال أو السماد الطبيعي أو الحيواني، ونستخدم الأسمدة المناسبة.'), ('droplet', 'توفير مياه الري', 'نحفر الآبار عند الحاجة، ونستخدم الري الحديث كالتنقيط.'),
    ('sun', 'نباتات تتحمّل الجفاف', 'نزرع نباتات تتحمّل الجفاف والحرارة.'), ('droplets', 'غسل التربة المالحة', 'عند الحاجة وبالطريقة المناسبة.'),
    ('house', 'الزراعة المحمية', 'في الظروف المناسبة.'), ('recycle', 'الدورة الزراعية', 'زراعة البقوليات أو البرسيم وفق خطة زراعية.')], 4),
}

# ------------------------------------------------------------------ assemble
def load(name): return open(os.path.join(B, name), encoding='utf-8').read()

def build_book(pages=None):
    css = load('book.css')
    body = load('front.html') + load('unit1.html') + load('unit2.html') + load('unit3.html') + load('back.html')
    body = tone(body)
    body = re.sub(r'\{\{IC:([\w-]+)\}\}', lambda m: I.html(m.group(1)), body)
    for k, v in mk_svgs().items(): body = body.replace('{{SVG_' + k + '}}', v)
    for k, v in CARDS.items(): body = body.replace('{{CARDS_' + k + '}}', v)
    for n in LQ: body = body.replace('{{ASSESS_%d}}' % n, assess_student(n))
    for u in (1, 2, 3): body = body.replace('{{REVIEW_%d}}' % u, review_student(RQ[u]))
    body = body.replace('{{FINAL}}', review_student(FINAL)).replace('{{GLOSSARY}}', glossary_html())
    body = iconify(body)
    for key in re.findall(r'\{\{PG:(\w+)\}\}', body):
        body = body.replace('{{PG:%s}}' % key, str((pages or {}).get(key, '—')))
    body = arabic_clean(body)
    html = f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>كتاب العلوم — السنة الثانية</title><style>{css}</style></head><body>{body}</body></html>'
    open(os.path.join(B, 'book.html'), 'w', encoding='utf-8').write(html)

REVIEW_LIST = [
 ('تسمية المستوى', 'كُتب على الغلاف «السنة الثانية» بطلب المركز. محتوى الكتاب مبني على وثيقة تنقية كتاب العلوم للصف الرابع الابتدائي؛ فليُراجَع مستوى الصياغة والأسئلة بما يناسب طلاب السنة الثانية.'),
 ('الخط', 'استُعمل خط «ثمانية» (Thmanyah Sans) من مستودع موقع البركة. تُراجَع رخصة الخط قبل النشر العام.'),
 ('الشعار والهوية', 'الشعار الرسمي والشعار المختصر وألوان الهوية (البترولي والأزرق الداكن) من مستودع منصة المعرفة. اسم الجهة في الشعار «للتأصيل الشرعي» بينما يظهر في بعض ملفات الهوية الأخرى «للتأصيل العلمي»؛ يؤكَّد الاسم المعتمد.'),
 ('الرسوم والأيقونات', 'الرسوم متجهة بسيطة بألوان الهوية، والأيقونات من مكتبة Lucide (رخصة ISC). تُستبدل بصور واقعية أو رسوم علمية دقيقة إن رغب المركز.'),
 ('آيات قرآنية', 'أُضيفت ثلاث آيات موجزة في افتتاح الوحدات (الأنعام: 99، النور: 45، الرعد: 3) لأن نص الكتاب الأصلي لم يكن متاحًا. تُراجَع كتابتها وضبطها ومراجعها.'),
 ('أمثلة اللافقاريات', 'ذُكرت المجموعات كما في الوثيقة، وأُضيفت أيقونات توضيحية (حشرة، حلزون) من خارج المصدر، وتحتاج موافقة المؤلف.'),
 ('تصنيف النباتات اللازهرية', 'ذكرت الوثيقة الطحالب والحزازيات والسرخسيات ضمن النباتات اللازهرية مع التنبيه على ضبط المصطلحات. وردت كما هي مع عبارة «من أمثلتها» وتحتاج مراجعة علمية.'),
 ('عبارة «المصدر الوحيد للغذاء»', 'لم تُستخدم. عُوّضت بأن النباتات منتِجات، والحيوانات والإنسان مستهلِكون في السلاسل المبسّطة.'),
 ('التلوّث والاحتباس الحراري', 'حُذف الحديث عن الاحتباس الحراري، واكتُفي بأن احتراق الوقود ينتج دخانًا وملوِّثات، إلى أن يُبسَّط الموضوع علميًا ويُراجَع.'),
 ('الغبار والجهاز التنفسي', 'لم يُنقل أي إيحاء بأن قطعة قماش مبلّلة تكفي. أُضيف تنبيه عام (البقاء داخل المبنى وقت العواصف الترابية واستعمال كمامة عند الحاجة وبتوجيه الكبار) وهو إضافة تحتاج موافقة.'),
 ('المبيدات', 'أُبرزت تعليمات السلامة: الابتعاد عن أماكن الرش، وعدم لمس المبيد، وغسل الفواكه والخضراوات.'),
 ('وصف مجموعات الفقاريات', 'استُعملت عبارات مثل «كثير منها» لتجنّب تعميم صفة بعض الأنواع على المجموعة كلها (الشعر/الصوف، الحراشف، القشور).'),
 ('الدورة الزراعية ووسائل التصحّر', 'عبارات الغاية من كل وسيلة (مثل: المصدّات تحمي الحقول من الرياح والرمال) بصياغة تعليمية قريبة من المصدر؛ يراجعها المؤلف.'),
 ('التربة', 'جدول مقارن واحد لأنواع التربة الثلاثة، مع إعادة تحرير العبارة المضطربة في الخلاصة. يُطابَق مع النص الأصلي.'),
 ('الأسئلة والأنشطة', 'أسئلة التقويم ومراجعات الوحدات والمراجعة الشاملة جديدة، وُضعت بحسب «بنك الأنشطة» في الوثيقة. الإجابات في هذا الدليل فقط.'),
 ('الاحتياج إلى النص الأصلي', 'لم يكن الكتاب الأصلي متاحًا؛ بُني الكتاب على وثيقة التنقية وحدها. تُدقَّق الأمثلة المحلية عند الرجوع إلى الأصل.'),
 ('تنسيق النص العربي', 'اتجاه الصفحات من اليمين إلى اليسار، والترقيم بشارات غير مرتبطة بعلامات ترقيم (لتفادي انقلاب النقطة والقوس)، وتنقية النص بأداة PyArabic (إزالة التطويل وتوحيد علامات الترقيم العربية).'),
 ('تجارب الأنشطة', 'أنشطة مراقبة التربة والبذور بإشراف المعلم وبعد غسل اليدين، دون مواد خطرة.'),
]

def build_guide():
    css = load('book.css')
    h = '<div class="gcover"><h1>دليل إجابات <b>المعلم</b></h1><p>كتاب العلوم — السنة الثانية — الفصل الدراسي الأول</p><p class="cap">للمعلم والمراجع فقط، ولا يوزَّع على الطلاب.</p></div>'
    h += '<h2 class="gh2 pb">أولًا: إجابات أسئلة الدروس</h2>'
    titles = {1: 'البيئة ومكوّناتها', 2: 'العلاقة بين مكوّنات البيئة', 3: 'موارد البيئة', 4: 'تلوّث البيئة', 5: 'الحيوانات', 6: 'النباتات', 7: 'الأرض والصخور', 8: 'التربة', 9: 'الزراعة ومكافحة التصحّر'}
    for n in range(1, 10):
        d = LQ[n]
        h += f'<h3 class="gh">الدرس {ORD[n-1]}: {titles[n]}</h3>' + render_activity_key(d['activity'])
        for i, q in enumerate(d['qs']): h += render_q(q, i + 1, False)
    h += '<h2 class="gh2 pb">ثانيًا: إجابات مراجعات الوحدات</h2>'
    for u in (1, 2, 3):
        h += f'<h3 class="gh">مراجعة الوحدة {["الأولى", "الثانية", "الثالثة"][u-1]}</h3>'
        for i, q in enumerate(RQ[u]): h += render_q(q, i + 1, False)
    h += '<h3 class="gh">المراجعة الشاملة</h3>'
    for i, q in enumerate(FINAL): h += render_q(q, i + 1, False)
    h += '<h2 class="gh2 pb">ثالثًا: قائمة المراجعة العلمية (للمؤلف قبل الطباعة)</h2><p>كل موضع أُضيف فيه شيء أو أُعيدت صياغته أو تُرك فيه قرار للمؤلف. لم تُدخَل أي معلومة من خارج الوثيقة على أنها من المصدر.</p><ol class="rl">'
    for t, d in REVIEW_LIST: h += f'<li><b>{t}:</b> {d}</li>'
    h += '</ol>'
    h = arabic_clean(h)
    html = f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>دليل إجابات المعلم</title><style>{css}</style></head><body class="guide u1">{h}</body></html>'
    open(os.path.join(B, 'guide.html'), 'w', encoding='utf-8').write(html)

if __name__ == '__main__':
    pages = json.load(open(os.path.join(B, 'pages.json'))) if os.path.exists(os.path.join(B, 'pages.json')) else None
    build_book(pages); build_guide()
    print('built', STATS)
