# Sprawa 007 „Biała cisza” — miejsca, mapa, zegar, zagadki, raport, zakończenia, bazy (część skryptu build_007.py)
from b007_evidence import N

def spot(id, name, text, gives, requires=None, lockedText=None, expires=None, expiredText=None):
    d = {'id': id, 'name': name, 'text': text, 'gives': gives}
    if requires: d['requires'] = requires; d['lockedText'] = lockedText
    if expires: d['expires'] = expires; d['expiredText'] = expiredText
    return d

clock = {
 'start': f'{N} 08:00', 'par': '19:50', 'unit': 10,
 'costs': {'search': 10, 'ask': 5, 'show': 5, 'confront': 10, 'attach': 5, 'hq': 15, 'listen': 5, 'wait': 30},
 'events': [
  {'id': 'ev-ash', 'at': '12:00', 'title': 'Południe w schronisku',
   'text': 'Zdzisław Hampel, jak co dzień, wyczyścił piec w suszarni i wysypał popiół na hałdę za schroniskiem. Śnieg zaraz go przykryje.'},
  {'id': 'ev-storm', 'at': '13:00', 'public': True, 'weather': 'storm', 'title': 'Śnieżyca',
   'text': 'Z grani zjeżdża biała ściana. Wiatr w porywach do 90 km/h, widać na kilka metrów. GOPR zamyka szlak zielony przez Żleb Mglisty — na przełęcz da się dojść już tylko trasą zimową, wzdłuż tyczek, i to wolniej niż rano.'},
  {'id': 'ev-autopsy', 'at': '15:00', 'public': True, 'title': 'Telefon z Zakładu Medycyny Sądowej',
   'text': 'Biegły z Wrocławia przekazuje wstępne wyniki sekcji. Prokurator prosi, żebyście przeczytali je od razu.', 'gives': ['e36']},
 ]}

MAP = {
 'w': 1000, 'h': 700, 'start': 'hs',
 'note': 'Strzałka w górę — czas podejścia, w dół — zejścia',
 'nodes': [
  {'id': 'hs', 'name': 'Schronisko „Hala Szronów”', 'alt': 1220, 'x': 340, 'y': 500, 'lx': 24, 'ly': 8, 'anchor': 'start', 'hy': 56},
  {'id': 'gar', 'name': 'Garaż ratraków', 'alt': 1210, 'x': 130, 'y': 612, 'lx': 0, 'ly': 42},
  {'id': 'roz', 'name': 'Rozdroże pod Jaworem', 'alt': 1330, 'x': 600, 'y': 330, 'lx': 24, 'ly': 8, 'anchor': 'start'},
  {'id': 'pass', 'name': 'Przełęcz Mglista — schron', 'alt': 1495, 'x': 800, 'y': 125, 'ly': -46},
 ],
 'edges': [
  {'a': 'hs', 'b': 'gar', 't': [3, 3], 'storm': [5, 5], 'kind': 'path', 'name': '', 'lx': 195, 'ly': 580},
  {'a': 'hs', 'b': 'roz', 't': [35, 25], 'storm': [55, 40], 'kind': 'trail', 'name': 'szlak zielony', 'path': 'M340 500 C 420 470, 510 410, 600 330', 'lx': 525, 'ly': 452, 'nx': 400, 'ny': 446},
  {'a': 'roz', 'b': 'pass', 't': [45, 30], 'storm': None, 'closedWhy': 'lawiny w żlebie', 'kind': 'trail', 'name': 'Żleb Mglisty', 'path': 'M600 330 C 680 290, 740 210, 800 125', 'lx': 800, 'ly': 260, 'nx': 800, 'ny': 318},
  {'a': 'hs', 'b': 'pass', 't': [105, 75], 'storm': [130, 95], 'kind': 'winter', 'name': 'trasa zimowa (tyczki)', 'path': 'M340 500 C 230 330, 480 110, 800 125', 'lx': 330, 'ly': 300, 'nx': 470, 'ny': 175},
 ],
 'deco': [
  {'d': 'M560 40 C 700 18, 900 50, 1000 110', 'k': 'ridge'},
  {'d': 'M650 80 C 730 60, 870 90, 950 150 C 890 200, 770 200, 690 170 C 640 150, 620 110, 650 80 Z'},
  {'d': 'M560 140 C 690 110, 910 140, 1000 220 L1000 300 C 900 300, 720 300, 610 260 C 520 230, 500 170, 560 140 Z'},
  {'d': 'M500 250 C 640 210, 900 250, 1000 330 L1000 440 C 860 420, 720 440, 600 420 C 480 400, 430 300, 500 250 Z'},
  {'d': 'M0 470 C 120 440, 240 430, 340 440 C 450 450, 540 500, 620 560 C 660 600, 660 650, 640 700 L0 700 Z', 'k': 'forest'},
  {'d': 'M700 215 L735 195 L770 220 L748 245 Z', 'k': 'rock'},
 ],
 'labels': [{'x': 860, 'y': 32, 't': 'grań Karkonoszy'}, {'x': 140, 'y': 480, 't': 'las regla', 'k': 'small'}],
}

