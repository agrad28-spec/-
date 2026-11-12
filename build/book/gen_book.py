# -*- coding: utf-8 -*-
import sys, os, re, subprocess, json, base64
sys.path.insert(0, os.path.dirname(__file__))
import svglib as S
import cover as COV
from qdata import L as LQ, R as RQ, FINAL

B = os.path.dirname(os.path.abspath(__file__))
LET = ['أ', 'ب', 'ج', 'د', 'هـ']
UNIT_COL = {1: '#2b8a3e', 2: '#e8590c', 3: '#8d5a2b'}

def esc(s): return s

def dots(n=30): return '<span class="dots">' + '.' * n + '</span>'

def fill_blanks(q):
    return q.replace('____', '<span class="blank">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>')

def shown(items, k=1):
    return items[k:] + items[:k]

def perm(n):
    k = 1 if n <= 3 else n // 2
    return [(i + k) % n for i in range(n)]


# ------------------------------------------------------------------ brand: icons (from the platform's icon set, 24x24 stroke 1.75) & palette
ICON_PATHS = {
  'arrow': "M5 12h14M13 6l6 6-6 6",
  'book': "M12 6.5C10.5 5 8 4.5 4 4.5v13c4 0 6.5.5 8 2 1.5-1.5 4-2 8-2v-13c-4 0-6.5.5-8 2zM12 6.5v13",
  'star': "m12 3.5 2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z",
  'edit': "M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4",
  'check': "M20 6 9 17l-5-5",
  'sun': "M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41",
  'alert': "M12 3 2 20h20zM12 10v4M12 17h.01",
  'globe': "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18M3 12h18M12 3c2.5 2.7 3.5 5.7 3.5 9s-1 6.3-3.5 9c-2.5-2.7-3.5-5.7-3.5-9s1-6.3 3.5-9",
  'mapPin': "M12 21s-7-6.2-7-11.5a7 7 0 1 1 14 0C19 14.8 12 21 12 21M12 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5",
}
def ic(name):
    return ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{ICON_PATHS[name]}"/></svg>')

EMOJI_ICON = [('🎯', 'arrow'), ('📖', 'book'), ('📚', 'book'), ('⭐', 'star'), ('🧪', 'edit'), ('✅', 'check'), ('💡', 'sun'),
              ('⚠️', 'alert'), ('🧴', 'alert'), ('🧭', 'globe'), ('🔭', 'globe'), ('📌', 'mapPin')]

def iconify(html):
    html = re.sub(r'(<div class="tip">)(?:🌱|🌳|💡)\s*', lambda m: m.group(1) + ic('sun') + ' ', html)
    for e, n in EMOJI_ICON:
        html = html.replace(e, ic(n))
    return html

COLOR_MAP = {  # recolor diagrams to the center's palette (teal #0A5F6A, navy #054473, greys); status colors stay for warnings only
 '#2b8a3e': '#0a5f6a', '#1c7ed6': '#054473', '#e8590c': '#3e8086', '#868e96': '#5d656e', '#c92a2a': '#054473', '#8d5a2b': '#5d656e',
 '#c08a2b': '#5d656e', '#7048e8': '#054473', '#495057': '#303336', '#0b2a6b': '#054473',
 '#ebfbee': '#e8f1f2', '#fff4e6': '#f3eeec', '#fff5f5': '#e6eef5', '#e7f5ff': '#e8f1f2', '#fff9db': '#f3eeec', '#fdf0e0': '#f3eeec',
 '#f1f3f5': '#eeeded', '#f3f0ff': '#e6eef5', '#fafbfc': '#ffffff',
}
def brandify(svg):
    for a, b in COLOR_MAP.items():
        svg = svg.replace(a, b)
    return svg

