# Sprawa 004 „Martwy kanał” — miejsca, zagadki, raport, zakończenia (część skryptu build_004.py)
from b004_evidence import T, D, F

def spot(id, name, text, gives, requires=None, lockedText=None):
    d = {'id': id, 'name': name, 'text': text, 'gives': gives}
    if requires: d['requires'] = requires; d['lockedText'] = lockedText
    return d

locations = [
 {'id': 'station', 'name': 'Stacja nadawcza „Kolonia”', 'kind': 'Miejsce znalezienia ciała',
  'desc': 'Niski budynek z cegły pod kratownicowym masztem na wzgórzu. W środku pomieszczenie nadajnika SN-1, szafa z rozdzielnią i drzwi D1 z czytnikami po obu stronach.',
  'spots': [
   spot('sp-body', 'Ciało przy szafie', 'Lasota leży przy otwartej szafie SN-1. Przy ciele zegarek, w kieszeni kurtki telefon.', ['e07', 'e08', 'e44']),
   spot('sp-cabinet', 'Szafa nadajnika SN-1', 'Panel dziennika zdarzeń z zabezpieczoną pamięcią. Wydruk jest jeden.', ['e09']),
   spot('sp-switch', 'Przełącznik SERWIS/PRACA', 'Przełącznik kluczykowy na panelu szafy.', ['e10']),
   spot('sp-k3', 'Złącze anteny K3', 'Skrzynka na dole szafy, za osłoną.', ['e11']),
   spot('sp-door', 'Drzwi D1 i czytniki', 'Czytniki kart po obu stronach drzwi, z pamięcią zdarzeń.', ['e12']),
   spot('sp-tools', 'Kanał kablowy za szafą', 'Wąska szczelina między szafą a ścianą, ciemna.', ['e13']),
   spot('sp-gate', 'Brama i dojazd', 'Żwirowy dojazd i brama zamykana na kłódkę, nad nią kamera.', ['e14']),
  ], 'img': None},
 {'id': 'czk', 'name': 'Centrum Zarządzania Kryzysowego', 'kind': 'Sala dyżurna, ul. Hutnicza',
  'desc': 'Sala z konsolą, ścianą monitorów i jednym biurkiem. Nocą pracuje tu jedna osoba. Serwerownia jest za drzwiami z kodem.',
  'spots': [
   spot('sp-console', 'Konsola dyżurna', 'Pasek zdarzeń z nocy, wydruk z konsoli.', ['e16']),
   spot('sp-trash', 'Kosz przy biurku', 'Kosz na odpady, nieopróżniany od nocy.', ['e17']),
   spot('sp-camera', 'Kamera nad konsolą', 'Zapis z kamery sali dyżurnej.', ['e18']),
   spot('sp-roster', 'Grafik i procedury', 'Teczka z grafikiem i instrukcjami zmiany.', ['e19', 'e20']),
  ], 'img': None},
 {'id': 'chemrud', 'name': 'Zakład Chemrud', 'kind': 'Wydział chloru, osiedle Zielone',
  'desc': 'Hale produkcyjne i biurowiec za płotem. Linia Cl-3 jest odcięta, teren zabezpieczony przez straż.',
  'spots': [
   spot('sp-gasnet', 'Dziennik czujników GasNet', 'Terminal w nastawni wydziału chloru.', ['e21']),
   spot('sp-shift', 'Dziennik zmiany', 'Zeszyt nocnej zmiany na biurku kierownika.', ['e22']),
   spot('sp-valve', 'Zawór Cl-3', 'Pęknięty zawór, protokół awarii obok.', ['e23']),
   spot('sp-office', 'Gabinet prezesa', 'Komputer prezesa z otwartym plikiem.', ['e24']),
  ], 'img': None},
 {'id': 'hospital', 'name': 'Szpital Miejski', 'kind': 'SOR i oddział toksykologii',
  'desc': 'Korytarz izby przyjęć po nocnym szczycie. Lekarz dyżurny ma kwadrans.',
  'spots': [
   spot('sp-sor', 'Rejestr przyjęć SOR', 'Rejestr nocnych przyjęć.', ['e25']),
   spot('sp-tox', 'Lekarz toksykolog', 'Krótka rozmowa na korytarzu.', ['e26']),
  ], 'img': None},
 {'id': 'city', 'name': 'Urząd Miasta', 'kind': 'Referat Zarządzania Kryzysowego i gabinety',
  'desc': 'Korytarz z wykładziną i biura z tabliczkami. Gabinet Lasoty jest zaplombowany przez policję, ale pozwolenie macie.',
  'spots': [
   spot('sp-desk', 'Gabinet Lasoty', 'Biurko, kalendarz i karteczka na monitorze.', ['e27']),
   spot('sp-safe', 'Sejf w gabinecie', 'Mały sejf za szafą, zamek czterocyfrowy.', ['e29', 'e30'], requires={'puzzle': 'p-pin'}, lockedText='Zamknięty sejf z czterocyfrowym zamkiem. Bez kodu go nie otworzycie, a rozwiercenie zniszczyłoby zawartość.'),
   spot('sp-archive', 'Archiwum zamówień', 'Segregatory z umową i aneksami SYRION-4.', ['e28', 'e31']),
   spot('sp-mw', 'System wniosków serwisowych', 'Komputer referatu z systemem MW.', ['e32']),
   spot('sp-vice', 'Gabinet wiceprezydenta', 'Biurko wiceprezydenta, szuflada z dokumentami.', ['e33'], requires={'all': ['lie:s-l2']}, lockedText='Bez podstaw nikt wam gabinetu wiceprezydenta nie otworzy. Najpierw musicie wykazać, że jego zeznania nie trzymają się dokumentów.'),
  ], 'img': None},
 {'id': 'parking', 'name': 'Parking leśny pod Kolonią', 'kind': 'Dojazd do wzgórza',
  'desc': 'Żwirowy plac w lesie, półtora kilometra od stacji. Na drzewie fotopułapka leśnictwa.',
  'spots': [
   spot('sp-trap', 'Fotopułapka leśnictwa', 'Karta pamięci z zapisem zdjęć.', ['e34']),
   spot('sp-ground', 'Plac i pniak', 'Ślady butów i śmieci po nocy.', ['e35']),
  ], 'img': None},
 {'id': 'newsroom', 'name': 'Redakcja „Głosu Rudy”', 'kind': 'Biurko reporterki',
  'desc': 'Open space nad drukarnią. Biurko Leny Hajduk jest pod oknem.',
  'spots': [
   spot('sp-notes', 'Notatnik reporterki', 'Notatnik w górnej szufladzie.', ['e36'], requires={'all': ['lie:h-l1']}, lockedText='Bez nakazu redakcja nie wyda notatek reporterki, a tajemnica dziennikarska to nie wymysł. Potrzebujecie podstawy.'),
   spot('sp-mail', 'Skrzynka pocztowa reporterki', 'Korespondencja z czwartku.', ['e37'], requires={'all': ['lie:h-l1']}, lockedText='Bez nakazu nikt wam skrzynki nie otworzy. Najpierw wykażcie, że reporterka mówi nieprawdę.'),
  ], 'img': None},
 {'id': 'syreon', 'name': 'Syreon Polska, Gliwice', 'kind': 'Siedziba i garaż firmy serwisowej',
  'desc': 'Hala z garażem, magazynem i niewielkim biurem. Szef firmy zgodził się na oględziny dopiero po telefonie z prokuratury.',
  'spots': [
   spot('sp-reg', 'Rejestr kart i kluczy', 'Zeszyt wydań i grafik serwisantów.', ['e39', 'e40'], requires={'all': ['lie:k-l1']}, lockedText='Bez podstawy firma nie pokaże wam rejestrów. Najpierw ustalcie, czy Kopeć mówi prawdę o tej nocy.'),
   spot('sp-van', 'Bus Ducato', 'Furgon zaparkowany w garażu.', ['e41'], requires={'all': ['lie:k-l1']}, lockedText='Bez podstawy nie przeszukacie samochodu firmowego. Najpierw ustalcie, czy Kopeć mówi prawdę o tej nocy.'),
   spot('sp-tw', 'Wykaz narzędzi', 'Segregator z przydziałami narzędzi.', ['e42'], requires={'all': ['lie:k-l1']}, lockedText='Bez podstawy firma nie wyda wykazów. Najpierw ustalcie, czy Kopeć mówi prawdę o tej nocy.'),
   spot('sp-orders', 'Archiwum zamówień', 'Szafa z teczkami zamówień z 2024 roku.', ['e43'], requires={'all': ['lie:k-l1']}, lockedText='Bez podstawy firma nie otworzy archiwum zamówień. Najpierw ustalcie, czy Kopeć mówi prawdę o tej nocy.'),
  ], 'img': None},
]
for l in locations:
    if l.get('img') is None: l.pop('img', None)

