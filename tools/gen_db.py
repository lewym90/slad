#!/usr/bin/env python3
"""Generator tła ogólnopolskiej bazy danych ŚLAD (osoby, pojazdy, firmy, księgi wieczyste).
Wynik jest deterministyczny (stałe ziarno) i zapisywany na stałe w data/baza/tlo-*.json.
Nie uruchamiać ponownie po wydaniu sprawy korzystającej z bazy — zmieniłoby to rekordy tła.
Rekordy spraw (np. sprawa-005.json) są pisane ręcznie przez skrypty budujące sprawy."""
import json, os, random, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from dbutil import pesel, nip, kw, dowod

R = random.Random(20260313)
OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'baza')
RESERVED = json.load(open(os.path.join(OUT, 'zastrzezone.json'))) if os.path.exists(os.path.join(OUT, 'zastrzezone.json')) else {}

# miasto: (kody pocztowe, prefiksy tablic, sąd wieczystoksięgowy, organ wydający dowody, województwo)
CITIES = [
 ('Warszawa', ['00', '01', '02', '03', '04'], ['WI', 'WE', 'WW', 'WB', 'WN', 'WY'], 'WA1M', 'Prezydent m.st. Warszawy', 'mazowieckie', 30),
 ('Kraków', ['30', '31'], ['KR', 'KK'], 'KR1P', 'Prezydent Miasta Krakowa', 'małopolskie', 14),
 ('Łódź', ['90', '91', '92', '93'], ['EL'], 'LD1M', 'Prezydent Miasta Łodzi', 'łódzkie', 11),
 ('Wrocław', ['50', '51', '52', '53', '54'], ['DW'], 'WR1K', 'Prezydent Wrocławia', 'dolnośląskie', 11),
 ('Poznań', ['60', '61'], ['PO', 'PY'], 'PO1P', 'Prezydent Miasta Poznania', 'wielkopolskie', 9),
 ('Gdańsk', ['80'], ['GD'], 'GD1G', 'Prezydent Miasta Gdańska', 'pomorskie', 8),
 ('Szczecin', ['70', '71'], ['ZS'], 'SZ1S', 'Prezydent Miasta Szczecin', 'zachodniopomorskie', 9),
 ('Bydgoszcz', ['85'], ['CB'], 'BY1B', 'Prezydent Miasta Bydgoszczy', 'kujawsko-pomorskie', 6),
 ('Lublin', ['20'], ['LU'], 'LU1I', 'Prezydent Miasta Lublin', 'lubelskie', 6),
 ('Białystok', ['15'], ['BI'], 'BI1B', 'Prezydent Miasta Białegostoku', 'podlaskie', 5),
 ('Katowice', ['40'], ['SK'], 'KA1K', 'Prezydent Miasta Katowice', 'śląskie', 5),
 ('Gdynia', ['81'], ['GA'], 'GD1Y', 'Prezydent Miasta Gdyni', 'pomorskie', 4),
 ('Rzeszów', ['35'], ['RZ'], 'RZ1Z', 'Prezydent Miasta Rzeszowa', 'podkarpackie', 4),
 ('Toruń', ['87'], ['CT'], 'TO1T', 'Prezydent Miasta Torunia', 'kujawsko-pomorskie', 4),
 ('Kielce', ['25'], ['TK'], 'KI1L', 'Prezydent Miasta Kielce', 'świętokrzyskie', 3),
 ('Olsztyn', ['10'], ['NO'], 'OL1O', 'Prezydent Olsztyna', 'warmińsko-mazurskie', 3),
 ('Opole', ['45'], ['OP'], 'OP1O', 'Prezydent Miasta Opola', 'opolskie', 3),
 ('Koszalin', ['75'], ['ZK'], 'KO1K', 'Prezydent Miasta Koszalina', 'zachodniopomorskie', 3),
 ('Słupsk', ['76'], ['GS'], 'SL1S', 'Prezydent Miasta Słupska', 'pomorskie', 2),
 ('Zamość', ['22'], ['LZ'], 'ZA1Z', 'Prezydent Miasta Zamość', 'lubelskie', 2),
 ('Zakopane', ['34'], ['KTT'], 'NS1Z', 'Burmistrz Miasta Zakopane', 'małopolskie', 1),
 ('Świnoujście', ['72'], ['ZSW'], 'SZ1W', 'Prezydent Miasta Świnoujście', 'zachodniopomorskie', 2),
 ('Kołobrzeg', ['78'], ['ZKL'], 'KO1L', 'Prezydent Miasta Kołobrzeg', 'zachodniopomorskie', 2),
 ('Police', ['72'], ['ZPL'], 'SZ2T', 'Burmistrz Polic', 'zachodniopomorskie', 2),
 ('Goleniów', ['72'], ['ZGL'], 'SZ1O', 'Burmistrz Gminy Goleniów', 'zachodniopomorskie', 1),
 ('Nowy Sącz', ['33'], ['KN'], 'NS1S', 'Prezydent Miasta Nowego Sącza', 'małopolskie', 2),
 ('Płock', ['09'], ['WP'], 'PL1P', 'Prezydent Miasta Płocka', 'mazowieckie', 2),
 ('Elbląg', ['82'], ['NE'], 'EL1E', 'Prezydent Miasta Elbląg', 'warmińsko-mazurskie', 2),
 ('Zielona Góra', ['65'], ['FZ'], 'ZG1Z', 'Prezydent Miasta Zielona Góra', 'lubuskie', 2),
 ('Gorzów Wielkopolski', ['66'], ['FG'], 'GW1G', 'Prezydent Miasta Gorzowa Wlkp.', 'lubuskie', 2),
]
WEIGHTED = [c for c in CITIES for _ in range(c[6])]

