#!/usr/bin/env python3
# Sprawa 005 — rekordy dopisywane do ogólnopolskiej bazy (data/baza/sprawa-005.json).
# case='005' → rekord widoczny w sprawie 005 i w późniejszych sprawach dopiero po jej rozwiązaniu na urządzeniu.
# neutral=True → rekord widoczny zawsze (zwykłe dane, nic nie zdradza).
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from dbutil import pesel_ok, nip_ok, kw_ok, dowod_ok, pesel as _pesel, dowod as _dowod
import datetime as _D

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'baza')
PESEL = {'szulc': '63051741216', 'marta': '66090220807', 'kraska': '78112337503', 'pietras': '67082145713', 'pietras2': '90021112011',
         'kraska2': '85040923300', 'lis': '01273006119', 'morawiec': '64120531811', 'kosowski': '73061429019', 'dabrowska': '81100814401',
         'rudnicka': '47030307709', 'szulc2': '58012653017'}
KRS_REST, NIP_REST = '0000781264', '8513124409'
KRS_PB, NIP_PB = '0000412377', '8512047718'
KRS_HOTEL, NIP_HOTEL = '0000208815', '8512047724'
KRS_PIEK, NIP_PIEK = '0000530146', '8513124415'
KW_CLAIM = 'SZ1S/00045218/0'
KW_JAG = 'SZ1S/00131740/8'
ADR_PIETRAS = 'ul. Szafera 8, 71-245 Szczecin'
ADR_REST = 'ul. Jagiellońska 12/4, 70-435 Szczecin'
ADR_PB = 'ul. Fabryczna 3, 72-010 Police'

def P(id, sur, names, ps, born, place, father, mother, adres, dow, issued, organ, stan, case=None, neutral=None, **kw):
    ser, rest = dow.split(' '); dow = _dowod(ser, int(rest[-5:]))
    r = {'id': id, 'nazwisko': sur, 'imiona': names, 'pesel': ps, 'plec': 'M' if int(ps[9]) % 2 else 'K', 'urodzony': born, 'miejsceUr': place,
         'ojciec': father, 'matka': mother, 'adres': adres,
         'dowod': {'nr': dow, 'wydany': issued, 'wazny': str(int(issued[:4]) + 10) + issued[4:], 'organ': organ}, 'stan': stan}
    r.update(kw)
    if case: r['case'] = case
    if neutral: r['neutral'] = True
    return r

