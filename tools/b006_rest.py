# Sprawa 006 „Ostatni seans” — miejsca, zagadki, raport, zakończenia, bazy (część skryptu build_006.py)
from b006_evidence import T, D, N, LETTER
from b006_db import PESEL

def spot(id, name, text, gives, requires=None, lockedText=None):
    d = {'id': id, 'name': name, 'text': text, 'gives': gives}
    if requires: d['requires'] = requires; d['lockedText'] = lockedText
    return d

# Położenia śladów na zdjęciach (x, y, r — względem szerokości i wysokości obrazu) ustawiane po wygenerowaniu grafik.
locations = [
 {'id': 'booth', 'name': 'Kabina projekcyjna', 'kind': 'Nad balkonem sali, wejście z korytarza balkonu',
  'desc': 'Ciasne pomieszczenie z dwoma projektorami Meopta, stołem przewijarki i regałem z taśmami. Przez okienka projekcyjne widać ciemną salę. Ciało zabrano w nocy — na środku podłogi został zarys kredą.',
  'spots': [
   spot('sp-log', 'Dziennik kabiny', 'Gruby zeszyt na pulpicie między projektorami.', ['e06']),
   spot('sp-proj', 'Projektor A', 'Pełna szpula na projektorze A po lewej.', ['e07']),
   spot('sp-can', 'Puszka na podłodze', 'Stalowa puszka przy zarysie ciała, pod regałem.', ['e08']),
   spot('sp-photo', 'Zdjęcie w ramce', 'Czarno-białe zdjęcie na ścianie nad przewijarką.', ['e09']),
   spot('sp-door', 'Drzwi ewakuacyjne', 'Stalowe drzwi na schody pożarowe.', ['e10']),
   spot('sp-card', 'Puszka części II', 'Otwarta puszka przy projektorze B, w środku karta.', ['e11']),
   spot('sp-desk', 'Biurko kinooperatora', 'Termos, okulary, koperta.', ['e12']),
   spot('sp-calc', 'Projektor B', 'Wasze wyliczenie godziny zmiany projektorów.', ['e26'], requires={'puzzle': 'p-reel'},
        lockedText='Projektor B przejął film w trakcie seansu. Żeby ustalić, kiedy dokładnie, policzcie to z karty kopii i dziennika — zagadka „Zmiana projektorów”.'),
  ],
  'search': {'aspect': 1.5, 'spots': {'sp-log': [0.33, 0.49, 0.05], 'sp-proj': [0.135, 0.15, 0.07], 'sp-can': [0.845, 0.655, 0.045], 'sp-photo': [0.607, 0.25, 0.05],
                                      'sp-door': [0.81, 0.34, 0.06], 'sp-card': [0.49, 0.715, 0.045], 'sp-desk': [0.885, 0.86, 0.06]}}},
 {'id': 'foyer', 'name': 'Foyer', 'kind': 'Parter kina, za kasami',
  'desc': 'Marmurowa posadzka, bar z ciemnego drewna, girlandy po wczorajszym pożegnaniu. Na ścianie przeszklona gablota z plakatami, przy drzwiach na salę panel oświetlenia.',
  'spots': [
   spot('sp-case', 'Gablota z plakatami', 'Cztery stare plakaty filmowe za szkłem.', ['e13']),
   spot('sp-panel', 'Panel oświetlenia sali', 'Szafka z przełącznikami przy drzwiach na salę.', ['e14']),
  ]},
 {'id': 'office', 'name': 'Biuro kierowniczki', 'kind': 'Korytarz zaplecza, przy tylnych drzwiach',
  'desc': 'Małe biuro z biurkiem, szafą na dokumenty i wieszakiem. Na biurku kasetka z utargiem i wydruk przemówienia pożegnalnego z dopiskami.',
  'spots': [
   spot('sp-coat', 'Wieszak', 'Jasny płaszcz kierowniczki.', ['e16'], requires={'all': ['lie:e-l1']},
        lockedText='Płaszcz kierowniczki kina. Bez powodu prokurator nie zgodzi się go zabezpieczyć — najpierw wykażcie, że jego właścicielka mija się z prawdą o tym, co robiła w czasie seansu.'),
   spot('sp-folder', 'Szafa z dokumentami', 'Segregatory i teczki kina.', ['e17']),
   spot('sp-keys', 'Szafka z kluczami', 'Zapasowe klucze i zeszyt wydań.', ['e18']),
  ]},
 {'id': 'yard', 'name': 'Podwórze za kinem', 'kind': 'Wspólne podwórze z oficyną pod numerem 43',
  'desc': 'Ciasna łódzka studnia: mokry bruk, latarnia, kontenery pod ścianą. Na tylnej ścianie kina żelazne schody pożarowe prowadzą do drzwi kabiny. Obok nich tylne drzwi zaplecza.',
  'spots': [
   spot('sp-stairs', 'Schody pożarowe', 'Stalowe schody od drzwi kabiny na bruk.', ['e19']),
   spot('sp-bin', 'Kontener na makulaturę', 'Niebieski kontener przy tylnych drzwiach.', ['e20']),
   spot('sp-wedge', 'U stóp schodów', 'Coś leży w kałuży tuż przy schodach.', ['e21']),
   spot('sp-back', 'Tylne drzwi zaplecza', 'Metalowe drzwi z czujnikiem nad framugą.', ['e22']),
   spot('sp-letter', 'Złożone skrawki', 'Kartka złożona z mokrych skrawków z kontenera.', ['e27'], requires={'puzzle': 'p-torn'},
        lockedText='Mokre skrawki z kontenera to jedna kartka. Złóżcie ją — zagadka „Podarty list”.'),
  ],
  'search': {'aspect': 1.5, 'spots': {'sp-stairs': [0.7, 0.62, 0.07], 'sp-bin': [0.475, 0.69, 0.05], 'sp-wedge': [0.635, 0.875, 0.035], 'sp-back': [0.355, 0.64, 0.05]}}},
 {'id': 'flat', 'name': 'Mieszkanie pana Lipki', 'kind': 'Oficyna, ul. Gdańska 43, II piętro',
  'desc': 'Jeden pokój z kuchnią, kredens, stół nakryty ceratą, fotel przy oknie. Pan Lipka zaprasza: „Proszę zobaczyć, skąd patrzyłem”.',
  'spots': [
   spot('sp-window', 'Okno', 'Fotel przy oknie, za szybą podwórze.', ['e23']),
   spot('sp-clock', 'Zegar ścienny', 'Okrągły zegar nad kredensem.', ['e24']),
   spot('sp-watch', 'Pudełko na stole', 'Otwarte pudełko z zegarkiem, obok baterie.', ['e25']),
  ],
  'search': {'aspect': 1.5, 'spots': {'sp-window': [0.75, 0.25, 0.09], 'sp-clock': [0.157, 0.13, 0.06], 'sp-watch': [0.3, 0.85, 0.065]}}},
]