# ------------------------------------------------------------------ question rendering
def table_classify(cols, rows, student, group=False, multi=False, first='العنصر'):
    t = f'<table class="cls"><tr><th>{first}</th>' + ''.join(f'<th>{c}</th>' for c in cols) + ('<th>المجموعة</th>' if group else '') + '</tr>'
    for r in rows:
        name, a = r
        t += f'<tr><td class="rt">{name}</td>'
        marks = set()
        grp = ''
        if group: marks = {a[0]}; grp = a[1]
        elif multi: marks = set(a)
        else: marks = {a}
        for i in range(len(cols)):
            t += '<td>' + ('✓' if (not student and i in marks) else '') + '</td>'
        if group: t += '<td>' + ('' if student else grp) + '</td>'
        t += '</tr>'
    return t + '</table>'

def render_q(q, n, student=True):
    k = q['k']
    head = f'<span class="qn">{n}</span>'
    if k == 'mcq':
        if student:
            opts = ' &nbsp; '.join(f'<span class="opt">{LET[i]}) {o}</span>' for i, o in enumerate(q['o']))
            return f'<div class="qb">{head}<b>{q["q"]}</b><div class="opts">{opts}</div></div>'
        return f'<div class="ab">{head}{LET[q["a"]]}) {q["o"][q["a"]]}</div>'
    if k == 'tf':
        if student:
            return f'<div class="qb">{head}<b>{q["q"]}</b> <span class="tfbox">( &nbsp;&nbsp;&nbsp; )</span></div>'
        s = 'صح ✓' if q['a'] else 'خطأ ✗'
        if not q['a'] and q.get('fix'): s += f' — التصحيح: {q["fix"]}'
        return f'<div class="ab">{head}{s}</div>'
    if k == 'fill':
        if student:
            return f'<div class="qb">{head}<b>{fill_blanks(q["q"])}</b></div>'
        return f'<div class="ab">{head}' + ' ، '.join(q['a']) + '</div>'
    if k == 'open':
        if student:
            return f'<div class="qb">{head}<b>{q["q"]}</b><div class="ln"></div><div class="ln"></div></div>'
        return f'<div class="ab">{head}{q["a"]}</div>'
    if k == 'match':
        pairs = q['pairs']; m = len(pairs); p = perm(m)
        if student:
            t = f'<div class="qb">{head}<b>{q["q"]}</b><table class="mt">'
            for i in range(m):
                t += f'<tr><td class="rt">{i+1}) {pairs[i][0]}</td><td class="bx">( &nbsp;&nbsp; )</td><td class="rt">{LET[i]}) {pairs[p[i]][1]}</td></tr>'
            return t + '</table><div class="hint">اكتب بين القوسين حرف العبارة المناسبة.</div></div>'
        # answer: item i matches description that is at position j where p[j]==i
        out = []
        for i in range(m):
            j = p.index(i)
            out.append(f'{i+1} ← {LET[j]}')
        return f'<div class="ab">{head}' + ' ، '.join(out) + ' &nbsp;(' + ' ؛ '.join(f'{a} = {b}' for a, b in pairs) + ')</div>'
    if k == 'order':
        items = q['items']; sh = shown(items)
        if student:
            li = ''.join(f'<span class="ob">( &nbsp; ) {x}</span>' for x in sh)
            return f'<div class="qb">{head}<b>{q["q"]}</b><div class="opts">{li}</div></div>'
        return f'<div class="ab">{head}' + ' ← '.join(items) + '</div>'
    if k == 'classify':
        if student:
            return f'<div class="qb">{head}<b>{q["q"]}</b>' + table_classify(q['cols'], q['rows'], True) + '</div>'
        return f'<div class="ab">{head}' + ' ؛ '.join(f'{r[0]} ← {q["cols"][r[1]]}' for r in q['rows']) + '</div>'
    return ''

