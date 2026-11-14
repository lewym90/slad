# Sprawa 007 „Biała cisza” — dowody (część skryptu build_007.py)
D = '2027-01-15'; N = '2027-01-16'

def ev(id, type, title, summary, body, **kw):
    d = {'id': id, 'type': type, 'title': title, 'summary': summary, 'body': body}
    d.update({k: v for k, v in kw.items() if v is not None})
    return d

def T(h, m, text, src, day=D):
    return [f'{day} {h:02d}:{m:02d}', text, src]

CALL = 'Baza, tu Mglista. Minus dwadzieścia dwa, wiatr ucichł, wszystko gra. Następna łączność o szóstej. Bez odbioru.'

evidence = [
 # ---------- AKTA POCZĄTKOWE ----------
 ev('e01', 'Raport', 'Raport z miejsca zdarzenia', 'Sobota, 7:40. Ratownik GOPR i patrol z Karpacza.', [
   {'kv': [['Miejsce', 'Przełęcz Mglista (1495 m n.p.m.), Karkonosze — skała z masztem antenowym przy starym schronie turystycznym'],
           ['Zmarły', 'Krystian Lis, 38 l., łącznościowiec wyprawy „Północ 2028”'],
           ['Znaleźli', 'Adam Rogala, kierownik wyprawy, i ratownik GOPR Tomasz Kulig, około 7:10'],
           ['Zgłoszenie', 'Adam Rogala do GOPR, 6:25 — brak łączności ze schronem']]},
   'Krystian Lis został w piątek sam w schronie na przełęczy, żeby przez dobę testować w mrozie radiostację i baterie. O 6:00 nie odpowiedział na wywołanie z bazy w schronisku „Hala Szronów”. Kierownik wyprawy wezwał ratownika i obaj pojechali skuterem śnieżnym trasą zimową na przełęcz.',
   'Ciało leżało u stóp skały, na której stoi maszt anteny wyprawy, piętnaście metrów od drzwi schronu. Rana tyłu głowy. Drzwi schronu zamknięte, ale nie na klucz. W piecu zimno, radiostacja włączona.',
   {'note': 'Wstępna ocena: nieszczęśliwy wypadek — upadek ze skały w nocy, przy wietrze i oblodzeniu, podczas sprawdzania anteny. Prokurator nie przyjął tej wersji bez sprawdzenia. Ciało zostaje na miejscu do waszych oględzin, pilnuje go ratownik.'}],
   start=True, time=[T(6, 0, 'Schron nie odpowiada na wywołanie bazy', 'Raport', N), T(7, 10, 'Adam Rogala i ratownik GOPR znajdują ciało pod skałą z masztem', 'Raport', N)]),
 ev('e02', 'Zlecenie', 'Polecenie prokuratora', 'Wypadek czy zbrodnia?', [
   {'quote': 'Łącznościowiec ginie nocą, sam na przełęczy, a po północy jego głos słychać w radiu. Chcę wiedzieć, czy spadł z tej skały, czy ktoś mu pomógł. Jeśli ktoś — to kto, kiedy i dlaczego. Wszyscy, którzy byli w nocy w schronisku, zostają na miejscu.', 'by': 'prok. Jan Sobczak, Prokuratura Rejonowa w Jeleniej Górze'},
   {'kv': [['Zakres', 'przyczyna i czas śmierci Krystiana Lisa; sprawca, jeśli był; nocna łączność radiowa; motyw'],
           ['Dostęp', 'schronisko „Hala Szronów” z otoczeniem, schron na Przełęczy Mglistej, szlaki, rejestry PESEL, CEPiK, KRS i EKW']]}],
   start=True),
 ev('e03', 'Komunikat', 'Komunikat GOPR na sobotę', 'Dyżurka GOPR w Karpaczu, 7:30.', [
   {'kv': [['Pogoda', 'do południa wiatr 40–60 km/h, widoczność dobra; od około 13:00 śnieżyca, porywy do 90 km/h'],
           ['Szlak zielony przez Żleb Mglisty', 'od 13:00 zamknięty — zagrożenie lawinowe 3. stopnia; na przełęcz tylko trasą zimową, wzdłuż tyczek'],
           ['Zmierzch', '16:21'],
           ['Sekcja zwłok', 'Zakład Medycyny Sądowej we Wrocławiu przekaże wstępne wyniki telefonicznie około 15:00']]},
   {'note': 'Ratownik poprowadzi was w rakietach śnieżnych. Czasy przejść są na mapie w zakładce Miejsca.'}],
   start=True),
 ev('e04', 'Notatka', 'Czasy przejść zimą', 'Notatka ratownika Tomasza Kuliga dla prokuratora.', [
   {'log': ['Hala Szronów → Przełęcz Mglista, szlak zielony    pieszo, w rakietach 1:20    narty skiturowe 0:50–1:05',
            'Przełęcz Mglista → Hala Szronów, szlak zielony    pieszo, w rakietach 0:55    zjazd na nartach 0:15–0:20',
            'Hala Szronów → Przełęcz Mglista, trasa zimowa     pieszo, w rakietach 1:45    narty skiturowe 1:15',
            'Przełęcz Mglista → Hala Szronów, trasa zimowa     pieszo, w rakietach 1:15    zjazd na nartach 0:30',
            'Hala Szronów ↔ Rozdroże pod Jaworem               w górę 0:35 · w dół 0:25']},
   {'note': 'Czasy dla dobrej widoczności i warunków z piątkowej nocy. Podejście na nartach w 50 minut to tempo zawodnika. Zjazd nocą, z czołówką, zajmuje 15–20 minut. Skuter śnieżny jeździ tylko trasą zimową.'}],
   start=True),
 ev('e05', 'Wydruk', 'Plan obozu treningowego', 'Kartka przypięta na ścianie jadalni.', [
   {'log': ['wt 12.01    wejście na Przełęcz Mglistą, noc w schronie — cały zespół',
            'śr 13.01    trening: pulki, namioty, łączność; noc w schronie',
            'czw 14.01   trening nocny, zdjęcia do filmu; noc w schronie',
            'pt 15.01    16:00 zjazd do schroniska „Hala Szronów” (bez K. Lisa)',
            '            K. Lis — test radiostacji i baterii w mrozie, 24 h, sam w schronie',
            '            łączności z bazą: 22:00 i 6:00',
            'sob 16.01   8:00 zjazd K. Lisa do schroniska, podsumowanie obozu',
            'pon 18.01   konferencja prasowa ze sponsorem — Polar-Tex S.A., Warszawa']},
   {'note': 'Dopisek długopisem: „Nocne wyjścia poza schronisko tylko w parach i po zgłoszeniu. A.R.”'}],
   start=True),
 ev('e06', 'Wykaz', 'Kto był w nocy w schronisku', 'Lista sporządzona przez patrol.', [
   {'kv': [['Wyprawa', 'Adam Rogala (kierownik), Weronika Kos (menedżerka z ramienia sponsora, Polar-Tex S.A.), Igor Szadkowski (operator kamery), Natalia Brandt (lekarka)'],
           ['Obsługa', 'Zdzisław Hampel (gospodarz schroniska), Mirosław Kuźnik (operator ratraku, mieszka w pokoiku przy garażu)'],
           ['Inni', 'nikt — schronisko jest zamknięte na czas remontu i otwarte wyłącznie dla wyprawy'],
           ['Pokoje', 'piętro: nr 2 — Adam Rogala, nr 4 — Natalia Brandt, nr 5 — Igor Szadkowski, nr 6 — Weronika Kos; parter: jadalnia, biuro z radiostacją bazy, suszarnia z tylnymi drzwiami']]},
   {'note': 'Pies gospodarza, owczarek Bari, nocuje w korytarzu na parterze.'}],
   start=True),

 # ---------- SCHRONISKO: BIURO ----------
 ev('e07', 'Wydruk', 'Dziennik łączności bazy', 'Z rejestratora radiostacji w biurze schroniska.', [
   {'log': ['pt 15.01   16:00:00   rejestrator uruchomiony (wcześniej łączności nie nagrywano)',
            'pt 15.01   16:21:40   ID 02 → baza   „Jestem w schronie, zaczynam test. Mróz trzyma.”',
            'pt 15.01   22:05:14   ID 01 → baza   „Baza, tu Mglista. Dwudziesta druga, minus szesnaście, wieje coraz mocniej, w piecu napalone. Następna łączność o szóstej. Bez odbioru.”',
            f'sob 16.01  00:40:08   ID 04 → baza   „{CALL}”',
            'sob 16.01  06:00:30   baza → ID 01   wywołanie — brak odpowiedzi',
            'sob 16.01  06:10:05   baza → ID 01   wywołanie — brak odpowiedzi',
            'sob 16.01  06:20:12   baza → ID 01   wywołanie — brak odpowiedzi']},
   {'note': 'ID to numer radiotelefonu albo stacji. Radiostacja odczytuje go automatycznie przy każdym nadaniu. Rejestrator zapisuje dźwięk każdej łączności.'}],
   time=[T(16, 21, 'Krystian Lis zgłasza się ze schronu, zaczyna test', 'Dziennik łączności'), T(22, 5, 'Łączność ze stacji w schronie (ID 01) — głos Krystiana', 'Dziennik łączności'),
         T(0, 40, 'Łączność z radiotelefonu ID 04 — głos Krystiana', 'Dziennik łączności', N), T(6, 0, 'Baza wywołuje schron — bez odpowiedzi', 'Dziennik łączności', N)]),
 ev('e08', 'Nagranie', 'Nagranie łączności z 0:40', 'Plik z rejestratora radiostacji bazy.', [
   'Rejestrator zapisał dźwięk tak, jak wyszedł z radiostacji: z szumem, trzaskami i tłem.',
   {'quote': CALL, 'by': 'transkrypcja'},
   {'note': 'Odsłuchajcie i zaznaczcie dźwięki w tle. Pomagają słuchawki albo głośniejszy głośnik.'}]),
 ev('e09', 'Wykaz', 'Radiotelefony wyprawy', 'Lista naklejona na ładowarce w biurze.', [
   {'kv': [['01', 'stacja stała — schron na Przełęczy Mglistej'], ['02', 'radiotelefon — Krystian Lis'], ['03', 'radiotelefon — Adam Rogala'],
           ['04', 'radiotelefon zapasowy — zostaje w ładowarce w bazie, w biurze schroniska'], ['05', 'radiostacja bazy z rejestratorem — biuro schroniska']]},
   'W ładowarce stoją dwa radiotelefony: 03 i 04. Oba naładowane do pełna.',
   {'note': 'Ładowarka stoi trzy kroki od drzwi na korytarz, który prowadzi do suszarni i tylnych drzwi schroniska.'}]),

 # ---------- SCHRONISKO: SUSZARNIA, TARAS, JADALNIA, POKÓJ ----------
 ev('e10', 'Oględziny', 'Narty i foki w suszarni', 'Stojak przy piecu.', [
   {'kv': [['Adam Rogala', 'narty 68 mm pod butem, foki suche'], ['Natalia Brandt', 'narty 92 mm, foki suche'], ['Igor Szadkowski', 'splitboard, foki suche'],
           ['Weronika Kos', 'narty 85 mm; foki mokre i sztywne od lodu, na krawędziach i wiązaniach zamarznięte grudy śniegu'], ['Krystian Lis', 'miejsce puste — jego narty zostały w schronie']]},
   {'note': 'Gospodarz: w suszarni przez noc jest ponad trzydzieści stopni. Foki, które w piątek po południu zjechały z przełęczy, do rana wyschły na wiór.'}]),
 ev('e11', 'Oględziny', 'Plecaki pod ścianą suszarni', 'Cztery duże plecaki wyprawowe i jeden mały.', [
   'Mały plecak skiturowy ma wzdłuż szelek żółtą taśmę odblaskową, przyszytą grubymi ściegami. Na klapie wyszyte inicjały: W.K.',
   'W bocznej kieszeni czołówka z mokrą opaską i para mokrych rękawiczek.']),
 ev('e12', 'Przedmiot', 'Popiół z pieca w suszarni', 'Z popielnika żeliwnego pieca.', [
   'Wśród popiołu z drewna stopiona bryłka pomarańczowego plastiku z wtopionym aluminiowym karabińczykiem i kawałek zielonej płytki elektronicznej. Na płytce da się odczytać nadruk: „SAT-COM 2”.',
   {'note': 'Pomarańczowy komunikator satelitarny z karabińczykiem nosił przy pasie Krystian Lis — widać go na zdjęciu zespołu w jadalni.'}]),
 ev('e13', 'Kadry', 'Klatki z aparatu na tarasie', 'Karta pamięci z aparatu Igora Szadkowskiego.', [
   'Zdjęcia co 30 sekund, od 22:02 do 0:31, razem 299 klatek. Na żadnej nie widać nikogo przy statywie, a na kolejnych klatkach rośnie czapa śniegu na aparacie.',
   'Klatka z 23:41: pod tarasem, w świetle lampy nad drzwiami suszarni, ktoś z nartami na ramieniu idzie w stronę tylnych drzwi. Twarzy nie widać. Na plecach mały plecak, na szelkach pas żółtej taśmy odblaskowej.'],
   time=[T(23, 41, 'Ktoś z nartami na ramieniu idzie od szlaku do tylnych drzwi suszarni', 'Klatki z tarasu')]),
 ev('e14', 'Wydruk', 'Laptop wyprawy — historia pliku', 'Folder „Materiały / 14.01 schron”, dziennik zdarzeń systemu.', [
   {'log': ['czw 14.01   23:58   C0112.MP4 — nagranie z kamery Igora, 1 min 04 s',
            'pt 15.01    10:12   C0112.MP4 skopiowany z karty kamery na laptop',
            'pt 15.01    21:32   C0112.MP4 skopiowany na urządzenie „iPhone — Weronika”',
            'pt 15.01    21:33   urządzenie „iPhone — Weronika” odłączone']},
   {'note': 'Klip C0112: Krystian przy radiostacji w schronie, w czwartek tuż przed północą, nadaje łączność do bazy. Na końcu słychać głos Igora: „mam”.'}],
   time=[T(21, 32, 'Klip C0112 z łącznością Krystiana trafia z laptopa na telefon Weroniki Kos', 'Laptop wyprawy')]),
 ev('e15', 'Fotografia', 'Zdjęcia na ścianie jadalni', 'Zdjęcia z wypraw i obozów.', [
   'Największe, w ramie: Adam Rogala z pulką na tle lodowca, podpis „Spitsbergen solo 2025 — z Sørkapp na północ, 640 km w 34 dni. Sam”.',
   'Obok zdjęcie zespołu przed schronem na przełęczy, z wtorku: Adam, Krystian, Natalia, Igor i Weronika w kurtkach Polar-Tex. Krystian ma przy pasie pomarańczowy komunikator satelitarny z karabińczykiem.']),
 ev('e16', 'Oględziny', 'Pokój nr 6', 'Za zgodą prokuratora.', [
   'Na kaloryferze suszą się wełniane skarpety narciarskie i wkładki do butów skiturowych — wciąż wilgotne.',
   'Na stoliku blister z dwiema tabletkami przeciwbólowymi od Natalii. Obie na miejscu.',
   {'note': 'Łóżko zasłane, poduszka bez wgniecenia. Butelka wody nieotwarta.'}]),
 ev('e17', 'Wydruk', 'Telefon Weroniki Kos', 'Za zgodą prokuratora, odblokowany przez właścicielkę.', [
   {'kv': [['Plik', 'C0112.MP4 — zapisany w piątek o 21:32'], ['Ostatnie odtworzenie', 'sobota, 0:39:51 — cały klip, 1 min 04 s'],
           ['Lokalizacja telefonu', 'wyłączona od 21:50 do 23:45']]}],
   time=[T(0, 39, 'Na telefonie Weroniki Kos odtwarzany jest klip C0112', 'Telefon W. Kos', N)]),

 # ---------- ROZDROŻE ----------
 ev('e18', 'Oględziny', 'Ślady nart przy rozdrożu', 'Pobocze szlaku zielonego, w zawietrznej skał.', [
   'Częściowo zawiany podwójny ślad nart: zakosy podejścia na fokach i — obok — łuki zjazdu w linii spadku. Szerokość śladu nart około 8,5 cm.',
   'Ślad podejścia omija drogowskaz i prowadzi dalej w górę Żlebu Mglistego, w stronę przełęczy. Ślad zjazdu wraca z żlebu.',
   {'note': 'Ratownik: to ślad z nocy. Rano nikt tędy nie szedł, a od północy nawiało tyle, że ślad sprzed wieczora byłby już niewidoczny.'}]),

 # ---------- PRZEŁĘCZ: SCHRON ----------
 ev('e19', 'Oględziny', 'Żeliwny piec w schronie', 'Piec przy pryczach.', [
   'Na ostrym kancie płyty pieca, na wysokości bioder, zaschnięta krew i kilka krótkich ciemnych włosów — niedbale starte. Szmata z brunatnymi plamami leży wciśnięta w wiadro z węglem.',
   'Piec zimny, popiół zbity — nikt nie dokładał do ognia od wielu godzin.',
   {'note': 'Krew zabezpieczono do badań. Krystian Lis miał krótkie ciemne włosy.'}]),
 ev('e20', 'Dokument', 'Zeszyt testu', 'Na stole pod oknem, obok baterii.', [
   {'log': ['pt 15.01 — test 24 h, odczyty co 30 minut',
            '20:00   bat. A 92% · B 80% · w izbie +9,4 °C',
            '20:30   A 91% · B 79% · +9,6',
            '21:00   A 90% · B 77% · +9,5',
            '21:30   A 89% · B 76% · +9,4',
            '22:00   A 88% · B 74% · +9,8   łączność OK',
            '22:30   A 86% · B 71% · +9,4']},
   {'note': 'Dalej strona jest pusta. Ołówek leży w zeszycie, między kartkami.'}],
   time=[T(22, 30, 'Ostatni wpis Krystiana w zeszycie testu', 'Zeszyt testu')]),
 ev('e21', 'Wydruk', 'Rejestrator temperatury w schronie', 'Mały rejestrator przy bateriach. Odczyt co 10 minut.', [
   {'log': ['22:30   +9,4 °C', '22:40   +9,2', '22:50   +3,6   ← gwałtowny spadek', '23:00   +6,9', '23:10   +7,8', '23:20   +2,1   ← gwałtowny spadek',
            '23:30   +4,4', '00:00   +3,7', '00:40   +2,6', '02:00   −0,9', '04:00   −4,8', '06:00   −8,2']},
   {'note': 'Krystian mierzył nim temperaturę w izbie. Spadek o kilka stopni w kilka minut to otwarte drzwi przy mrozie i wietrze. Od 23:20 temperatura już tylko spada — nikt nie dokładał do pieca.'}],
   time=[T(22, 50, 'Ktoś otwiera drzwi schronu (gwałtowny spadek temperatury)', 'Rejestrator temperatury'), T(23, 20, 'Drzwi schronu znów otwarte — potem w izbie już tylko chłodnieje', 'Rejestrator temperatury')]),
 ev('e22', 'Oględziny', 'Radiostacja w schronie', 'Stacja stała ID 01, na stole pod oknem.', [
   'Radiostacja włączona, kanał 3, mikrofon na haczyku. Na wyświetlaczu: „OST. NADAWANIE 22:05:14”.',
   {'note': 'Po 22:05 ze stacji w schronie nikt nie nadawał.'}]),
 ev('e23', 'Oględziny', 'Czapka i rękawice na stole', 'Obok zeszytu testu.', [
   'Na stole leżą czapka i grube rękawice Krystiana. Jego czołówka wisi na gwoździu przy drzwiach.',
   {'note': 'Ratownik: przy minus czternastu i takim wietrze nikt nie wychodzi do masztu bez rękawic, czapki i czołówki. Nikt.'}]),
 ev('e24', 'Oględziny', 'Ładowarka bez komunikatora', 'Przy pryczy Krystiana.', [
   'Powerbank z kablem do komunikatora satelitarnego SAT-COM 2. Samego komunikatora nie ma — ani w schronie, ani przy ciele, ani w plecaku.']),
 ev('e25', 'Dokument', 'Teczka z plecaka Krystiana', 'Plastikowa teczka z wydrukami.', [
   {'h': 'Ślad GPS „Spitsbergen solo 2025” — nadajnik Adama Rogali (dane z bazy w Longyearbyen)'},
   {'log': ['03.03.2025   18:40   pkt 45   biwak — odcinek dzienny 19 km',
            '04.03.2025   18:55   pkt 46   biwak — odcinek dzienny 18 km',
            '05.03.2025   09:10   pkt 47   wyjście z biwaku',
            '05.03.2025   15:10   pkt 48   210 km od punktu 47',
            '06.03.2025   18:30   pkt 49   biwak — odcinek dzienny 17 km']},
   {'h': 'Wydruk maila z 14 kwietnia 2025 r.'},
   {'quote': 'Krystian, rozumiem Twoje wątpliwości, ale zarząd nie może się o tym dowiedzieć w środku kampanii. Ekspertyza dziennika z pracowni we Wrocławiu rozwieje plotki. Proszę, zostaw to mnie. W.', 'by': 'nadawca: Weronika Kos, Polar-Tex S.A.'},
   {'note': 'Na odwrocie, pismem Krystiana: „Pon. 18.01 — konferencja. Powiem wszystko. Adam miał czas do poniedziałku. W. też.”'}]),

 # ---------- PRZEŁĘCZ: SKAŁA ----------
 ev('e26', 'Oględziny', 'Ciało pod skałą', 'U stóp skały z masztem, pod folią NRC.', [
   'Krystian Lis leży na plecach u stóp skały, głową w stronę schronu. Kurtka rozpięta, bez czapki i rękawic, na butach nie ma raków. Z tyłu głowy rana tłuczona.',
   'Ciało przykrywa warstwa nawianego śniegu grubości 12–14 cm. Pod ciałem jest stary, zmrożony śnieg bez śladu świeżego nawiania.',
   {'note': 'W kieszeni kurtki radiotelefon ID 02 — wyłączony. Na piętach butów i na plecach kurtki otarcia i zbity śnieg, jakby ciało ciągnięto po ziemi.'}]),
 ev('e27', 'Oględziny', 'Drabinka i maszt', 'Czterometrowa skała z przykręconą drabinką.', [
   'Na stalowych szczeblach drabinki gruba warstwa szadzi, nigdzie nienaruszona. Pierwszy szczebel jest na wysokości półtora metra — żeby na nim stanąć, trzeba by strącić szadź.',
   {'note': 'Ratownik: nikt nie wchodził tej nocy na skałę. Szadź przyrasta przy takim wietrze, ale ślad dłoni czy buta byłby widoczny.'}]),

 # ---------- GARAŻ ----------
 ev('e28', 'Wydruk', 'GPS ratraku', 'Wydruk z kabiny ratraku, dla zarządu parku narodowego.', [
   {'log': ['pt 15.01    22:00–22:40   droga dojazdowa poniżej schroniska — równanie',
            'pt 15.01    22:40–00:20   postój — garaż ratraków',
            'sob 16.01   00:20–01:10   plac przed schroniskiem — równanie, 23 manewry cofania',
            'sob 16.01   01:10         postój — garaż ratraków']},
   {'note': 'Przy każdym cofaniu ratrak włącza sygnał dźwiękowy — tego wymagają przepisy.'}],
   time=[T(22, 0, 'Ratrak równa drogę dojazdową poniżej schroniska (do 22:40)', 'GPS ratraku'), T(0, 20, 'Ratrak równa plac przed schroniskiem, często cofając (do 1:10)', 'GPS ratraku', N)]),

 # ---------- WYNIKI ZAGADEK ----------
 ev('e29', 'Wyliczenie', 'Szósty dzień — wyliczenie', 'Wasze wyliczenie z wydruku śladu GPS z 2025 roku.', [
   '210 km między 9:10 a 15:10 to sześć godzin, czyli 35 km/h. W dni przed i po Adam pokonywał po 17–19 km dziennie.',
   {'note': 'Z prędkością 35 km/h nie idzie nikt na nartach z pulką. Tak jedzie skuter śnieżny. Część „samotnego” przejścia Spitsbergenu odbyła się skuterem.'}]),
 ev('e30', 'Zestawienie', 'Kto gdzie był o 22:50', 'Wasze zestawienie alibi.', [
   {'kv': [['Adam Rogala', 'jadalnia — pisze, widzi go gospodarz'], ['Zdzisław Hampel', 'bar przy jadalni'], ['Igor Szadkowski i Natalia Brandt', 'pokój nr 4'],
           ['Mirosław Kuźnik', 'garaż ratraków — przerwa po równaniu drogi'], ['Weronika Kos', 'od 21:45 do 0:15 nikt jej nie widział']]},
   {'note': 'O 22:50 ktoś otworzył drzwi schronu na przełęczy. Spośród osób ze schroniska mogła to być tylko Weronika Kos.'}]),

 # ---------- ANALIZA NAGRANIA ----------
 ev('e31', 'Analiza nagrania', 'Nagranie z 0:40: wiatr', 'Rozpoznany dźwięk w tle.', [
   'W tle mocne porywy wiatru, dwa razy wyraźnie narastające. Tymczasem głos mówi, że „wiatr ucichł”.']),
 ev('e32', 'Analiza nagrania', 'Nagranie z 0:40: ogień w piecu', 'Rozpoznany dźwięk w tle.', [
   'Pod głosem, od pierwszych sekund, ciche trzaski ognia — jakby mówiący siedział przy rozpalonym piecu.']),
 ev('e33', 'Analiza nagrania', 'Nagranie z 0:40: pies', 'Rozpoznany dźwięk w tle.', [
   'Dwa krótkie szczeknięcia psa, blisko mikrofonu.']),
 ev('e34', 'Analiza nagrania', 'Nagranie z 0:40: drugi głos', 'Rozpoznany dźwięk w tle.', [
   'Po słowach „bez odbioru” cichy męski głos mówi: „mam”. To nie jest głos Krystiana.']),
 ev('e35', 'Analiza nagrania', 'Nagranie z 0:40: pikanie', 'Rozpoznany dźwięk w tle.', [
   'Rytmiczne, wysokie pikanie — osiem sygnałów w równych odstępach, jak przy cofaniu ciężkiej maszyny.']),

 # ---------- ZDARZENIE O 15:00 ----------
 ev('e36', 'Opinia', 'Sekcja zwłok — wstępne wyniki', 'Zakład Medycyny Sądowej we Wrocławiu, telefonicznie, sobota 15:00.', [
   'Rana tyłu głowy powstała od jednego uderzenia o twardą, prostą krawędź; w ranie drobiny rdzy i sadzy. Uraz pozbawił Krystiana przytomności, ale nie był śmiertelny.',
   'Na błonie śluzowej żołądka liczne plamy Wiszniewskiego — znak, że Krystian żył jeszcze przez pewien czas w mrozie. Otarcia pięt i pleców powstały przy życiu: ciało ciągnięto.',
   {'kv': [['Przyczyna śmierci', 'wychłodzenie organizmu'], ['Czas zgonu', 'najpewniej między 23:30 a 1:30; utrata przytomności wcześniej'],
           ['Wniosek', 'nieprzytomnego pozostawiono na mrozie; upadek ze skały wykluczony']]}]),

 # ---------- TAJNE AKTA / CENTRALA ----------
 ev('x1', 'Komunikat', 'Dane meteo z przełęczy', 'Automatyczna stacja IMGW Przełęcz Mglista.', [
   {'log': ['czw 14.01   23:00   −21,8 °C   wiatr  4 km/h',
            'czw 14.01   23:50   −22,1 °C   wiatr  3 km/h',
            'pt 15.01    01:00   −22,4 °C   wiatr  5 km/h',
            'pt 15.01    22:00   −16,0 °C   wiatr 35 km/h',
            'pt 15.01    23:00   −15,2 °C   wiatr 42 km/h',
            'sob 16.01   00:00   −14,6 °C   wiatr 55 km/h, porywy 80',
            'sob 16.01   00:40   −14,3 °C   wiatr 61 km/h, porywy 85',
            'sob 16.01   06:00   −13,1 °C   wiatr 58 km/h']},
   {'note': 'W schronisku „Hala Szronów”, 275 m niżej, wiatr w nocy był o połowę słabszy, ale w porywach dochodził do 50 km/h.'}],
   private=True),
 ev('x2', 'Wydruk', 'Wiadomości z komunikatora Krystiana', 'Odpowiedź operatora SAT-COM na zapytanie prokuratora.', [
   {'kv': [['Urządzenie', 'SAT-COM 2, abonent: Krystian Lis'], ['Piątek 15.01, 19:12', 'SMS do: Weronika Kos'], ['Inne wiadomości w piątek', 'brak']]},
   {'quote': 'Mam pełne logi z 2025 i Twoje maile. W poniedziałek na konferencji mówię wszystko — o Adamie i o Tobie. Nie dzwoń. Jutro rano zjadę, możemy pogadać.', 'by': 'treść SMS-a z komunikatora'}],
   private=True, time=[T(19, 12, 'Krystian wysyła z komunikatora SMS do Weroniki Kos', 'Operator SAT-COM')]),
 ev('x3', 'Wydruk', 'Punkty śledzenia komunikatora', 'Operator SAT-COM — pozycje zapisywane co 10 minut.', [
   {'log': ['pt 15.01   16:20   Przełęcz Mglista — schron',
            '            (co 10 minut ta sama pozycja, do 23:10)',
            'pt 15.01   23:20   Przełęcz Mglista — schron',
            'pt 15.01   23:30   szlak zielony, Rozdroże pod Jaworem',
            'pt 15.01   23:40   schronisko „Hala Szronów”',
            'pt 15.01   23:42   urządzenie wyłączone — brak dalszych pozycji']},
   {'note': 'Z przełęczy do schroniska szlakiem zielonym jest 3,4 km i 275 m w dół.'}],
   private=True, time=[T(23, 30, 'Komunikator Krystiana jest przy Rozdrożu pod Jaworem — w drodze w dół', 'Operator SAT-COM'), T(23, 40, 'Komunikator Krystiana jest w schronisku „Hala Szronów”', 'Operator SAT-COM')]),
 ev('x4', 'Dokument', 'Dokumenty Polar-Tex', 'Udostępnione przez zarząd spółki na żądanie prokuratora.', [
   {'kv': [['Umowa „Spitsbergen solo 2025”', 'premia 600 000 zł za samotne przejście, potwierdzone śladem GPS i dziennikiem; wypłacona 30.05.2025 na rachunek Rogala Expeditions sp. z o.o.'],
           ['Ekspertyza „Dziennika Lodu”', 'Pracownia Konserwacji i Ekspertyz Papieru VESPER, Wrocław, 12.05.2025: zapisy jednorodne, bez śladów późniejszych zmian; zamawiająca: Weronika Kos'],
           ['Raport dla zarządu, czerwiec 2025', '„Przejście zweryfikowane, wątpliwości wyjaśnione” — podpisała Weronika Kos'],
           ['Umowa „Północ 2028”', '2 400 000 zł; podpisana 3.11.2026 przez członka zarządu Weronikę Kos']]},
   {'note': 'Członek zarządu, który świadomie poświadcza nieprawdę wobec spółki, odpowiada karnie i majątkowo.'}],
   private=True),
 ev('x5', 'Notatka', 'Nawiewanie śniegu w nocy', 'Notatka ratownika GOPR z pola pomiarowego przy schronie.', [
   'Wiatr na przełęczy wzmógł się po 23:00, a od około 23:30 przenosił śnieg z grani. Na polu pomiarowym przy schronie do 6:00 przybyło 14 cm nawianego śniegu, z czego do 0:40 — około 5 cm.',
   {'note': 'Gdyby ktoś upadł w tym miejscu po 0:40, pod jego ciałem leżałaby warstwa świeżego śniegu.'}],
   private=True),

 # ---------- WYDRUKI Z BAZ ----------
 ev('d01', 'Wydruk z bazy', 'KRS: Polar-Tex', 'Sponsor wyprawy.', [], db='F-007-polartex'),
 ev('d02', 'Wydruk z bazy', 'PESEL: Kos Weronika', 'Menedżerka wyprawy z ramienia sponsora.', [], db='O-007-weronika'),
 ev('d03', 'Wydruk z bazy', 'KRS: Rogala Expeditions', 'Odbiorca premii za 2025 rok.', [], db='F-007-rogala'),

 # ---------- ZEZNANIA PO KONFRONTACJI ----------
 ev('t1', 'Zeznanie', 'Adam Rogala: kłótnia w czwartek', 'Po konfrontacji.', [
   'W czwartek pokłóciliśmy się w schronie. Krystian powiedział, że mam czas do poniedziałku, żeby sam wyznać prawdę o 2025 roku. W piątek wieczorem nie wychodziłem ze schroniska.'],
   testimony=True, time=[T(21, 0, 'Kłótnia Adama Rogali z Krystianem Lisem w schronie', 'Zeznanie A. Rogali', '2027-01-14')]),
 ev('t2', 'Zeznanie', 'Adam Rogala: Spitsbergen', 'Po konfrontacji.', [
   'Szóstego dnia miałem odmrożone palce i pękniętą płozę. Norweg zawiózł mnie skuterem 210 km na północ. Dziennik przepisałem potem w kraju. Weronika wiedziała od początku — to ona załatwiła ekspertyzę i premię. Krystian chciał to ujawnić w poniedziałek.'],
   testimony=True),
 ev('t3', 'Zeznanie', 'Weronika Kos: nocne narty', 'Po konfrontacji.', [
   'Wyszłam z pokoju koło dziesiątej. Założyłam narty i doszłam do rozdroża, żeby przewietrzyć głowę. Wróciłam przed północą. Nie chciałam, żeby Adam wiedział, że łamię zakaz nocnych wyjść.'],
   testimony=True),
 ev('t4', 'Zeznanie', 'Weronika Kos: przełęcz', 'Po konfrontacji.', [
   'Byłam na przełęczy. Chciałam porozmawiać z Krystianem o tej wiadomości. Odepchnęłam go, uderzył głową o róg pieca i przestał się ruszać. Wyciągnęłam go pod skałę, żeby wyglądało, że spadł z masztu. Zabrałam jego komunikator i spaliłam go w suszarni.'],
   testimony=True, time=[T(22, 50, 'Weronika Kos w schronie z Krystianem (według jej przyznania)', 'Zeznanie W. Kos')]),
 ev('t5', 'Zeznanie', 'Weronika Kos: wiadomość', 'Po konfrontacji.', [
   'Przy kolacji dostałam SMS-a z komunikatora Krystiana. Pisał, że ma logi z 2025 roku i moje maile i że w poniedziałek powie wszystko.'],
   testimony=True),
 ev('t6', 'Zeznanie', 'Weronika Kos: 2025 rok', 'Po konfrontacji.', [
   'O skuterze wiedziałam od kwietnia 2025. Zamówiłam ekspertyzę dziennika, wypłaciłam premię i podpisałam raport dla zarządu, że wszystko sprawdzone. Gdyby to wyszło, straciłabym wszystko.'],
   testimony=True),
 ev('t7', 'Zeznanie', 'Weronika Kos: łączność o 0:40', 'Po konfrontacji.', [
   'W czasie gry w karty wyszłam na kilka minut. Wzięłam z biura zapasowy radiotelefon, stanęłam za tylnymi drzwiami i puściłam do niego z telefonu nagranie Igora — Krystian przy radiu, z czwartku. Chciałam, żeby wszyscy myśleli, że po północy jeszcze żył.'],
   testimony=True, time=[T(0, 40, 'Weronika Kos nadaje z radiotelefonu 04 nagranie głosu Krystiana (według jej przyznania)', 'Zeznanie W. Kos', N)]),
 ev('t8', 'Zeznanie', 'Igor Szadkowski: noc', 'Po konfrontacji.', [
   'Ustawiłem aparat na tarasie i poszedłem do Natalii. Byłem u niej od dziesiątej do wpół do pierwszej. Kłamałem, bo Natalia ma narzeczonego, a Adam nie znosi romansów w zespole.'],
   testimony=True),
 ev('t9', 'Zeznanie', 'Natalia Brandt: noc', 'Po konfrontacji.', [
   'Igor był u mnie w pokoju od dziesiątej do wpół do pierwszej. Żadne z nas nie wychodziło.'],
   testimony=True),
]