puzzles = [
 {'id': 'p-reel', 'kind': 'Obliczenie', 'title': 'Zmiana projektorów',
  'prompt': 'Film szedł bez przerwy, a dziennik kabiny milczy. O której godzinie ktoś musiał uruchomić projektor B? Policzcie z karty kopii i z dziennika.',
  'requires': ['e06', 'e11'], 'input': 'time', 'answers': ['2104'],
  'hints': ['Na okładce dziennika jest wszystko, czego trzeba: ile klatek przesuwa się w sekundę i ile milimetrów ma jedna klatka. Policzcie, ile metrów taśmy przesuwa się w minutę.',
            '24 klatki po 19 mm to 456 mm, czyli 0,456 m na sekundę i 27,36 m na minutę. Podzielcie przez to długość części I z karty kopii.',
            '1 750 m podzielone przez 27,36 m na minutę to prawie dokładnie 64 minuty. Projekcja ruszyła o 20:00, więc zmiana nastąpiła o 21:04.'],
  'solution': 'Część I ma 1 750 m, a taśma przesuwa się z prędkością 27,36 m na minutę — to 64 minuty projekcji. Start o 20:00, więc projektor B ruszył o 21:04. Leon Barcz nie wpisał tej zmiany i nie przewinął części I. Zmianę zrobił ktoś inny.',
  'reward': {'search': True, 'spots': ['sp-calc']}},
 {'id': 'p-torn', 'kind': 'Rekonstrukcja', 'title': 'Podarty list',
  'prompt': 'Mokre skrawki z kontenera to jedna kartka w linie. Złóżcie ją z powrotem.',
  'requires': ['e20'], 'input': 'torn', 'answers': [],
  'torn': {'lines': LETTER, 'cols': 3, 'rows': 3, 'font': 'hand', 'stain': True},
  'hints': ['Zacznijcie od narożników — każdy ma dwie proste krawędzie.',
            'Pierwsza linijka to miejsce i data, ostatnia — podpis. Linie na papierze muszą przechodzić gładko z kawałka na kawałek.',
            'Tylko jeden skrawek nie ma żadnej prostej krawędzi. To on trafia w sam środek kartki.'],
  'solution': 'To list Leona Barcza do miejskiej konserwator zabytków: dwa plakaty w gablocie to kopie, a oryginały trafiły na aukcję do domu aukcyjnego „Rewers”. Klucz do gabloty mieli tylko on i kierowniczka kina.',
  'reward': {'search': True, 'spots': ['sp-letter']}},
]

