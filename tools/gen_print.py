#!/usr/bin/env python3
# Materiały do wydruku (nieobowiązkowe): assets/print/NNN.pdf dla każdej gotowej sprawy.
# Tylko to, co gracze widzą od pierwszej minuty: wprowadzenie, zadania, osoby, miejsca, puste arkusze notatek.
# Żadnych dowodów ani niczego, co odkrywa się w trakcie gry.
import json, os, sys, io
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color, black

ROOT = os.path.join(os.path.dirname(__file__), '..')
F = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('Serif', F + 'DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('SerifB', F + 'DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('SerifI', F + 'DejaVuSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Sans', F + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('SansB', F + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Mono', F + 'DejaVuSansMono.ttf'))
W, H = A4
M = 46
GREY = Color(.42, .4, .37)
LINE = Color(.75, .73, .7)
RED = Color(.6, .12, .1)


def wrap(text, font, size, width):
    out = []
    for para in text.split('\n'):
        words, line = para.split(' '), ''
        for w in words:
            t = (line + ' ' + w).strip()
            if pdfmetrics.stringWidth(t, font, size) <= width: line = t
            else:
                if line: out.append(line)
                line = w
        out.append(line)
    return out


class Doc:
    def __init__(self, path, case):
        self.c = canvas.Canvas(path, pagesize=A4); self.case = case; self.page = 0
        self.c.setTitle(f"ŚLAD {case['id']} — {case['title']} — materiały do wydruku"); self.c.setAuthor('ŚLAD')
        self.new()

    def new(self):
        if self.page: self.c.showPage()
        self.page += 1; c = self.c
        c.setFont('Mono', 7.5); c.setFillColor(GREY)
        c.drawString(M, H - 28, f"ŚLAD · AKTA {self.case['id']} · {self.case['title'].upper()}")
        c.drawRightString(W - M, H - 28, f"materiały pomocnicze · strona {self.page}")
        c.drawCentredString(W / 2, 22, 'Nieobowiązkowe. Wszystko, czego potrzebujecie do rozwiązania sprawy, jest w aplikacji.')
        c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(M, H - 34, W - M, H - 34)
        c.setFillColor(black); self.y = H - 62

    def need(self, h):
        if self.y - h < 46: self.new()

    def head(self, text, sub=None):
        self.need(60); c = self.c
        c.setFont('SerifB', 19); c.drawString(M, self.y, text); self.y -= 8
        if sub: self.y -= 12; c.setFont('SerifI', 9.5); c.setFillColor(GREY); c.drawString(M, self.y, sub); c.setFillColor(black)
        self.y -= 16

    def para(self, text, font='Serif', size=10.5, lead=15, indent=0, color=black, gap=6):
        lines = wrap(text, font, size, W - 2 * M - indent)
        for ln in lines:
            self.need(lead); self.c.setFont(font, size); self.c.setFillColor(color); self.c.drawString(M + indent, self.y, ln); self.y -= lead
        self.c.setFillColor(black); self.y -= gap


def img_reader(rel, maxw):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): return None
    im = Image.open(p).convert('RGB')
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82); b.seek(0)
    return ImageReader(b), im.width / im.height


def svg_path(c, d, sx, sy, ox, oy):
    """Rysuje prostą ścieżkę SVG (M, L, C, Z, współrzędne bezwzględne)."""
    import re
    tok = re.findall(r'[MLCZ]|-?[\d.]+', d); i = 0; p = c.beginPath(); cmd = None
    X = lambda v: ox + float(v) * sx; Y = lambda v: oy - float(v) * sy
    while i < len(tok):
        t = tok[i]
        if t in 'MLCZ': cmd = t; i += 1
        if cmd == 'Z': p.close(); continue
        if cmd == 'M': p.moveTo(X(tok[i]), Y(tok[i + 1])); i += 2; cmd = 'L'
        elif cmd == 'L': p.lineTo(X(tok[i]), Y(tok[i + 1])); i += 2
        elif cmd == 'C': p.curveTo(X(tok[i]), Y(tok[i + 1]), X(tok[i + 2]), Y(tok[i + 3]), X(tok[i + 4]), Y(tok[i + 5])); i += 6
    return p


def map_page(d, case):
    """Mapa szlaków (pole map w sprawie): to samo, co gracze widzą w aplikacji od początku."""
    m = case['map']; c = d.c
    d.new(); d.head('Mapa', m.get('note', ''))
    mw = W - 2 * M; sx = sy = mw / m['w']; mh = m['h'] * sy; ox = M; oy = d.y - 4
    c.setStrokeColor(LINE); c.rect(ox, oy - mh, mw, mh)
    for g in m.get('deco', []):
        k = g.get('k'); pth = svg_path(c, g['d'], sx, sy, ox, oy)
        if k == 'ridge': c.setStrokeColor(GREY); c.setLineWidth(1.2); c.drawPath(pth, stroke=1, fill=0)
        elif k == 'forest': c.setFillColor(Color(.86, .9, .85)); c.drawPath(pth, stroke=0, fill=1)
        elif k == 'rock': c.setFillColor(Color(.7, .7, .7)); c.drawPath(pth, stroke=0, fill=1)
        else: c.setFillColor(Color(.93, .93, .95)); c.setStrokeColor(Color(.85, .85, .88)); c.setLineWidth(.6); c.drawPath(pth, stroke=1, fill=1)
    c.setFillColor(GREY)
    for lb in m.get('labels', []):
        c.setFont('SansB' if lb.get('k') != 'small' else 'Sans', 8 if lb.get('k') != 'small' else 7); c.drawCentredString(ox + lb['x'] * sx, oy - lb['y'] * sy, lb['t'])
    nodes = {n['id']: n for n in m['nodes']}
    for e in m['edges']:
        a, b = nodes[e['a']], nodes[e['b']]
        pth = svg_path(c, e['path'], sx, sy, ox, oy) if e.get('path') else svg_path(c, f"M{a['x']} {a['y']} L{b['x']} {b['y']}", sx, sy, ox, oy)
        kind = e.get('kind'); c.setLineWidth(2 if kind == 'trail' else 1.4)
        c.setStrokeColor(Color(.15, .5, .2) if kind == 'trail' else (Color(.25, .3, .55) if kind == 'winter' else black))
        c.setDash(6, 4) if kind == 'winter' else c.setDash()
        c.drawPath(pth, stroke=1, fill=0); c.setDash()
        x, y = ox + e.get('lx', (a['x'] + b['x']) / 2) * sx, oy - e.get('ly', (a['y'] + b['y']) / 2) * sy
        c.setFillColor(black); c.setFont('Sans', 7.6)
        lines = []
        if e.get('name'): lines.append(e['name'])
        lines.append(f"↑ {e['t'][0]} min  ↓ {e['t'][1]} min")
        if e.get('storm') is None: lines.append('śnieżyca: zamknięte' + (f" ({e['closedWhy']})" if e.get('closedWhy') else ''))
        else: lines.append(f"śnieżyca: ↑ {e['storm'][0]}  ↓ {e['storm'][1]} min")
        wmax = max(pdfmetrics.stringWidth(ln, 'SansB', 7.4) for ln in lines) + 8
        c.setFillColor(Color(1, 1, 1, alpha=0.85)); c.rect(x - wmax / 2, y - (len(lines) - 1) * 9 - 3, wmax, len(lines) * 9 + 4, stroke=0, fill=1); c.setFillColor(black)
        for k, ln in enumerate(lines):
            c.setFont('SansB' if k == 0 and e.get('name') else 'Sans', 7.4); c.drawCentredString(x, y - k * 9, ln)
    for n in m['nodes']:
        x, y = ox + n['x'] * sx, oy - n['y'] * sy
        c.setFillColor(RED if n['id'] == m.get('start') else black); c.circle(x, y, 4, stroke=0, fill=1)
        c.setFillColor(black); c.setFont('SerifB', 9)
        tx, ty = x + n.get('lx', 0) * sx, y - n.get('ly', 14) * sy
        txt = f"{n['name']}"; alt = f"{n['alt']} m n.p.m."
        if n.get('anchor') == 'start': c.drawString(tx, ty, txt); c.setFont('Sans', 7); c.setFillColor(GREY); c.drawString(tx, ty - 9, alt)
        else: c.drawCentredString(tx, ty, txt); c.setFont('Sans', 7); c.setFillColor(GREY); c.drawCentredString(tx, ty - 9, alt)
    d.y = oy - mh - 16
    c.setFillColor(GREY); c.setFont('Sans', 8)
    c.drawString(M, d.y, 'Linia ciągła zielona — szlak; przerywana — trasa zimowa; czerwony punkt — miejsce startu zespołu. Czasy dla zespołu w rakietach.')
    c.setFillColor(black)


def build(cid):
    case = json.load(open(os.path.join(ROOT, 'cases', cid + '.json'), encoding='utf-8'))
    os.makedirs(os.path.join(ROOT, 'assets', 'print'), exist_ok=True)
    out = os.path.join(ROOT, 'assets', 'print', cid + '.pdf')
    d = Doc(out, case); c = d.c
    # 1. wprowadzenie
    c.setFont('Mono', 9); c.setFillColor(RED); c.drawString(M, d.y, f"AKTA {cid}"); c.setFillColor(black); d.y -= 30
    c.setFont('SerifB', 30); c.drawString(M, d.y, case['title']); d.y -= 22
    meta = ' · '.join(x for x in [case.get('genre'), case.get('duration'), ('gracze: ' + case['players']) if case.get('players') else None] if x)
    c.setFont('Sans', 9); c.setFillColor(GREY); c.drawString(M, d.y, meta); c.setFillColor(black); d.y -= 26
    intro = case['intro']
    d.para(intro['lead'], 'SerifI', 12, 17, gap=10)
    for p in intro.get('brief', []):
        if 'Do wydruku' not in p: d.para(p)
    d.y -= 6; d.head('Zadania')
    for i, t in enumerate(intro.get('task', []), 1): d.para(f'{i}. {t}', 'Serif', 11, 16, gap=3)
    d.y -= 10
    d.para('Jak korzystać: wydrukujcie to, co wam się przyda — listę osób, plan miejsc albo puste arkusze na oś czasu i podejrzanych. '
           'Gra nie wymaga drukowania; te kartki tylko ułatwiają wspólne notowanie przy stole.', 'Sans', 8.5, 12, color=GREY)
    # 2. osoby
    d.new(); d.head('Osoby', 'Wszyscy, z którymi możecie rozmawiać od początku sprawy.')
    col_w = (W - 2 * M - 18) / 2; ph_w = 74; x0 = [M, M + col_w + 18]; i = 0; row_h = 0; ytop = d.y
    for p in case['people']:
        if i % 2 == 0:
            d.y = ytop - row_h if i else d.y
            if d.y < 170: d.new(); d.head('Osoby (cd.)')
            ytop = d.y; row_h = 0
        x = x0[i % 2]; y = ytop
        r = img_reader(p['img'], 300) if p.get('img') else None
        if r: c.drawImage(r[0], x, y - ph_w / r[1], ph_w, ph_w / r[1]); c.setStrokeColor(LINE); c.rect(x, y - ph_w / r[1], ph_w, ph_w / r[1])
        tx = x + (ph_w + 10 if r else 0); tw = col_w - (ph_w + 10 if r else 0)
        c.setFont('SerifB', 11.5); c.drawString(tx, y - 11, p['name'])
        c.setFont('Sans', 8.2); c.setFillColor(GREY); role = p.get('role', '') + (f", {p['age']} l." if p.get('age') else '')
        yy = y - 24
        for ln in wrap(role, 'Sans', 8.2, tw): c.drawString(tx, yy, ln); yy -= 10.5
        c.setFillColor(black); c.setFont('Serif', 8.6); yy -= 3
        for ln in wrap(p.get('desc', ''), 'Serif', 8.6, tw): c.drawString(tx, yy, ln); yy -= 11.5
        h = max((ph_w / r[1]) if r else 0, y - yy) + 18; row_h = max(row_h, h); i += 1
    d.y = ytop - row_h
    # 3. miejsca
    d.new(); d.head('Miejsca', 'Lokalizacje dostępne od początku sprawy.')
    for l in case['locations']:
        r = img_reader(l['img'], 520) if l.get('img') else None
        iw = 150; ih = iw / r[1] if r else 0
        lines = wrap(l.get('desc', ''), 'Serif', 9, W - 2 * M - (iw + 12 if r else 0))
        h = max(ih, 30 + 12 * len(lines)) + 16
        d.need(h); y = d.y
        if r: c.drawImage(r[0], M, y - ih, iw, ih); c.setStrokeColor(LINE); c.rect(M, y - ih, iw, ih)
        tx = M + (iw + 12 if r else 0)
        c.setFont('SerifB', 12); c.drawString(tx, y - 12, l['name'])
        c.setFont('Sans', 8.2); c.setFillColor(GREY); c.drawString(tx, y - 25, l.get('kind', '')); c.setFillColor(black)
        yy = y - 40; c.setFont('Serif', 9)
        for ln in lines: c.drawString(tx, yy, ln); yy -= 12
        d.y = y - h
    if case.get('map'): map_page(d, case)
    # 4. oś czasu
    d.new(); d.head('Oś czasu', 'Wpisujcie zdarzenia w kolejności. Zaznaczajcie źródło — kto to powiedział albo z którego dowodu to wiecie.')
    cols = [(M, 'Dzień, godzina'), (M + 92, 'Co się stało'), (W - M - 120, 'Źródło')]
    c.setFont('SansB', 8.5)
    for x, t in cols: c.drawString(x + 3, d.y, t)
    d.y -= 6; c.setStrokeColor(LINE)
    while d.y > 60:
        c.line(M, d.y, W - M, d.y); d.y -= 21
    for x, _ in cols[1:]: c.line(x, H - 112, x, d.y + 21)
    # 5. podejrzani
    d.new(); d.head('Podejrzani', 'Motyw, okazja, alibi i to, co się nie zgadza. Ołówek przyda się bardziej niż długopis.')
    heads = ['Osoba', 'Motyw', 'Okazja', 'Alibi', 'Co się nie zgadza']
    widths = [110, 95, 95, 95, W - 2 * M - 395]
    xs = [M]; [xs.append(xs[-1] + w) for w in widths]
    c.setFont('SansB', 8.5)
    for x, t in zip(xs, heads): c.drawString(x + 4, d.y, t)
    d.y -= 6; top = d.y; n = len(case['people'])
    rh = min(92, (d.y - 60) / max(n, 1))
    for p in case['people']:
        c.setStrokeColor(LINE); c.line(M, d.y, W - M, d.y)
        c.setFont('Serif', 9.5); c.drawString(M + 4, d.y - 13, p['name'])
        c.setFont('Sans', 7); c.setFillColor(GREY)
        for k, ln in enumerate(wrap(p.get('role', ''), 'Sans', 7, 100)[:3]): c.drawString(M + 4, d.y - 24 - k * 8.5, ln)
        c.setFillColor(black); d.y -= rh
    c.line(M, d.y, W - M, d.y)
    for x in xs[1:-1]: c.line(x, top, x, d.y)
    # 6. notatki
    d.new(); d.head('Notatki')
    c.setStrokeColor(LINE)
    while d.y > 60: c.line(M, d.y, W - M, d.y); d.y -= 22
    c.save()
    return out


if __name__ == '__main__':
    ids = sys.argv[1:] or [x['id'] for x in json.load(open(os.path.join(ROOT, 'cases', 'index.json')))['cases'] if x.get('ready')]
    for cid in ids:
        p = build(cid); print(cid, os.path.getsize(p) // 1024, 'KB')