puzzles = [
 {'id': 'p-pin', 'kind': 'Zamek szyfrowy', 'title': 'Sejf w gabinecie Lasoty',
  'prompt': 'Sejf w gabinecie ma czterocyfrowy zamek. Jaki kod ustawił Lasota? Wskazówkę zostawił sam, na biurku.',
  'requires': ['e27', 'e28'], 'input': 'digits4', 'answers': ['1406'],
  'hints': ['Karteczka na monitorze mówi, z czym związany jest PIN. Szukajcie dokumentu, w którym ta data występuje.',
            'Chodzi o odbiór systemu. Protokół odbioru podaje datę. Potrzebujecie dnia i miesiąca, bez roku.',
            'Odbiór nastąpił 14.06.2024. Dzień 14, miesiąc 06 — kod 1406.'],
  'solution': 'Kod to dzień i miesiąc odbioru systemu: 14.06 — 1406. Lasota zapisał go sobie w ten sposób, bo odbiór SYRION-4 miał dla niego znaczenie, a on sam wtedy nie podpisał protokołu.',
  'reward': {'spots': ['sp-safe']}},
 {'id': 'p-service', 'kind': 'Analiza danych', 'title': 'Jak długo trwał tryb SERWIS',
  'prompt': 'Ile minut nadajnik SN-1 pozostawał w trybie SERWIS, licząc od włączenia do powrotu do trybu PRACA? Podajcie liczbę minut, zaokrągloną do pełnej minuty.',
  'requires': ['e09'], 'input': 'number', 'answers': ['118-119'],
  'hints': ['Dziennik nadajnika zapisuje włączenie SERWIS i powrót do PRACA z dokładnością do sekundy. Szukajcie dwóch wpisów z oznaczeniem klucza.',
            'Włączenie: 1:03:22. Powrót do PRACA: 3:02:11. Policzcie różnicę.',
            'Od 1:03:22 do 3:02:11 mija 1 godzina 58 minut i 49 sekund, czyli po zaokrągleniu 119 minut.'],
  'solution': 'Tryb SERWIS trwał 1 godzinę 58 minut 49 sekund, czyli około 119 minut. Okno miało trwać dwie i pół godziny, ale w tym czasie system nie mógł wysłać żadnego alarmu.',
  'reward': {'time': [[f'{F} 01:03', 'SN-1 głuchy na polecenia alarmowe przez 119 minut (1:03–3:02)', 'Analiza dziennika SN-1']]}},
 {'id': 'p-time', 'kind': 'Analiza danych', 'title': 'Godzina na zegarku',
  'prompt': 'Zegarek Lasoty zapisał ostatnią chwilę, w której został zdjęty z nadgarstka. O której godzinie czasu prawdziwego to nastąpiło? Zegarek nie był synchronizowany z siecią.',
  'requires': ['x6', 'x1'], 'input': 'time', 'answers': ['0241'],
  'hints': ['Zegarek zapisał połączenie wychodzące do L. Hajduk. Billing operatora pokazuje to samo połączenie.',
            'Porównajcie godzinę połączenia na zegarku i w billingu. O ile minut zegarek się spóźnia?',
            'Zegarek: 02:27, billing: 02:34. Spóźnia się o 7 minut. Ostatni zapis zegarka, 02:34, to w czasie prawdziwym 02:41.'],
  'solution': 'Zegarek spóźniał się o 7 minut (połączenie do Hajduk: 02:27 na zegarku, 02:34 w billingu). Zdjęcie z nadgarstka o 02:34 na zegarku to prawdziwe 02:41. Wtedy właśnie doszło do ataku.',
  'reward': {'time': [[f'{F} 02:41', 'Atak na Lasotę, zegarek zdjęty z nadgarstka (czas prawdziwy)', 'Analiza zegarka i billingu']]}},
 {'id': 'p-alibi', 'kind': 'Macierz alibi', 'title': 'Gdzie kto był',
  'prompt': 'Uzupełnijcie tabelę: gdzie była każda z pięciu osób o 1:47, gdy czujniki wysłały żądanie alarmu, i o 2:41, w chwili ataku na Lasotę? Wybierzcie miejsce dla każdej osoby w obu kolumnach.',
  'requires': ['p-time', 'e12', 'e18', 'e22', 'e39', 'e40', 'x2'], 'input': 'grid',
  'grid': {
   'rows': [{'id': 'kopec', 'label': 'Dariusz Kopeć'}, {'id': 'burda', 'label': 'Agnieszka Burda'}, {'id': 'szczerba', 'label': 'Piotr Szczerba'}, {'id': 'hajduk', 'label': 'Lena Hajduk'}, {'id': 'pyka', 'label': 'Witold Pyka'}],
   'cols': [{'id': 't1', 'label': '1:47 — żądanie alarmu'}, {'id': 't2', 'label': '2:41 — atak na Lasotę'}],
   'options': [{'id': 'kol', 'label': 'Wzgórze Kolonia'}, {'id': 'czk', 'label': 'Centrum (CZK)'}, {'id': 'che', 'label': 'Zakład Chemrud'}, {'id': 'dom', 'label': 'Dom'}, {'id': 'dro', 'label': 'W drodze'}],
   'constraints': [
    {'t': 'is', 'r': 'kopec', 'c': 't1', 'v': 'kol', 'src': ['e12', 'e39', 'e40'], 'why': 'Karta SRV-07 weszła na stację o 0:41 i wyszła o 3:09. Pobrał ją Kopeć, a pozostali serwisanci byli na urlopie i zwolnieniu.'},
    {'t': 'is', 'r': 'kopec', 'c': 't2', 'v': 'kol', 'src': ['e12', 'e39', 'e40'], 'why': 'Ta sama karta była na stacji nieprzerwanie od 0:41 do 3:09.'},
    {'t': 'in', 'r': 'burda', 'c': 't1', 'vs': ['czk', 'dom'], 'src': ['x2'], 'why': 'Telefon Burdy w komórce Centrum-2, która obejmuje CZK i część mieszkań.'},
    {'t': 'is', 'r': 'burda', 'c': 't1', 'v': 'czk', 'src': ['e18'], 'why': 'Kamera sali dyżurnej pokazuje ją przy konsoli o 1:47.'},
    {'t': 'is', 'r': 'burda', 'c': 't2', 'v': 'czk', 'src': ['e18'], 'why': 'Kamera: operatorka cały czas w sali, sama, do 3:00.'},
    {'t': 'is', 'r': 'szczerba', 'c': 't1', 'v': 'dom', 'src': ['x2'], 'why': 'Komórka Parkowe-7 to osiedle domów jednorodzinnych.'},
    {'t': 'is', 'r': 'szczerba', 'c': 't2', 'v': 'dom', 'src': ['x2'], 'why': 'Komórka Parkowe-7 to osiedle domów jednorodzinnych.'},
    {'t': 'is', 'r': 'hajduk', 'c': 't1', 'v': 'dom', 'src': ['x2'], 'why': 'Komórka Parkowe-7 to osiedle domów jednorodzinnych.'},
    {'t': 'is', 'r': 'hajduk', 'c': 't2', 'v': 'dro', 'src': ['x2'], 'why': 'Komórka Droga-5 to droga bez zabudowy, więc telefon jest w samochodzie.'},
    {'t': 'in', 'r': 'pyka', 'c': 't1', 'vs': ['dom', 'che'], 'src': ['x2'], 'why': 'Komórka Zielone-4 obejmuje osiedle i zakład Chemrud.'},
    {'t': 'not', 'r': 'pyka', 'c': 't1', 'v': 'che', 'src': ['e22'], 'why': 'Prezes przyjechał na zakład dopiero o 2:20.'},
    {'t': 'in', 'r': 'pyka', 'c': 't2', 'vs': ['dom', 'che'], 'src': ['x2'], 'why': 'Komórka Zielone-4 obejmuje osiedle i zakład Chemrud.'},
    {'t': 'not', 'r': 'pyka', 'c': 't2', 'v': 'dom', 'src': ['e22'], 'why': 'Prezes był na zakładzie od 2:20 do 3:30.'},
    {'t': 'exactly', 'c': 't1', 'v': 'czk', 'n': 1, 'src': ['e18'], 'why': 'W sali dyżurnej jest jedna osoba.'},
    {'t': 'exactly', 'c': 't2', 'v': 'kol', 'n': 1, 'src': ['e12'], 'why': 'Wśród podejrzanych jedna karta serwisowa na stacji (LAS-01 należy do ofiary).'},
   ]},
  'answers': [{'kopec': {'t1': 'kol', 't2': 'kol'}, 'burda': {'t1': 'czk', 't2': 'czk'}, 'szczerba': {'t1': 'dom', 't2': 'dom'}, 'hajduk': {'t1': 'dom', 't2': 'dro'}, 'pyka': {'t1': 'dom', 't2': 'che'}}],
  'hints': ['Zacznijcie od tych, o których macie twarde dane: karta serwisowa na stacji, kamera w sali dyżurnej i dziennik zmiany w zakładzie.',
            'Dane lokalizacyjne podają tylko komórki, nie miejsca. Rozstrzygnijcie, które komórki dają się odczytać jednoznacznie, a w których jest dwóch kandydatów.',
            'Kopeć: stacja o obu porach. Burda: CZK. Szczerba: dom. Hajduk: dom o 1:47 i w drodze o 2:41. Pyka: dom o 1:47, zakład o 2:41.'],
  'solution': 'O 1:47 Kopeć był na stacji, Burda w CZK, Szczerba, Hajduk i Pyka w domach. O 2:41 Kopeć wciąż na stacji, Burda w CZK, Szczerba w domu, Hajduk w drodze na Kolonię, Pyka na zakładzie. Na stacji nie było nikogo innego niż Kopeć i Lasota.',
  'reward': {'time': [[f'{F} 02:41', 'Na stacji tylko Kopeć (i ofiara). Burda w CZK, Szczerba w domu, Hajduk w drodze, Pyka na zakładzie', 'Macierz alibi']]}},
]