STREETS = ['Polna', 'Leśna', 'Słoneczna', 'Krótka', 'Szkolna', 'Ogrodowa', 'Lipowa', 'Brzozowa', 'Łąkowa', 'Kwiatowa', 'Mickiewicza', 'Kościuszki',
 'Sienkiewicza', 'Kolejowa', 'Parkowa', 'Długa', 'Spacerowa', 'Klonowa', 'Akacjowa', 'Słowackiego', 'Żeromskiego', 'Reymonta', 'Kopernika', 'Prusa',
 'Wiśniowa', 'Jaśminowa', 'Różana', 'Sosnowa', 'Dębowa', 'Jesionowa', 'Topolowa', 'Morelowa', 'Wrzosowa', 'Graniczna', 'Cicha', 'Zielona', 'Rzemieślnicza',
 'Fabryczna', 'Piaskowa', 'Okrężna', 'Wąska', 'Kasztanowa', 'Wierzbowa', 'Ogrodnicza', 'Podgórna', 'Słowicza', 'Jodłowa', 'Konwaliowa', 'Bukowa', 'Miodowa']

# nazwisko w formie męskiej → forma żeńska wyliczana
SURNAMES = ['Nowak', 'Kowalski', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Lewandowski', 'Zieliński', 'Szymański', 'Woźniak', 'Dąbrowski',
 'Kozłowski', 'Jankowski', 'Mazur', 'Kwiatkowski', 'Wojciechowski', 'Krawczyk', 'Kaczmarek', 'Piotrowski', 'Grabowski', 'Zając', 'Pawłowski',
 'Michalski', 'Król', 'Wieczorek', 'Jabłoński', 'Wróbel', 'Nowakowski', 'Majewski', 'Olszewski', 'Stępień', 'Malinowski', 'Jaworski', 'Adamczyk',
 'Dudek', 'Nowicki', 'Pawlak', 'Górski', 'Witkowski', 'Walczak', 'Sikora', 'Baran', 'Rutkowski', 'Michalak', 'Szewczyk', 'Ostrowski', 'Tomaszewski',
 'Pietrzak', 'Duda', 'Zalewski', 'Wróblewski', 'Jasiński', 'Marciniak', 'Bąk', 'Zawadzki', 'Sadowski', 'Jakubowski', 'Włodarczyk', 'Chmielewski',
 'Borkowski', 'Sokołowski', 'Szczepański', 'Sawicki', 'Lis', 'Kucharski', 'Mazurek', 'Kubiak', 'Kalinowski', 'Wysocki', 'Maciejewski', 'Czarnecki',
 'Kołodziej', 'Urbański', 'Kaźmierczak', 'Sobczak', 'Konieczny', 'Głowacki', 'Zakrzewski', 'Krupa', 'Wasilewski', 'Laskowski', 'Ziółkowski',
 'Gajewski', 'Szulc', 'Makowski', 'Kaczmarczyk', 'Baranowski', 'Przybylski', 'Domański', 'Nowacki', 'Borowski', 'Błaszczyk', 'Chojnacki', 'Ciesielski',
 'Mróz', 'Szczepaniak', 'Wesołowski', 'Górecki', 'Krajewski', 'Szulc', 'Kraska', 'Pietras', 'Morawiec', 'Kosowski', 'Wilk', 'Sowa', 'Gołąb', 'Kruk',
 'Wrona', 'Czajka', 'Bielecki', 'Rogalski', 'Lewicki', 'Kaczor', 'Kurek', 'Sobolewski', 'Wójtowicz', 'Mikołajczyk', 'Filipek', 'Grzelak', 'Ratajczak',
 'Kostrzewa', 'Leśniak', 'Banaś', 'Fijałkowski', 'Pluta', 'Szostak', 'Kmiecik', 'Rybak', 'Kowal', 'Żak', 'Bednarek', 'Tomczak', 'Matusiak', 'Kołodziejczyk']
