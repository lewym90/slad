#!/usr/bin/env python3
"""Szkice miejsc zdarzenia (plany) dla spraw — zapisuje sekcję "plan" w cases/NNN.json.
Współrzędne w układzie viewBox. Plan rysuje tylko to, co śledczy widzi na miejscu;
znaczniki punktów pojawiają się dopiero po przeszukaniu, ciało — po oględzinach."""
import json

def R(x, y, w, h, label='', loc=None, cls='', sub='', lx=None, ly=None):
    d = {'t': 'room', 'x': x, 'y': y, 'w': w, 'h': h, 'label': label}
    if loc: d['loc'] = loc
    if cls: d['cls'] = cls
    if sub: d['sub'] = sub
    if lx is not None: d['lx'] = lx
    if ly is not None: d['ly'] = ly
    return d
def F(x, y, w, h, label='', rot=0, lx=None, ly=None):
    d = {'t': 'furn', 'x': x, 'y': y, 'w': w, 'h': h}
    if label: d['label'] = label
    if rot: d['rot'] = rot
    if lx is not None: d['lx'] = lx
    if ly is not None: d['ly'] = ly
    return d
def C(x, y, r, cls=''): return {'t': 'circ', 'x': x, 'y': y, 'r': r, 'cls': cls}
def D(x1, y1, x2, y2): return {'t': 'door', 'p': [x1, y1, x2, y2]}
def W(x1, y1, x2, y2): return {'t': 'win', 'p': [x1, y1, x2, y2]}
def T(x, y, label, cls='', anchor='middle', rot=0):
    d = {'t': 'text', 'x': x, 'y': y, 'label': label}
    if cls: d['cls'] = cls
    if anchor != 'middle': d['anchor'] = anchor
    if rot: d['rot'] = rot
    return d
def L(x1, y1, x2, y2, cls=''): return {'t': 'line', 'p': [x1, y1, x2, y2], 'cls': cls}

# ---------------- 001 Dom, który pamięta ----------------
parter = {'id': 'parter', 'name': 'Parter i podwórze', 'w': 960, 'h': 730, 'north': True, 'items': [
    T(480, 26, 'OGRÓD', 'area'),
    R(40, 60, 170, 325, 'Zachodnie', 'westwing', 'closed', 'skrzydło · zamknięte', ly=215),
    R(210, 60, 190, 150, 'Biblioteka', 'library', ly=198, lx=270),
    R(400, 60, 300, 150, 'Gabinet', 'study', ly=198, lx=560),
    R(210, 210, 490, 45, 'korytarz', cls='plain', ly=238),
    R(700, 36, 180, 219, 'Oranżeria', 'orangery', 'glass', ly=236),
    R(210, 255, 190, 130, 'Hol', cls='plain', lx=270),
    R(400, 255, 180, 130, 'Jadalnia', cls='plain'),
    R(580, 255, 190, 130, 'Kuchnia', cls='plain'),
    D(240, 255, 300, 255), D(400, 300, 400, 340), D(580, 300, 580, 340), D(210, 305, 210, 345),
    D(352, 210, 386, 210), D(414, 210, 448, 210), D(700, 216, 700, 250), D(880, 70, 880, 110),
    D(250, 385, 300, 385), D(700, 385, 736, 385),
    W(240, 60, 330, 60), W(600, 60, 690, 60), W(440, 385, 540, 385), W(600, 385, 680, 385),
    # gabinet
    F(470, 62, 90, 14, 'kominek', lx=430, ly=88),
    F(402, 64, 12, 140), F(420, 150, 36, 30, 'gramofon', lx=438, ly=196),
    F(445, 118, 62, 10, 'drabina', -38, lx=452, ly=106),
    F(596, 108, 84, 48, 'biurko', lx=626, ly=146), F(676, 64, 20, 18),
    # biblioteka
    F(226, 66, 120, 26, 'kanapa', lx=286, ly=84), F(352, 112, 36, 36, 'fotel', lx=370, ly=163), C(372, 90, 7), F(262, 118, 56, 26),
    # oranżeria
    C(740, 80, 14, 'pot'), C(820, 70, 16, 'pot'), C(760, 160, 13, 'pot'), C(845, 170, 13, 'pot'),
    # hol
    F(352, 262, 40, 80, 'schody', lx=372, ly=357),
    T(275, 405, 'wejście główne', 'small'),
    # podwórze i oficyna
    T(380, 500, 'podwórze · bruk', 'area'),
    L(718, 397, 718, 553, 'dim'), T(740, 482, 'ok. 30 m', 'hand', 'start'),
    R(560, 565, 300, 120, 'Oficyna', 'outbuilding', ly=675, lx=780),
    L(700, 565, 700, 685), T(630, 585, 'pokój Heleny', 'small'), T(780, 585, 'sień', 'small'),
    D(706, 565, 740, 565), D(700, 630, 700, 660), W(580, 685, 660, 685),
    F(570, 600, 28, 60), F(620, 640, 36, 28), F(812, 600, 24, 16, 'telefon', lx=824, ly=630),
    {'t': 'body', 'x': 522, 'y': 80, 'rot': 0, 's': 1.1, 'req': 'sp-body'},
  ],
  'spots': {'sp-body': [552, 120], 'sp-fire': [584, 92], 'sp-gramo': [474, 166], 'sp-desk': [612, 172],
            'sp-cups': [662, 124], 'sp-drawer': [648, 172], 'sp-printer': [686, 98],
            'sp-lamp': [240, 128], 'sp-shoes': [300, 168], 'sp-wall': [388, 190],
            'sp-floor': [790, 190], 'sp-pots': [826, 110], 'sp-gdoor': [862, 90],
            'sp-phone': [790, 610], 'sp-hroom': [640, 620]}}