def render_activity(a, student=True):
    s = f'<div class="act"><div class="act-t">🧪 {a["title"]}</div><p>{a["text"]}</p>'
    k = a['kind']
    if k == 'classify':
        s += table_classify(a['cols'], a['rows'], student, group=a.get('with_group', False), multi=a.get('multi', False))
    elif k == 'order':
        if student:
            s += '<div class="opts">' + ''.join(f'<span class="ob">( &nbsp; ) {x}</span>' for x in shown(a['items'])) + '</div>'
            s += '<div class="ln"></div>'
        else:
            s += '<div class="ab">' + ' ← '.join(a['items']) + '<br>' + a.get('note', '') + '</div>'
    elif k == 'table':
        cols = a['cols']; fixed = a.get('fixed')
        t = '<table class="cls"><tr>' + ''.join(f'<th>{c}</th>' for c in cols) + '</tr>'
        rows = fixed if fixed else [None] * a['n']
        for r in rows:
            t += '<tr>' + (f'<td class="rt">{r}</td>' if r else '<td>&nbsp;</td>') + '<td>&nbsp;</td>' * (len(cols) - 1) + '</tr>'
        s += t + '</table>'
    elif k == 'match':
        pairs = a['pairs']; m = len(pairs); p = perm(m)
        t = '<table class="mt">'
        for i in range(m):
            t += f'<tr><td class="rt">{i+1}) {pairs[i][0]}</td><td class="bx">( &nbsp;&nbsp; )</td><td class="rt">{LET[i]}) {pairs[p[i]][1]}</td></tr>'
        s += '<b>(أ)</b>' + t + '</table>'
        s += '<b>(ب) رتِّب:</b><div class="opts">' + ''.join(f'<span class="ob">( &nbsp; ) {x}</span>' for x in shown(a['order'])) + '</div>'
    elif k == 'lines':
        s += ''.join(f'<div class="ln">{i+1}-</div>' for i in range(a['n']))
    return s + '</div>'

def render_activity_key(a):
    k = a['kind']; s = f'<div class="ab"><b>{a["title"]}:</b> '
    if k == 'classify':
        if a.get('with_group'):
            s += ' ؛ '.join(f'{r[0]} ← {a["cols"][r[1][0]]} ({r[1][1]})' for r in a['rows'])
        elif a.get('multi'):
            s += ' ؛ '.join(f'{r[0]} ← ' + ' و'.join(a['cols'][i] for i in r[1]) for r in a['rows'])
        else:
            s += ' ؛ '.join(f'{r[0]} ← {a["cols"][r[1]]}' for r in a['rows'])
    elif k == 'order':
        s += ' ← '.join(a['items']) + ' — ' + a.get('note', '')
    elif k == 'match':
        p = perm(len(a['pairs']))
        s += ' ؛ '.join(f'{x} ← {y}' for x, y in a['pairs']) + ' — الترتيب: ' + ' ← '.join(a['order'])
    else:
        s += a.get('note', '')
    return s + '</div>'

def assess_student(n):
    d = LQ[n]
    s = f'<div class="assess"><h3>✅ أقيّم نفسي</h3>'
    s += render_activity(d['activity'], True)
    for i, q in enumerate(d['qs']):
        s += render_q(q, i + 1, True)
    return s + '</div>'

def review_student(qs, title='مراجعة الوحدة', start=1):
    s = ''
    for i, q in enumerate(qs):
        s += render_q(q, i + start, True)
    return s