MALE = ['Jan', 'Piotr', 'Krzysztof', 'Andrzej', 'Tomasz', 'Paweł', 'Michał', 'Marcin', 'Marek', 'Grzegorz', 'Adam', 'Łukasz', 'Zbigniew', 'Jerzy',
 'Tadeusz', 'Mateusz', 'Dariusz', 'Mariusz', 'Wojciech', 'Ryszard', 'Jakub', 'Henryk', 'Robert', 'Rafał', 'Kazimierz', 'Jacek', 'Maciej', 'Kamil',
 'Janusz', 'Józef', 'Damian', 'Edward', 'Stanisław', 'Sławomir', 'Dawid', 'Bartosz', 'Leszek', 'Lech', 'Adrian', 'Konrad', 'Roman', 'Szymon',
 'Wiesław', 'Bogdan', 'Artur', 'Filip', 'Przemysław', 'Waldemar', 'Sebastian', 'Kacper', 'Zdzisław', 'Witold', 'Eugeniusz', 'Ireneusz']
FEMALE = ['Anna', 'Maria', 'Katarzyna', 'Małgorzata', 'Agnieszka', 'Barbara', 'Ewa', 'Krystyna', 'Elżbieta', 'Magdalena', 'Joanna', 'Zofia',
 'Monika', 'Teresa', 'Danuta', 'Natalia', 'Aleksandra', 'Karolina', 'Marta', 'Beata', 'Dorota', 'Halina', 'Jadwiga', 'Janina', 'Alicja', 'Iwona',
 'Grażyna', 'Renata', 'Justyna', 'Paulina', 'Irena', 'Helena', 'Urszula', 'Wiesława', 'Bożena', 'Jolanta', 'Hanna', 'Kinga', 'Sylwia', 'Agata',
 'Izabela', 'Emilia', 'Weronika', 'Julia', 'Wanda', 'Lucyna', 'Stanisława', 'Genowefa', 'Edyta', 'Patrycja', 'Kamila', 'Marianna', 'Bogumiła']

def fem(s):
    for a, b in (('ski', 'ska'), ('cki', 'cka'), ('dzki', 'dzka')):
        if s.endswith(a): return s[:-len(a)] + b
    return s