hintTrail = [
 {'unless': ['sp-can'], 'text': 'Zacznijcie od kabiny projekcyjnej. Obejrzyjcie zdjęcie z oględzin i przybliżcie je — czy ta puszka naprawdę mogła spaść z półki?'},
 {'unless': ['sp-log'], 'when': ['sp-can'], 'text': 'Kinooperator prowadził dziennik kabiny. Co do niego wpisał w sobotę — i czego nie wpisał?'},
 {'unless': ['d-q2'], 'when': ['sp-log'], 'text': 'Technik projekcji zna zwyczaje pana Leona. Zapytajcie, jak prowadził seans z taśmy.'},
 {'unless': ['p-reel'], 'when': ['e06', 'e11'], 'text': 'Film poszedł bez przerwy, a w dzienniku brakuje zmiany projektora. Policzcie, o której musiała nastąpić.'},
 {'unless': ['l-q1'], 'when': ['sp-door'], 'text': 'Drzwi kabiny prowadzą na schody pożarowe nad podwórzem. Sąsiad z oficyny naprzeciwko twierdzi, że coś widział.'},
 {'unless': ['sp-clock'], 'when': ['l-q1'], 'text': 'Pan Lipka podał bardzo dokładną godzinę. Sprawdźcie, skąd ją wziął — obejrzyjcie jego mieszkanie.'},
 {'unless': ['lie:l-m1'], 'when': ['e24'], 'text': 'Zegar pana Lipki pokazuje godzinę więcej niż wasze telefony. Wskażcie to przy jego zeznaniu w protokole.'},
 {'unless': ['sp-bin'], 'when': ['sp-stairs'], 'text': 'Kto zbiegł schodami, był na podwórzu. Zajrzyjcie do kontenera przy tylnych drzwiach.'},
 {'unless': ['p-torn'], 'when': ['e20'], 'text': 'Skrawki z kontenera to jedna kartka. Złóżcie ją w zakładce Analiza.'},
 {'unless': ['j-q4'], 'when': ['ew-q1'], 'text': 'Kierowniczka twierdzi, że nie wychodziła z biura. Bufetowa przez cały seans widziała, kto wchodzi do foyer.'},
 {'unless': ['lie:e-l1'], 'when': ['st:j-c2'], 'text': 'Bufetowa widziała kierowniczkę wracającą od zaplecza, mokrą. Skonfrontujcie to z jej zeznaniem.'},
 {'unless': ['show:j-s1'], 'when': ['e09'], 'text': 'Na zdjęciu z kabiny jest kobieta z nazwiskiem. Pokażcie je komuś, kto pracuje w kinie od dawna.'},
 {'unless': ['d02'], 'when': ['x6'], 'text': 'Komitent z katalogu aukcji to spółka. Sprawdźcie ją w KRS — kto nią kieruje?'},
 {'text': 'Macie dość, by złożyć raport. Najważniejsze: kto był w kabinie o 21:04.'},
]

