# Sprawa 005 „Pokój bez okien” — dowody (część skryptu build_005.py)
D = '2026-03-12'; F = '2026-03-13'

def ev(id, type, title, summary, body, **kw):
    d = {'id': id, 'type': type, 'title': title, 'summary': summary, 'body': body}
    d.update({k: v for k, v in kw.items() if v is not None})
    return d

def T(h, m, text, src, day=D):
    return [f'{day} {h:02d}:{m:02d}', text, src]

evidence = [
 # ---------- AKTA POCZĄTKOWE ----------
 ev('e01', 'Raport', 'Zgłoszenie zaginięcia', 'Piątek, 10:20. Pierwsze ustalenia patrolu w hotelu „Gryf”.', [
   {'kv': [['Miejsce', 'Hotel „Gryf”, ul. Panieńska 22, Szczecin — pokój 214 (II piętro)'],
           ['Zgłaszająca', 'mec. Ewa Dąbrowska, radca prawny Urzędu Miasta, piątek 10:05'],
           ['Zaginiony', 'dr Edward Szulc, 63 l., kierownik Oddziału Zbiorów Notarialnych Archiwum Państwowego w Koszalinie'],
           ['Ostatni ślad', 'zameldowanie w recepcji, czwartek 12.03, 23:05']]},
   'Dr Szulc przyjechał do Szczecina jako biegły na zamknięte posiedzenie Komisji Ugodowej ds. Roszczeń Reprywatyzacyjnych, wyznaczone na piątek 9:00 w sali „Bursztynowej” hotelu. Na posiedzenie nie przyszedł. Pokój 214 był zamknięty od środka na zasuwę, a po jej przecięciu okazał się pusty.',
   'Rozpytanie gości II piętra: Marek Banaś (pokój 216, po drugiej stronie korytarza, ukosem od 214) około 23:20 słyszał z głębi budynku metaliczne trzaśnięcie, „jak drzwi przeciwpożarowe”. Pozostali goście niczego nie zauważyli.',
   {'note': 'Pokój 214 nie ma okien. Jedyne wejście z korytarza to drzwi z zamkiem na kartę.'}],
   start=True, time=[T(10, 5, 'Mec. Dąbrowska zgłasza zaginięcie dr. Szulca', 'Zgłoszenie', F), T(23, 20, 'Gość z 216 słyszy w głębi budynku metaliczne trzaśnięcie', 'Zgłoszenie')]),
 ev('e02', 'Zlecenie', 'Polecenie prokuratora', 'Szukać człowieka, nie tylko sprawcy.', [
   {'quote': 'Sześćdziesięciotrzyletni biegły znika z zamkniętego pokoju w noc przed posiedzeniem, na którym ważą się miliony. Nie interesuje mnie, czy uciekł, czy go porwano — chcę wiedzieć, gdzie jest. Macie dostęp do baz danych i do hotelu. Raport do wieczora.', 'by': 'prok. Anna Wilk, Prokuratura Rejonowa Szczecin-Śródmieście'},
   {'kv': [['Zakres', 'miejsce pobytu dr. Szulca; sprawcy i pomocnicy; sposób opuszczenia pokoju 214; usunięcie biegłego z listy uczestników'], ['Dostęp', 'rejestry PESEL, CEPiK, KRS, EKW']]}],
   start=True),
 ev('e03', 'Notatka', 'Rozmowa z żoną zaginionego', 'Marta Szulc, telefon do hotelu o 9:58.', [
   'Hotel zadzwonił do Marty Szulc jako osoby kontaktowej. Żona mówi, że mąż choruje na cukrzycę i bierze insulinę rano i wieczorem. Ostatnią dawkę przyjął w czwartek około 19:00, w pociągu. Bez insuliny jego stan pogorszy się w ciągu doby.',
   'Marta Szulc wyjechała z Koszalina samochodem. Będzie w hotelu około 12:40 i jest gotowa odpowiadać na pytania.'],
   start=True, time=[T(19, 0, 'Szulc przyjmuje ostatnią dawkę insuliny w pociągu', 'Notatka z rozmowy z żoną')]),
 ev('e04', 'Dokument', 'Lista uczestników — wersja ze środy', 'Rozesłana uczestnikom 11.03 o 16:05.', [
   'Komisja Ugodowa ds. Roszczeń Reprywatyzacyjnych przy Prezydencie Miasta Szczecin. Posiedzenie zamknięte, 13.03.2026, godz. 9:00, Hotel „Gryf”, sala „Bursztynowa”. Sprawa: wniosek Heleny Rudnickiej-Lange o zwrot nieruchomości przy ul. Wielkopolskiej 21.',
   {'kv': [['Przewodniczący', 'Tadeusz Rogalski, sędzia w stanie spoczynku'], ['Sekretarz komisji', 'Iwona Kraska'], ['Za Gminę Miasto Szczecin', 'mec. Ewa Dąbrowska, radca prawny'],
           ['Pełnomocnik wnioskodawczyni', 'mec. Adrian Kosowski, adwokat'], ['Biegły', 'dr Edward Szulc, Archiwum Państwowe w Koszalinie'], ['Członkowie komisji', 'trzy osoby z Urzędu Miasta']]},
   {'note': 'Rozesłała: Iwona Kraska, sekretariat komisji.'}],
   start=True),
 ev('e05', 'Dokument', 'Lista uczestników — wydruk z piątku', 'Wyłożona w sali „Bursztynowej” przed posiedzeniem.', [
   'Ta sama lista co w środę, z jedną różnicą: nie ma na niej biegłego dr. Edwarda Szulca. W jego miejscu wpisano: „Biegły: dr Lech Morawiec (zastępstwo, § 9 ust. 3 regulaminu)”.',
   {'log': ['Lista_uczestnikow_v3.docx', 'ostatni zapis:  12.03.2026 23:58', 'autor zapisu: ikraska', 'wydruk:  13.03.2026 07:31, drukarka centrum biznesowego']},
   {'note': 'Stopka wydruku pochodzi z drukarki hotelu. Poprzednia wersja pliku (v2) była zapisana 11.03 o 15:40.'}],
   start=True, time=[T(23, 58, 'Ostatni zapis listy uczestników bez Szulca (plik v3, autor: ikraska)', 'Stopka wydruku listy'), T(7, 31, 'Wydruk listy bez Szulca w centrum biznesowym', 'Stopka wydruku listy', F)]),
 ev('e06', 'Korespondencja', 'E-mail „rezygnuję”', 'Wiadomość ze skrzynki dr. Szulca, czwartek 23:50.', [
   {'kv': [['Od', 'e.szulc@archiwum-kz.pl'], ['Do', 'sekretariat komisji (I. Kraska)'], ['Wysłano', '12.03.2026, 23:50'], ['Temat', 'rezygnacja']]},
   {'quote': 'Rezygnuję z udziału w posiedzeniu. Proszę mnie nie szukać. E.S.', 'by': 'treść wiadomości'},
   'Iwona Kraska przekazała wiadomość członkom komisji w piątek o 8:50, na sali.'],
   start=True, time=[T(23, 50, 'Ze skrzynki Szulca wychodzi mail z rezygnacją', 'E-mail')]),
 ev('e07', 'Protokół', 'Protokół otwarcia pokoju 214', 'Piątek, 9:47, w obecności dyrektora hotelu.', [
   {'kv': [['Obecni', 'Krzysztof Sowa (dyrektor hotelu), Zbigniew Wrona (kierownik techniczny), mec. Ewa Dąbrowska'],
           ['9:41', 'karta MASTER-02 — zamek odmawia otwarcia (zasunięta zasuwa wewnętrzna)'],
           ['9:47', 'Wrona przecina zasuwę od strony korytarza i otwiera drzwi']]},
   'Pokój pusty. Łóżko zasłane, walizka na stojaku. W pokoju nie ma okien, jest tylko kratka wentylacji mechanicznej 20 × 20 cm pod sufitem, przykręcona czterema śrubami, nienaruszona. Nikt nie ukrywał się w łazience ani w szafie.'],
   start=True, time=[T(9, 47, 'Technik przecina zasuwę 214 — pokój pusty', 'Protokół otwarcia', F)]),

 # ---------- POKÓJ 214 ----------
 ev('e09', 'Oględziny', 'Walizka w pokoju 214', 'Szara walizka na kółkach na stojaku.', [
   'W walizce: dwie koszule, sweter, bielizna, kosmetyczka. W kosmetyczce glukometr i dwa zapasowe wstrzykiwacze z insuliną, oba pełne. Na wierzchu teczka z kopiami regulaminu komisji.',
   'Brak: telefonu, portfela, dowodu osobistego, płaszcza i kapelusza. Brak także skórzanej teczki na dokumenty.',
   {'note': 'Wstrzykiwacze leżą w kosmetyczce, której nikt nie otwierał — suwak zapięty, w środku metka z apteki.'}]),
 ev('e10', 'Oględziny', 'Łóżko i łazienka', 'Pokój wygląda, jakby nikt w nim nie spał.', [
   'Narzuta zasłana, poduszki nietknięte. Ręczniki w łazience suche i złożone. Mydełka i szampony hotelowe zamknięte. Czajnik pusty i zimny, kubki czyste.',
   'Na podłodze przy drzwiach wilgotne smugi po butach, już prawie wyschnięte. W czwartek od 21:00 w Szczecinie padał deszcz.']),
 ev('e11', 'Oględziny', 'Szafa wnękowa — tylna ściana', 'Za szafą są drugie drzwi.', [
   'Tylna ściana szafy to płyta na czterech zatrzaskach. Zdejmuje się ją ręką, bez narzędzi. Za nią są stalowe drzwi z wkładką na klucz, zamknięte. Klamki od strony pokoju brak — jest tylko pokrętło zamka.',
   'Na dnie szafy drobny pył gipsowy, a przy jednym z zatrzasków świeże zarysowanie. Wieszaki zsunięte na jedną stronę drążka.',
   {'note': 'Pokrętłem od strony pokoju drzwi da się otworzyć, ale zamknąć od zewnątrz można je tylko kluczem.'}]),
 ev('e12', 'Oględziny', 'Biurko w pokoju 214', 'Koperta z recepcji i hotelowy notes.', [
   'Na biurku koperta recepcji z drugą kartą do pokoju: „214-B”. Karta nieużywana. Notes hotelowy czysty, bez odcisków pisma na pierwszej kartce. Długopis w etui.']),

 # ---------- RECEPCJA ----------
 ev('e13', 'Dokument', 'Karta meldunkowa — pokój 214', 'Wypełniona w czwartek o 23:05.', [
   {'kv': [['Gość', 'Edward Szulc'], ['Dokument tożsamości', 'dowód osobisty CGB 741827'], ['Przyjazd', '12.03.2026, 23:05, pieszo'], ['Pojazd', '— (brak)'],
           ['Rezerwacja', 'Komisja Ugodowa (płatnik: Urząd Miasta), zamówiła I. Kraska'], ['Przyjął', 'B. Lis'], ['Podpis gościa', '„E. Szulc”']]},
   'Podpis nakreślony szybko, pochylonym pismem: duże „E”, kropka i nazwisko. Wydano dwie karty: 214-A (gość) i 214-B (w kopercie do pokoju).'],
   time=[T(23, 5, '„Edward Szulc” melduje się w recepcji, przyjął B. Lis', 'Karta meldunkowa')]),
 ev('e14', 'Dokument', 'Skan dowodu osobistego gościa', 'Skaner w recepcji, 23:05.', [
   {'kv': [['Nazwisko i imię', 'SZULC EDWARD'], ['Seria i numer', 'CGB 741827'], ['Data wydania', '10.04.2018'], ['Data ważności', '10.04.2028']]},
   'Zdjęcie na dowodzie przedstawia mężczyznę około pięćdziesięciu pięciu lat, w okularach, z krótką, siwiejącą brodą.']),
 ev('e15', 'Rejestr', 'Księga gości — noc z 12 na 13 marca', 'System recepcji, wyciąg dla policji.', [
   {'log': ['105  Laskowski Wojciech      zam. 12.03 17:10  poj. GD 2LM47', '112  Michalak Piotr, Anna     zam. 12.03 19:05  poj. PO 51RT3',
            '118  Morawiec Lech           zam. 12.03 21:20  —         rez. 12.03 19:40 (online), tel. 512 300 846',
            '121  Sobolewska Kinga        zam. 12.03 16:30  —', '203  Ratajczak Tomasz        zam. 12.03 18:55  poj. DW 6TK02',
            '207  Fijałkowski Grzegorz    zam. 12.03 20:10  poj. ZK 40112', '214  Szulc Edward            zam. 12.03 23:05  —         rez. 05.03 (I. Kraska)',
            '216  Banaś Marek             zam. 12.03 22:20  poj. KR 7PW15', '305  Kraska Iwona            zam. 12.03 18:22  poj. ZS 3K118',
            '309  Kosowski Adrian         zam. 12.03 19:40  —', '312  Kmiecik Bożena          zam. 12.03 21:05  poj. LU 204CK']},
   {'note': 'Zameldowania od 22:00 przyjmował nocny recepcjonista Bartosz Lis. Wcześniejsze — zmiana dzienna. Goście podają numer rejestracyjny, jeśli korzystają z parkingu.'}],
   time=[T(21, 20, 'Morawiec melduje się w hotelu (rezerwacja online z 19:40)', 'Księga gości'), T(22, 20, 'Lis melduje M. Banasia w pokoju 216', 'Księga gości')]),
 ev('e16', 'Rejestr', 'Dziennik centrali telefonicznej', 'Połączenia wewnętrzne do recepcji, noc 12/13.03.', [
   {'log': ['22:10  pok. 118 → room service    odebrane   0:48', '22:47  pok. 312 → recepcja        odebrane   0:21', '23:22  pok. 118 → recepcja        NIEODEBRANE (sygnał 60 s)',
            '23:41  pok. 207 → recepcja        odebrane   0:35', '06:15  pok. 203 → recepcja        odebrane   0:40']},
   {'note': 'Recepcja ma jeden aparat na ladzie. Nocą nie ma przekierowania na telefon komórkowy.'}],
   time=[T(23, 22, 'Telefon z pokoju 118 do recepcji — nikt nie odbiera', 'Dziennik centrali')]),
 ev('e17', 'Korespondencja', 'Rezerwacja pokoju dla biegłego', 'E-mail Iwony Kraski do hotelu, 5 marca.', [
   {'kv': [['Od', 'I. Kraska, sekretariat Komisji Ugodowej'], ['Do', 'rezerwacje, Hotel „Gryf”'], ['Data', '05.03.2026, 11:12']]},
   {'quote': 'Dla biegłego, dr. Edwarda Szulca, proszę o pokój 214, przyjazd 12.03 wieczorem, jedna noc. Doktor prosi o pokój cichy, bez okien od ulicy. Płatnik: Urząd Miasta.', 'by': 'treść wiadomości'},
   {'note': 'Recepcja: pokój 214 jest jedynym pokojem w hotelu bez okien. Zwykle sprzedajemy go jako ostatni.'}]),
 ev('e27', 'Rejestr', 'Zdarzenia zamków na kartę', 'Eksport systemu zamków, wybrane drzwi.', [
   {'log': ['12.03 18:31:10  305           karta 305-A          otwarcie', '12.03 20:04:22  centrum bizn.  karta 305-A          otwarcie',
            '12.03 21:24:05  118           karta 118-A          otwarcie', '12.03 22:44:16  centrum bizn.  karta 305-A          otwarcie',
            '12.03 23:02:55  305           karta 305-A          otwarcie', '12.03 23:05:31  recepcja      karta 214-A, 214-B   zakodowane (B. Lis)',
            '12.03 23:09:14  214           karta 214-A          otwarcie', '12.03 23:13:40  214           zasuwa wewnętrzna    ZAŁĄCZONA',
            '13.03 09:41:02  214           karta MASTER-02      ODMOWA (zasuwa)']},
   {'note': 'Zamki zapisują otwarcia kartą oraz załączenie i zwolnienie zasuwy. Wyjścia z pokoju bez użycia karty nie są zapisywane. Po 23:13:40 drzwi 214 nie zarejestrowały żadnego zdarzenia aż do rana.'}],
   time=[T(23, 9, 'Drzwi 214 otwarte kartą 214-A', 'Zamki na kartę'), T(23, 13, 'W 214 załączona zasuwa wewnętrzna — drzwi nie otwierają się do rana', 'Zamki na kartę')]),

 # ---------- PARKING ----------
 ev('e18', 'Rejestr', 'Rejestr szlabanu parkingu (ANPR)', 'Kamera odczytuje tablice przy wjeździe i wyjeździe.', [
   {'log': ['12.03 17:10  WJAZD  GD 2LM47', '12.03 18:22  WJAZD  ZS 3K118', '12.03 18:55  WJAZD  DW 6TK02', '12.03 19:05  WJAZD  PO 51RT3',
            '12.03 20:10  WJAZD  ZK 40112', '12.03 21:05  WJAZD  LU 204CK', '12.03 21:36  WYJAZD ZS 3K118', '12.03 22:20  WJAZD  KR 7PW15',
            '12.03 22:41  WJAZD  ZS 3K118', '12.03 22:58  WJAZD  ZS 7PR04', '12.03 23:31  WYJAZD ZS 7PR04', '13.03 05:40  WJAZD  ZPL 4C71',
            '13.03 05:52  WYJAZD ZPL 4C71', '13.03 05:55  WJAZD  ZS 86HE4', '13.03 06:50  WYJAZD DW 6TK02', '13.03 07:45  WJAZD  ZS 12KA7', '13.03 08:10  WYJAZD GD 2LM47']},
   {'note': 'Parking jest za hotelem. Szlaban otwiera się automatycznie każdemu pojazdowi. Kamera zapisuje tylko numer i godzinę.'}],
   time=[T(21, 36, 'Samochód ZS 3K118 wyjeżdża z parkingu', 'ANPR'), T(22, 41, 'ZS 3K118 wraca na parking', 'ANPR'), T(22, 58, 'Wjeżdża ZS 7PR04', 'ANPR'), T(23, 31, 'Wyjeżdża ZS 7PR04', 'ANPR')]),
 ev('e41', 'Oględziny', 'Dojazd za hotelem', 'Wąska alejka między parkingiem a wyjściem służbowym.', [
   'Alejka prowadzi od parkingu wzdłuż tylnej ściany hotelu do wyjścia służbowego B — około trzydziestu metrów. Nad wyjściem jest lampa, ale kamera nad drzwiami nie działa od lutego (zgłoszenie serwisowe z 9.02, czeka na część).',
   'Z okna palarni personelu widać alejkę i kilka ostatnich miejsc parkingowych.']),
 ev('e40', 'Oględziny', 'Samochód Iwony Kraski', 'Toyota Corolla, ZS 3K118, przeszukana za zgodą prokuratora.', [
   'Pod fotelem pasażera, wciśnięty między szyny: bilet kolejowy PKP Intercity, IC 38170 „Parsęta”, Koszalin 19:27 → Szczecin Główny 21:47, 12.03.2026, wagon 6, miejsce 45. Bilet imienny: Edward Szulc.',
   'Na dywaniku po stronie pasażera zaschnięte ślady błota. W bagażniku parasol i torba z wydrukami materiałów komisji.']),

 # ---------- SALA „BURSZTYNOWA” ----------
 ev('e19', 'Dokument', 'Wniosek Heleny Rudnickiej-Lange', 'Streszczenie z akt komisji.', [
   {'kv': [['Nieruchomość', 'kamienica, ul. Wielkopolska 21, Szczecin, KW SZ1S/00045218/0'], ['Wartość według operatu', '38,4 mln zł'],
           ['Podstawa roszczenia', 'akt nadania własności z 14.09.1946 dla Karola Rudnickiego, wydany przez Zarząd Miejski w Szczecinie'],
           ['Wnioskodawczyni', 'Helena Rudnicka-Lange (79 l., Hamburg), córka Karola Rudnickiego'],
           ['Cesjonariusz roszczenia', 'Restytucja Pomorska sp. z o.o. (umowa cesji z 07.02.2022)'], ['Pełnomocnik', 'mec. Adrian Kosowski']]},
   'Komisja może zawrzeć ugodę: zwrot kamienicy albo odszkodowanie. Wszystko zależy od tego, czy akt z 1946 roku jest autentyczny. Oceny miał dokonać biegły z archiwum, które przechowuje oryginał.']),
 ev('e20', 'Dokument', 'Regulamin komisji — § 9', 'Kto opiniuje dokumenty i co, gdy biegły nie przyjdzie.', [
   {'quote': '§ 9 ust. 3. W razie nieobecności biegłego sekretarz komisji może zaproponować innego biegłego z listy biegłych sądowych. Komisja rozstrzyga sprawę na podstawie opinii biegłego obecnego na posiedzeniu.', 'by': 'Regulamin Komisji Ugodowej'},
   {'note': 'Ugoda zawarta na posiedzeniu jest wykonalna po podpisie prezydenta miasta. Termin: 14 dni.'}]),
 ev('e21', 'Protokół', 'Notatka z piątkowego posiedzenia', 'Od 8:55 do przerwy o 9:40.', [
   '8:55 — sekretarz komisji Iwona Kraska informuje, że dr Szulc zrezygnował w nocy mailem, i proponuje biegłego dr. Lecha Morawca (§ 9 ust. 3). Dr Morawiec jest obecny na sali.',
   '9:05 — mec. Dąbrowska sprzeciwia się i żąda sprawdzenia pokoju dr. Szulca. Mec. Kosowski wnosi o kontynuowanie posiedzenia z nowym biegłym.',
   '9:20 — recepcja nie może się dodzwonić do pokoju 214. 9:40 — przewodniczący zarządza przerwę do wyjaśnienia sprawy.'],
   time=[T(8, 55, 'Kraska ogłasza rezygnację Szulca i proponuje Morawca', 'Notatka z posiedzenia', F)]),
 ev('e22', 'Dokument', 'Kopia aktu nadania z 1946', 'Kserokopia z akt komisji. Oryginał jest w Koszalinie.', [
   'Akt nadania własności nieruchomości przy ul. Wielkopolskiej 21 dla Karola Rudnickiego, datowany 14.09.1946, z pieczęcią Zarządu Miejskiego w Szczecinie i podpisem wiceprezydenta miasta.',
   {'note': 'Na kopii widać tylko zarys znaku wodnego w rogu karty — kilka liter, nieczytelne. Ocena papieru wymaga oryginału.'}]),

 # ---------- DZIAŁ TECHNICZNY ----------
 ev('e23', 'Plan', 'Plan II piętra z 1974 roku', 'Archiwum techniczne hotelu.', [
   'Skrzydło B, II piętro. Pokoje gościnne po stronie ulicy. Po drugiej stronie korytarza gościnnego, naprzeciw pokoi 213 i 215, wąskie pomieszczenie bez okien opisane jako „magazyn bielizny”. Magazyn ma dwoje drzwi: od korytarza gościnnego i drugie, oznaczone M2, w tylnej ścianie — do korytarza gospodarczego, który biegnie wzdłuż ściany od podwórza aż do klatki schodowej B.',
   {'note': 'Klatka B to schody personelu. Na parterze kończy się wyjściem służbowym na tył budynku.'}]),
 ev('e24', 'Dokument', 'Dokumentacja adaptacji z 2019 roku', 'Opis powykonawczy: magazyn → pokój 214.', [
   {'quote': 'Adaptacja magazynu bielizny na pokój hotelowy nr 214 (bez okien, wentylacja mechaniczna). Drzwi M2 do korytarza gospodarczego pozostawiono jako drzwi rewizyjne (dostęp do pionów wod.-kan.), zakryte tylną ścianą szafy wnękowej, demontowaną bez narzędzi. Drzwi zamykane na klucz od strony korytarza. Klucz R-2 w szafce technicznej.', 'by': 'opis powykonawczy, wrzesień 2019'},
   {'kv': [['Wykonawca', 'PB Pietras Budownictwo sp. z o.o., Police'], ['Kierownik robót', 'D. Pietras'], ['Odbiór', 'Zbigniew Wrona, kierownik techniczny hotelu']]}]),
 ev('e25', 'Dokument', 'Faktura za adaptację pokoju 214', 'Archiwum księgowe hotelu, 2019.', [
   {'kv': [['Faktura', 'VAT nr 47/2019 z 30.09.2019'], ['Sprzedawca', 'PB Pietras Budownictwo sp. z o.o., ul. Fabryczna 3, 72-010 Police'], ['NIP sprzedawcy', '8512047718'],
           ['Nabywca', 'Hotel Gryf sp. z o.o.'], ['Usługa', 'adaptacja pom. gospodarczego II p. na pokój hotelowy nr 214 wraz z zabudową szafy i drzwiami rewizyjnymi'], ['Kwota', '86 400 zł brutto']]}]),
 ev('e26', 'Rejestr', 'Wyjście służbowe B — dziennik drzwi', 'Kontroler drzwi na parterze klatki B.', [
   {'log': ['12.03 21:58:02  otwarcie kartą     K. Nowicka (kelnerka)', '12.03 23:24:51  otwarcie przyciskiem wyjścia (od wewnątrz)', '13.03 05:31:40  otwarcie kartą     P. Krupa (kucharz)', '13.03 06:12:19  otwarcie przyciskiem wyjścia (od wewnątrz)']},
   {'note': 'Od zewnątrz drzwi otwiera tylko karta personelu. Od środka wystarczy przycisk — bez alarmu, bez karty.'}],
   time=[T(23, 24, 'Ktoś wychodzi wyjściem służbowym B (przycisk od środka)', 'Dziennik drzwi B')]),
 ev('e28', 'Oględziny', 'Szafka z kluczami technicznymi', 'Pokój kierownika technicznego.', [
   'Klucz R-2 wisi na swoim haczyku. W zeszycie wydań ostatni wpis przy R-2: 14.01.2025, hydraulik, zwrot tego samego dnia.',
   'Kierownik techniczny Wrona: „Zamek w M2 to zwykła wkładka. Dorobienie klucza zajmuje ślusarzowi pięć minut. Kopie mógł mieć każdy, kto przy tym robił.”']),

 # ---------- KORYTARZ GOSPODARCZY I KLATKA B ----------
 ev('e29', 'Oględziny', 'Drzwi M2 od strony korytarza', 'Korytarz gospodarczy za pokojami 210–216.', [
   'Korytarz biegnie wzdłuż ściany od podwórza, za pokojem 214. Jest zakurzony i rzadko używany. Klamka i szyld drzwi M2 są czyste, a na posadzce przed drzwiami kurz jest starty w kształt półokręgu — drzwi niedawno otwierano. Drzwi zamknięte na klucz.',
   'Od M2 do klatki B jest dwanaście metrów.']),
 ev('e31', 'Przedmiot', 'Karta hotelowa na klatce B', 'Podest między I a II piętrem, pod kaloryferem.', [
   'Biała karta z nadrukiem „Hotel Gryf · 214”. Recepcja odczytała ją czytnikiem: karta 214-A, zakodowana w czwartek o 23:05:31, użyta raz — o 23:09:14 przy drzwiach 214.']),
 ev('e30', 'Oględziny', 'Palarnia personelu', 'Mała wiata na tyłach, przy wyjściu B.', [
   'W popielniczce kilkanaście niedopałków tej samej marki, część świeża. Na parapecie kubek z nadrukiem „BARTEK” z resztką zimnej kawy.',
   'Z palarni widać alejkę, wyjście służbowe B i koniec parkingu.']),

 # ---------- BAR ----------
 ev('e32', 'Rejestr', 'Rachunki baru „Kotwica”', 'Kasa fiskalna, czwartek wieczorem.', [
   {'log': ['21:04  stolik 4   rachunek pok. 309  piwo, woda', '21:36  stolik 2   gotówka            herbata x2', '22:31  stolik 4   rachunek pok. 309  whisky, orzeszki',
            '23:47  stolik 4   rachunek pok. 309  whisky', '00:22  stolik 4   rachunek pok. 309  zamknięcie rachunku, podpis A. Kosowski']},
   {'note': 'Bar jest na parterze, obok holu. Czynny do 0:30.'}],
   time=[T(21, 4, 'Kosowski zaczyna wieczór w barze (rachunek pok. 309)', 'Rachunki baru')]),
 ev('e33', 'Zeznanie', 'Barman o czwartkowym wieczorze', 'Rafał Czajka, barman.', [
   {'quote': 'Mecenas siedział przy czwórce od dziewiątej do zamknięcia. Wyszedł raz, do toalety, na pięć minut, koło jedenastej. Dużo rozmawiał przez telefon, głośno, o jakiejś ugodzie.', 'by': 'Rafał Czajka'},
   'Barman nie widział nikogo, kto przypominałby dr. Szulca. Z baru widać tylko część holu, bez recepcji.'], testimony=True),
 ev('e34', 'Rejestr', 'Room service — zamówienie z pokoju 118', 'Kuchnia hotelowa, czwartek.', [
   {'kv': [['Zamówienie', 'telefon z pok. 118, 22:10'], ['Doręczenie', '22:18, kelnerka K. Nowicka, do rąk gościa'], ['Pozycje', 'zupa rybna, herbata'], ['Rachunek', 'na pokój, podpis L. Morawiec']]}],
   time=[T(22, 18, 'Morawiec odbiera kolację w pokoju 118', 'Room service')]),

 # ---------- ARCHIWUM W KOSZALINIE ----------
 ev('e35', 'Notatka', 'Notatki na biurku dr. Szulca', 'Kartka przypięta do monitora, wideorozmowa z archiwum.', [
   {'quote': 'Wielkopolska 21 — akt z 1946: filigran „WIEPRZA”!!! Sprawdzić, kiedy ruszyła papiernia. Hasło do projektu opinii = miesiąc i rok uruchomienia (MM + dwie ostatnie cyfry roku). Hasło podać tylko sekretarzowi komisji, telefonicznie.', 'by': 'pismo dr. Szulca'},
   'Zastępczyni dr. Szulca, Joanna Kurek, potwierdza, że kartkę napisał on, w poniedziałek 9.03.']),
 ev('e45', 'Dokument', 'Karta katalogowa papierni', 'Kartoteka znaków wodnych archiwum.', [
   {'kv': [['Znak wodny', '„WIEPRZA” w owalu'], ['Wytwórca', 'Zakłady Papiernicze „Wieprza” w Sławnie'], ['Uruchomienie produkcji', '3 października 1951'], ['Uwagi', 'papier kancelaryjny dla urzędów województwa koszalińskiego i szczecińskiego, lata 1951–1968']]},
   {'note': 'Karta z kartoteki prowadzonej przez dr. Szulca od 2009 roku.'}]),
 ev('e36', 'Korespondencja', 'Wysłane e-maile dr. Szulca', 'Skrzynka służbowa, wyciąg.', [
   {'log': ['10.03 09:12  do: E. Dąbrowska     temat: posiedzenie 13.03   „Czuję presję. Dostałem list od pełnomocnika wnioskodawczyni. Chciałbym porozmawiać przed posiedzeniem.”',
            '11.03 14:20  do: sekretariat komisji (I. Kraska)   temat: projekt opinii   załącznik: Projekt_opinii_Wielkopolska21.pdf (zaszyfrowany)',
            '11.03 15:02  do: sekretariat komisji (I. Kraska)   temat: hasło   „Hasło podam telefonicznie, jak ustaliliśmy.”']},
   {'note': 'Archiwum ma kopię wysłanego pliku. Hasła nie zapisano w skrzynce.'}],
   time=[T(14, 20, 'Szulc wysyła Kraskiej zaszyfrowany projekt opinii', 'E-maile Szulca', '2026-03-11')]),
 ev('e38', 'Dokument', 'Zaszyfrowany projekt opinii', 'Plik PDF chroniony hasłem.', [
   'Projekt_opinii_Wielkopolska21.pdf — 14 stron. Hasło: cztery cyfry. Podgląd pokazuje tylko stronę tytułową: „Opinia w przedmiocie autentyczności aktu nadania z 14.09.1946 r.”']),
 ev('e39', 'Opinia', 'Projekt opinii dr. Szulca', 'Odszyfrowany plik z archiwum.', [
   {'quote': 'Akt nadania z 14.09.1946 r. sporządzono na papierze ze znakiem wodnym Zakładów Papierniczych „Wieprza” w Sławnie, które rozpoczęły produkcję w 1951 r. Ponadto numer aktu nie figuruje w dzienniku podawczym Zarządu Miejskiego za 1946 r. Dokument nie mógł powstać w dacie, którą nosi. Jest falsyfikatem.', 'by': 'dr Edward Szulc, projekt opinii, 11.03.2026'},
   {'note': 'Bez autentycznego aktu z 1946 roku roszczenie do kamienicy przy Wielkopolskiej 21 upada.'}]),
 ev('e37', 'Dokument', 'Wzory podpisów dr. Szulca', 'Dokumenty z archiwum z lat 2021–2026.', [
   'Siedem podpisów pod pismami służbowymi i protokołami. Na każdym pełne imię i nazwisko: „Edward Szulc”, pismo okrągłe, prawie pionowe, z charakterystycznie zawiniętym „z”. Żadnego podpisu skrótem.']),

 # ---------- OD MARTY SZULC ----------
 ev('e42', 'Zdjęcie', 'Zdjęcie dr. Szulca z lutego 2026', 'Urodziny w domu, 21 lutego.', [
   'Dr Edward Szulc przy stole, w swetrze, uśmiechnięty. Gładko ogolony, w okularach w cienkiej oprawie. Siwe, krótko obcięte włosy.']),
 ev('e43', 'Korespondencja', 'List mec. Kosowskiego do dr. Szulca', 'Zdjęcie listu z 2 marca, przesłane przez żonę.', [
   {'quote': 'Szanowny Panie Doktorze, w związku z posiedzeniem 13 marca proponuję prywatną konsultację w zakresie historii dokumentu z 1946 r. Moja klientka gotowa jest pokryć honorarium w wysokości 50 000 zł. Proszę o kontakt pod numerem 501 664 092.', 'by': 'mec. Adrian Kosowski, 02.03.2026'},
   {'note': 'Na marginesie dopisek dr. Szulca: „NIE. Zgłosić Dąbrowskiej.”'}]),
 ev('e44', 'Zdjęcie', 'SMS od męża — zrzut ekranu', 'Telefon Marty Szulc, numer 694 117 230.', [
   {'kv': [['Od', 'Edward (601 238 447)'], ['Godzina', '12.03.2026, 21:49'], ['Treść', '„Jestem. Pani Kraska już czeka przed dworcem, mam z nią jechać. Zadzwonię z hotelu.”']]},
   'Ostatnia wiadomość od męża. Telefonu z hotelu nie było.'],
   time=[T(21, 49, 'Szulc pisze do żony: „Pani Kraska już czeka przed dworcem”', 'SMS do żony')]),

 # ---------- TAJNE AKTA / CENTRALA ----------
 ev('x1', 'Dane', 'Operator: telefon dr. Szulca', 'Zdarzenia w sieci, numer 601 238 447.', [
   {'log': ['12.03 21:47:12  SZC-DWORZEC-02       rejestracja w sieci', '12.03 21:49:03  SZC-DWORZEC-02       SMS wychodzący do 694 117 230',
            '12.03 21:58:51  SZC-ŚRÓDMIEŚCIE-14   aktualizacja lokalizacji', '12.03 22:03:17  SZC-ŚRÓDMIEŚCIE-14   wylogowanie (telefon wyłączony)',
            '12.03 23:48:05  SZC-STAREMIASTO-05   rejestracja w sieci', '12.03 23:52:44  SZC-STAREMIASTO-05   wylogowanie (telefon wyłączony)']},
   {'kv': [['SZC-DWORZEC-02', 'Dworzec Główny, ul. Kolumba, Nabrzeże Wieleckie'], ['SZC-ŚRÓDMIEŚCIE-14', 'ul. Jagiellońska (nr 1–40), al. Piastów (odc. pl. Szarych Szeregów – ul. Bogusława X), ul. Bogusława X (część)'],
           ['SZC-CENTRUM-03', 'pl. Armii Krajowej (Urząd Miasta), ul. Mazowiecka, ul. Matejki'], ['SZC-STAREMIASTO-05', 'ul. Panieńska, Wały Chrobrego, Rynek Sienny (m.in. Hotel „Gryf”)']]},
   {'note': 'Od 21:00 do 22:03 numer nie wysłał ani nie odebrał żadnego SMS-a ani połączenia poza SMS-em o 21:49.'}],
   private=True, time=[T(21, 58, 'Telefon Szulca w komórce Śródmieście-14 (Jagiellońska / al. Piastów)', 'Operator — telefon Szulca'), T(22, 3, 'Telefon Szulca wyłączony w komórce Śródmieście-14', 'Operator — telefon Szulca'), T(23, 48, 'Telefon Szulca włączony przy hotelu (Stare Miasto-05) na 4 minuty', 'Operator — telefon Szulca')]),
 ev('x2', 'Dane', 'Operator: telefon Iwony Kraski', 'Zdarzenia w sieci, numer 605 482 119.', [
   {'log': ['12.03 19:32:15  SZC-STAREMIASTO-05   połączenie wychodzące do 512 300 846, 2 min 41 s', '12.03 20:15:40  SZC-STAREMIASTO-05   SMS wychodzący do 601 238 447',
            '12.03 21:44:30  SZC-DWORZEC-02       aktualizacja lokalizacji', '12.03 21:59:20  SZC-ŚRÓDMIEŚCIE-14   aktualizacja lokalizacji',
            '12.03 22:32:05  SZC-ŚRÓDMIEŚCIE-14   ostatnie zdarzenie w tej komórce', '12.03 22:39:48  SZC-STAREMIASTO-05   aktualizacja lokalizacji',
            '12.03 22:46:10  SZC-STAREMIASTO-05   połączenie wychodzące do 603 951 004, 0 min 48 s', '12.03 23:33:02  SZC-STAREMIASTO-05   SMS przychodzący od 603 951 004']},
   {'kv': [['512 300 846', 'abonent: Lech Morawiec'], ['601 238 447', 'abonent: Edward Szulc'], ['603 951 004', 'abonent: Restytucja Pomorska sp. z o.o. (numer firmowy)']]},
   {'note': 'Opis komórek jak w danych telefonu dr. Szulca: Śródmieście-14 obejmuje ul. Jagiellońską i część al. Piastów, a Urząd Miasta leży w komórce Centrum-03.'}],
   private=True, time=[T(19, 32, 'Kraska dzwoni do Morawca (2 min 41 s)', 'Operator — telefon Kraski'), T(21, 59, 'Telefon Kraski w komórce Śródmieście-14', 'Operator — telefon Kraski'), T(22, 46, 'Kraska dzwoni pod numer firmowy Restytucji Pomorskiej', 'Operator — telefon Kraski'), T(23, 33, 'Kraska dostaje SMS z numeru Restytucji Pomorskiej', 'Operator — telefon Kraski')]),
 ev('x3', 'Dane', 'Hotelowa sieć Wi-Fi — dziennik urządzeń', 'Eksport od firmy obsługującej sieć „Gryf-Guest”.', [
   {'log': ['Galaxy-A53-Edward   pierwsze połączenie z siecią: 17.10.2024', 'Galaxy-A53-Edward   12.03 23:48:20–23:52:30  punkt AP-3B   0,4 MB',
            'iPhone-Iwona        12.03 18:31–21:35  AP-1A / AP-3B', 'iPhone-Iwona        12.03 22:44–23:01  AP-1A', 'iPhone-Iwona        12.03 23:03–13.03 07:12  AP-3B',
            'Pixel-AK            12.03 21:00–13.03 00:31  AP-1A']},
   {'kv': [['AP-1A', 'parter: hol, recepcja, bar, centrum biznesowe'], ['AP-2B', 'II piętro, skrzydło B: pokoje 210–216'], ['AP-3B', 'III piętro, skrzydło B: pokoje 305–312']]},
   {'note': 'Telefon łączy się z siecią sam, jeśli kiedyś już był do niej podłączony. W nocy z 12 na 13 marca urządzenie Galaxy-A53-Edward ani razu nie połączyło się z punktem AP-2B.'}],
   private=True, time=[T(23, 48, 'Telefon Szulca łączy się z Wi-Fi na III piętrze (AP-3B)', 'Wi-Fi hotelu')]),
 ev('x4', 'Dane', 'Dyspozytornia Taxi Pomorze', 'Kursy w czwartek wieczorem, rejon dworca i Starego Miasta.', [
   {'log': ['22:02  ul. Monte Cassino → Hotel „Gryf”     klient: E. Dąbrowska (konto)   przyjazd 22:12', '22:52  Hotel „Gryf” → ul. Monte Cassino     klient: E. Dąbrowska (konto)']},
   {'note': 'Między 21:40 a 23:10 żadna taksówka korporacji nie wiozła klienta spod Dworca Głównego na ul. Panieńską. Dworzec obsługują w tych godzinach tylko dwie korporacje; druga (Radio Taxi 91) też nie miała takiego kursu.'}],
   private=True, time=[T(22, 12, 'Dąbrowska przyjeżdża taksówką pod hotel', 'Dyspozytornia taxi'), T(22, 52, 'Dąbrowska odjeżdża taksówką spod hotelu', 'Dyspozytornia taxi')]),
 ev('x5', 'Dane', 'Ochrona Urzędu Miasta — rejestr wejść', 'Budynek przy pl. Armii Krajowej 1.', [
   'Budynek jest zamknięty od 18:00 do 6:00. W czwartek 12.03 po 18:00 nie odnotowano żadnego wejścia — ani kartą, ani przez ochronę. Ostatnie wyjście sekretariatu komisji: Iwona Kraska, 16:42.',
   {'note': 'Biuro komisji i jej akta są w tym budynku, pokój 112.'}], private=True),
 ev('x6', 'Zeznanie', 'Kierownik pociągu IC 38170', 'Rozmowa telefoniczna, piątek 12:30.', [
   {'quote': 'Pamiętam tego pana, siedział w szóstce. Starszy, bez brody, w szarym płaszczu i kapeluszu. Walizka na kółkach i skórzana teczka pod pachą. Na peronie czekała na niego kobieta z parasolem, koło pięćdziesiątki, w beżowym płaszczu. Wzięła od niego teczkę i poszli do wyjścia.', 'by': 'Waldemar Gołąb, kierownik pociągu'}],
   private=True, testimony=True, time=[T(21, 47, 'Szulc wysiada w Szczecinie; na peronie czeka na niego kobieta z parasolem', 'Kierownik pociągu')]),

 # ---------- WYDRUKI Z BAZ (treść generuje aplikacja z rekordu) ----------
 ev('d01', 'Wydruk z bazy', 'CEPiK: ZS 7PR04', 'Pojazd z rejestru szlabanu.', [], db='V-005-rest'),
 ev('d02', 'Wydruk z bazy', 'KRS: Restytucja Pomorska', 'Spółka, która przejęła roszczenie.', [], db='F-005-rest'),
 ev('d03', 'Wydruk z bazy', 'PESEL: Pietras Damian', 'Prezes Restytucji Pomorskiej.', [], db='O-005-pietras'),
 ev('d04', 'Wydruk z bazy', 'EKW: SZ1S/00045218/0', 'Kamienica przy ul. Wielkopolskiej 21.', [], db='K-005-claim'),
 ev('d05', 'Wydruk z bazy', 'KRS: PB Pietras Budownictwo', 'Wykonawca adaptacji pokoju 214.', [], db='F-005-pb'),
 ev('d06', 'Wydruk z bazy', 'PESEL: Kraska Iwona', 'Sekretarz komisji.', [], db='O-005-kraska'),
 ev('d07', 'Wydruk z bazy', 'PESEL: Szulc Edward', 'Zaginiony biegły.', [], db='O-005-szulc'),
]
