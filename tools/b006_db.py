#!/usr/bin/env python3
# Sprawa 006 — rekordy dopisywane do ogólnopolskiej bazy (data/baza/sprawa-006.json).
# case='006' → rekord widoczny w sprawie 006 i w późniejszych sprawach dopiero po jej rozwiązaniu na urządzeniu.
# neutral=True → rekord widoczny zawsze (zwykłe dane, nic nie zdradza).
import json, os, sys, datetime as _D
sys.path.insert(0, os.path.dirname(__file__))
from dbutil import pesel_ok, nip_ok, kw_ok, dowod_ok, pesel as _pesel, dowod as _dowod, kw as _kw

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'baza')

def ps(y, m, d, serial, male): return _pesel(_D.date(y, m, d), serial, male)
PESEL = {
 'ewa': ps(1974, 4, 19, 382, False), 'tomasz': ps(1971, 9, 2, 515, True), 'leon': ps(1953, 1, 11, 207, True),
 'grzegorz': ps(1980, 6, 23, 649, True), 'damian': ps(1995, 2, 14, 731, True), 'joanna': ps(1968, 8, 30, 804, False),
 'lipka': ps(1942, 10, 7, 113, True), 'ewa2': ps(1990, 12, 3, 926, False), 'tomasz2': ps(1985, 3, 17, 458, True),
 'wrzos': ps(1977, 5, 28, 562, False), 'nowak_rew': ps(1966, 11, 9, 671, True), 'pawlak': ps(1969, 7, 4, 239, True),
}
KRS_ARS, NIP_ARS = '0000611480', '7272841237'
KRS_KINA, NIP_KINA = '0000140762', '7251843314'
KRS_REW, NIP_REW = '0000287315', '6762409854'
ARS = 'ARS-LOKUS SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'
KINA = 'ŁÓDZKIE KINA STUDYJNE SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'
REW = 'DOM AUKCYJNY REWERS SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'
ADR_SITEK = 'ul. Lumumby 9/12, 91-404 Łódź'
KW_ZORZA = _kw('LD1M', 87412)

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
 P('O-006-ewa', 'Sitek', ['Ewa', 'Maria'], PESEL['ewa'], '1974-04-19', 'Łódź', 'Henryk', 'Barbara', ADR_SITEK,
   'DEL 40217', '2019-06-03', 'Prezydent Miasta Łodzi', 'zamężna', case='006', rodowe='Kalinowska',
   malzonek={'pesel': PESEL['tomasz'], 'nazwisko': 'Sitek', 'imie': 'Tomasz'}),
 P('O-006-tomasz', 'Sitek', ['Tomasz', 'Adam'], PESEL['tomasz'], '1971-09-02', 'Zgierz', 'Adam', 'Krystyna', ADR_SITEK,
   'DEL 38861', '2018-02-19', 'Prezydent Miasta Łodzi', 'żonaty', case='006',
   malzonek={'pesel': PESEL['ewa'], 'nazwisko': 'Sitek', 'imie': 'Ewa'}),
 P('O-006-ewa2', 'Sitek', ['Ewa'], PESEL['ewa2'], '1990-12-03', 'Gdańsk', 'Marek', 'Alicja', 'ul. Kartuska 140/6, 80-138 Gdańsk',
   'DGS 51204', '2021-01-15', 'Prezydent Miasta Gdańska', 'panna', neutral=True),
 P('O-006-tomasz2', 'Sitek', ['Tomasz'], PESEL['tomasz2'], '1985-03-17', 'Kielce', 'Józef', 'Danuta', 'ul. Warszawska 88/3, 25-547 Kielce',
   'DKI 26690', '2022-09-08', 'Prezydent Miasta Kielce', 'kawaler', neutral=True),
 P('O-006-leon', 'Barcz', ['Leon'], PESEL['leon'], '1953-01-11', 'Łódź', 'Władysław', 'Stefania', 'ul. Gdańska 74/5, 90-731 Łódź',
   'DEL 21144', '2017-03-28', 'Prezydent Miasta Łodzi', 'wdowiec', neutral=True),
 P('O-006-grzegorz', 'Barcz', ['Grzegorz', 'Leon'], PESEL['grzegorz'], '1980-06-23', 'Łódź', 'Leon', 'Halina', 'ul. Grochowska 301/44, 03-823 Warszawa',
   'DKT 70512', '2020-11-30', 'Prezydent m.st. Warszawy', 'rozwiedziony', neutral=True),
 P('O-006-damian', 'Wróbel', ['Damian', 'Paweł'], PESEL['damian'], '1995-02-14', 'Pabianice', 'Paweł', 'Ewelina', 'ul. Zielona 33/2, 90-604 Łódź',
   'DEL 55730', '2023-04-11', 'Prezydent Miasta Łodzi', 'kawaler', neutral=True),
 P('O-006-joanna', 'Rak', ['Joanna', 'Teresa'], PESEL['joanna'], '1968-08-30', 'Łódź', 'Stanisław', 'Teresa', 'ul. Limanowskiego 41/18, 91-030 Łódź',
   'DEL 33092', '2016-10-05', 'Prezydent Miasta Łodzi', 'wdowa', neutral=True, rodowe='Mazur'),
 P('O-006-lipka', 'Lipka', ['Stanisław'], PESEL['lipka'], '1942-10-07', 'Łódź', 'Józef', 'Marianna', 'ul. Gdańska 43/9 (oficyna), 90-730 Łódź',
   'DEL 12608', '2019-01-21', 'Prezydent Miasta Łodzi', 'wdowiec', neutral=True),
 P('O-006-wrzos', 'Wrzos', ['Alicja'], PESEL['wrzos'], '1977-05-28', 'Łódź', 'Tadeusz', 'Irena', 'ul. Narutowicza 60/4, 90-136 Łódź',
   'DEL 47315', '2020-07-14', 'Prezydent Miasta Łodzi', 'zamężna', neutral=True, rodowe='Kępa'),
 P('O-006-nowak', 'Szymański', ['Ryszard'], PESEL['nowak_rew'], '1966-11-09', 'Kraków', 'Jan', 'Zofia', 'ul. Długa 50/7, 31-146 Kraków',
   'DKR 60094', '2018-12-03', 'Prezydent Miasta Krakowa', 'żonaty', neutral=True),
 P('O-006-pawlak', 'Pawlak', ['Andrzej'], PESEL['pawlak'], '1969-07-04', 'Łódź', 'Henryk', 'Maria', 'ul. Piotrkowska 120/3, 90-006 Łódź',
   'DEL 29981', '2017-09-25', 'Prezydent Miasta Łodzi', 'żonaty', neutral=True),
]