# Położenia śladów na zdjęciach (x, y, r — względem szerokości i wysokości) ustawiane po wygenerowaniu grafik.
locations = [
 {'id': 'office', 'name': 'Biuro gospodarza', 'kind': 'Parter schroniska, przy korytarzu do suszarni', 'at': 'hs',
  'desc': 'Ciasny pokój z biurkiem, kasą schroniska i szafą z kluczami. Na półce radiostacja bazy wyprawy z rejestratorem łączności, obok ładowarka z radiotelefonami. Drzwi się nie zamykają.',
  'spots': [
   spot('sp-radio', 'Radiostacja bazy', 'Radiostacja z rejestratorem — zapisuje każdą łączność.', ['e07', 'e08']),
   spot('sp-charger', 'Ładowarka radiotelefonów', 'Dwa radiotelefony w gniazdach, lista naklejona na obudowie.', ['e09']),
  ]},
 {'id': 'dry', 'name': 'Suszarnia', 'kind': 'Parter schroniska, przy tylnych drzwiach', 'at': 'hs',
  'desc': 'Gorące, duszne pomieszczenie pachnące mokrą wełną. Na stojaku narty i foki, pod ścianą plecaki i buty, w rogu żeliwny piec na drewno. Tylne drzwi prowadzą prosto na zielony szlak.',
  'spots': [
   spot('sp-skis', 'Stojak z nartami', 'Narty i foki całej wyprawy.', ['e10']),
   spot('sp-packs', 'Plecaki pod ścianą', 'Cztery duże plecaki i jeden mały.', ['e11']),
   spot('sp-ash', 'Piec w suszarni', 'Żeliwny piec na drewno, popielnik pełny.', ['e12'], expires='12:00',
        expiredText='Gospodarz wyczyścił piec w południe, jak co dzień. Popiół trafił na hałdę za schroniskiem, pod świeży śnieg.'),
  ],
  'search': {'aspect': 1.5, 'spots': {'sp-skis': [0.3, 0.45, 0.08], 'sp-packs': [0.62, 0.72, 0.07], 'sp-ash': [0.86, 0.55, 0.07]}}},
 {'id': 'terrace', 'name': 'Taras', 'kind': 'Pierwsze piętro schroniska, nad drzwiami suszarni', 'at': 'hs',
  'desc': 'Drewniany taras z widokiem na zielony szlak. Na statywie wciąż stoi aparat Igora, przysypany śniegiem.',
  'spots': [spot('sp-tl', 'Aparat na statywie', 'Aparat ustawiony na szlak i drzwi suszarni.', ['e13'])]},
 {'id': 'dining', 'name': 'Jadalnia', 'kind': 'Parter schroniska', 'at': 'hs',
  'desc': 'Długie drewniane stoły, kominek, zdjęcia z dawnych wypraw na ścianach. W kącie stolik z laptopem wyprawy i dyskami Igora. Na stole wciąż leży talia kart.',
  'spots': [
   spot('sp-photos', 'Zdjęcia na ścianie', 'Fotografie z wypraw i obozu.', ['e15']),
   spot('sp-laptop', 'Laptop wyprawy', 'Wspólny laptop z materiałami filmowymi.', ['e14'], requires={'all': ['st:i-c3']},
        lockedText='Na laptopie są tysiące plików. Najpierw ustalcie, czego właściwie szukać i kto go używa.'),
  ]},
 {'id': 'room6', 'name': 'Pokój nr 6', 'kind': 'Piętro schroniska — pokój Weroniki Kos', 'at': 'hs',
  'desc': 'Mały pokój z jednym łóżkiem, kaloryferem i stolikiem. Okno wychodzi na zaśnieżony szlak.',
  'spots': [
   spot('sp-room', 'Kaloryfer i stolik', 'Rzeczy rozłożone do suszenia, tabletki, woda.', ['e16'], requires={'all': ['lie:w-l1']},
        lockedText='Bez zgody prokuratora nie przeszukacie pokoju. Najpierw wykażcie, że jego lokatorka mija się z prawdą o tym, gdzie była w nocy.'),
   spot('sp-phone', 'Telefon Weroniki', 'Telefon w etui z logo Polar-Tex.', ['e17'], requires={'all': ['lie:w-l2']},
        lockedText='Prokurator zgodzi się na przeszukanie telefonu, gdy wykażecie, że jego właścicielka była tej nocy na przełęczy.'),
  ]},
 {'id': 'notes', 'name': 'Kwatera śledczych', 'kind': 'Schronisko, pokój nr 1 — wasze notatki', 'at': 'hs',
  'desc': 'Stół zawalony aktami, termos z herbatą od gospodarza. Tu trafiają wyniki waszych obliczeń i zestawień.',
  'spots': [
   spot('sp-calc', 'Wyliczenie z wydruku GPS', 'Wynik zagadki „Szósty dzień”.', ['e29'], requires={'puzzle': 'p-track'},
        lockedText='Wydruk śladu GPS z 2025 roku kryje liczbę, którą trzeba policzyć — zagadka „Szósty dzień”.'),
   spot('sp-alibi', 'Zestawienie alibi', 'Wynik zagadki „Okno 22:50”.', ['e30'], requires={'puzzle': 'p-alibi'},
        lockedText='Zestawcie, gdzie kto był o 22:50 — zagadka „Okno 22:50”.'),
  ]},
 {'id': 'fork', 'name': 'Rozdroże pod Jaworem', 'kind': 'Szlak zielony, 1330 m n.p.m.', 'at': 'roz',
  'desc': 'Drogowskaz oblepiony szadzią, karłowate świerki. Wyżej szlak wchodzi w wąski Żleb Mglisty, którym wiatr przewiewa śnieg.',
  'spots': [spot('sp-tracks', 'Pobocze szlaku', 'Zawietrzna pod skałami, tuż przy szlaku.', ['e18'], expires='13:00',
                 expiredText='Śnieżyca zasypała wszystko równą warstwą. Jeśli były tu jakieś ślady, już ich nie ma.')]},
 {'id': 'shelter', 'name': 'Wnętrze schronu', 'kind': 'Przełęcz Mglista, 1495 m — kamienny schron z 1936 roku', 'at': 'pass',
  'desc': 'Jedna izba z pryczami, żeliwny piec, stół pod oknem z radiostacją i stosem baterii. Szyby od środka pokryte szronem. Przy drzwiach czeka ratownik GOPR.',
  'spots': [
   spot('sp-stove', 'Żeliwny piec', 'Piec przy pryczach, obok wiadro z węglem.', ['e19']),
   spot('sp-notebook', 'Zeszyt na stole', 'Zeszyt w kratkę z ołówkiem w środku.', ['e20']),
   spot('sp-logger', 'Rejestrator przy bateriach', 'Mały szary rejestrator z wyświetlaczem.', ['e21']),
   spot('sp-station', 'Radiostacja', 'Stacja stała z mikrofonem na haczyku.', ['e22']),
   spot('sp-cap', 'Czapka i rękawice', 'Leżą na stole, obok zeszytu.', ['e23']),
   spot('sp-satcable', 'Powerbank przy pryczy', 'Kabel ładowania prowadzi donikąd.', ['e24']),
   spot('sp-bag', 'Plecak Krystiana', 'Duży plecak oparty o pryczę.', ['e25']),
  ],
  'search': {'aspect': 1.5, 'spots': {'sp-stove': [0.18, 0.55, 0.07], 'sp-notebook': [0.52, 0.62, 0.04], 'sp-logger': [0.62, 0.58, 0.035], 'sp-station': [0.58, 0.42, 0.05],
                                      'sp-cap': [0.43, 0.6, 0.035], 'sp-satcable': [0.84, 0.72, 0.045], 'sp-bag': [0.93, 0.5, 0.05]}}},
 {'id': 'rock', 'name': 'Skała z masztem', 'kind': 'Przełęcz Mglista — piętnaście metrów od schronu', 'at': 'pass',
  'desc': 'Czterometrowa skała z przykręconą stalową drabinką i masztem anteny. U jej stóp, pod złotą folią NRC, leży ciało Krystiana Lisa. Ratownik czeka na wasze oględziny, żeby zwieźć je skuterem.',
  'spots': [
   spot('sp-body', 'Ciało pod skałą', 'Pod folią, w zawianym śniegu.', ['e26']),
   spot('sp-mast', 'Drabinka i maszt', 'Szczeble pokryte szadzią.', ['e27']),
  ]},
 {'id': 'garage', 'name': 'Garaż ratraków', 'kind': 'Sto metrów poniżej schroniska', 'at': 'gar',
  'desc': 'Blaszany garaż z dwoma ratrakami, beczkami paliwa i pokoikiem operatora za ścianką z płyty. Pachnie ropą i kawą z termosu.',
  'spots': [spot('sp-ratrak', 'Kabina ratraku', 'Na fotelu leży wydruk z GPS.', ['e28'])]},
]