# ------------------------------------------------------------------ glossary
GLOSS = [
 ('البيئة', 'المكان الذي يعيش فيه الكائن الحي ويجد فيه حاجاته.'),
 ('المكوّنات الحية', 'الإنسان والحيوان والنبات.'),
 ('المكوّنات غير الحية', 'الماء والهواء واليابسة.'),
 ('البيئة الطبيعية', 'مكان لم يتدخّل الإنسان في تكوينه.'),
 ('البيئة المشيّدة', 'مكان تدخّل الإنسان في تكوينه.'),
 ('المنتِج', 'كائن يصنع غذاءه بنفسه، مثل النبات.'),
 ('المستهلِك', 'كائن يتغذّى على غيره، مثل الحيوان والإنسان.'),
 ('الحيوان العاشب', 'حيوان يتغذّى على النباتات.'),
 ('الحيوان اللاحم', 'حيوان يتغذّى على حيوانات أخرى.'),
 ('السلسلة الغذائية', 'ترتيب الكائنات الحية حسب من يتغذّى على من.'),
 ('الموارد', 'ما نحصل عليه من البيئة لسدّ حاجاتنا.'),
 ('التلوّث', 'وجود مواد أو مؤثرات ضارة في البيئة.'),
 ('الضوضاء', 'أصوات مرتفعة مزعجة.'),
 ('الفقاريات', 'حيوانات لها عمود فقري.'),
 ('اللافقاريات', 'حيوانات ليس لها عمود فقري.'),
 ('الحشرات', 'لافقاريات من المفصليات، لها ثلاثة أزواج من الأرجل.'),
 ('النبات الزهري', 'نبات يكوّن أزهارًا.'),
 ('الفلقة', 'جزء من البذرة؛ قد تكون واحدة أو اثنتين.'),
 ('الصخور', 'كتل طبيعية صلبة تتكوّن منها اليابسة.'),
 ('المعدن', 'مادة تدخل في تركيب الصخور.'),
 ('الكثبان الرملية', 'تلال من الرمال تتكوّن حين تترسّب الرمال التي تنقلها الرياح.'),
 ('التربة', 'الوسط الذي تنبت فيه النباتات وتثبّت جذورها فيه.'),
 ('الدبال', 'بقايا نباتات وحيوانات ميتة تحلّلت.'),
 ('التصحّر', 'زحف الرمال إلى الأراضي الزراعية ودفنها.'),
 ('الدورة الزراعية', 'تغيير المحاصيل المزروعة وفق خطة زراعية، كزراعة البقوليات أو البرسيم.'),
]

def glossary_html():
    return '<table class="gl"><tr><th style="width:26%">المصطلح</th><th>معناه</th></tr>' + ''.join(f'<tr><td class="rt"><b>{a}</b></td><td class="rt">{b}</td></tr>' for a, b in GLOSS) + '</table>'