report = {'questions': [
 {'id': 'r-who', 'q': 'Kto zabił Leona Barcza?', 'type': 'single', 'points': 16,
  'options': [['ewa', 'Ewa Sitek, kierowniczka kina'], ['damian', 'Damian Wróbel, technik projekcji'], ['grzegorz', 'Grzegorz Barcz, syn kinooperatora'],
              ['joanna', 'Joanna Rak, bufetowa'], ['accident', 'Nikt — to był wypadek, puszka spadła z regału']],
  'correct': 'ewa',
  'proof': {'count': 3, 'each': 4, 'valid': ['e16', 'x5', 't4', 'e26', 'e27', 'e17', 'x2', 'e19', 'e20', 't5', 't6', 't7', 't9', 'd02', 'd03', 'x6', 'e09', 'd01', 'e18'],
            'label': 'Wskażcie trzy dowody, które najmocniej łączą tę osobę ze zbrodnią.'}},
 {'id': 'r-change', 'q': 'Kto i kiedy zmienił projektor w czasie seansu?', 'type': 'single', 'points': 14,
  'options': [['ewa', 'Ewa Sitek, około 21:04'], ['leon', 'Leon Barcz, tuż przed śmiercią'], ['damian', 'Damian Wróbel, około 21:04'],
              ['grzegorz', 'Grzegorz Barcz, gdy wyszedł z sali'], ['none', 'Nikt — cały film był na jednej szpuli']],
  'correct': 'ewa'},
 {'id': 'r-route', 'q': 'Którędy sprawca dostał się do kabiny i jak z niej wyszedł?', 'type': 'single', 'points': 12,
  'options': [['fire', 'Tylnymi drzwiami zaplecza na podwórze i schodami pożarowymi do drzwi podpartych klinem; wyszedł tą samą drogą, a drzwi bez klina się zatrzasnęły'],
              ['key', 'Wewnętrznymi drzwiami, zapasowym kluczem z biura, i zamknął je za sobą'],
              ['hall', 'Wyjściem ewakuacyjnym z sali, w ciemności, w trakcie filmu'],
              ['stay', 'Ukrył się w kabinie i wyszedł dopiero przy znalezieniu ciała o 22:41']],
  'correct': 'fire'},
 {'id': 'r-lipka', 'q': 'Dlaczego pan Lipka podał godzinę 22:10?', 'type': 'single', 'points': 12,
  'options': [['clock', 'Nastawił zegar z zegarka po bracie, którego nikt nie przestawił na czas zimowy'], ['cover', 'Chronił kogoś z personelu kina'],
              ['other', 'Widział inną osobę, która wyszła na podwórze po seansie'], ['day', 'Pomylił sobotę z piątkiem']],
  'correct': 'clock'},
 {'id': 'r-motive', 'q': 'Jaki był motyw?', 'type': 'single', 'points': 10,
  'options': [['posters', 'Leon Barcz chciał ujawnić, że oryginały dwóch plakatów z gabloty sprzedaje firma męża kierowniczki, a w gablocie wiszą kopie'],
              ['flat', 'Spadek — mieszkanie kinooperatora'], ['job', 'Zemsta za odsunięcie od projekcji na ostatnim seansie'],
              ['building', 'Kinooperator blokował sprzedaż budynku kina']],
  'correct': 'posters'},
 {'id': 'r-liars', 'q': 'Kto skłamał w zeznaniach, choć nie zabił?', 'type': 'multi', 'points': 10,
  'hint': 'Zaznaczcie wszystkie właściwe odpowiedzi. Każda błędna odejmuje punkty za trafną. Pomyłka to nie kłamstwo.',
  'options': [['damian', 'Damian Wróbel'], ['grzegorz', 'Grzegorz Barcz'], ['joanna', 'Joanna Rak'], ['lipka', 'Stanisław Lipka']],
  'correct': ['damian', 'grzegorz']},
 {'id': 'r-order', 'q': 'Ułóżcie wydarzenia soboty we właściwej kolejności.', 'type': 'order', 'points': 14,
  'items': [['quarrel', 'Leon Barcz kłóci się z synem przy barze'], ['start', 'Rusza projekcja części I na projektorze A'], ['out', 'Ktoś wychodzi tylnymi drzwiami zaplecza na podwórze'],
            ['shop', 'Damian Wróbel płaci w sklepie przy Gdańskiej 60'], ['change', 'Ktoś w kabinie uruchamia projektor B'], ['rain', 'Zaczyna padać deszcz'],
            ['close', 'Drzwi ewakuacyjne kabiny się zamykają'], ['back', 'Ktoś wchodzi z podwórza tylnymi drzwiami zaplecza'], ['white', 'Po napisach ekran świeci na biało']],
  'correct': ['quarrel', 'start', 'out', 'shop', 'change', 'rain', 'close', 'back', 'white']},
]}