hintTrail = [
 {'unless': ['sp-body'], 'text': 'Zacznijcie od stacji nadawczej: ciało przy szafie nadajnika i to, co ofiara miała przy sobie.'},
 {'unless': ['sp-cabinet'], 'when': ['sp-body'], 'text': 'Szafa SN-1 ma własny dziennik zdarzeń. Sprawdźcie, co nadajnik robił tej nocy.'},
 {'unless': ['sp-door'], 'when': ['sp-cabinet'], 'text': 'Kto wchodził na stację? Drzwi mają czytniki kart po obu stronach.'},
 {'unless': ['sp-console'], 'when': ['sp-door'], 'text': 'Z archiwum Centrum zniknął zapis alarmu. Sprawdźcie, co mówi konsola operatorki.'},
 {'unless': ['sp-gasnet'], 'when': ['sp-console'], 'text': 'Czujniki Chemrud wysłały żądanie alarmu. Zobaczcie ich dziennik.'},
 {'unless': ['p-service'], 'when': ['e09'], 'text': 'Dziennik SN-1 ma dwa wpisy o trybie SERWIS. Ile trwał ten stan?'},
 {'unless': ['lie:k-l1'], 'when': ['e12'], 'text': 'Karta SRV-07 należy do puli firmy Syreon. Kopeć twierdzi, że spał w domu. Czy dokumenty to potwierdzają?'},
 {'unless': ['p-pin'], 'when': ['e27', 'e28'], 'text': 'Karteczka Lasoty podpowiada, z czym związany jest PIN do sejfu. Protokół odbioru zna datę.'},
 {'unless': ['p-time'], 'when': ['x6', 'x1'], 'text': 'Zegarek Lasoty nie był synchronizowany z siecią. Porównajcie jego wpis o telefonie z billingiem.'},
 {'unless': ['lie:b-l2'], 'when': ['x5'], 'text': 'Dziennik audytu pokazuje, kto i kiedy usunął zapis alarmu. Operatorka twierdzi, że niczego nie kasowała.'},
 {'unless': ['p-alibi'], 'when': ['p-time', 'e39'], 'text': 'Zbierzcie, gdzie kto był o 1:47 i o 2:41. Potrzebujecie kamery, czytnika, rejestru Syreon i danych lokalizacyjnych.'},
 {'unless': ['lie:k-l6'], 'when': ['x4', 'e13'], 'text': 'Sekcja i klucz dynamometryczny rozstrzygną, czy to był wypadek. Porównajcie je z przydziałem narzędzi w Syreon.'},
 {'text': 'Macie dość, by złożyć raport. Upewnijcie się, że każdy wniosek umiecie podeprzeć dowodem.'},
]