def addr(city):
    name, codes = city[0], city[1]
    flat = f'/{R.randint(1, 60)}' if R.random() < 0.65 else ''
    return f'ul. {R.choice(STREETS)} {R.randint(1, 120)}{flat}, {R.choice(codes)}-{R.randint(100, 999)} {name}'

def rdate(a, b):
    return a + datetime.timedelta(days=R.randint(0, (b - a).days))

used = {'pesel': set(RESERVED.get('pesel', [])), 'nr': set(RESERVED.get('nr', [])), 'vin': set(), 'krs': set(RESERVED.get('krs', [])),
        'nip': set(RESERVED.get('nip', [])), 'kw': set(RESERVED.get('kw', [])), 'dowod': set(RESERVED.get('dowod', []))}

def uniq(kind, fn):
    while True:
        v = fn()
        if v and v not in used[kind]: used[kind].add(v); return v

LET = 'ABCDEFGHIJKLMNPRSTUVWXYZ'
osoby = []
for i in range(4200):
    male = R.random() < 0.49
    city = R.choice(WEIGHTED)
    born = rdate(datetime.date(1936, 1, 1), datetime.date(2007, 12, 31))
    sur = R.choice(SURNAMES); sur = sur if male else fem(sur)
    names = [R.choice(MALE if male else FEMALE)]
    if R.random() < 0.35:
        n2 = R.choice(MALE if male else FEMALE)
        if n2 != names[0]: names.append(n2)
    p = uniq('pesel', lambda: pesel(born, R.randint(0, 4999), male))
    issued = rdate(max(born + datetime.timedelta(days=365 * 18), datetime.date(2016, 4, 1)), datetime.date(2025, 12, 31))
    rec = {'id': f'O{i:05d}', 'nazwisko': sur, 'imiona': names, 'pesel': p, 'plec': 'M' if male else 'K', 'urodzony': born.isoformat(),
           'miejsceUr': R.choice(WEIGHTED)[0], 'ojciec': R.choice(MALE), 'matka': R.choice(FEMALE), 'adres': addr(city),
           'dowod': {'nr': uniq('dowod', lambda: dowod(''.join(R.choice(LET[:-2] if j else 'ABCDEFG') for j in range(3)), R.randint(0, 99999))),
                     'wydany': issued.isoformat(), 'wazny': issued.replace(year=issued.year + 10).isoformat() if not (issued.month == 2 and issued.day == 29) else issued.replace(year=issued.year + 10, day=28).isoformat(),
                     'organ': city[4]},
           'stan': 'kawaler' if male else 'panna'}
    if born.year > 2007 - 18: rec['stan'] = 'kawaler' if male else 'panna'
    if R.random() < 0.025 and born.year < 1960:
        rec['zgon'] = rdate(datetime.date(2015, 1, 1), datetime.date(2025, 12, 31)).isoformat()
    rec['_city'] = city[0]
    osoby.append(rec)
# małżeństwa (symetryczne)
adults = [o for o in osoby if o['urodzony'] < '1998-01-01' and 'zgon' not in o]
men = [o for o in adults if o['plec'] == 'M']; women = [o for o in adults if o['plec'] == 'K']
R.shuffle(men); R.shuffle(women)
for m, w in zip(men[:int(len(men) * 0.55)], women):
    if abs(int(m['urodzony'][:4]) - int(w['urodzony'][:4])) > 9: continue
    if R.random() < 0.85: w['rodowe'] = w['nazwisko']; w['nazwisko'] = fem(m['nazwisko'])
    w['adres'] = m['adres']; w['_city'] = m['_city']
    m['stan'] = 'żonaty'; w['stan'] = 'zamężna'
    m['malzonek'] = {'pesel': w['pesel'], 'nazwisko': w['nazwisko'], 'imie': w['imiona'][0]}
    w['malzonek'] = {'pesel': m['pesel'], 'nazwisko': m['nazwisko'], 'imie': m['imiona'][0]}