# ------------------------------------------------------------------ SVG placeholders
def mk_svgs():
    D = {}
    D['COVER'] = COV.cover_svg()
    D['ENV'] = S.env_panorama()
    D['TREE_WL'] = S.tree('البيئة', [('بيئة مائية', '#1c7ed6', '🌊', ['مياه مالحة: البحار', 'مياه عذبة: الأنهار']),
                                    ('بيئة يابسة', '#2b8a3e', '⛰️', ['الصحاري', 'الغابات', 'المزارع'])], '#0b2a6b')
    D['TREE_LN'] = S.tree('مكوّنات البيئة', [('مكوّنات حية', '#2b8a3e', '🌱', ['الإنسان', 'الحيوان', 'النبات']),
                                           ('مكوّنات غير حية', '#868e96', '💧', ['الماء', 'الهواء', 'اليابسة'])], '#0b2a6b')
    D['FOODCHAIN'] = S.flow([dict(e='🌿', t='نبات', s='منتِج', c='#2b8a3e', f='#ebfbee'), dict(e='🐇', t='أرنب', s='مستهلِك (عاشب)', c='#e8590c', f='#fff4e6'),
                             dict(e='🦊', t='ثعلب', s='مستهلِك (لاحم)', c='#c92a2a', f='#fff5f5')])
    D['PLANTNEEDS'] = S.plant_needs()
    D['RES'] = S.tree('موارد البيئة', [('موارد حية', '#2b8a3e', '🌳', ['نباتية: الحبوب، القطن، الأخشاب', 'حيوانية: الأبقار، الأغنام، الأسماك']),
                                    ('موارد غير حية', '#1c7ed6', '💧', ['الماء', 'الهواء', 'اليابسة: التربة والصخور والنفط'])], '#0b2a6b')
    D['CLEANPOL'] = S.clean_vs_polluted()
    D['VERTTREE'] = S.tree('الحيوانات', [('لافقاريات', '#e8590c', '🐛', ['الإسفنجيات', 'الديدان', 'المفصليات', 'الرخويات', 'شوكيات الجلد']),
                                      ('فقاريات', '#2b8a3e', '🐄', ['الثدييات', 'الطيور', 'الزواحف', 'البرمائيات', 'الأسماك'])], '#0b2a6b')
    D['INSECT'] = S.insect()
    D['PLANT'] = S.plant()
    D['SEEDS'] = S.seeds()
    D['PLANTTREE'] = S.tree('النباتات', [('حسب مكان العيش', '#1c7ed6', '📍', ['مائية: عذبة / مالحة', 'يابسة: غابات / صحارى']),
                                      ('حسب البذور', '#e8590c', '🌰', ['بذرية', 'لا بذرية']),
                                      ('حسب الأزهار', '#d6336c', '🌸', ['زهرية', 'لازهرية'])], '#0b2a6b')
    D['EARTH'] = S.earth()
    D['ROCKS1'] = S.flow([dict(e='🌋', t='مواد منصهرة', c='#c92a2a', f='#fff5f5'), dict(e='❄️', t='تبرد وتتصلّب', c='#1c7ed6', f='#e7f5ff'), dict(e='🪨', t='صخر ناري', s='مثال: الجرانيت', c='#495057', f='#f1f3f5')], H=190)
    D['ROCKS2'] = S.flow([dict(e='🏖️', t='فتات ورواسب', c='#c08a2b', f='#fff9db'), dict(e='🧱', t='تراكم والتحام', c='#8d5a2b', f='#fdf0e0'), dict(e='🪨', t='صخر رسوبي', s='مثال: الحجر الجيري', c='#495057', f='#f1f3f5')], H=190)
    D['ROCKS3'] = S.flow([dict(e='🪨', t='صخر سابق', c='#495057', f='#f1f3f5'), dict(e='🔥', t='حرارة وضغط', c='#e8590c', f='#fff4e6'), dict(e='⬜', t='صخر متحوّل', s='مثال: الرخام', c='#7048e8', f='#f3f0ff')], H=190)
    D['ERODE'] = S.flow([dict(e='💨🌊', t='تفتيت', s='الرياح والمياه تفتّت الصخور', c='#c92a2a', f='#fff5f5'), dict(e='🚚', t='نقل', s='تنقل الفتات', c='#1c7ed6', f='#e7f5ff'), dict(e='⛰️', t='ترسيب', s='يترسّب حين تقلّ السرعة', c='#8d5a2b', f='#fdf0e0')], H=215)
    D['DUNES'] = S.dunes()
    D['SOIL'] = S.soil()
    D['DESERT'] = S.desertification()
    D['DESERTFLOW'] = S.flow([dict(e='🏜️', t='المشكلة', s='التصحّر', c='#c92a2a', f='#fff5f5'), dict(e='💨', t='أسبابه', s='رمال، رياح، جفاف، حرارة', c='#e8590c', f='#fff4e6'), dict(e='🌱', t='وسائل الحدّ منه', s='حلول متعدّدة', c='#2b8a3e', f='#ebfbee')], H=215)
    for k in ('ENV', 'TREE_WL', 'TREE_LN', 'FOODCHAIN', 'RES', 'VERTTREE', 'PLANTTREE', 'ROCKS1', 'ROCKS2', 'ROCKS3', 'ERODE', 'DESERTFLOW'):
        D[k] = brandify(D[k])
    return D

# ------------------------------------------------------------------ cards helper (HTML)
def emoji_cards(items, cols=3):
    s = f'<div class="ec" style="grid-template-columns:repeat({cols},1fr)">'
    for e, t, d in items:
        s += f'<div class="ecard"><div class="ee">{e}</div><b>{t}</b><br><span>{d}</span></div>'
    return s + '</div>'