solution = {
 'summary': 'Leona Barcza zabiła Ewa Sitek, kierowniczka kina. Kinooperator odkrył, że dwa najcenniejsze plakaty w gablocie to faksymile, a oryginały wystawiła na aukcję spółka jej męża, i chciał po seansie wręczyć list konserwator zabytków. Za dwadzieścia dziewiąta Sitek wyszła tylnymi drzwiami, weszła schodami pożarowymi do kabiny przez drzwi podparte klinem i uderzyła Barcza puszką. Potem — jako dawna kinooperatorka — o 21:04 sama zmieniła projektor, żeby film szedł dalej i nikt nie zajrzał do kabiny. Wyszła po 21:10, wyrzucając klin; drzwi się zatrzasnęły. List podarła i wyrzuciła do kontenera.',
 'steps': [
  {'h': 'Puszka, która nie spadła', 'p': 'Na górnej półce regału nienaruszony kurz, a na stole przewijarki okrągły ślad po puszce. Syn: ojciec zawsze trzymał pustą puszkę na stole. Sekcja: uderzenie z zamachem, przez osobę stojącą za ofiarą — upadek puszki wykluczony.'},
  {'h': 'Zmiana, której nikt nie zapisał', 'p': 'Część I ma 1 750 m, taśma biegnie 27,36 m na minutę: zmiana projektorów musiała nastąpić o 21:04. Film nie przerwał się ani na chwilę, a Barcz — który od lat wpisywał każdą zmianę i od razu przewijał pierwszą część — nie zrobił ani jednego, ani drugiego. O 21:04 przy projektorach stał ktoś inny.'},
  {'h': 'Kto umiał to zrobić', 'p': 'Zmienić projektor umieli Damian Wróbel, Grzegorz Barcz i — o czym nikt już nie pamiętał — Ewa Sitek, z domu Kalinowska, kinooperatorka „Zorzy” w latach 1996–2001. Zdjęcie w kabinie, bufetowa i rejestr PESEL mówią to samo.'},
  {'h': 'Alibi o 21:04', 'p': 'Damian Wróbel o 21:03 płacił kartą w sklepie 300 m od kina, a kamera pizzerii widziała go wychodzącego i wracającego frontem. Grzegorz Barcz od 21:01 do 21:12 stał przed kinem z telefonem. Joanna Rak nie odchodziła od baru. Sitek była „w biurze” — sama.'},
  {'h': 'Godzina pana Lipki', 'p': 'Sąsiad widział osobę w jasnym płaszczu zbiegającą schodami pożarowymi „dziesięć po dziesiątej”. Jego zegar śpieszy się o godzinę: nastawił go z zegarka po bracie, wciąż na czasie letnim. Naprawdę była 21:10 — minuta przed zamknięciem drzwi kabiny o 21:11:02 w dzienniku alarmu. Pomylił się, ale nie kłamał.'},
  {'h': 'Droga przez podwórze', 'p': 'Tylne drzwi zaplecza, trzy kroki od biura: wyjście o 20:41, powrót o 21:13. Deszcz od 21:05. Mokry płaszcz kierowniczki z farbą i rdzą z poręczy schodów pożarowych, starta farba na poręczy, klin kinooperatora na czerwonym sznurku w kałuży u stóp schodów.'},
  {'h': 'List i plakaty', 'p': 'W kontenerze przy tylnych drzwiach — skrawki listu Barcza do konserwator: dwa plakaty to kopie, oryginały są w katalogu „Rewersu”, klucz do gabloty mieli tylko on i kierowniczka. Sitek zamówiła w październiku 2026 roku faksymile, a komitentem aukcji jest Ars-Lokus — spółka jej męża, Tomasza Sitka.'},
  {'h': 'Fałszywe tropy', 'p': 'Damian ukrył wyjście po wódkę na po imprezie, Grzegorz — telefon do wierzyciela i kłótnię z ojcem o pieniądze. Obaj kłamali, żaden nie zabił. Pan Lipka nie kłamał wcale: pomylił godzinę przez nieprzestawiony zegarek.'},
 ]}