pietro = {'id': 'pietro', 'name': 'Piętro', 'w': 960, 'h': 470, 'north': True, 'items': [
    T(480, 26, 'OGRÓD', 'area'),
    {'t': 'room', 'x': 40, 'y': 60, 'w': 840, 'h': 325, 'label': '', 'cls': 'ghost'},
    T(470, 420, 'obrys parteru (linia przerywana)', 'small'),
    R(40, 60, 170, 110, 'Pokój Anny', 'westwing', 'closed', '2013', ly=110),
    R(40, 170, 110, 215, 'pokoje', cls='closed', sub='spalone', ly=270),
    R(150, 170, 60, 215, '', 'westwing', 'closed'),
    T(186, 280, 'korytarz', 'small', rot=-90),
    T(40, 410, 'ZACHODNIE SKRZYDŁO · ZAMKNIĘTE OD POŻARU', 'small', 'start'),
    W(80, 60, 140, 60), D(160, 170, 200, 170), D(150, 210, 150, 240), D(150, 300, 150, 330),
    T(110, 50, 'okno ok. 6 m nad tarasem', 'hand'),
    R(400, 225, 370, 160, '', cls='plain'),
    R(520, 225, 140, 64, 'Pokój „Anny”', 'guestrooms', ly=268),
    R(520, 321, 140, 64, 'Pokój Marty', 'guestrooms', ly=364),
    T(720, 310, 'korytarz', 'small'),
    F(406, 289, 44, 32, 'schody', lx=428, ly=338), T(428, 352, 'do holu', 'small'),
    D(600, 289, 634, 289), D(600, 321, 634, 321), W(550, 225, 630, 225), W(550, 385, 630, 385),
    T(585, 215, 'SKRZYDŁO WSCHODNIE', 'small'),
  ],
  'spots': {'sp-door13': [180, 192], 'sp-window13': [110, 80], 'sp-aroom': [538, 244], 'sp-mroom': [538, 340]}}