puzzles = [
 {'id': 'p-track', 'kind': 'Obliczenie', 'title': 'Szósty dzień',
  'prompt': 'Wydruk śladu GPS z 2025 roku pokazuje dwa kolejne punkty z jednego marcowego dnia. Z jaką średnią prędkością poruszał się wtedy Adam Rogala? Podajcie wynik w km/h.',
  'requires': ['e25'], 'input': 'number', 'answers': ['34-36'],
  'hints': ['Znajdźcie na wydruku dwa punkty z tego samego dnia i policzcie, ile godzin minęło między nimi.',
            'Między 9:10 a 15:10 minęło sześć godzin. Podzielcie przez to odległość między punktami.',
            '210 km podzielone przez 6 godzin to 35 km/h. W inne dni Adam robił po 17–19 km na dobę.'],
  'solution': '210 km w sześć godzin to 35 km/h — tyle, ile w inne dni przechodził przez cały tydzień. Tak szybko nie idzie nikt na nartach z pulką. Tak jedzie skuter śnieżny.',
  'reward': {'search': True, 'spots': ['sp-calc']}},
 {'id': 'p-alibi', 'kind': 'Zestawienie', 'title': 'Okno 22:50',
  'prompt': 'O 22:50 ktoś otworzył drzwi schronu na przełęczy. Ustalcie, gdzie o tej godzinie był każdy, kto nocował w schronisku.',
  'requires': ['st:h-c1', 't8', 't9', 'e28', 'st:k-c1', 'e21'], 'input': 'grid',
  'grid': {
   'rows': [{'id': 'adam', 'label': 'Adam Rogala'}, {'id': 'hampel', 'label': 'Zdzisław Hampel'}, {'id': 'igor', 'label': 'Igor Szadkowski'},
            {'id': 'natalia', 'label': 'Natalia Brandt'}, {'id': 'kuznik', 'label': 'Mirosław Kuźnik'}, {'id': 'weronika', 'label': 'Weronika Kos'}],
   'cols': [{'id': 't', 'label': 'O 22:50'}],
   'options': [{'id': 'jad', 'label': 'jadalnia i bar'}, {'id': 'n4', 'label': 'pokój nr 4'}, {'id': 'gar', 'label': 'garaż ratraków'}, {'id': 'pass', 'label': 'schron na przełęczy'}],
   'constraints': [
    {'t': 'is', 'r': 'adam', 'c': 't', 'v': 'jad', 'src': ['st:h-c1'], 'why': 'Gospodarz widział, jak Adam pisał w jadalni do 23:20.'},
    {'t': 'is', 'r': 'hampel', 'c': 't', 'v': 'jad', 'src': ['st:h-c1'], 'why': 'Gospodarz siedział w barze przy jadalni do 23:20 — razem z Adamem gasili światło.'},
    {'t': 'is', 'r': 'igor', 'c': 't', 'v': 'n4', 'src': ['t8'], 'why': 'Igor przyznał, że od 22:00 do 0:30 był w pokoju Natalii.'},
    {'t': 'same', 'r1': 'natalia', 'r2': 'igor', 'c': 't', 'src': ['t9'], 'why': 'Natalia potwierdza: Igor był z nią.'},
    {'t': 'is', 'r': 'kuznik', 'c': 't', 'v': 'gar', 'src': ['e28', 'st:k-c1'], 'why': 'O 22:40 ratrak wrócił do garażu, a jego operator miał tam przerwę — do przełęczy jest stamtąd ponad godzina drogi.'},
    {'t': 'exactly', 'c': 't', 'v': 'pass', 'n': 1, 'src': ['e21'], 'why': 'O 22:50 ktoś otworzył drzwi schronu — tak pokazuje rejestrator temperatury.'},
   ]},
  'answers': [{'adam': {'t': 'jad'}, 'hampel': {'t': 'jad'}, 'igor': {'t': 'n4'}, 'natalia': {'t': 'n4'}, 'kuznik': {'t': 'gar'}, 'weronika': {'t': 'pass'}}],
  'hints': ['Zacznijcie od tych, których ktoś widział: gospodarz i Adam mają siebie nawzajem, Igor i Natalia też.',
            'Ratrakowy o 22:40 skończył równać drogę poniżej schroniska i wrócił do garażu. Rejestrator w schronie pokazuje, że o 22:50 ktoś otworzył drzwi.',
            'Tylko jedna osoba nie ma nikogo, kto by ją widział o 22:50: Weronika Kos. To ona była w schronie.'],
  'solution': 'O 22:50 Adam i gospodarz byli w jadalni, Igor z Natalią w pokoju nr 4, a ratrakowy w garażu. Drzwi schronu na przełęczy mogła otworzyć tylko Weronika Kos.',
  'reward': {'search': True, 'spots': ['sp-alibi']}},
]

