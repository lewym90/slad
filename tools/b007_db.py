#!/usr/bin/env python3
# Sprawa 007 — rekordy dopisywane do ogólnopolskiej bazy (data/baza/sprawa-007.json).
# case='007' → rekord widoczny w sprawie 007 i w późniejszych sprawach dopiero po jej rozwiązaniu; neutral=True → widoczny zawsze.
import json, os, sys, datetime as _D
sys.path.insert(0, os.path.dirname(__file__))
from dbutil import pesel_ok, nip_ok, dowod_ok, pesel as _pesel, dowod as _dowod

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'baza')
def ps(y, m, d, serial, male): return _pesel(_D.date(y, m, d), serial, male)
PESEL = {
 'weronika': ps(1985, 7, 12, 416, False), 'adam': ps(1979, 9, 3, 287, True), 'krystian': ps(1988, 5, 21, 634, True),
 'igor': ps(1997, 2, 9, 155, True), 'natalia': ps(1990, 11, 27, 742, False), 'hampel': ps(1963, 4, 2, 318, True),
 'kuznik': ps(1974, 8, 15, 529, True), 'weronika2': ps(1999, 3, 30, 864, False), 'adam2': ps(1990, 1, 18, 471, True),
 'kos_m': ps(1956, 6, 6, 203, True), 'prezes': ps(1968, 10, 21, 593, True),
}
KRS_PT, NIP_PT = '0000217846', '5252318916'
KRS_RE, NIP_RE = '0000704219', '6112847302'
PT = 'POLAR-TEX SPÓŁKA AKCYJNA'
RE = 'ROGALA EXPEDITIONS SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'

def P(id, sur, names, pesel, born, place, father, mother, adres, dow, issued, organ, stan, case=None, neutral=None, **kw):
    ser, rest = dow.split(' '); dow = _dowod(ser, int(rest[-5:]))
    r = {'id': id, 'nazwisko': sur, 'imiona': names, 'pesel': pesel, 'plec': 'M' if int(pesel[9]) % 2 else 'K', 'urodzony': born, 'miejsceUr': place,
         'ojciec': father, 'matka': mother, 'adres': adres,
         'dowod': {'nr': dow, 'wydany': issued, 'wazny': str(int(issued[:4]) + 10) + issued[4:], 'organ': organ}, 'stan': stan}
    r.update(kw)
    if case: r['case'] = case
    if neutral: r['neutral'] = True
    return r

osoby = [
 P('O-007-weronika', 'Kos', ['Weronika', 'Anna'], PESEL['weronika'], '1985-07-12', 'Jelenia Góra', 'Ryszard', 'Elżbieta', 'ul. Puławska 182/40, 02-670 Warszawa',
   'DGP 41862', '2021-09-14', 'Prezydent m.st. Warszawy', 'panna', case='007'),
 P('O-007-weronika2', 'Kos', ['Weronika'], PESEL['weronika2'], '1999-03-30', 'Lublin', 'Marek', 'Joanna', 'ul. Narutowicza 12/3, 20-016 Lublin',
   'DLU 30417', '2022-04-05', 'Prezydent Miasta Lublin', 'panna', neutral=True),
 P('O-007-kosm', 'Kos', ['Marian'], PESEL['kos_m'], '1956-06-06', 'Kłodzko', 'Józef', 'Stanisława', 'ul. Wojska Polskiego 8/2, 57-300 Kłodzko',
   'DKL 18820', '2019-12-02', 'Burmistrz Miasta Kłodzka', 'żonaty', neutral=True),
 P('O-007-adam', 'Rogala', ['Adam', 'Piotr'], PESEL['adam'], '1979-09-03', 'Kraków', 'Piotr', 'Maria', 'ul. Zakopiańska 58/4, 30-418 Kraków',
   'DKR 52093', '2020-02-17', 'Prezydent Miasta Krakowa', 'rozwiedziony', neutral=True),
 P('O-007-adam2', 'Rogala', ['Adam'], PESEL['adam2'], '1990-01-18', 'Rzeszów', 'Tadeusz', 'Halina', 'ul. Hetmańska 21/9, 35-045 Rzeszów',
   'DRZ 27735', '2023-06-12', 'Prezydent Miasta Rzeszowa', 'żonaty', neutral=True),
 P('O-007-krystian', 'Lis', ['Krystian'], PESEL['krystian'], '1988-05-21', 'Wrocław', 'Andrzej', 'Beata', 'ul. Kasprowicza 33/7, 51-137 Wrocław',
   'DWR 66201', '2018-11-08', 'Prezydent Wrocławia', 'kawaler', neutral=True),
 P('O-007-igor', 'Szadkowski', ['Igor'], PESEL['igor'], '1997-02-09', 'Gdynia', 'Paweł', 'Ewa', 'ul. Świętojańska 70/11, 81-389 Gdynia',
   'DGY 14550', '2022-10-19', 'Prezydent Miasta Gdyni', 'kawaler', neutral=True),
 P('O-007-natalia', 'Brandt', ['Natalia', 'Maria'], PESEL['natalia'], '1990-11-27', 'Poznań', 'Jerzy', 'Monika', 'ul. Grunwaldzka 104/2, 60-307 Poznań',
   'DPO 73318', '2020-08-27', 'Prezydent Miasta Poznania', 'panna', neutral=True),
 P('O-007-hampel', 'Hampel', ['Zdzisław'], PESEL['hampel'], '1963-04-02', 'Karpacz', 'Henryk', 'Gertruda', 'Schronisko Hala Szronów, 58-540 Karpacz',
   'DJG 20916', '2017-05-30', 'Burmistrz Miasta Karpacza', 'wdowiec', neutral=True),
 P('O-007-kuznik', 'Kuźnik', ['Mirosław'], PESEL['kuznik'], '1974-08-15', 'Kowary', 'Stefan', 'Danuta', 'ul. Zamkowa 4/1, 58-530 Kowary',
   'DJG 31884', '2021-01-11', 'Burmistrz Miasta Kowary', 'żonaty', neutral=True),
 P('O-007-prezes', 'Malicki', ['Jerzy'], PESEL['prezes'], '1968-10-21', 'Warszawa', 'Stanisław', 'Irena', 'ul. Wiertnicza 96, 02-952 Warszawa',
   'DGP 22507', '2018-03-22', 'Prezydent m.st. Warszawy', 'żonaty', neutral=True),
]