for o in osoby:
    if o['stan'] in ('kawaler', 'panna') and o['urodzony'] < '1975-01-01' and R.random() < 0.18:
        o['stan'] = 'rozwiedziony' if o['plec'] == 'M' else 'rozwiedziona'

city_of = {c[0]: c for c in CITIES}
ROOTS = ['Bałt', 'Mar', 'Pol', 'Agro', 'Euro', 'Trans', 'Bud', 'Dom', 'Stal', 'Drew', 'Med', 'Inter', 'Lux', 'Nord', 'Fol', 'Kram', 'Wars', 'Sil',
 'Tech', 'Eko', 'Geo', 'Hydro', 'Term', 'Prim', 'Vis', 'Alfa', 'Delta', 'Omega', 'Mega', 'Opti', 'Rol', 'Mleko', 'Piek', 'Auto', 'Mot', 'Elektro']
SUFS = ['-TRANS', '-BUD', 'POL', '-MED', 'EX', '-SERWIS', '-PLAST', 'MAR', '-INVEST', '-DREW', '-STAL', '-LOG', 'TECH', '-SYSTEM', 'PRO', '-HANDEL']
FORMS = [('SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ', 0.7), ('SPÓŁKA AKCYJNA', 0.06), ('SPÓŁKA KOMANDYTOWA', 0.08), ('SPÓŁKA JAWNA', 0.16)]
PKD = ['41.20.Z Roboty budowlane związane ze wznoszeniem budynków', '49.41.Z Transport drogowy towarów', '68.10.Z Kupno i sprzedaż nieruchomości na własny rachunek',
 '68.20.Z Wynajem i zarządzanie nieruchomościami', '47.11.Z Sprzedaż detaliczna w niewyspecjalizowanych sklepach', '62.01.Z Działalność związana z oprogramowaniem',
 '56.10.A Restauracje i inne stałe placówki gastronomiczne', '43.21.Z Wykonywanie instalacji elektrycznych', '45.20.Z Konserwacja i naprawa pojazdów',
 '10.71.Z Produkcja pieczywa', '69.10.Z Działalność prawnicza', '70.22.Z Doradztwo w zakresie prowadzenia działalności gospodarczej', '16.23.Z Produkcja wyrobów stolarskich']
firmy = []
names_used = set()
for i in range(650):
    while True:
        nm = R.choice(ROOTS).upper() + R.choice(SUFS)
        if R.random() < 0.3: nm += ' ' + R.choice(['POLSKA', 'GRUPA', 'PARTNERZY', 'NORD', 'CENTRUM'])
        if nm not in names_used: names_used.add(nm); break
    form = R.choices([f for f, _ in FORMS], [w for _, w in FORMS])[0]
    city = R.choice(WEIGHTED)
    reg = rdate(datetime.date(2002, 1, 1), datetime.date(2025, 6, 30))
    board_n = 1 if R.random() < 0.6 else 2
    board = R.sample([o for o in osoby if o['urodzony'] < '1998-01-01' and 'zgon' not in o], board_n)
    rec = {'id': f'F{i:04d}', 'krs': uniq('krs', lambda: f'0000{R.randint(100000, 999999)}'), 'nip': uniq('nip', lambda: nip(f'{R.randint(100, 999)}{R.randint(100000, 999999)}')),
           'regon': f'{R.randint(100000000, 999999999)}', 'nazwa': f'{nm} {form}', 'forma': form.lower(), 'adres': addr(city).replace('ul.', 'ul.', 1),
           'dataWpisu': reg.isoformat(), 'kapital': f'{R.choice([5000, 10000, 50000, 100000, 200000, 500000]):,} zł'.replace(',', ' '),
           'zarzad': [{'funkcja': 'PREZES ZARZĄDU' if j == 0 else ('WICEPREZES ZARZĄDU' if R.random() < 0.5 else 'CZŁONEK ZARZĄDU'),
                       'nazwisko': b['nazwisko'].upper(), 'imiona': ' '.join(b['imiona']).upper(), 'pesel': b['pesel']} for j, b in enumerate(board)],
           'pkd': R.sample(PKD, 2), 'status': 'aktywny' if R.random() < 0.93 else 'wykreślony'}
    if form in ('SPÓŁKA JAWNA', 'SPÓŁKA KOMANDYTOWA'):
        rec['zarzad'] = [{'funkcja': 'WSPÓLNIK REPREZENTUJĄCY', 'nazwisko': b['nazwisko'].upper(), 'imiona': ' '.join(b['imiona']).upper(), 'pesel': b['pesel']} for b in board]
        rec.pop('kapital')
    firmy.append(rec)