_wrong = {'accident': 'Nieszczęśliwy wypadek'}
report = {'questions': [
 {'id': 'r-who', 'q': 'Kto zabił Bogdana Lasotę?', 'type': 'single', 'points': 12,
  'options': [['kopec', 'Dariusz Kopeć, inżynier serwisowy'], ['burda', 'Agnieszka Burda, operatorka dyżurna'], ['szczerba', 'Piotr Szczerba, wiceprezydent'], ['hajduk', 'Lena Hajduk, dziennikarka'], ['pyka', 'Witold Pyka, prezes Chemrud'], ['accident', 'Nikt — to był nieszczęśliwy wypadek przy rozdzielni']],
  'correct': 'kopec',
  'proof': {'count': 3, 'each': 4, 'valid': ['e09', 'e12', 'e13', 'e39', 'e42', 'e41', 'x3', 'x4', 't05'], 'label': 'Wskażcie trzy dowody, które najmocniej łączą sprawcę z zabójstwem.'}},
 {'id': 'r-help', 'q': 'Kto — oprócz sprawcy — bezpośrednio przyczynił się do ciszy syren lub zniknięcia zapisu: zatwierdził okno serwisowe albo usunął zapis alarmu z archiwum?', 'type': 'multi', 'points': 12,
  'hint': 'Zaznaczcie wszystkie właściwe osoby. Każda błędna odpowiedź odejmuje punkty za trafną.',
  'options': [['burda', 'Agnieszka Burda'], ['szczerba', 'Piotr Szczerba'], ['hajduk', 'Lena Hajduk'], ['pyka', 'Witold Pyka']], 'correct': ['burda', 'szczerba']},
 {'id': 'r-how', 'q': 'Dlaczego syreny nie zawyły o 1:47?', 'type': 'single', 'points': 10,
  'options': [['service', 'Nadajnik SN-1 był w trybie SERWIS i ignorował polecenia'], ['sensor', 'Czujniki Chemrud nie wysłały żądania alarmu'], ['operator', 'Operatorka nie wcisnęła przycisku alarmu'], ['link', 'Awaria łącza K1 w mieście'], ['hack', 'Atak na serwer CZK przez łącze serwisowe']], 'correct': 'service'},
 {'id': 'r-when', 'q': 'Kiedy doszło do ataku na Lasotę?', 'type': 'single', 'points': 10,
  'options': [['0147', 'Ok. 1:47'], ['0231', 'Ok. 2:31'], ['0234', 'Ok. 2:34'], ['0241', 'Ok. 2:41'], ['0309', 'Ok. 3:09']], 'correct': '0241'},
 {'id': 'r-motive', 'q': 'Jaki był motyw?', 'type': 'single', 'points': 12,
  'options': [['cover', 'Lasota miał rano ujawnić NIK i prasie, że kanału K3 nie ma, a odbiór systemu sfałszowano'], ['dispute', 'Spór o wynagrodzenie za wymianę modułu K3'], ['chlorine', 'Lasota chciał zgłosić wyciek w Chemrud'], ['audit', 'Lasota przyłapał sprawcę na kradzieży części z magazynu Syreon']], 'correct': 'cover'},
 {'id': 'r-k3', 'q': 'Co naprawdę stało się z kanałem rezerwowym K3 w 2024 roku?', 'type': 'single', 'points': 10,
  'options': [['dummy', 'Wykreślono go aneksem, zamontowano atrapę, a w protokole wpisano pozytywny test'], ['failed', 'Zamontowano go, ale uległ awarii po odbiorze'], ['removed', 'Zdemontowano go w nocy zdarzenia podczas okna serwisowego'], ['works', 'K3 działał, tylko tej nocy zablokował go tryb SERWIS']], 'correct': 'dummy'},
 {'id': 'r-log', 'q': 'Jak zniknął zapis alarmu z archiwum?', 'type': 'single', 'points': 10,
  'options': [['burda', 'Operatorka usunęła go na stanowisku CZK z polecenia wiceprezydenta'], ['kopec', 'Kopeć usunął go zdalnie przez łącze serwisowe'], ['lasota', 'Skasował go Lasota, zanim zginął'], ['crash', 'Zniknął w awarii serwera']], 'correct': 'burda'},
 {'id': 'r-order', 'q': 'Ułóżcie wydarzenia tej nocy we właściwej kolejności.', 'type': 'order', 'points': 12,
  'items': [['park', 'Lasota zaczyna spotkanie z Leną Hajduk na parkingu pod Kolonią (ok. północy)'], ['enter', 'Kopeć wchodzi na stację kartą SRV-07'], ['service', 'Kopeć przełącza SN-1 w tryb SERWIS'], ['alarm', 'Czujniki Chemrud wysyłają alarm, SN-1 go ignoruje'], ['lasota', 'Lasota wchodzi na stację'], ['attack', 'Kopeć zabija Lasotę'], ['clear', 'Kopeć kasuje kolejkę alarmów i wychodzi z trybu SERWIS'], ['delete', 'Operatorka usuwa zapis alarmu z archiwum']],
  'correct': ['park', 'enter', 'service', 'alarm', 'lasota', 'attack', 'clear', 'delete']},
]}