endings = {
 'correct': {'title': 'Ostatni seans', 'text': 'Ewa Sitek zostaje zatrzymana w niedzielę po południu, a jej mąż wieczorem. Dom aukcyjny „Rewers” wycofuje pozycje 117 i 118 z aukcji; oryginały plakatów wracają do Łodzi w tekturowych tubach, z pieczęcią prokuratury. Kino „Zorza” zostaje zamknięte zgodnie z planem, ale na drzwiach kabiny ktoś przykleja kartkę: „Klin! Lampy grzeją. L.B.”',
  'decision': {'q': 'Plakaty wróciły. Co jeszcze zrobicie w tej sprawie?', 'options': [
   {'id': 'museum', 'label': 'Wnioskować, by oryginały trafiły do muzeum kinematografii jako depozyt kolekcji „Zorzy”', 'text': 'Muzeum przyjmuje cztery plakaty z tabliczką „Z kolekcji kina »Zorza« 1958–2026. Ocalone przez Leona Barcza”. Grzegorz Barcz przychodzi na otwarcie wystawy. Nie mówi nic, tylko długo stoi przed „Dziewczyną z Bałut”.'},
   {'id': 'auction', 'label': 'Zawiadomić prokuraturę o sprawdzeniu wszystkich obiektów, które Ars-Lokus oddała do „Rewersu” w ostatnich latach', 'text': 'Okazuje się, że spółka Sitków sprzedała przez „Rewers” jedenaście obiektów — każdy „z kolekcji prywatnej, Łódź”. Trzy pochodziły z miejskich instytucji. Proces Ewy Sitek obejmuje także oszustwa.'},
   {'id': 'vesper', 'label': 'Ustalić, kto w pracowni VESPER wykonał faksymile i czy wiedział, do czego posłużą', 'text': 'Wrocławska pracownia odpowiada uprzejmym pismem: wykonała faksymile ekspozycyjne zgodnie ze zleceniem, oznaczone dyskretnym nadrukiem, jak każe dobra praktyka. Pismo podpisuje prezes, Teodor Ancel. Do pisma dołączono katalog usług. Na ostatniej stronie, drobnym drukiem: „ekspertyzy autentyczności dokumentów dawnych”.'},
  ]}},
 'wrong': {
  'damian': {'title': 'Uczeń', 'text': 'Damian umiał zmienić projektor i skłamał, gdzie był, więc wskazujecie jego. Ale o 21:03 płacił kartą w sklepie przy Gdańskiej 60, a kamera pizzerii widziała, jak wraca frontem z reklamówką. Zanim śledztwo wróci na właściwy tor, plakaty zostaną sprzedane na aukcji.'},
  'grzegorz': {'title': 'Syn', 'text': 'Kłótnia o pieniądze, długi, umiejętność zmiany projektora — wszystko pasowało. Tyle że od 21:01 do 21:12 Grzegorz stał przed kinem z telefonem, na oczach kamery. Prawdziwa sprawczyni ma czas, by odebrać z Krakowa pieniądze za plakaty.'},
  'joanna': {'title': 'Bufet', 'text': 'Joanna Rak nie odchodziła od baru i nie umiała obsłużyć projektora. Jej zeznania były prawdziwe od pierwszego do ostatniego słowa — i to one powinny was zaprowadzić do sprawczyni.'},
  'accident': {'title': 'Nieszczęśliwy wypadek', 'text': 'Uznajecie, że ciężka puszka spadła z regału. Dokładnie tak miało to wyglądać. Sekcja mówi co innego, ale zanim ktokolwiek zestawi ją z waszym raportem, w Krakowie stuka młotek licytatora. „Czarna perła” idzie za sto dziesięć tysięcy.'},
 },
 'partial': 'Wskazaliście właściwą osobę, ale część wniosków jest błędna lub niepoparta dowodami. Sitek zostaje zatrzymana, ale obrona będzie miała o co walczyć.',
}