hintTrail = [
 {'unless': ['sp-radio'], 'text': 'Zacznijcie od biura gospodarza. Radiostacja bazy zapisuje każdą łączność — sprawdźcie, co nadano w nocy.'},
 {'unless': ['show:a-s1'], 'when': ['e07'], 'text': 'W dzienniku łączności przy każdym nadaniu jest numer radiotelefonu. Który radiotelefon to który? Zapytajcie kierownika wyprawy albo zajrzyjcie do ładowarki.'},
 {'unless': ['sp-station'], 'when': ['e07'], 'text': 'Ktoś musi wejść na przełęcz i obejrzeć schron. Zróbcie to przed 13:00 — po śnieżycy droga wydłuży się prawie dwukrotnie.'},
 {'unless': ['m-dog'], 'when': ['e08'], 'text': 'Odsłuchajcie nagranie łączności z 0:40 i zaznaczcie dźwięki w tle. Tło zdradza, skąd nadawano.'},
 {'unless': ['show:i-s1'], 'when': ['e34'], 'text': 'W nagraniu z 0:40 ktoś na końcu mówi „mam”. Pokażcie ten dźwięk osobie, która tak kończy swoje ujęcia.'},
 {'unless': ['sp-laptop'], 'when': ['st:i-c3'], 'text': 'Klip z łącznością Krystiana jest na laptopie wyprawy w jadalni. Sprawdźcie, co się z nim działo w piątek.'},
 {'unless': ['sp-skis'], 'when': ['e21'], 'text': 'Rejestrator w schronie pokazuje, kiedy ktoś otwierał drzwi. Kto mógł zdążyć tam i z powrotem? Zajrzyjcie do suszarni — narty i foki pamiętają noc.'},
 {'unless': ['lie:w-l1'], 'when': ['e10'], 'text': 'Czyje foki były rano mokre? Skonfrontujcie to z zeznaniem o nocy spędzonej w pokoju.'},
 {'unless': ['lie:i-l1'], 'when': ['e13'], 'text': 'Na klatkach z tarasu nikt nie stoi przy aparacie. Kto twierdził, że stał przy nim całą noc?'},
 {'unless': ['p-alibi'], 'when': ['t8', 't9', 'e28'], 'text': 'Zestawcie, gdzie kto był o 22:50 — zagadka „Okno 22:50” w zakładce Analiza.'},
 {'unless': ['lie:w-l2'], 'when': ['lie:w-l1'], 'text': 'Weronika twierdzi, że doszła tylko do rozdroża. Dokąd prowadzi ślad komunikatora Krystiana — i kiedy zjechał z przełęczy?'},
 {'unless': ['lie:w-l5'], 'when': ['lie:w-l2'], 'text': 'Kto i kiedy odchodził od stołu przy kartach? Zapytajcie gospodarza i zestawcie to z ostatnim zeznaniem Weroniki.'},
 {'unless': ['p-track'], 'when': ['e25'], 'text': 'W teczce Krystiana jest ślad GPS z 2025 roku. Policzcie prędkość z szóstego dnia — zagadka „Szósty dzień”.'},
 {'text': 'Macie dość, by złożyć raport. Najważniejsze: kto był w schronie między 22:50 a 23:20 i kto nadał łączność o 0:40.'},
]