# ---------------- 002 Ostatni pociąg ----------------
CW = 55
sk = {'id': 'sklad', 'name': 'Skład i wagon 2', 'w': 1000, 'h': 500, 'items': [
    T(500, 30, 'SKŁAD · LOKOMOTYWA Z PRZODU', 'small'),
    R(30, 46, 170, 84, 'Lokomotywa', 'loco', ly=108),
    R(210, 46, 220, 84, 'Wagon 1', cls='plain', sub='miejsca siedzące', ly=88),
    R(440, 46, 250, 84, 'Wagon 2', cls='hi', sub='sypialny · szczegóły niżej', ly=88),
    R(700, 46, 240, 84, 'Wagon 3 · bar', 'bar', sub='ostatni', ly=104),
    D(940, 72, 940, 104), T(944, 150, 'tylne drzwi', 'small'),
    L(440, 134, 20, 196, 'dim'), L(690, 134, 980, 196, 'dim'),
    R(20, 200, 80, 190, '', cls='plain'), T(60, 300, 'wejście', 'small'), D(20, 270, 20, 320), D(45, 390, 80, 390),
    *[R(100 + i * CW, 200, CW, 120, str(i + 1), 'compartment' if i == 9 else None, '' if i == 9 else 'plain', ly=226, lx=(636 if i == 9 else None)) for i in range(10)],
    R(650, 200, 80, 120, 'T2B', cls='plain', ly=224),
    R(730, 200, 150, 120, 'Służbowy', 'service', ly=310),
    R(100, 320, 780, 70, 'korytarz', 'corridor', ly=362, lx=380),
    R(880, 200, 100, 190, '', cls='plain'), T(930, 360, 'przedsionek', 'small'),
    D(905, 200, 945, 200), T(930, 258, 'drzwi', 'small'), T(930, 272, 'techniczne', 'small'), D(980, 270, 980, 320),
    *[D(108 + i * CW, 320, 134 + i * CW, 320) for i in range(10)], D(675, 320, 705, 320), D(790, 320, 830, 320), D(880, 335, 880, 375),
    *[W(110 + i * CW, 200, 145 + i * CW, 200) for i in range(10)], W(670, 200, 710, 200), W(770, 200, 860, 200),
    *[W(130 + i * 75, 390, 180 + i * 75, 390) for i in range(10)],
    F(598, 272, 48, 24), F(598, 206, 20, 14),
    F(776, 206, 96, 28, 'biurko', lx=824, ly=225), F(736, 206, 24, 74),
    T(380, 420, '← do wagonu 1', 'small'), T(930, 420, 'do wagonu 3 →', 'small'),
    {'t': 'body', 'x': 690, 'y': 266, 'rot': 0, 's': 0.9, 'pose': 'seated', 'req': 'e08'},
  ],
  'spots': {'sp-driver': [70, 68], 'sp-radio': [170, 68], 'sp-till': [740, 68], 'sp-locker': [900, 68],
            'sp-table': [610, 240], 'sp-bag': [636, 254], 'sp-hook': [640, 306],
            'sp-t2b': [690, 340], 'sp-door': [925, 222], 'sp-tech': [220, 352],
            'sp-log': [800, 256], 'sp-window': [856, 256], 'sp-lanyard': [748, 296], 'sp-roster': [840, 286]}}

wrzos = {'id': 'wrzos', 'name': 'Stacja Wrzos', 'w': 1000, 'h': 470, 'items': [
    L(20, 50, 980, 50, 'rail'), L(20, 66, 980, 66, 'rail'), T(500, 40, 'tor', 'small'),
    R(80, 80, 840, 70, 'peron', 'wrzos', ly=104, lx=200),
    *[C(130 + i * 95, 140, 8, 'tree') for i in range(9)], T(860, 170, 'rząd klonów', 'hand'),
    R(470, 88, 60, 40, 'kiosk', 'wrzos', ly=114), F(536, 92, 12, 32), T(556, 112, 'gablota', 'small', 'start'),
    R(370, 180, 280, 110, 'Budynek dworca', 'wrzos', ly=242),
    D(490, 180, 530, 180), D(490, 290, 530, 290),
    F(670, 250, 22, 30), F(696, 250, 22, 30), F(722, 250, 22, 30), T(708, 300, 'kontenery', 'small'),
    R(80, 320, 840, 70, 'droga dojazdowa', cls='plain', ly=370, lx=200),
    F(420, 330, 120, 30, 'postój taksówek'),
    T(500, 430, 'schemat · nie w skali', 'hand'),
  ],
  'spots': {'sp-kiosk': [452, 108], 'sp-bin': [745, 236], 'sp-taxi': [560, 346]}}

trasa = {'id': 'trasa', 'name': 'Trasa', 'w': 1000, 'h': 300, 'items': [
    R(640, 130, 260, 80, 'Las Karski', 'tracks', 'forest', ly=196),
    L(60, 170, 940, 170, 'track'),
    *[x for i, (n, xx) in enumerate([('Wierzbno', 60), ('Gaj', 240), ('Wrzos', 420), ('Olszyny', 600), ('Karsk', 940)])
      for x in (C(xx, 170, 9, 'st'), T(xx, 120 if i % 2 == 0 else 236, n, ''))],
    T(500, 60, 'KIERUNEK JAZDY →', 'small'), T(500, 280, 'schemat · nie w skali', 'hand'),
  ],
  'spots': {'sp-ballast': [770, 150]}}

for cid, views in [('001', [parter, pietro]), ('002', [sk, wrzos, trasa])]:
    p = f'cases/{cid}.json'
    c = json.load(open(p, encoding='utf-8'))
    c['plan'] = {'views': views}
    json.dump(c, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')