solution = {
 'summary': 'Bogdana Lasotę zabił Dariusz Kopeć, inżynier serwisowy firmy Syreon, o 2:41 w stacji nadawczej „Kolonia”. Tego samego wieczora, pod pozorem okna serwisowego zatwierdzonego przez wiceprezydenta Szczerbę, wyłączył nadajnik kluczem SERWIS, więc o 1:47 alarm z Chemrud nie poszedł do syren. Zapis alarmu usunęła potem operatorka Burda na polecenie Szczerby.',
 'steps': [
  {'h': 'Głuchy nadajnik', 'p': 'Dziennik SN-1 pokazuje tryb SERWIS od 1:03:22 do 3:02:11 (119 minut) i polecenie alarmu zignorowane o 1:47:09. Syreny nie zawyły dlatego, że ktoś wyłączył nadajnik kluczem, a nie z awarii łącza.'},
  {'h': 'Kto miał klucz', 'p': 'Klucz SYR-1 i kartę SRV-07 wydano 26.11 o 16:10 Dariuszowi Kopeciowi. Wolak był na urlopie, Tarka na zwolnieniu. Czytnik D1 pokazuje SRV-07 na stacji od 0:41 do 3:09, a GPS busa zgadza się z tym w granicach kilku minut.'},
  {'h': 'Okno bez administratora', 'p': 'Okno MW-2611 zatwierdził Szczerba, choć regulamin pozwalał na to tylko przy nieobecności administratora powyżej 72 godzin. Lasota był w pracy i o oknie nie wiedział.'},
  {'h': 'Kanał, którego nie ma', 'p': 'Aneks nr 2 z maja 2024 usunął K3 z dostawy (oszczędność 612 000 zł), a protokół odbioru z czerwca podał K3 jako przetestowany na 25 W. Telemetria z nadajnika zapisała dwa negatywne testy i ręczny wpis „PASS” z klucza SYR-1. Do złącza K3 wpięto atrapę 50 Ω. Faktura Alfa-Doradztwo (310 000 zł, firma żony Szczerby, płatnik Syreon) pokazuje, kto zyskał.'},
  {'h': 'Motyw', 'p': 'Lasota porównał telemetrię z protokołem, przekazał kopię dziennikarce i miał o 9:00 powiedzieć wszystko NIK. Kopeć i Szczerba mieli czas do rana.'},
  {'h': 'Zegarek', 'p': 'Zegarek Lasoty spóźniał się o 7 minut: połączenie do Hajduk o 2:34 widnieje na nim jako 2:27. Zdjęcie z nadgarstka o 2:34 na zegarku to prawdziwe 2:41, moment ataku.'},
  {'h': 'Wypadek, który nim nie był', 'p': 'Sekcja: uderzenie okrągłym przedmiotem o średnicy 38 mm w potylicę i pośmiertne oparzenia. Klucz dynamometryczny SY-TW-17 przypisany Kopeciowi leżał w kanale za szafą, a jego gniazdo w busie było puste.'},
  {'h': 'Zacieranie śladów', 'p': 'Kopeć skasował kolejkę alarmów o 3:01:50 i wyszedł z SERWIS, żeby alarm nie poszedł spóźniony. O 3:35 Szczerba kazał Burdzie usunąć zapis, a ta o 3:41:07 skasowała go własnym PIN-em jako „testowy”.'},
  {'h': 'Fałszywe tropy', 'p': 'Hajduk skłamała, bo chroniła źródło, i wjechała pod Kolonię dopiero o 3:05, kiedy Lasota już nie żył. Pyka skłamał o wycieku, bo nie chciał kolejnej kontroli. Był winny zaniedbania, ale nie tej nocy na stacji. Burda uwierzyła w „test czujnika”, a potem wykonała polecenie przełożonego.'},
 ]}