report = {'questions': [
 {'id': 'r-who', 'q': 'Kto odpowiada za śmierć Krystiana Lisa?', 'type': 'single', 'points': 16,
  'options': [['weronika', 'Weronika Kos, menedżerka wyprawy'], ['adam', 'Adam Rogala, kierownik wyprawy'], ['igor', 'Igor Szadkowski, operator kamery'],
              ['natalia', 'Natalia Brandt, lekarka wyprawy'], ['accident', 'Nikt — to był wypadek, Krystian spadł ze skały']],
  'correct': 'weronika',
  'proof': {'count': 3, 'each': 4, 'valid': ['e10', 'e11', 'e12', 'e13', 'e14', 'e16', 'e17', 'e18', 'e30', 'x2', 'x3', 't3', 't4', 't5', 't6', 't7', 'd02'],
            'label': 'Wskażcie trzy dowody, które najmocniej łączą tę osobę ze zbrodnią.'}},
 {'id': 'r-call', 'q': 'Kto i jak nadał łączność o 0:40?', 'type': 'single', 'points': 12,
  'options': [['weronika', 'Weronika Kos — zapasowym radiotelefonem zza tylnych drzwi schroniska, puszczając z telefonu czwartkowe nagranie Igora'],
              ['krystian', 'Krystian Lis — ze stacji w schronie, tuż przed wyjściem do masztu'],
              ['adam', 'Adam Rogala — z pokoju, naśladując głos Krystiana'],
              ['igor', 'Igor Szadkowski — z tarasu, z własnego nagrania']],
  'correct': 'weronika'},
 {'id': 'r-time', 'q': 'Kiedy Krystian został zaatakowany?', 'type': 'single', 'points': 12,
  'options': [['2250', 'Między 22:50 a 23:20, w schronie'], ['0040', 'Po łączności o 0:40, przy maszcie'], ['0600', 'Nad ranem, tuż przed łącznością o 6:00'], ['2200', 'Jeszcze przed łącznością o 22:05']],
  'correct': '2250'},
 {'id': 'r-route', 'q': 'Jak sprawczyni zdążyła dotrzeć na przełęcz i wrócić?', 'type': 'single', 'points': 10,
  'options': [['ski', 'Na nartach skiturowych, szlakiem zielonym: podejście w niespełna godzinę, zjazd w 20 minut'],
              ['foot', 'Pieszo, w rakietach: 1 h 20 min w górę i 55 min w dół'],
              ['ratrak', 'Ratrakiem, trasą zimową'], ['skuter', 'Skuterem GOPR']],
  'correct': 'ski'},
 {'id': 'r-death', 'q': 'Co było przyczyną śmierci Krystiana?', 'type': 'single', 'points': 10,
  'options': [['cold', 'Wychłodzenie — nieprzytomnego po uderzeniu o piec wyciągnięto na śnieg'], ['fall', 'Upadek ze skały z masztem'],
              ['stove', 'Uderzenie głową o piec — zginął na miejscu'], ['pole', 'Cios kijkiem narciarskim']],
  'correct': 'cold'},
 {'id': 'r-motive', 'q': 'Jaki był motyw?', 'type': 'single', 'points': 8,
  'options': [['fraud', 'Krystian chciał ujawnić, że część „samotnego” przejścia Spitsbergenu odbyła się skuterem, a ona to tuszowała'],
              ['money', 'Krystian był jej winien pieniądze'], ['love', 'Zazdrość o Igora'], ['contract', 'Krystian chciał przejąć kontrakt sponsorski']],
  'correct': 'fraud'},
 {'id': 'r-liars', 'q': 'Kto skłamał w zeznaniach, choć nie zabił?', 'type': 'multi', 'points': 10,
  'hint': 'Zaznaczcie wszystkie właściwe odpowiedzi. Każda błędna odejmuje punkty za trafną.',
  'options': [['adam', 'Adam Rogala'], ['igor', 'Igor Szadkowski'], ['natalia', 'Natalia Brandt'], ['hampel', 'Zdzisław Hampel'], ['kuznik', 'Mirosław Kuźnik']],
  'correct': ['adam', 'igor', 'natalia']},
 {'id': 'r-order', 'q': 'Ułóżcie wydarzenia we właściwej kolejności.', 'type': 'order', 'points': 10,
  'items': [['clip', 'Igor nagrywa łączność Krystiana z bazą'], ['msg', 'Krystian wysyła z komunikatora SMS do Weroniki'], ['copy', 'Klip C0112 trafia na telefon Weroniki'],
            ['call', 'Ostatnia prawdziwa łączność Krystiana'], ['door', 'Ktoś otwiera drzwi schronu — pierwszy spadek temperatury'], ['down', 'Komunikator Krystiana zjeżdża z przełęczy do schroniska'],
            ['fake', 'Łączność z radiotelefonu nr 04'], ['none', 'Schron nie odpowiada na wywołanie bazy']],
  'correct': ['clip', 'msg', 'copy', 'call', 'door', 'down', 'fake', 'none']},
]}