MAKES = [('Skoda', ['Octavia', 'Fabia', 'Superb', 'Kodiaq', 'Karoq']), ('Toyota', ['Corolla', 'Yaris', 'RAV4', 'Auris', 'C-HR']),
 ('Volkswagen', ['Golf', 'Passat', 'Polo', 'Tiguan', 'Touran', 'Transporter']), ('Opel', ['Astra', 'Corsa', 'Insignia', 'Zafira']),
 ('Ford', ['Focus', 'Mondeo', 'Fiesta', 'Kuga', 'Transit']), ('Renault', ['Clio', 'Megane', 'Captur', 'Kangoo']), ('Kia', ['Ceed', 'Sportage', 'Rio']),
 ('Hyundai', ['i30', 'Tucson', 'i20']), ('Dacia', ['Duster', 'Sandero', 'Logan']), ('Audi', ['A4', 'A6', 'A3', 'Q5']), ('BMW', ['Seria 3', 'Seria 5', 'X3']),
 ('Mercedes-Benz', ['Klasa C', 'Klasa E', 'Sprinter', 'Vito']), ('Fiat', ['Panda', 'Tipo', 'Ducato', '500']), ('Peugeot', ['308', '208', '3008', 'Partner']),
 ('Citroën', ['C4', 'C3', 'Berlingo']), ('Mazda', ['3', '6', 'CX-5']), ('Nissan', ['Qashqai', 'Micra', 'X-Trail']), ('Volvo', ['V60', 'XC60', 'S60'])]
COLORS = ['czarny', 'srebrny', 'biały', 'szary', 'granatowy', 'czerwony', 'niebieski', 'zielony', 'grafitowy', 'beżowy', 'brązowy']
VIN = 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789'
INS = ['PZU SA', 'Warta SA', 'Ergo Hestia SA', 'Allianz SA', 'Generali SA', 'Uniqa SA', 'Link4 SA', 'Compensa SA']

def plate(prefix):
    if len(prefix) == 2:
        pats = ['DLLDD', 'DDDLL', 'DDDDD', 'DLDDD', 'DDLLD']
    else:
        pats = ['DLDD', 'DDLL', 'LDDD', 'DDDL']
    p = R.choice(pats)
    return prefix + ' ' + ''.join(R.choice('0123456789') if ch == 'D' else R.choice('ACEFGHJKLMNPRSTUVWXY') for ch in p)

pojazdy = []
for i in range(2400):
    own_firm = R.random() < 0.18
    if own_firm:
        f = R.choice(firmy); city = city_of[f['adres'].rsplit(' ', 1)[-1]] if f['adres'].rsplit(' ', 1)[-1] in city_of else R.choice(WEIGHTED)
        city = next((c for c in CITIES if f['adres'].endswith(c[0])), R.choice(WEIGHTED))
        owner = {'typ': 'firma', 'nazwa': f['nazwa'], 'krs': f['krs'], 'adres': f['adres']}
    else:
        o = R.choice([x for x in osoby if x['urodzony'] < '2006-01-01' and 'zgon' not in x])
        city = city_of[o['_city']]
        owner = {'typ': 'osoba', 'nazwa': f"{' '.join(o['imiona'])} {o['nazwisko']}", 'pesel': o['pesel'], 'adres': o['adres']}
    mk, models = R.choice(MAKES); year = R.randint(2005, 2025)
    regd = rdate(datetime.date(max(year, 2012), 1, 1), datetime.date(2025, 12, 31))
    oc = rdate(datetime.date(2026, 1, 15), datetime.date(2027, 1, 14))
    pojazdy.append({'id': f'V{i:05d}', 'nr': uniq('nr', lambda: plate(R.choice(city[2]))), 'vin': uniq('vin', lambda: ''.join(R.choice(VIN) for _ in range(17))),
                    'marka': mk, 'model': R.choice(models), 'rok': year, 'kolor': R.choice(COLORS), 'rodzaj': 'samochód osobowy' if R.random() < 0.9 else 'samochód ciężarowy (do 3,5 t)',
                    'wlasciciel': owner, 'rejestracja': regd.isoformat(), 'oc': {'ubezpieczyciel': R.choice(INS), 'do': oc.isoformat()},
                    'badanie': rdate(datetime.date(2026, 2, 1), datetime.date(2027, 1, 31)).isoformat(), 'status': 'zarejestrowany'})