CARDS = {}
CARDS['ANIM'] = emoji_cards([
    ('🐄🐑🐪', 'الثدييات', 'ترضع صغارها الحليب. يغطي أجسام كثير منها الشعر أو الصوف.'),
    ('🐔🦅', 'الطيور', 'يغطي أجسامها الريش، ولها مناقير، وتتكاثر بالبيض. منها ما يطير ومنها ما لا يطير.'),
    ('🐍🐊🦎🐢', 'الزواحف', 'يغطي أجسام كثير منها حراشف، وتتكاثر بالبيض. بعضها يزحف لقصر أطرافه أو لعدم وجودها.'),
    ('🐸', 'البرمائيات', 'تقضي جزءًا من حياتها في الماء وجزءًا على اليابسة. جلد الضفدع رطب، وله أطراف تساعده على السباحة، ويتكاثر بالبيض.'),
    ('🐟🐠', 'الأسماك', 'تعيش في الماء، وتتنفّس بالخياشيم، ولها زعانف تساعدها على الحركة، ويغطي أجسام كثير منها القشور.'),
    ('🐝🪱🦀🐌', 'اللافقاريات', 'ليس لها عمود فقري؛ منها الإسفنجيات والديدان والمفصليات (ومنها الحشرات) والرخويات وشوكيات الجلد.'),
], 3)
CARDS['INSECTS'] = emoji_cards([
    ('🐝', 'النحل', 'نافع: يلقّح الأزهار وينتج العسل.'), ('🐛', 'دودة القزّ', 'نافعة: تعطينا الحرير.'),
    ('🪰', 'الذباب', 'ضارّ: قد ينقل الأمراض.'), ('🦟', 'البعوض', 'ضارّ: قد ينقل الأمراض.'), ('🦗', 'الجراد', 'ضارّ: يتلف المحاصيل.')], 5)
CARDS['RESCARDS'] = emoji_cards([
    ('🌾', 'الحبوب', 'غذاء'), ('🌿', 'القطن', 'ملابس'), ('🪵', 'الأخشاب', 'أثاث وبناء'), ('🛞', 'المطاط', 'إطارات وأدوات'),
    ('🐄', 'الأبقار', 'لحم وحليب'), ('🐑', 'الأغنام', 'لحم وصوف'), ('🐪', 'الجمال', 'نقل وحمل الأمتعة'), ('🐔', 'الدجاج', 'لحم وبيض'),
    ('🐟', 'الأسماك', 'غذاء'), ('💧', 'الماء', 'شرب وغسل وري'), ('🪨', 'الصخور', 'بناء وصناعة'), ('🛢️', 'النفط والغاز', 'وقود')], 6)
CARDS['POLL'] = emoji_cards([
    ('🏭🚗', 'تلوّث الهواء', 'الغبار والدخان واحتراق الوقود.'), ('🛢️🚰', 'تلوّث الماء', 'مخلّفات المصانع ومياه المجاري وتسرّب النفط.'),
    ('🗑️', 'تلوّث اليابسة', 'تراكم النفايات والقمامة.'), ('📢', 'الضوضاء', 'أصوات مرتفعة مزعجة: المنبّهات والآلات والمركبات.')], 4)
CARDS['SOLUTIONS'] = emoji_cards([
    ('🌱', 'زراعة الأراضي الصالحة', 'نزرع الأراضي الصالحة ونحسّنها.'), ('🌳🌳', 'مصدّات الرياح', 'أحزمة من الأشجار حول الحقول.'),
    ('🐄🌾', 'السماد والدبال', 'نضيف الدبال أو السماد الطبيعي أو الحيواني، ونستخدم الأسمدة المناسبة.'), ('⛲', 'توفير مياه الري', 'نحفر الآبار عند الحاجة، ونستخدم الري الحديث كالتنقيط.'),
    ('🌵', 'نباتات تتحمّل الجفاف', 'نزرع نباتات تتحمّل الجفاف والحرارة.'), ('🚿', 'غسل التربة المالحة', 'عند الحاجة وبالطريقة المناسبة.'),
    ('🏠🌿', 'الزراعة المحمية', 'في الظروف المناسبة.'), ('🔄', 'الدورة الزراعية', 'زراعة البقوليات أو البرسيم وفق خطة زراعية.')], 4)

# ------------------------------------------------------------------ assemble
def load(name): return open(os.path.join(B, name), encoding='utf-8').read()

def write_footer_svg():
    b64 = base64.b64encode(open(os.path.join(B, 'assets', 'emblem.png'), 'rb').read()).decode()
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="52" height="37" viewBox="0 0 52 37">'
           f'<image width="52" height="37" xlink:href="data:image/png;base64,{b64}"/></svg>')
    open(os.path.join(B, 'assets', 'footer_emblem.svg'), 'w').write(svg)