solution = {
 'summary': 'Krystiana Lisa zostawiła na śmierć Weronika Kos. Łącznościowiec miał dowody, że część „samotnego” przejścia Spitsbergenu w 2025 roku Adam Rogala odbył skuterem, a Kos — członkini zarządu sponsora — wiedziała o tym i zatuszowała sprawę. W piątek o 19:12 Krystian napisał jej, że w poniedziałek ujawni wszystko. Kos wyszła nocą na nartach, o 22:50 weszła do schronu, odepchnęła go — uderzył głową o kant pieca i stracił przytomność. Wyciągnęła go pod skałę z masztem, żeby wyglądało na upadek, i zostawiła na mrozie. Zjechała w 20 minut, spaliła jego komunikator w suszarni, a o 0:40 nadała z zapasowego radiotelefonu czwartkowe nagranie jego głosu, żeby wszyscy uwierzyli, że po północy jeszcze żył.',
 'steps': [
  {'h': 'To nie był upadek', 'p': 'Szadź na drabince nienaruszona, czapka i rękawice na stole, na kancie pieca krew i włosy, a na piętach i plecach otarcia od ciągnięcia. Sekcja: uraz głowy tylko go ogłuszył, zabił go mróz.'},
  {'h': 'Łączność, której nie nadał Krystian', 'p': 'Stacja w schronie ostatni raz nadawała o 22:05. Łączność z 0:40 przyszła z radiotelefonu nr 04, który zawsze stoi w biurze schroniska. Słowa — minus dwadzieścia dwa, wiatr ucichł — pasują do nocy z czwartku, nie do piątkowej, gdy na przełęczy wiało 60 km/h. W tle wieje wiatr, szczeka Bari i pika cofający ratrak, który równał wtedy plac przed schroniskiem. Na końcu Igor mówi „mam”: to jego czwartkowy klip C0112.'},
  {'h': 'Prawdziwa godzina', 'p': 'Ostatni wpis w zeszycie testu: 22:30. Rejestrator temperatury: drzwi otwarte około 22:50 i 23:20, potem już nikt nie dokładał do pieca. Na ciele 12–14 cm nawianego śniegu, a pod nim stary śnieg — leżało tam, zanim zaczęło mocno nawiewać.'},
  {'h': 'Kto mógł zdążyć', 'p': 'Pieszo w obie strony to 2 godziny 15 minut, a na nartach — niewiele ponad godzinę. O 22:50 Adam i gospodarz byli w jadalni, Igor z Natalią w pokoju nr 4, ratrakowy w garażu. Od 21:45 do 0:15 nikt nie widział tylko Weroniki Kos.'},
  {'h': 'Nocne narty', 'p': 'Rano tylko jej foki były mokre i oblodzone. Ślad nart szerokich na 8,5 cm prowadził przez rozdroże w żleb — jej narty mają 85 mm. Ratrakowy widział czołówkę idącą w górę o 22:10 i światło zjeżdżające po 23:30. O 23:41 aparat Igora sfotografował kogoś z nartami i małym plecakiem z żółtą taśmą — jej plecakiem.'},
  {'h': 'Komunikator', 'p': 'Komunikator Krystiana o 23:20 był w schronie, o 23:30 przy rozdrożu, o 23:40 w schronisku — 3,4 km w 20 minut, czyli zjazd na nartach. Potem go wyłączono, a jego stopione resztki trafiły do pieca w suszarni.'},
  {'h': 'Nagranie w telefonie', 'p': 'O 21:32 klip C0112 trafił z laptopa wyprawy na telefon Weroniki. O 0:35 odeszła od stołu przy kartach; o 0:39 odtworzyła klip, a o 0:40 radio w biurze nadało go jako łączność z przełęczy.'},
  {'h': 'Motyw i fałszywe tropy', 'p': 'Krystian napisał do niej o 19:12, że w poniedziałek powie wszystko — „o Adamie i o Tobie”. Kos zamówiła ekspertyzę dziennika, wypłaciła premię i poświadczyła zarządowi nieprawdę. Adam kłamał o kłótni i o Spitsbergenie, Igor i Natalia — o wspólnej nocy. Żadne z nich nie mogło być o 22:50 na przełęczy.'},
 ]}