firmy = [
 {'id': 'F-007-polartex', 'krs': KRS_PT, 'nip': NIP_PT, 'regon': '015637284', 'nazwa': PT, 'forma': 'spółka akcyjna', 'adres': 'ul. Postępu 21, 02-676 Warszawa',
  'dataWpisu': '2004-10-11', 'kapital': '18 500 000 zł',
  'zarzad': [{'funkcja': 'PREZES ZARZĄDU', 'nazwisko': 'MALICKI', 'imiona': 'JERZY', 'pesel': PESEL['prezes']},
             {'funkcja': 'CZŁONEK ZARZĄDU DS. MARKETINGU', 'nazwisko': 'KOS', 'imiona': 'WERONIKA ANNA', 'pesel': PESEL['weronika']}],
  'pkd': ['14.13.Z Produkcja pozostałej odzieży wierzchniej', '46.42.Z Sprzedaż hurtowa odzieży i obuwia'],
  'status': 'aktywny', 'neutral': True},
 {'id': 'F-007-rogala', 'krs': KRS_RE, 'nip': NIP_RE, 'regon': '368215090', 'nazwa': RE, 'forma': 'spółka z ograniczoną odpowiedzialnością', 'adres': 'ul. Zakopiańska 58/4, 30-418 Kraków',
  'dataWpisu': '2017-11-06', 'kapital': '5 000 zł',
  'zarzad': [{'funkcja': 'PREZES ZARZĄDU', 'nazwisko': 'ROGALA', 'imiona': 'ADAM PIOTR', 'pesel': PESEL['adam']}],
  'wspolnicy': [{'nazwa': 'ADAM PIOTR ROGALA', 'udzialy': '100 udziałów o łącznej wartości 5 000 zł'}],
  'pkd': ['79.90.A Działalność pilotów wycieczek i przewodników turystycznych', '90.04.Z Działalność obiektów kulturalnych'],
  'status': 'aktywny', 'neutral': True},
]

for o in osoby: assert pesel_ok(o['pesel']), o['id']; assert dowod_ok(o['dowod']['nr']), (o['id'], o['dowod']['nr'])
for f in firmy: assert nip_ok(f['nip']), (f['id'], f['nip'])
json.dump({'osoby': osoby, 'pojazdy': [], 'firmy': firmy, 'ksiegi': []}, open(os.path.join(OUT, 'sprawa-007.json'), 'w'), ensure_ascii=False, indent=1)
idx = os.path.join(OUT, 'index.json'); I = json.load(open(idx))
if 'sprawa-007.json' not in I['files']:
    I['files'].insert(I['files'].index('uniwersum.json'), 'sprawa-007.json'); json.dump(I, open(idx, 'w'), ensure_ascii=False)
print('007 baza: osoby', len(osoby), 'firmy', len(firmy))