def build_book(pages=None):
    write_footer_svg()
    css = load('book.css')
    body = load('front.html') + load('unit1.html') + load('unit2.html') + load('unit3.html') + load('back.html')
    svgs = mk_svgs()
    for k, v in svgs.items():
        body = body.replace('{{SVG_' + k + '}}', v)
    for k, v in CARDS.items():
        body = body.replace('{{CARDS_' + k + '}}', v)
    for n in LQ:
        body = body.replace('{{ASSESS_%d}}' % n, assess_student(n))
    for u in (1, 2, 3):
        body = body.replace('{{REVIEW_%d}}' % u, review_student(RQ[u]))
    body = body.replace('{{FINAL}}', review_student(FINAL))
    body = body.replace('{{GLOSSARY}}', glossary_html())
    body = iconify(body)
    # page numbers for TOC
    for key in re.findall(r'\{\{PG:(\w+)\}\}', body):
        body = body.replace('{{PG:%s}}' % key, str((pages or {}).get(key, '—')))
    html = f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>كتاب العلوم — الصف الرابع الابتدائي</title><style>{css}</style></head><body>{body}</body></html>'
    open(os.path.join(B, 'book.html'), 'w', encoding='utf-8').write(html)

REVIEW_LIST = [
 ('آيات قرآنية', 'أضفتُ ثلاث آيات موجزة في افتتاح الوحدات (الأنعام: 99، النور: 45، الرعد: 3) لأن نص الكتاب الأصلي لم يكن بين يديّ. تُراجَع كتابتها وضبطها ومراجعها، أو تُستبدل بآيات الكتاب الأصلي.'),
 ('صور الكتاب', 'الرسوم المستخدمة رسوم متجهة ورموز تعبيرية مسمّاة. تُستبدل بصور واقعية أو رسوم علمية دقيقة حسب مواصفات الشكل النهائي، مع الإبقاء على التسميات.'),
 ('أمثلة اللافقاريات', 'ذكرتُ الإسفنجيات والديدان والمفصليات والرخويات وشوكيات الجلد كما في المصدر، وأضفتُ رموزًا مصوّرة توضيحية (دودة، سرطان، حلزون…). هذه الأمثلة من خارج المصدر وتحتاج موافقة المؤلف.'),
 ('تصنيف النباتات اللازهرية', 'ذكر المصدر الطحالب والحزازيات والسرخسيات ضمن النباتات اللازهرية مع التنبيه على ضبط المصطلحات. أوردتُها كما وردت مع جملة «من أمثلتها» وتحتاج مراجعة علمية قبل النشر.'),
 ('عبارة «المصدر الوحيد للغذاء»', 'لم أستخدم هذه العبارة. عوّضتها بأن النباتات منتِجات، والحيوانات والإنسان مستهلِكون في السلاسل المبسّطة.'),
 ('التلوّث والاحتباس الحراري', 'حذفتُ الحديث عن الاحتباس الحراري واكتفيتُ بأن احتراق الوقود ينتج دخانًا وملوِّثات، إلى أن يُبسَّط الموضوع علميًا ويُراجَع.'),
 ('الغبار والجهاز التنفسي', 'لم أنقل أي إيحاء بأن قطعة قماش مبلّلة تكفي. أضفتُ في الدرس الرابع تنبيهًا عامًّا (البقاء داخل المبنى وقت العواصف الترابية واستعمال كمامة عند الحاجة وبتوجيه الكبار). هذا التنبيه إضافة تحتاج موافقة.'),
 ('المبيدات', 'أبرزتُ تعليمات السلامة (الابتعاد عن أماكن الرش، عدم لمس المبيد، غسل الفواكه والخضراوات).'),
 ('وصف مجموعات الفقاريات', 'استعملتُ عبارات مثل «كثير منها» و«يغطي أجسام كثير منها» لتجنّب تعميم صفة بعض الأنواع على المجموعة كلها (الشعر/الصوف، الحراشف، القشور).'),
 ('الدورة الزراعية ووسائل التصحّر', 'استخدمتُ عبارات الغاية من كل وسيلة (مثل: المصدّات تحمي الحقول من الرياح والرمال) بصياغة تعليمية قريبة من المصدر؛ يُراجعها المؤلف.'),
 ('التربة', 'اعتمدتُ جدولًا مقارنًا واحدًا لأنواع التربة الثلاثة، وأعدتُ تحرير العبارة المضطربة في الخلاصة. يُطابَق مع النص الأصلي.'),
 ('الأسئلة والأنشطة', 'أسئلة التقويم ومراجعات الوحدات والمراجعة الشاملة وضعتُها بحسب «بنك الأنشطة» في الوثيقة، وهي جديدة وليست منقولة من الكتاب الأصلي. الإجابات في هذا الدليل فقط، ولا تظهر في نسخة التلميذ.'),
 ('الاحتياج إلى النص الأصلي', 'لم يكن الكتاب الأصلي (الملف المرفق) متاحًا لي؛ بُني الكتاب على وثيقة التنقية وحدها. قد توجد تفاصيل في الأصل ليست هنا، ويُرجَع إليه لتدقيق الأمثلة المحلية.'),
 ('تجارب الأنشطة', 'أنشطة مراقبة التربة والبذور تُنفَّذ بإشراف المعلم وبعد غسل اليدين، ولا يُستعمل فيها مواد خطرة.'),
]