def V(id, nr, vin, marka, model, rok, kolor, owner, regd, ins, oc_do, bad, case=None, neutral=None, rodzaj='samochód osobowy'):
    r = {'id': id, 'nr': nr, 'vin': vin, 'marka': marka, 'model': model, 'rok': rok, 'kolor': kolor, 'rodzaj': rodzaj, 'wlasciciel': owner,
         'rejestracja': regd, 'oc': {'ubezpieczyciel': ins, 'do': oc_do}, 'badanie': bad, 'status': 'zarejestrowany'}
    if case: r['case'] = case
    if neutral: r['neutral'] = True
    return r
def own_p(k, name, adres): return {'typ': 'osoba', 'nazwa': name, 'pesel': PESEL[k], 'adres': adres}

pojazdy = [
 V('V-006-sitek', 'EL 4K271', 'VF1RFB00X63519284', 'Renault', 'Captur', 2020, 'beżowy metalik', own_p('tomasz', 'Tomasz Sitek', ADR_SITEK),
   '2020-05-12', 'PZU SA', '2027-05-11', '2027-05-06', neutral=True),
 V('V-006-grzegorz', 'WI 72058', 'WVWZZZAUZJW204417', 'Volkswagen', 'Golf', 2018, 'czarny', own_p('grzegorz', 'Grzegorz Barcz', 'ul. Grochowska 301/44, 03-823 Warszawa'),
   '2021-08-03', 'Link4 SA', '2027-08-02', '2027-07-20', neutral=True),
]