breakthroughs = [
 {'id': 'b-change', 'when': 'p-reel', 'title': 'Zmiana o 21:04', 'text': 'Film nie przerwał się ani na sekundę. Ktoś stanął przy projektorach dokładnie o 21:04 i zrobił to, co Leon Barcz robił przez pięćdziesiąt lat — tylko że tej zmiany nikt nie wpisał do dziennika.'},
 {'id': 'b-clock', 'when': 'lie:l-m1', 'title': 'Godzina pana Lipki', 'text': 'Zegar pana Lipki śpieszy się o godzinę. Człowiek na schodach pożarowych nie zbiegał po seansie, lecz w jego trakcie — minutę przed tym, jak zatrzasnęły się drzwi kabiny.'},
 {'id': 'b-student', 'when': 'show:j-s1', 'title': 'Uczennica', 'text': 'Na zdjęciu z kabiny, przy dźwigni zmiany, stoi młoda Ewa Kalinowska. Dziś nazywa się Sitek i prowadzi kino. Twierdziła, że nigdy nie dotknęła projektora.'},
 {'id': 'b-letter', 'when': 'p-torn', 'title': 'List do konserwator', 'text': 'Mokre skrawki układają się w list, którego Leon Barcz nie zdążył wręczyć. Dwa plakaty w gablocie to kopie. Klucz do niej mieli tylko on i kierowniczka.'},
]

tableMode = {'parBonus': 5, 'locations': [
 {'id': 'hq', 'name': 'Centrala wydziału', 'kind': 'Zapytania przez radio i telefon',
  'desc': 'Wóz łączności przed kinem. Każde zapytanie to jeden ruch, odpowiedzi przychodzą od razu.',
  'img': 'assets/places/001-hq.webp',
  'spots': [
   spot('sp-hq-imgw', 'IMGW', 'Prosicie o dane o opadach w Śródmieściu.', ['x1']),
   spot('sp-hq-zms', 'Zakład Medycyny Sądowej', 'Prosicie o wnioski z sekcji zwłok.', ['x2']),
   spot('sp-hq-pizza', 'Pizzeria naprzeciwko kina', 'Prosicie o nagranie z kamery nad wejściem.', ['x3']),
   spot('sp-hq-bank', 'Bank', 'Prosicie o transakcje kartami osób z personelu w czasie seansu.', ['x4']),
   spot('sp-hq-alarm', 'Firma ochrony kina', 'Prosicie o dziennik czujników centrali alarmowej.', ['x5']),
   spot('sp-hq-rewers', 'Dom aukcyjny „Rewers”', 'Prosicie o katalog najbliższej aukcji plakatów.', ['x6'], requires={'all': ['e27']},
        lockedText='Nie macie jeszcze powodu, by pytać krakowski dom aukcyjny o cokolwiek.'),
  ]}], 'questions': {}}

db = {'date': N, 'bases': ['osoby', 'pojazdy', 'firmy', 'ksiegi'], 'attach': [
 {'rec': 'O-006-ewa', 'ev': 'd01', 'paths': [{'q': {'nazwisko': 'Sitek', 'imie': 'Ewa'}, 'from': ['e05']}, {'q': {'pesel': PESEL['ewa']}, 'from': ['d03']}]},
 {'rec': 'F-006-ars', 'ev': 'd02', 'paths': [{'q': {'nazwa': 'Ars-Lokus'}, 'from': ['x6']}]},
 {'rec': 'O-006-tomasz', 'ev': 'd03', 'paths': [{'q': {'pesel': PESEL['tomasz']}, 'from': ['d02']}, {'q': {'nazwisko': 'Sitek', 'imie': 'Tomasz'}, 'from': ['d01']}]},
]}