endings = {
 'correct': {'title': 'Biała cisza', 'text': 'Weronika Kos zostaje zatrzymana jeszcze w schronisku, gdy śnieżyca na chwilę cichnie. Poniedziałkowa konferencja Polar-Tex się nie odbywa. Ciało Krystiana zjeżdża skuterem do Karpacza, a na maszcie przy schronie ratownicy wieszają jego czapkę — taki zwyczaj w Karkonoszach.',
  'decision': {'q': 'Krystiana nie ma, ale jego dowody zostały. Co z nimi zrobicie?', 'options': [
   {'id': 'sponsor', 'label': 'Przekazać zarządowi Polar-Tex i prokuraturze komplet dowodów o premii za sfałszowane przejście', 'text': 'Polar-Tex zrywa kontrakt na Grenlandię i żąda zwrotu 600 000 zł. Adam Rogala odpowiada za wyłudzenie, „Dziennik Lodu” znika z księgarń. W wywiadzie mówi tylko jedno zdanie: „Krystian miał rację, a ja miałem czas do poniedziałku”.'},
   {'id': 'memorial', 'label': 'Poprosić GOPR, by nowa stacja łączności na przełęczy nosiła imię Krystiana Lisa', 'text': 'Wiosną na schronie zawisa mosiężna tabliczka: „Stacja łączności im. Krystiana Lisa — on zawsze się zgłaszał”. Łącznościowcy z całej Polski przez tydzień nadają z przełęczy jego znak wywoławczy.'},
   {'id': 'vesper', 'label': 'Zlecić niezależną ekspertyzę „Dziennika Lodu” i sprawdzić, jak powstała ta z 2025 roku', 'text': 'Biegły z Krakowa stwierdza, że część kartek dziennika to palimpsest: pierwotny tekst wywabiono i napisano nowy, na tym samym papierze. Pracownia VESPER odpowiada uprzejmym pismem, że ekspertyzę wykonano rzetelnie, na podstawie dostarczonych materiałów. Podpisuje prezes, Teodor Ancel. Do pisma dołączono katalog usług pracowni.'},
  ]}},
 'wrong': {
  'adam': {'title': 'Czas do poniedziałku', 'text': 'Kłótnia, sfałszowany wyczyn, groźba kompromitacji — wszystko wskazywało na Adama. Tyle że o 22:50 pisał w jadalni na oczach gospodarza, a pieszo nie zdążyłby na przełęcz nawet do północy. Weronika Kos wraca do Warszawy i usuwa z telefonu jeden klip.'},
  'igor': {'title': 'Klip', 'text': 'Głos z nocnej łączności pochodził z nagrania Igora, więc wskazujecie jego. Ale Igor przez całą noc był w pokoju nr 4, a klipu z laptopa nie kopiował. Prawdziwa sprawczyni ma czas, by zatrzeć resztę śladów.'},
  'natalia': {'title': 'Pokój nr 4', 'text': 'Natalia skłamała o nocy, ale nie po to, by kogoś zabić. Była z Igorem i żadne z nich nie wychodziło ze schroniska. Śledztwo traci dni, których nie odzyska.'},
  'accident': {'title': 'Upadek ze skały', 'text': 'Uznajecie, że Krystian spadł, sprawdzając antenę. Dokładnie tak miało to wyglądać. Szadź na drabince, czapka na stole i łączność z radiotelefonu nr 04 zostają w aktach, których nikt już nie otworzy.'},
 },
 'partial': 'Wskazaliście właściwą osobę, ale część wniosków jest błędna albo niepoparta dowodami. Kos zostaje zatrzymana, lecz jej obrona będzie mówić o nieszczęśliwym wypadku i panice.',
}