osoby = [
 P('O-005-szulc', 'Szulc', ['Edward'], PESEL['szulc'], '1963-05-17', 'Słupsk', 'Józef', 'Irena', 'ul. Morska 41/6, 75-221 Koszalin',
   'CGB 741827', '2018-04-10', 'Prezydent Miasta Koszalina', 'żonaty', neutral=True,
   malzonek={'pesel': PESEL['marta'], 'nazwisko': 'Szulc', 'imie': 'Marta'}),
 P('O-005-marta', 'Szulc', ['Marta', 'Irena'], PESEL['marta'], '1966-09-02', 'Koszalin', 'Stanisław', 'Wanda', 'ul. Morska 41/6, 75-221 Koszalin',
   'CHK 120934', '2021-09-14', 'Prezydent Miasta Koszalina', 'zamężna', neutral=True, rodowe='Bielecka',
   malzonek={'pesel': PESEL['szulc'], 'nazwisko': 'Szulc', 'imie': 'Edward'}),
 P('O-005-szulc2', 'Szulc', ['Edward', 'Marian'], PESEL['szulc2'], '1958-01-26', 'Opole', 'Marian', 'Helena', 'ul. Ozimska 112/9, 45-310 Opole',
   'CFW 888412', '2019-02-05', 'Prezydent Miasta Opola', 'wdowiec', neutral=True),
 P('O-005-kraska', 'Kraska', ['Iwona', 'Anna'], PESEL['kraska'], '1978-11-23', 'Szczecin', 'Ryszard', 'Teresa', ADR_PIETRAS,
   'CMR 305117', '2022-03-30', 'Prezydent Miasta Szczecin', 'zamężna', case='005',
   malzonek={'pesel': PESEL['pietras'], 'nazwisko': 'Pietras', 'imie': 'Damian'}),
 P('O-005-kraska2', 'Kraska', ['Iwona'], PESEL['kraska2'], '1985-04-09', 'Toruń', 'Jerzy', 'Maria', 'ul. Kasztanowa 14, 87-100 Toruń',
   'CDP 412265', '2020-06-18', 'Prezydent Miasta Torunia', 'panna', neutral=True),
 P('O-005-pietras', 'Pietras', ['Damian', 'Jan'], PESEL['pietras'], '1967-08-21', 'Stargard', 'Jan', 'Krystyna', ADR_PIETRAS,
   'CLS 662091', '2019-11-04', 'Prezydent Miasta Szczecin', 'żonaty', case='005',
   malzonek={'pesel': PESEL['kraska'], 'nazwisko': 'Kraska', 'imie': 'Iwona'}),
 P('O-005-pietras2', 'Pietras', ['Damian'], PESEL['pietras2'], '1990-02-11', 'Rzeszów', 'Adam', 'Bożena', 'ul. Podgórna 7, 35-321 Rzeszów',
   'CEK 108840', '2023-01-12', 'Prezydent Miasta Rzeszowa', 'kawaler', neutral=True),
 P('O-005-lis', 'Lis', ['Bartosz'], PESEL['lis'], '2001-07-30', 'Szczecin', 'Krzysztof', 'Agata', 'ul. Jasna 5/14, 70-777 Szczecin',
   'CPA 220478', '2019-08-21', 'Prezydent Miasta Szczecin', 'kawaler', neutral=True),
 P('O-005-morawiec', 'Morawiec', ['Lech', 'Tadeusz'], PESEL['morawiec'], '1964-12-05', 'Poznań', 'Tadeusz', 'Halina', 'ul. Grunwaldzka 88/3, 60-311 Poznań',
   'CJN 518806', '2017-05-22', 'Prezydent Miasta Poznania', 'rozwiedziony', neutral=True),
 P('O-005-kosowski', 'Kosowski', ['Adrian'], PESEL['kosowski'], '1973-06-14', 'Warszawa', 'Wiesław', 'Danuta', 'ul. Puławska 140/22, 02-624 Warszawa',
   'CKT 734410', '2020-10-02', 'Prezydent m.st. Warszawy', 'żonaty', neutral=True),
 P('O-005-dabrowska', 'Dąbrowska', ['Ewa', 'Maria'], PESEL['dabrowska'], '1981-10-08', 'Szczecin', 'Andrzej', 'Lucyna', 'ul. Monte Cassino 33/2, 70-466 Szczecin',
   'CMB 091273', '2021-04-27', 'Prezydent Miasta Szczecin', 'rozwiedziona', neutral=True),
 P('O-005-rudnicka', 'Rudnicka-Lange', ['Helena'], PESEL['rudnicka'], '1947-03-03', 'Szczecin', 'Karol', 'Gertruda', 'pobyt stały za granicą: Hamburg (Niemcy)',
   'CAE 502918', '2016-11-08', 'Prezydent Miasta Szczecin', 'wdowa', neutral=True, rodowe='Rudnicka'),
]
# goście hotelu (tło sprawy — zwykłe dane)
GUESTS = [
 ('laskowski', 'Laskowski', ['Wojciech'], '1979-03-14', 'Gdańsk', 'ul. Grunwaldzka 211/5, 80-266 Gdańsk', 'CGS 220871', '2020-02-12', 'Prezydent Miasta Gdańska'),
 ('michalak', 'Michalak', ['Piotr'], '1983-07-02', 'Poznań', 'ul. Dąbrowskiego 74/11, 60-529 Poznań', 'CJT 411830', '2022-05-30', 'Prezydent Miasta Poznania'),
 ('ratajczak', 'Ratajczak', ['Tomasz'], '1970-10-19', 'Wrocław', 'ul. Legnicka 52/8, 54-203 Wrocław', 'CDW 337102', '2018-09-03', 'Prezydent Wrocławia'),
 ('fijalkowski', 'Fijałkowski', ['Grzegorz'], '1962-01-28', 'Koszalin', 'ul. Zwycięstwa 102/4, 75-033 Koszalin', 'CHG 600154', '2017-12-11', 'Prezydent Miasta Koszalina'),
 ('banas', 'Banaś', ['Marek'], '1975-05-06', 'Kraków', 'ul. Kalwaryjska 31/2, 30-504 Kraków', 'CKR 812433', '2021-03-17', 'Prezydent Miasta Krakowa'),
 ('kmiecik', 'Kmiecik', ['Bożena'], '1958-12-15', 'Lublin', 'ul. Narutowicza 18/6, 20-016 Lublin', 'CLU 270611', '2016-06-29', 'Prezydent Miasta Lublin'),
 ('krupa', 'Krupa', ['Paweł'], '1988-08-08', 'Szczecin', 'ul. Kolumba 9/17, 70-035 Szczecin', 'CPB 455216', '2023-10-04', 'Prezydent Miasta Szczecin'),
]
for i, (k, sur, names, born, place, adres, dow, issued, organ) in enumerate(GUESTS):
    y, m, d = map(int, born.split('-'))
    male = not sur.endswith(('ska', 'cka')) and names[0] not in ('Bożena',)
    ps = _pesel(_D.date(y, m, d), 600 + i * 37, male)
    PESEL[k] = ps
    osoby.append(P(f'O-005-{k}', sur, names, ps, born, place, 'Jan', 'Maria', adres, dow, issued, organ,
                   'żonaty' if male else 'zamężna', neutral=True))