TYPES = [('lokal mieszkalny', 'Lokal mieszkalny nr {n}, pow. {a} m², {r} pokoje, kuchnia, łazienka'), ('działka zabudowana', 'Działka nr {d}, pow. {a2} m², budynek mieszkalny jednorodzinny'),
 ('lokal użytkowy', 'Lokal użytkowy nr {n}, pow. {a} m²'), ('działka niezabudowana', 'Działka nr {d}, pow. {a2} m², grunt orny')]
ksiegi = []
for i in range(1400):
    city = R.choice(WEIGHTED); typ, tmpl = R.choice(TYPES)
    num = R.randint(10000, 300000)
    ownersel = R.random()
    if ownersel < 0.12:
        f = R.choice(firmy); owners = [{'nazwa': f['nazwa'], 'krs': f['krs'], 'udzial': 'całość'}]
    else:
        o = R.choice([x for x in osoby if x['urodzony'] < '2004-01-01'])
        owners = [{'nazwa': f"{' '.join(o['imiona'])} {o['nazwisko']}", 'pesel': o['pesel'], 'udzial': 'całość' if 'malzonek' not in o else 'wspólność ustawowa małżeńska'}]
        if 'malzonek' in o:
            m = o['malzonek']; owners.append({'nazwa': f"{m['imie']} {m['nazwisko']}", 'pesel': m['pesel'], 'udzial': 'wspólność ustawowa małżeńska'})
    rec = {'id': f'K{i:05d}', 'nr': uniq('kw', lambda: kw(city[3], R.randint(1000, 299999))), 'typ': typ,
           'polozenie': addr(city), 'opis': tmpl.format(n=R.randint(1, 60), a=R.randint(28, 140), r=R.randint(1, 5), d=f'{R.randint(1, 900)}/{R.randint(1, 40)}', a2=R.randint(300, 2400)),
           'wlasciciele': owners, 'podstawa': R.choice(['umowa sprzedaży', 'umowa darowizny', 'postanowienie o stwierdzeniu nabycia spadku', 'umowa ustanowienia odrębnej własności lokalu']) + f", akt notarialny Rep. A nr {R.randint(100, 9999)}/{R.randint(2005, 2025)}",
           'hipoteki': [] if R.random() < 0.55 else [f"hipoteka umowna {R.randint(8, 90) * 10000:,} zł na rzecz {R.choice(['PKO BP SA', 'Bank Pekao SA', 'mBank SA', 'ING Bank Śląski SA', 'Santander Bank Polska SA'])}".replace(',', ' ')],
           'ostrzezenia': []}
    ksiegi.append(rec)

for o in osoby: o.pop('_city', None)
os.makedirs(OUT, exist_ok=True)
for name, data in (('osoby', osoby), ('pojazdy', pojazdy), ('firmy', firmy), ('ksiegi', ksiegi)):
    json.dump({name: data}, open(os.path.join(OUT, f'tlo-{name}.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    print(name, len(data), os.path.getsize(os.path.join(OUT, f'tlo-{name}.json')) // 1024, 'KB')