breakthroughs = [
 {'id': 'b-voice', 'when': 'show:i-s1', 'title': 'Głos z czwartku', 'text': 'Głos, który po północy uspokoił całe schronisko, nagrano dobę wcześniej. Ktoś puścił do radia czwartkowy klip Igora.'},
 {'id': 'b-skis', 'when': 'lie:w-l1', 'title': 'Nocne narty', 'text': 'Weronika Kos nie spała z migreną. Kiedy schronisko myślało, że śpi, ona miała na nogach narty, a pod nartami foki.'},
 {'id': 'b-window', 'when': 'p-alibi', 'title': 'Okno 22:50', 'text': 'O 22:50 ktoś otworzył drzwi schronu na przełęczy. Każdy w schronisku ma na tę chwilę świadka — każdy poza jedną osobą.'},
 {'id': 'b-cold', 'when': 'e36', 'title': 'Biała cisza', 'text': 'Krystian Lis nie zginął od uderzenia. Żył, kiedy ktoś wyciągnął go na śnieg pod skałę i odszedł. Zabił go mróz.'},
]

tableMode = {'parBonus': 8, 'locations': [
 {'id': 'hq', 'name': 'Centrala wydziału', 'kind': 'Zapytania przez telefon satelitarny ratownika',
  'desc': 'Ratownik GOPR ma telefon satelitarny i łączność z dyżurką w Karpaczu. Każde zapytanie to 15 minut czekania na odpowiedź.',
  'img': 'assets/places/001-hq.webp',
  'spots': [
   spot('sp-hq-meteo', 'IMGW', 'Prosicie o dane ze stacji meteo na przełęczy z ostatnich nocy.', ['x1']),
   spot('sp-hq-sms', 'Operator SAT-COM — wiadomości', 'Prosicie o wiadomości wysłane z komunikatora Krystiana.', ['x2'], requires={'all': ['e24']},
        lockedText='Nie wiecie jeszcze, czy Krystian miał jakiś komunikator satelitarny.'),
   spot('sp-hq-track', 'Operator SAT-COM — pozycje', 'Prosicie o zapis pozycji komunikatora Krystiana.', ['x3'], requires={'all': ['e24']},
        lockedText='Nie wiecie jeszcze, czy Krystian miał jakiś komunikator satelitarny.'),
   spot('sp-hq-sponsor', 'Zarząd Polar-Tex', 'Prosicie o umowy sponsorskie i dokumenty z 2025 roku.', ['x4'], requires={'all': ['e25']},
        lockedText='Nie macie jeszcze powodu, by pytać zarząd sponsora o dokumenty.'),
   spot('sp-hq-snow', 'GOPR — pole pomiarowe', 'Prosicie o pomiar nawianego śniegu przy schronie.', ['x5']),
  ]}], 'questions': {}}

db = {'date': N, 'bases': ['osoby', 'pojazdy', 'firmy', 'ksiegi'], 'attach': [
 {'rec': 'F-007-polartex', 'ev': 'd01', 'paths': [{'q': {'nazwa': 'Polar-Tex'}, 'from': ['e06']}]},
 {'rec': 'O-007-weronika', 'ev': 'd02', 'paths': [{'q': {'nazwisko': 'Kos', 'imie': 'Weronika'}, 'from': ['e06']}]},
 {'rec': 'F-007-rogala', 'ev': 'd03', 'paths': [{'q': {'nazwa': 'Rogala Expeditions'}, 'from': ['x4']}]},
]}

novelties = [
 {'name': 'Zegar w grze', 'text': 'W tej sprawie zamiast ruchów liczy się czas. Każda czynność trwa kilka minut, a przejście szlakiem — tyle, ile pokazuje mapa. Zegar stoi, kiedy nic nie robicie. O ustalonych godzinach dzieją się rzeczy, na które nie macie wpływu.',
  'where': 'Godzina na górnym pasku — stuknijcie ją, żeby zobaczyć plan dnia.'},
 {'name': 'Mapa szlaków', 'text': 'Przeszukujecie tylko miejsca w punkcie mapy, w którym jesteście, i rozmawiacie tylko z osobami, które są obok. Żeby gdzieś przejść, stuknijcie punkt na mapie.',
  'where': 'Zakładka Miejsca, na samej górze.'},
 {'name': 'Dowód dźwiękowy', 'text': 'Nagranie można odsłuchać, zatrzymać w dowolnym miejscu i wskazać, co słychać w tle. Pudło nic nie kosztuje.',
  'where': 'Dokument z nagraniem w aktach — przycisk „Odsłuchaj i analizuj nagranie”.'},
]