def V(id, nr, vin, marka, model, rok, kolor, owner, regd, ins, oc_do, bad, case=None, neutral=None, rodzaj='samochód osobowy'):
    r = {'id': id, 'nr': nr, 'vin': vin, 'marka': marka, 'model': model, 'rok': rok, 'kolor': kolor, 'rodzaj': rodzaj, 'wlasciciel': owner,
         'rejestracja': regd, 'oc': {'ubezpieczyciel': ins, 'do': oc_do}, 'badanie': bad, 'status': 'zarejestrowany'}
    if case: r['case'] = case
    if neutral: r['neutral'] = True
    return r
def own_p(k, name, adres): return {'typ': 'osoba', 'nazwa': name, 'pesel': PESEL[k], 'adres': adres}
def own_f(name, krs, adres): return {'typ': 'firma', 'nazwa': name, 'krs': krs, 'adres': adres}
REST = 'RESTYTUCJA POMORSKA SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'
PB = 'PB PIETRAS BUDOWNICTWO SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'
HOTEL = 'HOTEL GRYF SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'
PIEK = 'PIEKARNIA KŁOS SPÓŁKA JAWNA'
PESEL['sowa'] = _pesel(_D.date(1970, 3, 18), 811, True); PESEL['klos'] = _pesel(_D.date(1966, 5, 24), 902, True)
osoby.append(P('O-005-sowa', 'Sowa', ['Krzysztof'], PESEL['sowa'], '1970-03-18', 'Szczecin', 'Henryk', 'Zofia', 'ul. Szczecińska 4, 72-006 Mierzyn', 'CMS 30418', '2020-08-11', 'Wójt Gminy Dobra (Szczecińska)', 'żonaty', neutral=True))
osoby.append(P('O-005-klos', 'Kłos', ['Roman'], PESEL['klos'], '1966-05-24', 'Police', 'Roman', 'Jadwiga', 'ul. Kościuszki 40, 72-010 Police', 'CPL 11726', '2018-01-30', 'Burmistrz Polic', 'żonaty', neutral=True))
g = {o['id'][6:]: o for o in osoby}
pojazdy = [
 V('V-005-rest', 'ZS 7PR04', 'TMBJR7NP4N7051873', 'Skoda', 'Superb', 2022, 'srebrny', own_f(REST, KRS_REST, ADR_REST), '2022-04-12', 'Warta SA', '2026-04-11', '2026-04-08', case='005'),
 V('V-005-kraska', 'ZS 3K118', 'SB1K93BE10E128064', 'Toyota', 'Corolla', 2020, 'granatowy', own_p('kraska', 'Iwona Anna Kraska', ADR_PIETRAS), '2020-09-01', 'PZU SA', '2026-08-31', '2026-08-25', case='005'),
 V('V-005-laskowski', 'GD 2LM47', 'TMBAG7NE6K0215530', 'Skoda', 'Octavia', 2019, 'granatowy', own_p('laskowski', 'Wojciech Laskowski', g['laskowski']['adres']), '2019-05-20', 'Ergo Hestia SA', '2026-05-19', '2026-05-15', neutral=True),
 V('V-005-michalak', 'PO 51RT3', 'U5YPU81BBML926401', 'Kia', 'Sportage', 2021, 'biały', own_p('michalak', 'Piotr Michalak', g['michalak']['adres']), '2021-03-08', 'Allianz SA', '2027-03-07', '2027-03-01', neutral=True),
 V('V-005-ratajczak', 'DW 6TK02', 'WVWZZZ3CZJE118274', 'Volkswagen', 'Passat', 2018, 'czarny', own_p('ratajczak', 'Tomasz Ratajczak', g['ratajczak']['adres']), '2018-06-14', 'PZU SA', '2026-06-13', '2026-06-10', neutral=True),
 V('V-005-fijalkowski', 'ZK 40112', 'W0LZT8GB2H1017745', 'Opel', 'Insignia', 2017, 'szary', own_p('fijalkowski', 'Grzegorz Fijałkowski', g['fijalkowski']['adres']), '2017-11-02', 'Generali SA', '2026-11-01', '2026-10-28', neutral=True),
 V('V-005-banas', 'KR 7PW15', 'WAUZZZF41LA084322', 'Audi', 'A4', 2020, 'grafitowy', own_p('banas', 'Marek Banaś', g['banas']['adres']), '2020-07-21', 'Uniqa SA', '2026-07-20', '2026-07-14', neutral=True),
 V('V-005-kmiecik', 'LU 204CK', 'UU1HSDAG456712093', 'Dacia', 'Duster', 2016, 'zielony', own_p('kmiecik', 'Bożena Kmiecik', g['kmiecik']['adres']), '2016-04-04', 'Link4 SA', '2027-01-03', '2026-12-20', neutral=True),
 V('V-005-krupa', 'ZS 86HE4', 'ZFA35600006M48127', 'Fiat', 'Tipo', 2019, 'czerwony', own_p('krupa', 'Paweł Krupa', g['krupa']['adres']), '2019-09-16', 'PZU SA', '2026-09-15', '2026-09-10', neutral=True),
 V('V-005-hotel', 'ZS 12KA7', 'WVGZZZ1TZPW033186', 'Volkswagen', 'Touran', 2023, 'biały', own_f(HOTEL, KRS_HOTEL, 'ul. Panieńska 22, 70-535 Szczecin'), '2023-02-28', 'Warta SA', '2027-02-27', '2026-02-20', neutral=True),
 V('V-005-piek', 'ZPL 4C71', 'ZFA25000002F61730', 'Fiat', 'Ducato', 2017, 'biały', own_f(PIEK, KRS_PIEK, 'ul. Kościuszki 40, 72-010 Police'), '2017-03-30', 'Compensa SA', '2026-03-29', '2026-03-25', neutral=True, rodzaj='samochód ciężarowy (do 3,5 t)'),
]
firmy = [
 {'id': 'F-005-rest', 'krs': KRS_REST, 'nip': NIP_REST, 'regon': '383017290', 'nazwa': REST, 'forma': 'spółka z ograniczoną odpowiedzialnością', 'adres': ADR_REST,
  'dataWpisu': '2019-03-04', 'kapital': '50 000 zł',
  'zarzad': [{'funkcja': 'PREZES ZARZĄDU', 'nazwisko': 'PIETRAS', 'imiona': 'DAMIAN JAN', 'pesel': PESEL['pietras']}],
  'wspolnicy': [{'nazwa': 'DAMIAN JAN PIETRAS', 'udzialy': '100 udziałów o łącznej wartości 50 000 zł'}],
  'pkd': ['68.10.Z Kupno i sprzedaż nieruchomości na własny rachunek', '70.22.Z Doradztwo w zakresie prowadzenia działalności gospodarczej'], 'status': 'aktywny', 'case': '005'},
 {'id': 'F-005-pb', 'krs': KRS_PB, 'nip': NIP_PB, 'regon': '320988415', 'nazwa': PB, 'forma': 'spółka z ograniczoną odpowiedzialnością', 'adres': ADR_PB,
  'dataWpisu': '2012-01-16', 'kapital': '100 000 zł',
  'zarzad': [{'funkcja': 'PREZES ZARZĄDU', 'nazwisko': 'PIETRAS', 'imiona': 'DAMIAN JAN', 'pesel': PESEL['pietras']}],
  'wspolnicy': [{'nazwa': 'DAMIAN JAN PIETRAS', 'udzialy': '200 udziałów o łącznej wartości 100 000 zł'}],
  'pkd': ['41.20.Z Roboty budowlane związane ze wznoszeniem budynków', '43.39.Z Wykonywanie pozostałych robót budowlanych wykończeniowych'], 'status': 'aktywny', 'case': '005'},
 {'id': 'F-005-hotel', 'krs': KRS_HOTEL, 'nip': NIP_HOTEL, 'regon': '811540207', 'nazwa': HOTEL, 'forma': 'spółka z ograniczoną odpowiedzialnością', 'adres': 'ul. Panieńska 22, 70-535 Szczecin',
  'dataWpisu': '2004-07-01', 'kapital': '2 000 000 zł',
  'zarzad': [{'funkcja': 'PREZES ZARZĄDU', 'nazwisko': 'SOWA', 'imiona': 'KRZYSZTOF', 'pesel': PESEL['sowa']}],
  'pkd': ['55.10.Z Hotele i podobne obiekty zakwaterowania'], 'status': 'aktywny', 'neutral': True},
 {'id': 'F-005-piek', 'krs': KRS_PIEK, 'nip': NIP_PIEK, 'regon': '321456980', 'nazwa': PIEK, 'forma': 'spółka jawna', 'adres': 'ul. Kościuszki 40, 72-010 Police',
  'dataWpisu': '2014-10-20',
  'zarzad': [{'funkcja': 'WSPÓLNIK REPREZENTUJĄCY', 'nazwisko': 'KŁOS', 'imiona': 'ROMAN', 'pesel': PESEL['klos']}],
  'pkd': ['10.71.Z Produkcja pieczywa'], 'status': 'aktywny', 'neutral': True},
]
ksiegi = [
 {'id': 'K-005-claim', 'nr': KW_CLAIM, 'typ': 'działka zabudowana', 'polozenie': 'ul. Wielkopolska 21, 70-450 Szczecin',
  'opis': 'Działka nr 14/3, obręb 1012 Śródmieście, pow. 612 m², kamienica pięciokondygnacyjna z 1904 r., 14 lokali',
  'wlasciciele': [{'nazwa': 'Gmina Miasto Szczecin', 'udzial': 'całość'}],
  'podstawa': 'nabycie z mocy prawa, decyzja Wojewody Szczecińskiego z 12.05.1992',
  'hipoteki': [],
  'ostrzezenia': ['Ostrzeżenie o niezgodności treści księgi z rzeczywistym stanem prawnym na rzecz Heleny Rudnickiej-Lange (wpis z 18.06.2021, sygn. I Ns 412/21)',
                  'Wzmianka: roszczenie przeniesione umową cesji z 07.02.2022 na rzecz RESTYTUCJA POMORSKA SP. Z O.O. (KRS 0000781264)'],
  'case': '005'},
 {'id': 'K-005-jag', 'nr': KW_JAG, 'typ': 'lokal użytkowy', 'polozenie': ADR_REST,
  'opis': 'Lokal użytkowy nr 4, pow. 86 m², I piętro kamienicy, 3 pomieszczenia, aneks kuchenny, łazienka',
  'wlasciciele': [{'nazwa': REST, 'krs': KRS_REST, 'udzial': 'całość'}],
  'podstawa': 'umowa sprzedaży, akt notarialny Rep. A nr 2107/2019', 'hipoteki': [], 'ostrzezenia': [], 'case': '005'},
]