endings = {
 'correct': {'title': 'Martwy kanał', 'text': 'Dariusz Kopeć zostaje zatrzymany w garażu Syreon, w kurtce z logo firmy. Nie próbuje uciekać. W prokuraturze przyznaje wszystko, a Szczerba i Burda stają przed zarzutami zatajenia i niedopełnienia obowiązków. Kontrola NIK zaczyna się o 9:00, jak zaplanowano, tylko bez człowieka, który miał ją otworzyć. Syreny w Rudzie dostają prawdziwy kanał rezerwowy po trzech miesiącach.',
  'decision': {'q': 'Zostaje pendrive od Lasoty, teczka K3 i komplet dokumentów z umowy. Co zrobicie?', 'options': [
   {'id': 'law', 'label': 'Wszystko do prokuratury i NIK — pełne rozliczenie umowy z 2024', 'text': 'Prokuratura i NIK dostają komplet i prowadzą wspólne postępowanie. Po roku Szczerba traci stanowisko, a Syreon płaci karę i wymienia K3 na własny koszt. Ruda dostaje rzetelny audyt systemu.'},
   {'id': 'press', 'label': 'Przekazać dokumenty Lenie Hajduk przed południem', 'text': 'Artykuł „Syreny na papierze” ukazuje się jeszcze w piątek. Prezydent miasta dymisjonuje Szczerbę w tydzień. Prokuratura zarzuca wam wyciek, ale postępowanie przeciw Syreon nabiera tempa dzięki presji opinii publicznej.'},
   {'id': 'fix', 'label': 'Zażądać u prezydenta natychmiastowej wymiany K3, zanim zacznie się proces', 'text': 'Prezydent zarządza awaryjną instalację kanału rezerwowego w dwa tygodnie. Ruda bezpiecznie przechodzi zimę, ale dokumentacja trafia do prokuratury później i dwóch urzędników zdąży usunąć część śladów.'},
  ]}},
 'wrong': {
  'burda': {'title': 'Operatorka', 'text': 'Oskarżacie Agnieszkę Burdę, bo skasowała zapis alarmu i skłamała o tej nocy. Dziennik audytu potwierdza usunięcie, ale kamera pokazuje, że o 2:41 siedziała w sali dyżurnej, a Lasotę zabił ktoś na wzgórzu. Burda dostaje zarzut za zatajenie, a sprawca czeka na kolejną okazję.'},
  'szczerba': {'title': 'Wiceprezydent', 'text': 'Szczerba zatwierdził okno i skłamał w kilku sprawach, więc oskarżacie go o zabójstwo. W nocy był jednak w domu, a telefon pokazuje go na osiedlu Parkowe. Prokurator przyjmie zarzuty o korupcję i poświadczenie nieprawdy, ale nie zabójstwo.'},
  'hajduk': {'title': 'Dziennikarka', 'text': 'Lena Hajduk skłamała, że nie widziała się z Lasotą, i dwa razy była pod Kolonią. Ale wjechała tam o 3:05, kiedy Lasota nie żył od ponad dwudziestu minut, a jej samochód nie ma nic wspólnego z busem Syreon. Redakcja dostaje pozew, a prawdziwy sprawca czyta o tym w gazecie.'},
  'pyka': {'title': 'Prezes', 'text': 'Witold Pyka ukrył wyciek i skłamał o telefonie do wiceprezydenta. Naprawdę jest odpowiedzialny za zaniedbanie, ale o 2:41 był już na zakładzie, kilkanaście kilometrów od stacji. Prokurator wnosi zarzut narażenia ludzi na utratę zdrowia, a sprawca pozostaje na wolności.'},
  'accident': {'title': 'Nieszczęśliwy wypadek', 'text': 'Porażenie prądem przy szafie nadajnika. Sprawa zostaje zamknięta po sekcji, w której zapisano oparzenia, ale pominięto pośmiertny charakter obrażeń. Po tygodniu NIK i tak znajduje atrapę kanału K3, a ktoś pyta, dlaczego administrator systemu był na stacji o 2:30 w nocy.'},
 },
 'partial': 'Wskazaliście właściwą osobę, ale część waszych wniosków jest błędna lub niepoparta dowodami. Prokurator przyjmuje sprawę, choć obrona będzie miała o co walczyć.',
}