firmy = [
 {'id': 'F-006-ars', 'krs': KRS_ARS, 'nip': NIP_ARS, 'regon': '364112907', 'nazwa': ARS, 'forma': 'spółka z ograniczoną odpowiedzialnością', 'adres': ADR_SITEK,
  'dataWpisu': '2016-04-07', 'kapital': '5 000 zł',
  'zarzad': [{'funkcja': 'PREZES ZARZĄDU', 'nazwisko': 'SITEK', 'imiona': 'TOMASZ ADAM', 'pesel': PESEL['tomasz']}],
  'wspolnicy': [{'nazwa': 'TOMASZ ADAM SITEK', 'udzialy': '100 udziałów o łącznej wartości 5 000 zł'}],
  'pkd': ['47.79.Z Sprzedaż detaliczna artykułów używanych prowadzona w wyspecjalizowanych sklepach', '74.90.Z Pozostała działalność profesjonalna, naukowa i techniczna'],
  'status': 'aktywny', 'case': '006'},
 {'id': 'F-006-kina', 'krs': KRS_KINA, 'nip': NIP_KINA, 'regon': '473215660', 'nazwa': KINA, 'forma': 'spółka z ograniczoną odpowiedzialnością',
  'adres': 'ul. Gdańska 41, 90-730 Łódź', 'dataWpisu': '2002-11-18', 'kapital': '1 200 000 zł',
  'zarzad': [{'funkcja': 'PREZES ZARZĄDU', 'nazwisko': 'PAWLAK', 'imiona': 'ANDRZEJ', 'pesel': PESEL['pawlak']}],
  'wspolnicy': [{'nazwa': 'GMINA MIASTO ŁÓDŹ', 'udzialy': '2 400 udziałów o łącznej wartości 1 200 000 zł'}],
  'pkd': ['59.14.Z Działalność związana z projekcją filmów'], 'status': 'aktywny', 'neutral': True},
 {'id': 'F-006-rew', 'krs': KRS_REW, 'nip': NIP_REW, 'regon': '120481775', 'nazwa': REW, 'forma': 'spółka z ograniczoną odpowiedzialnością',
  'adres': 'ul. Sławkowska 12, 31-014 Kraków', 'dataWpisu': '2007-08-20', 'kapital': '250 000 zł',
  'zarzad': [{'funkcja': 'PREZES ZARZĄDU', 'nazwisko': 'SZYMAŃSKI', 'imiona': 'RYSZARD', 'pesel': PESEL['nowak_rew']}],
  'pkd': ['47.79.Z Sprzedaż detaliczna artykułów używanych prowadzona w wyspecjalizowanych sklepach', '82.99.Z Pozostała działalność wspomagająca prowadzenie działalności gospodarczej'],
  'status': 'aktywny', 'neutral': True},
]

ksiegi = [
 {'id': 'K-006-zorza', 'nr': KW_ZORZA, 'typ': 'działka zabudowana', 'polozenie': 'ul. Gdańska 41, 90-730 Łódź',
  'opis': 'Działka nr 211/4, obręb S-3 Śródmieście, pow. 1 184 m², budynek kina z 1958 r. (sala na 280 miejsc z balkonem), podwórze wspólne z posesją nr 43',
  'wlasciciele': [{'nazwa': KINA, 'krs': KRS_KINA, 'udzial': 'całość'}],
  'podstawa': 'aport Gminy Miasto Łódź, akt notarialny Rep. A nr 5112/2002',
  'hipoteki': [], 'ostrzezenia': ['Wzmianka: umowa przedwstępna sprzedaży nieruchomości z 14.09.2026 (Rep. A nr 9033/2026), wydanie nieruchomości do 31.12.2026'],
  'neutral': True},
]

for o in osoby: assert pesel_ok(o['pesel']), o['id']; assert dowod_ok(o['dowod']['nr']), (o['id'], o['dowod']['nr'])
for f in firmy: assert nip_ok(f['nip']), (f['id'], f['nip'])
for k in ksiegi: assert kw_ok(k['nr']), k['id']
json.dump({'osoby': osoby, 'pojazdy': pojazdy, 'firmy': firmy, 'ksiegi': ksiegi}, open(os.path.join(OUT, 'sprawa-006.json'), 'w'), ensure_ascii=False, indent=1)
print('006 baza: osoby', len(osoby), 'pojazdy', len(pojazdy), 'firmy', len(firmy), 'ksiegi', len(ksiegi), '| KW', KW_ZORZA)