# kontrola sum
for o in osoby: assert pesel_ok(o['pesel']), o['id']; assert dowod_ok(o['dowod']['nr']), (o['id'], o['dowod']['nr'])
for f in firmy: assert nip_ok(f['nip']), f['id']
for k in ksiegi: assert kw_ok(k['nr']), k['id']
os.makedirs(OUT, exist_ok=True)
json.dump({'osoby': osoby, 'pojazdy': pojazdy, 'firmy': firmy, 'ksiegi': ksiegi}, open(os.path.join(OUT, 'sprawa-005.json'), 'w'), ensure_ascii=False, indent=1)
# zastrzeżone identyfikatory (generator tła ich nie użyje)
res = {'pesel': [o['pesel'] for o in osoby] + [z['pesel'] for f in firmy for z in f['zarzad']], 'nr': [v['nr'] for v in pojazdy],
       'krs': [f['krs'] for f in firmy], 'nip': [f['nip'] for f in firmy], 'kw': [k['nr'] for k in ksiegi], 'dowod': [o['dowod']['nr'] for o in osoby]}
json.dump(res, open(os.path.join(OUT, 'zastrzezone.json'), 'w'), indent=1)
print('osoby', len(osoby), 'pojazdy', len(pojazdy), 'firmy', len(firmy), 'ksiegi', len(ksiegi))
