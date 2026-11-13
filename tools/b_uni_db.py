#!/usr/bin/env python3
# Rekordy uniwersum ŚLAD niezwiązane z jedną sprawą (data/baza/uniwersum.json).
# Wszystkie neutral=True: zwykłe dane rejestrowe, widoczne zawsze, niczego nie zdradzają.
# Nie zmieniać po wydaniu — kolejne sprawy mogą dopisywać zmiany jako osobne rekordy (from/to, afterSolved).
import json, os, sys, datetime as D
sys.path.insert(0, os.path.dirname(__file__))
from dbutil import pesel_ok, nip_ok, dowod_ok, pesel as _pesel, dowod as _dowod

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'baza')

P_ANCEL = _pesel(D.date(1958, 2, 9), 417, True)
DOW_ANCEL = _dowod('DWR', 61530)
KRS_VESPER, NIP_VESPER = '0000331908', '8971790345'
ADR_VESPER = 'ul. Kiełbaśnicza 17, 50-110 Wrocław'
VESPER = 'PRACOWNIA KONSERWACJI I EKSPERTYZ PAPIERU VESPER SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'

osoby = [
 {'id': 'O-U-ancel', 'nazwisko': 'Ancel', 'imiona': ['Teodor', 'Feliks'], 'pesel': P_ANCEL, 'plec': 'M', 'urodzony': '1958-02-09', 'miejsceUr': 'Wrocław',
  'ojciec': 'Feliks', 'matka': 'Halina', 'adres': 'ul. Wita Stwosza 3/2, 50-148 Wrocław',
  'dowod': {'nr': DOW_ANCEL, 'wydany': '2019-11-04', 'wazny': '2029-11-04', 'organ': 'Prezydent Wrocławia'}, 'stan': 'wdowiec', 'neutral': True},
]
firmy = [
 {'id': 'F-U-vesper', 'krs': KRS_VESPER, 'nip': NIP_VESPER, 'regon': '021004872', 'nazwa': VESPER, 'forma': 'spółka z ograniczoną odpowiedzialnością',
  'adres': ADR_VESPER, 'dataWpisu': '2009-06-22', 'kapital': '80 000 zł',
  'zarzad': [{'funkcja': 'PREZES ZARZĄDU', 'nazwisko': 'ANCEL', 'imiona': 'TEODOR FELIKS', 'pesel': P_ANCEL}],
  'wspolnicy': [{'nazwa': 'TEODOR FELIKS ANCEL', 'udzialy': '160 udziałów o łącznej wartości 80 000 zł'}],
  'pkd': ['90.03.Z Artystyczna i literacka działalność twórcza', '91.01.B Działalność archiwów',
          '71.20.B Pozostałe badania i analizy techniczne'], 'status': 'aktywny', 'neutral': True},
]

for o in osoby: assert pesel_ok(o['pesel']), o['id']; assert dowod_ok(o['dowod']['nr']), o['id']
for f in firmy: assert nip_ok(f['nip']), (f['id'], f['nip'])
json.dump({'osoby': osoby, 'pojazdy': [], 'firmy': firmy, 'ksiegi': []},
          open(os.path.join(OUT, 'uniwersum.json'), 'w'), ensure_ascii=False, indent=1)
print('uniwersum: osoby', len(osoby), 'firmy', len(firmy))
