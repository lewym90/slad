# Sprawa 006 „Ostatni seans” — dowody (część skryptu build_006.py)
D = '2026-12-05'; N = '2026-12-06'

def ev(id, type, title, summary, body, **kw):
    d = {'id': id, 'type': type, 'title': title, 'summary': summary, 'body': body}
    d.update({k: v for k, v in kw.items() if v is not None})
    return d

def T(h, m, text, src, day=D):
    return [f'{day} {h:02d}:{m:02d}', text, src]

LETTER = [
 'Łódź, 5 grudnia 2026 r.',
 '',
 'Szanowna Pani Konserwator,',
 'dwa plakaty w gablocie „Zorzy”',
 'to nie są te, które wiszą tu',
 'od lat. To kopie. Znam każdą',
 'plamkę na oryginałach.',
 '„Czarną perłę” i „Dziewczynę',
 'z Bałut” znalazłem w katalogu',
 'domu aukcyjnego „Rewers”,',
 'aukcja 12 grudnia, poz. 117 i 118.',
 'Klucz do gabloty mają dwie osoby:',
 'ja i kierowniczka kina.',
 'Proszę o interwencję przed aukcją.',
 '',
 'Leon Barcz, kinooperator',
]

evidence = [
 # ---------- AKTA POCZĄTKOWE ----------
 ev('e01', 'Raport', 'Raport z miejsca zdarzenia', 'Sobota, 22:55. Pierwsze ustalenia patrolu w kinie „Zorza”.', [
   {'kv': [['Miejsce', 'Kino „Zorza”, ul. Gdańska 41, Łódź — kabina projekcyjna nad balkonem'],
           ['Zmarły', 'Leon Barcz, 73 l., kinooperator kina „Zorza” od 1974 roku'],
           ['Zgłoszenie', 'Ewa Sitek, kierowniczka kina, telefon na 112 o 22:43'],
           ['Znaleźli', 'Ewa Sitek i Damian Wróbel, około 22:41']]},
   'W sobotę kino zorganizowało „Ostatni seans” — pożegnalną projekcję z taśmy 35 mm przed zamknięciem kina. Film skończył się przed 22:00, potem w foyer trwało pożegnanie. Kinooperator na nie nie zszedł. Kierowniczka i technik poszli na górę. Wewnętrzne drzwi kabiny były zamknięte na klucz, a klucz od nich miał w kieszeni zmarły. Kierowniczka otworzyła zapasowym kluczem z biura.',
   'Leon Barcz leżał na podłodze na środku kabiny, przed stołem przewijarki, z raną tyłu głowy. Obok leżała stalowa puszka na taśmę filmową z krwią na krawędzi. Drzwi ewakuacyjne kabiny, prowadzące na zewnętrzne schody pożarowe, były zamknięte. W projektorze B wciąż paliła się lampa; zgasił ją technik.',
   {'note': 'Wstępna ocena patrolu: możliwy nieszczęśliwy wypadek — upadek ciężkiej puszki z regału. Prokurator nie przyjął tej wersji bez sekcji.'}],
   start=True, time=[T(22, 41, 'Ewa Sitek i Damian Wróbel znajdują ciało Leona Barcza w kabinie', 'Raport'), T(22, 43, 'Zgłoszenie na 112', 'Raport')]),
 ev('e02', 'Zlecenie', 'Polecenie prokuratora', 'Wypadek czy zabójstwo?', [
   {'quote': 'Siedemdziesięciotrzyletni kinooperator ginie w zamkniętej kabinie w trakcie ostatniego seansu w historii kina. Sto dwanaście osób na sali, nikt niczego nie zauważył, film poszedł do końca. Chcę wiedzieć, czy to był wypadek. A jeśli nie — kto i dlaczego.', 'by': 'prok. Marek Olszewski, Prokuratura Rejonowa Łódź-Śródmieście'},
   {'kv': [['Zakres', 'przyczyna śmierci Leona Barcza; sprawca, jeśli był; jak dostał się do kabiny i jak z niej wyszedł; motyw'], ['Dostęp', 'budynek kina, podwórze, rejestry PESEL, CEPiK, KRS i EKW']]}],
   start=True),
 ev('e03', 'Opinia', 'Wstępna opinia lekarza', 'Oględziny w kabinie, sobota 23:30.', [
   'Rana tłuczona tyłu głowy, w okolicy ciemieniowej, od jednego uderzenia krawędzią twardego, metalowego przedmiotu. Kształt rany zgodny z krawędzią wieczka puszki na taśmę filmową, zabezpieczonej przy ciele.',
   {'kv': [['Szacowany czas zgonu', 'między 20:30 a 21:30'], ['Śmierć', 'najpewniej w ciągu kilku minut od urazu'], ['Ślady walki', 'brak']]},
   {'note': 'Czy uraz mógł powstać od puszki spadającej z regału, rozstrzygnie sekcja.'}],
   start=True),
 ev('e04', 'Ulotka', 'Program wieczoru „Ostatni seans”', 'Rozdawany widzom przy wejściu.', [
   {'quote': 'Kino „Zorza” 1958–2026. Ostatni seans. 19:30 — lampka wina w foyer. 20:00 — „Dziewczyna z Bałut” (1958), pierwszy film wyświetlony w „Zorzy”, z oryginalnej kopii 35 mm, 104 minuty. Po seansie — pożegnanie z kinem w foyer. Projekcję poprowadzi pan Leon Barcz, kinooperator „Zorzy” od 1974 roku.', 'by': 'ulotka kina'},
   {'note': 'Na odwrocie: „Dziękujemy, że byliście z nami. Ewa Sitek, kierowniczka kina”.'}],
   start=True, time=[T(20, 0, 'Początek projekcji „Dziewczyny z Bałut” (104 min)', 'Program wieczoru')]),
 ev('e05', 'Wykaz', 'Kto był w budynku', 'Lista sporządzona przez patrol po północy.', [
   {'kv': [['Widzowie', '112 osób (sprzedane bilety i zaproszenia)'],
           ['Personel', 'Ewa Sitek (kierowniczka), Damian Wróbel (technik projekcji), Joanna Rak (bufet), Leon Barcz (kinooperator)'],
           ['Goście specjalni', 'dr Alicja Wrzos, miejska konserwator zabytków; Grzegorz Barcz, syn kinooperatora'],
           ['Sąsiedzi', 'Stanisław Lipka, ul. Gdańska 43 (oficyna) — zgłosił się sam: widział coś ze swojego okna']]},
   {'note': 'Dr Wrzos wyszła o 22:10, przed znalezieniem ciała. Pozostali z listy zgodzili się zostać do rana albo wrócić na przesłuchanie.'}],
   start=True),

 # ---------- KABINA PROJEKCYJNA ----------
 ev('e06', 'Dziennik', 'Dziennik kabiny', 'Gruby zeszyt w kratkę na pulpicie między projektorami.', [
   'Na wewnętrznej stronie okładki ołówkiem: „24 klatki = 1 sekunda. Klatka 35 mm (4 perforacje) = 19 mm.”',
   {'log': ['28.11  „Lato w Arkadii”, kopia 35 mm, 2 części',
            '       18:00  start — cz. I na A',
            '       18:59  zm. A→B',
            '       19:12  cz. I przewinięta',
            '       19:41  koniec, światło na sali             L.B.',
            ' 5.12  „Dziewczyna z Bałut”, kopia 35 mm, 2 części',
            '       20:00  start — cz. I na A                  L.B.']},
   {'note': 'Po wpisie o 20:00 strona jest pusta. Wcześniejsze kartki: przy każdym seansie z taśmy ta sama kolejność — start, zmiana projektora co do minuty, przewinięcie, koniec.'}],
   time=[T(20, 0, 'Leon Barcz wpisuje do dziennika start projekcji (cz. I na projektorze A)', 'Dziennik kabiny')]),
 ev('e07', 'Oględziny', 'Projektor A i stół przewijarki', 'Dwa projektory Meopta i stół do przewijania taśmy.', [
   'Projektor A wyłączony. Na jego szpuli cała część I, nawinięta końcem na zewnątrz — czyli po projekcji nieprzewinięta. Na projektorze B część II, puszczona do samego końca; luźny koniec taśmy zwisa aż do podłogi.',
   'Stół przewijarki pusty. Na blacie odciśnięty w kurzu okrągły ślad, wielkości puszki na szpulę.'],
   ),
 ev('e08', 'Przedmiot', 'Puszka przy ciele', 'Stalowa puszka na szpulę 1800 m.', [
   'Pusta stalowa puszka z wieczkiem, waga 2,9 kg. Etykieta: „Dziewczyna z Bałut — cz. I”. Na krawędzi wieczka krew i włosy.',
   'Puszka leżała u stóp regału z taśmami, metr od ciała — jakby spadła z góry. Na górnej półce regału, na wysokości około 1,9 m, gruba, nienaruszona warstwa kurzu — nie ma w niej śladu po niczym, co stałoby tam niedawno.'],
   ),
 ev('e09', 'Fotografia', 'Zdjęcie na ścianie kabiny', 'Oprawione w ramkę, nad stołem przewijarki.', [
   'Czarno-białe zdjęcie: wąsaty mężczyzna w roboczym fartuchu i młoda jasnowłosa kobieta z włosami spiętymi w kok, przy projektorze. Kobieta w białych rękawiczkach trzyma rękę na dźwigni zmiany.',
   {'quote': 'Kabina „Zorzy”, 1998. Leon i jego najzdolniejsza uczennica — Ewa Kalinowska.', 'by': 'podpis na passe-partout'}]),
 ev('e10', 'Oględziny', 'Drzwi ewakuacyjne kabiny', 'Stalowe drzwi na schody pożarowe.', [
   'Drzwi z samozamykaczem i drążkiem od środka, od zewnątrz bez klamki — zamknięte otwiera się je tylko z kabiny. Przy progu w linoleum świeże wgniecenie, jak od drewnianego klina. Klina w kabinie nie ma.',
   {'quote': 'KLIN! Lampy grzeją. L.B.', 'by': 'kartka przyklejona nad drążkiem'}]),
 ev('e11', 'Dokument', 'Karta kopii filmowej', 'W otwartej puszce części II, przy projektorze B.', [
   {'kv': [['Tytuł', '„Dziewczyna z Bałut” (1958)'], ['Kopia', '35 mm, obraz 1:1,37, dźwięk optyczny'],
           ['Część I', '1 750 m'], ['Część II', '1 096 m'], ['Razem', '2 846 m']]},
   {'note': 'Dopisek długopisem: „Złożone na dwie duże szpule — jedna zmiana. Zorza, 5.12, ostatni raz. L.B.”'}]),
 ev('e12', 'Oględziny', 'Biurko kinooperatora', 'Mały stolik przy regale z taśmami.', [
   'Termos z herbatą, okulary, ołówek, stos starych biletów. Na wierzchu leży koperta zaadresowana starannym pismem:',
   {'quote': 'Pani dr Alicja Wrzos, Miejska Konserwator Zabytków — do rąk własnych.', 'by': 'koperta'},
   {'note': 'Koperta jest niezaklejona i pusta.'}]),
 ev('e26', 'Wyliczenie', 'Godzina zmiany projektorów', 'Wasze wyliczenie z karty kopii i dziennika.', [
   '24 klatki na sekundę po 19 mm to 0,456 m taśmy na sekundę, czyli 27,36 m na minutę. Część I ma 1 750 m, więc trwa 64 minuty. Projekcja ruszyła o 20:00, a zatem projektor B musiał zostać uruchomiony około 21:04.',
   {'note': 'Film poszedł bez przerwy. O 21:04 ktoś stał w kabinie przy projektorach. Leon Barcz nie wpisał tej zmiany do dziennika i nie przewinął części I — wbrew zwyczajowi, którego trzymał się od lat.'}],
   time=[T(21, 4, 'Zmiana projektorów A→B — wykonał ją ktoś w kabinie', 'Wyliczenie')]),

 # ---------- FOYER ----------
 ev('e13', 'Oględziny', 'Gablota z plakatami', 'Przeszklona gablota na ścianie foyer.', [
   'Cztery plakaty filmowe w ramach: „Czarna perła” (1934), „Wiatr od Bałtyku” (1949), „Dziewczyna z Bałut” (1958), „Noc nad Wartą” (1962). Gablota zamknięta na zamek patentowy.',
   'Przy dolnej krawędzi dwóch plakatów — „Czarnej perły” i „Dziewczyny z Bałut” — widać pod lupą maleńki nadruk wtopiony w papier: „FX 25”. Na dwóch pozostałych nie ma niczego podobnego.']),
 ev('e14', 'Oględziny', 'Panel oświetlenia sali', 'Przy drzwiach z foyer na salę.', [
   'Szafka z przełącznikami oświetlenia widowni. Nad nią mosiężna tabliczka:',
   {'quote': 'Światło na sali zapala kinooperator z kabiny. Panel tylko w razie awarii. L.B.', 'by': 'tabliczka nad panelem'}]),

 # ---------- BIURO KIEROWNICZKI ----------
 ev('e16', 'Przedmiot', 'Płaszcz kierowniczki', 'Zabezpieczony za zgodą prokuratora.', [
   'Jasnobeżowy trencz z wieszaka w biurze. Ramiona i plecy jeszcze wilgotne. Na prawym rękawie, od mankietu do łokcia, i na prawej kieszeni rdzawe smugi oraz drobiny czerwonopomarańczowej farby.',
   {'note': 'Technik porównał je z próbką z poręczy schodów pożarowych kina: ta sama farba antykorozyjna (minia) i ta sama rdza. Kontener na makulaturę przy tylnych drzwiach jest plastikowy.'}]),
 ev('e17', 'Dokument', 'Teczka „Plakaty”', 'Z szafy w biurze kierowniczki.', [
   {'kv': [['Wycena (2024)', 'Pracownia Konserwacji i Ekspertyz Papieru VESPER, Wrocław: cztery plakaty, oryginały, łącznie 186 000 zł'],
           ['Najcenniejsze', '„Czarna perła” (1934) — 92 000 zł; „Dziewczyna z Bałut” (1958) — 41 000 zł'],
           ['Faktura VESPER z 14.10.2025', 'wykonanie dwóch faksymile ekspozycyjnych: „Czarna perła”, „Dziewczyna z Bałut” — 3 800 zł'],
           ['Zamawiająca', 'Ewa Sitek, kierowniczka kina']]},
   {'note': 'Na zamówieniu dopisek: „oryginały — do depozytu”. W teczce nie ma żadnego dokumentu depozytu.'}],
   time=[T(10, 0, 'Kierowniczka zamawia w pracowni VESPER dwie faksymile plakatów', 'Teczka „Plakaty”', '2025-10-14')]),
 ev('e18', 'Oględziny', 'Szafka z kluczami', 'W biurze, obok biurka.', [
   'Zapasowe klucze opisane na zawieszkach: kabina (drzwi wewnętrzne), zaplecze, gablota w foyer — kluczyk nr 2. Zeszyt wydań kluczy: kluczyk do gabloty nie był nikomu wydawany od 2019 roku.',
   {'note': 'Kluczyk nr 1 do gabloty nosił przy sobie Leon Barcz — znaleziono go w jego kieszeni razem z kluczem do kabiny.'}]),

 # ---------- PODWÓRZE ----------
 ev('e19', 'Oględziny', 'Schody pożarowe', 'Stalowe schody z kabiny na podwórze.', [
   'Dwa biegi z pomostem, poręcz pomalowana dawno temu czerwonopomarańczową farbą antykorozyjną, łuszcząca się i rdzawa. W połowie dolnego biegu, na wysokości dłoni, farba jest świeżo starta na długości kilkunastu centymetrów — jakby ktoś zjeżdżał ręką po mokrej poręczy.']),
 ev('e20', 'Przedmiot', 'Skrawki z kontenera', 'Niebieski plastikowy kontener na makulaturę przy tylnych drzwiach.', [
   'Na wierzchu, pod uchyloną klapą: mokra kartka w linie, podarta na dziewięć kawałków. Pismo odręczne, staranne, atrament miejscami się rozmył. Pod spodem kartony po kubkach z baru.',
   {'note': 'Skrawki zabezpieczono i wysuszono. Złóżcie je w analizie — zagadka „Podarty list”.'}]),
 ev('e21', 'Przedmiot', 'Drewniany klin', 'U stóp schodów pożarowych, w kałuży.', [
   'Gruby, wytarty klin z jasnego drewna z wywierconą dziurką i pętlą czerwonego sznurka — żeby dało się go wyszarpnąć spod drzwi jednym ruchem. Mokry. Na jednej krawędzi świeże wgniecenie, jakby spadł z wysoka na stalowy stopień.']),
 ev('e22', 'Oględziny', 'Tylne drzwi zaplecza', 'Z podwórza na korytarz zaplecza.', [
   'Metalowe drzwi z zamkiem i czujnikiem alarmu nad framugą. Za nimi korytarz zaplecza: po prawej, trzy kroki od drzwi, biuro kierowniczki; dalej korytarz prowadzi do foyer. Z podwórza nie ma innego wejścia do budynku poza schodami pożarowymi do kabiny.']),
 ev('e27', 'Dokument', 'List Leona Barcza', 'Złożony z mokrych skrawków z kontenera.', [
   {'quote': ' '.join(x for x in LETTER if x), 'by': 'odręczny list, pismo Leona Barcza'},
   {'note': 'To list z pustej koperty na biurku w kabinie. Ktoś go podarł i wyrzucił do kontenera przy tylnych drzwiach kina.'}]),

 # ---------- MIESZKANIE STANISŁAWA LIPKI ----------
 ev('e23', 'Oględziny', 'Widok z okna pana Lipki', 'II piętro oficyny naprzeciwko kina.', [
   'Okno wychodzi na wspólne podwórze. Wprost naprzeciwko, jakieś piętnaście metrów dalej, tylna ściana kina, schody pożarowe i drzwi kabiny. Latarnia na podwórzu oświetla dolny bieg schodów i tylne drzwi zaplecza.']),
 ev('e24', 'Oględziny', 'Zegar ścienny pana Lipki', 'Okrągły zegar nad stołem.', [
   'Okrągły zegar na baterię nad kredensem. Kiedy jesteście w mieszkaniu, pokazuje dokładnie o godzinę więcej niż wasze telefony.']),
 ev('e25', 'Przedmiot', 'Zegarek po bracie', 'Na stole, w otwartym pudełku.', [
   'Stary nakręcany zegarek kieszonkowy w pudełku z napisem „po Mietku”, obok otwarta paczka baterii — jednej brakuje. Zegarek chodzi równo — ale też pokazuje godzinę więcej niż wasze telefony. Nikt nie przestawił go od lata.']),

 # ---------- TAJNE AKTA / CENTRALA ----------
 ev('x1', 'Komunikat', 'Dane IMGW — opady', 'Punkt pomiarowy Łódź-Śródmieście, sobota 5.12.', [
   {'log': ['do 21:05        bez opadu, 4 °C', '21:05–23:40     deszcz słaby do umiarkowanego', 'wiatr           słaby, południowo-zachodni']}],
   private=True, time=[T(21, 5, 'Zaczyna padać deszcz', 'IMGW')]),
 ev('x2', 'Opinia', 'Sekcja zwłok — wnioski', 'Zakład Medycyny Sądowej, niedziela 8:00.', [
   'Jedno silne uderzenie krawędzią wieczka puszki e08 w tył głowy, zadane z góry i z zamachem przez osobę stojącą za ofiarą. Puszka o wadze 2,9 kg spadająca z wysokości 1,9 m nie wytworzyłaby takiego urazu ani takiego kąta rany.',
   {'kv': [['Czas zgonu', 'między 20:30 a 21:30, najpewniej w pierwszej połowie tego przedziału'], ['Wniosek', 'zabójstwo; wypadek wykluczony']]}],
   private=True),
 ev('x3', 'Kadry', 'Kamera pizzerii naprzeciwko kina', 'Pizzeria „Pod Zorzą”, ul. Gdańska 40 — kamera nad wejściem.', [
   {'log': ['20:56  młody mężczyzna w czarnej bluzie z logo „Zorzy” wychodzi z kina, idzie w prawo',
            '21:01  mężczyzna ok. 45 lat w ciemnej kurtce wychodzi z kina, telefon przy uchu',
            '21:01–21:12  ten sam mężczyzna stoi przed kinem, rozmawia, pali',
            '21:11  mężczyzna w czarnej bluzie wraca z reklamówką, wchodzi do kina',
            '21:12  mężczyzna w ciemnej kurtce wraca do kina']},
   {'note': 'Na kadrach rozpoznawalni: Damian Wróbel (bluza z logo kina) i Grzegorz Barcz. Kamera widzi tylko front kina, nie podwórze.'}],
   private=True, time=[T(20, 56, 'Damian Wróbel wychodzi z kina frontem, na ulicę', 'Kamera pizzerii'), T(21, 1, 'Grzegorz Barcz wychodzi przed kino z telefonem', 'Kamera pizzerii'),
                       T(21, 11, 'Damian Wróbel wraca z reklamówką', 'Kamera pizzerii'), T(21, 12, 'Grzegorz Barcz wraca do kina', 'Kamera pizzerii')]),
 ev('x4', 'Wydruk', 'Transakcja kartą Damiana Wróbla', 'Odpowiedź banku na zapytanie prokuratora.', [
   {'kv': [['Data i godzina', 'sobota 5.12.2026, 21:03:22'], ['Miejsce', 'sklep Żabka, ul. Gdańska 60, Łódź (ok. 300 m od kina)'], ['Kwota', '42,97 zł']]}],
   private=True, time=[T(21, 3, 'Damian Wróbel płaci kartą w sklepie przy Gdańskiej 60', 'Bank')]),
 ev('x5', 'Wydruk', 'Centrala alarmowa kina', 'Dziennik czujników drzwi, sobota 5.12.', [
   {'log': ['czuwanie: wyłączone 18:30–23:59 (impreza) — czujniki drzwi nadal zapisują zdarzenia',
            'strefa 4 — drzwi ewakuacyjne kabiny:  19:52:30 otwarte',
            '                                       21:11:02 zamknięte',
            'strefa 2 — tylne drzwi zaplecza:       20:41:12 otwarte · 20:41:19 zamknięte',
            '                                       21:13:05 otwarte · 21:13:14 zamknięte',
            'strefa 3 — wyjścia ewakuacyjne sali:   brak zdarzeń 19:00–22:40']},
   {'note': 'Czujnik strefy 4 rejestruje stan skrzydła drzwi: „otwarte” znaczy, że drzwi nie przylegają do framugi.'}],
   private=True, time=[T(19, 52, 'Drzwi ewakuacyjne kabiny zostają otwarte (na klin)', 'Centrala alarmowa'), T(20, 41, 'Ktoś wychodzi tylnymi drzwiami zaplecza na podwórze', 'Centrala alarmowa'),
                       T(21, 11, 'Drzwi ewakuacyjne kabiny zamykają się', 'Centrala alarmowa'), T(21, 13, 'Ktoś wchodzi tylnymi drzwiami z podwórza na zaplecze', 'Centrala alarmowa')]),
 ev('x6', 'Katalog', 'Katalog Domu Aukcyjnego „Rewers”', 'Aukcja „Plakat polski”, Kraków, 12.12.2026.', [
   {'kv': [['Poz. 117', '„Czarna perła” (1934), litografia barwna, 98 × 68 cm, cena wywoławcza 70 000 zł'],
           ['Poz. 118', '„Dziewczyna z Bałut” (1958), offset, 84 × 58 cm, cena wywoławcza 32 000 zł'],
           ['Pochodzenie obu', 'kolekcja prywatna, Łódź'],
           ['Komitent (umowa komisu z 2.11.2026)', 'Ars-Lokus sp. z o.o., Łódź; podpisał prezes zarządu']]},
   {'note': 'Dom aukcyjny nie podaje nazwiska prezesa — odsyła do rejestru KRS.'}],
   private=True, time=[T(12, 0, 'Spółka Ars-Lokus oddaje dwa plakaty do sprzedaży w domu aukcyjnym „Rewers”', 'Katalog aukcji', '2026-11-02')]),

 # ---------- WYDRUKI Z BAZ ----------
 ev('d01', 'Wydruk z bazy', 'PESEL: Sitek Ewa', 'Kierowniczka kina „Zorza”.', [], db='O-006-ewa'),
 ev('d02', 'Wydruk z bazy', 'KRS: Ars-Lokus', 'Komitent z katalogu aukcji.', [], db='F-006-ars'),
 ev('d03', 'Wydruk z bazy', 'PESEL: Sitek Tomasz', 'Prezes spółki Ars-Lokus.', [], db='O-006-tomasz'),

 # ---------- ZEZNANIA PO KONFRONTACJI ----------
 ev('t1', 'Zeznanie', 'Damian Wróbel: sklep zamiast podwórka', 'Po konfrontacji.', [
   'Od 20:56 do 21:11 nie było mnie na podwórku. Poszedłem do Żabki po wódkę i papierosy na po imprezie — pani Ewa zakazała alkoholu, więc nie chciałem się przyznać. Wróciłem frontem przez foyer.'],
   testimony=True, time=[T(21, 3, 'Damian Wróbel w sklepie, 300 m od kina', 'Zeznanie D. Wróbla')]),
 ev('t2', 'Zeznanie', 'Grzegorz Barcz: telefon przed kinem', 'Po konfrontacji.', [
   'Wyszedłem z sali o dziewiątej zadzwonić do człowieka, któremu jestem winien pieniądze. Stałem przed kinem do dwunastu po dziewiątej. Nie chciałem, żeby to wyszło.'],
   testimony=True),
 ev('t3', 'Zeznanie', 'Grzegorz Barcz: kłótnia z ojcem', 'Po konfrontacji.', [
   'Przed seansem prosiłem ojca, żeby poręczył mi pożyczkę albo dał mieszkanie pod zastaw. Odmówił. Pokłóciliśmy się przy barze. To była nasza ostatnia rozmowa.'],
   testimony=True, time=[T(19, 30, 'Grzegorz Barcz kłóci się z ojcem przy barze o pieniądze', 'Zeznanie G. Barcza')]),
 ev('t4', 'Zeznanie', 'Stanisław Lipka: sprostowanie godziny', 'Po wyjaśnieniu pomyłki.', [
   'Zegar nad stołem nastawiłem w czwartek z zegarka po bracie, a tego zegarka nikt nie przestawił na czas zimowy. Człowiek na schodach pożarowych zbiegał więc nie około 22:10, tylko około 21:10 — chwilę po tym, jak zaczęło kropić.'],
   testimony=True, time=[T(21, 10, 'Ktoś w długim jasnym płaszczu zbiega schodami pożarowymi kina', 'Zeznanie S. Lipki (po sprostowaniu)')]),
 ev('t5', 'Zeznanie', 'Ewa Sitek: schody pożarowe', 'Po konfrontacji.', [
   'Wyszłam tylnymi drzwiami za dwadzieścia dziewiąta. Weszłam po schodach pożarowych do kabiny. Pan Leon leżał na podłodze. Zamknęłam za sobą drzwi i zbiegłam — byłam na górze tylko chwilę.'],
   testimony=True),
 ev('t6', 'Zeznanie', 'Ewa Sitek: zmiana projektora', 'Po konfrontacji.', [
   'Byłam w kabinie dłużej. Kiedy kończyła się pierwsza część, zmieniłam projektor — nauczył mnie tego pan Leon trzydzieści lat temu. Wyszłam, kiedy zaczęło padać.'],
   testimony=True),
 ev('t7', 'Zeznanie', 'Ewa Sitek: przyznanie', 'Po konfrontacji.', [
   'Pan Leon pokazał mi list do pani konserwator i powiedział, że po seansie wręczy go przy wszystkich. Chwyciłam puszkę ze stołu przewijarki i uderzyłam. Potem pilnowałam, żeby film szedł dalej — póki szedł, wszyscy myśleli, że on żyje. List podarłam na schodach i wyrzuciłam do kontenera.'],
   testimony=True, time=[T(20, 50, 'Ewa Sitek zabija Leona Barcza w kabinie (według jej przyznania)', 'Zeznanie E. Sitek')]),
 ev('t8', 'Zeznanie', 'Ewa Sitek: plakaty', 'Po konfrontacji.', [
   'Oryginały „Czarnej perły” i „Dziewczyny z Bałut” oddaliśmy do sprzedaży przez firmę męża. W gablocie zawiesiłam faksymile. Kino i tak zamykają — myślałam, że nikt nie zauważy.'],
   testimony=True),
 ev('t9', 'Zeznanie', 'Ewa Sitek: praktyka w kabinie', 'Po konfrontacji.', [
   'Na zdjęciu jestem ja. Przed ślubem nazywałam się Kalinowska. Od 1996 do 2001 roku byłam kinooperatorką w „Zorzy”, uczył mnie pan Leon. Potem przeszłam do biura.'],
   testimony=True),
]