breakthroughs = [
 {'id': 'b-service', 'when': 'p-service', 'title': 'Głucha stacja', 'text': 'Przez 119 minut nadajnik SN-1 ignorował każde polecenie. Syreny milczały nie dlatego, że system się zepsuł, ale dlatego, że ktoś go wyłączył kluczem.'},
 {'id': 'b-k3', 'when': 'e30', 'title': 'Martwy kanał', 'text': 'Telemetria z nadajnika mówi, że kanał rezerwowy K3 od dwóch lat nie nadaje. W protokole odbioru ktoś wpisał, że działa.'},
 {'id': 'b-time', 'when': 'p-time', 'title': 'Siedem minut', 'text': 'Zegarek Lasoty spóźniał się o siedem minut. Cała noc przesuwa się o tyle, a wraz z nią to, kto mógł być gdzie.'},
 {'id': 'b-blow', 'when': 'lie:k-l6', 'title': 'Jedno uderzenie', 'text': 'Kopeć przyznaje: Lasota nie dotknął szyn. Został uderzony, a dopiero potem ułożony przy rozdzielni. Wypadek był wymyślony.'},
]

tableMode = {'parBonus': 6, 'locations': [
 {'id': 'hq', 'name': 'Centrala wydziału', 'kind': 'Zapytania przez radio',
  'desc': 'Wóz dowodzenia przed bramą stacji. Każde zapytanie to jeden ruch, odpowiedzi przychodzą od razu.',
  'img': 'assets/places/001-hq.webp',
  'spots': [
   spot('sp-hq-tel', 'Operator telekomunikacyjny', 'Prosicie o billing połączeń osób związanych ze sprawą.', ['x1']),
   spot('sp-hq-bts', 'Dane lokalizacyjne', 'Prosicie operatora o rejestracje telefonów w komórkach.', ['x2']),
   spot('sp-hq-flota', 'Telematyka Syreon', 'Prosicie firmę o wyciąg z GPS pojazdów floty.', ['x3']),
   spot('sp-hq-med', 'Zakład medycyny sądowej', 'Prosicie o wnioski z sekcji zwłok.', ['x4']),
   spot('sp-hq-cz', 'Informatyk CZK', 'Prosicie o odczyt dziennika audytu archiwum alarmów.', ['x5']),
   spot('sp-hq-zeg', 'Producent zegarka', 'Prosicie o odzyskanie danych z zegarka Lasoty.', ['x6']),
  ]}], 'questions': {}}