def build_guide():
    css = load('book.css')
    h = '<div class="gcover"><h1>دليل إجابات المعلم</h1><p>كتاب العلوم — الصف الرابع الابتدائي — الفصل الدراسي الأول</p><p class="cap">للمعلم والمراجع فقط، ولا يوزَّع على التلاميذ.</p></div>'
    h += '<h2 class="pb">أولًا: إجابات أسئلة الدروس</h2>'
    titles = {1: 'البيئة ومكوّناتها', 2: 'العلاقة بين مكوّنات البيئة', 3: 'موارد البيئة', 4: 'تلوّث البيئة', 5: 'الحيوانات', 6: 'النباتات', 7: 'الأرض والصخور', 8: 'التربة', 9: 'الزراعة ومكافحة التصحّر'}
    for n in range(1, 10):
        d = LQ[n]
        h += f'<h3 class="gh">الدرس {n}: {titles[n]}</h3>' + render_activity_key(d['activity'])
        for i, q in enumerate(d['qs']): h += render_q(q, i + 1, False)
    h += '<h2 class="pb">ثانيًا: إجابات مراجعات الوحدات</h2>'
    for u in (1, 2, 3):
        h += f'<h3 class="gh">مراجعة الوحدة {["الأولى","الثانية","الثالثة"][u-1]}</h3>'
        for i, q in enumerate(RQ[u]): h += render_q(q, i + 1, False)
    h += '<h3 class="gh">المراجعة الشاملة</h3>'
    for i, q in enumerate(FINAL): h += render_q(q, i + 1, False)
    h += '<h2 class="pb">ثالثًا: قائمة المراجعة العلمية (للمؤلف قبل الطباعة)</h2><p>هذه قائمة بكل موضع أضفتُ فيه شيئًا أو أعدتُ صياغته أو تركتُ فيه قرارًا للمؤلف. لم أُدخل أي معلومة من خارج الوثيقة على أنها من المصدر.</p><ol class="rl">'
    for t, d in REVIEW_LIST: h += f'<li><b>{t}:</b> {d}</li>'
    h += '</ol>'
    html = f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>دليل إجابات المعلم</title><style>{css}</style></head><body class="guide">{h}</body></html>'
    open(os.path.join(B, 'guide.html'), 'w', encoding='utf-8').write(html)

if __name__ == '__main__':
    pages = json.load(open(os.path.join(B, 'pages.json'))) if os.path.exists(os.path.join(B, 'pages.json')) else None
    build_book(pages)
    build_guide()
    print('built')
