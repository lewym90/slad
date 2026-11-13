# Sprawa 004 „Martwy kanał” — dowody (część skryptu build_004.py)
D = '2026-11-26'; F = '2026-11-27'

def ev(id, type, title, summary, body, **kw):
    d = {'id': id, 'type': type, 'title': title, 'summary': summary, 'body': body}
    d.update({k: v for k, v in kw.items() if v is not None})
    return d

def T(h, m, text, src, day=F):
    return [f'{day} {h:02d}:{m:02d}', text, src]

evidence = [
 # ---------- DOKUMENTY STARTOWE ----------
 ev('e01', 'Raport', 'Raport z miejsca zdarzenia', 'Piątek, 6:25. Pierwsze ustalenia patrolu.', [
   {'kv': [['Miejsce', 'Stacja nadawcza „Kolonia”, wzgórze Kolonia, Ruda — pomieszczenie nadajnika SN-1'],
           ['Zgłoszenie', 'piątek 27.11, 6:14, Henryk Mazur (konserwator stacji, Urząd Miasta), 112'],
           ['Przyjazd patrolu', '6:25'], ['Zmarły', 'Bogdan Lasota, 56 l., kierownik Referatu Zarządzania Kryzysowego UM']]},
   'Ciało leżało przy otwartej szafie nadajnika SN-1, obok rozdzielni zasilania 400 V. Drzwi stacji (D1) były zamknięte — konserwator wszedł własną kartą o 6:07. Stacja jest bez stałej obsady; nocą nikt tu nie pracuje. Noc była pochmurna, z mgłą i drobnym deszczem do rana.',
   'Pierwsza robocza hipoteza patrolu: porażenie prądem przy pracach przy zasilaniu. Technik odciął zasilanie szafy o 6:30, zanim ktokolwiek zbliżył się do ciała.',
   {'note': 'Lasota był administratorem systemu ostrzegania mieszkańców SYRION-4. Nic nie wskazuje, by miał tej nocy zaplanowane prace przy nadajniku.'}],
   start=True, time=[T(6, 14, 'Henryk Mazur zgłasza znalezienie ciała Lasoty', 'Raport')]),
 ev('e02', 'Opinia', 'Wstępna opinia lekarza', 'Oględziny o 7:20, przed przewiezieniem ciała.', [
   {'kv': [['Obrażenia', 'oparzenia prawej dłoni i przedramienia (ślady przepływu prądu); krwiak potyliczny'],
           ['Przyczyna zgonu', 'do ustalenia po sekcji'],
           ['Czas zgonu', 'piątek między 1:30 a 4:30 (wstępnie; w pomieszczeniu ok. 4°C)']]},
   'Krwiak potyliczny lekarz opisuje jako „do wyjaśnienia — możliwy uraz przy upadku po porażeniu”. Prosi o sekcję i o szczegółową analizę oparzeń.'],
   start=True),
 ev('e03', 'Raport', 'Raport Państwowej Straży Pożarnej', 'Wyciek chloru w zakładzie Chemrud, noc 26/27.11.', [
   {'kv': [['Zdarzenie', 'wyciek chloru, Chemrud S.A., wydział chloru, linia Cl-3'],
           ['Pierwsze zgłoszenie 112', 'piątek 2:09, mieszkaniec osiedla Zielone (duszący zapach)'],
           ['Straż na miejscu', '2:26'], ['Wyciek opanowany', '2:50'],
           ['Poszkodowani', '23 osoby przewiezione do Szpitala Miejskiego, nikt nie zmarł']]},
   'Syreny alarmowe SYRION-4 nie zawyły ani razu. Mieszkańcy dowiedzieli się z zapachu i z telefonów od sąsiadów.',
   {'note': 'Zgodnie z instrukcją zakładu, przekroczenie 3 ppm powinno automatycznie uruchamiać alarm syren w całym mieście.'}],
   start=True, time=[T(2, 9, 'Pierwsze zgłoszenie 112 o zapachu chloru na osiedlu Zielone', 'Raport PSP'), T(2, 50, 'Wyciek opanowany przez straż', 'Raport PSP')]),
 ev('e04', 'Zlecenie', 'Zlecenie prezydenta miasta', 'Dlaczego syreny milczały?', [
   {'quote': 'Syreny nie zawyły, a w nocy ktoś zginął na stacji, która je obsługuje. Producent czujników z Chemrud potwierdza, że żądanie alarmu wysłano o 1:47. W archiwum Centrum Zarządzania Kryzysowego nie ma po nim śladu. Chcę wiedzieć, co się stało — z alarmem i z Lasotą.', 'by': 'prezydent miasta Ruda'},
   {'kv': [['Zakres', 'przyczyna ciszy syren; zgon B. Lasoty; zniknięcie zapisu alarmu AL-2611-0147'], ['Termin', 'raport do poniedziałku']]}],
   start=True),
 ev('e05', 'Dokument', 'Schemat systemu SYRION-4', 'Jak polecenie alarmu trafia do syren.', [
   {'h': 'Tor alarmowy'},
   'Czujniki zakładów (np. Chemrud) wysyłają żądanie alarmu do serwera Centrum Zarządzania Kryzysowego (CZK, ul. Hutnicza). Serwer przekazuje polecenie kanałem K1 do nadajnika SN-1 na maszcie Kolonia, a nadajnik uruchamia 14 syren (S01–S14).',
   {'h': 'Kanał rezerwowy K3'},
   'Gdy K1 nie odpowiada, SN-1 automatycznie przełącza się na kanał rezerwowy K3 (osobna antena i osobny moduł nadawczy) i wysyła polecenie z lokalnego sterownika.',
   {'h': 'Tryb SERWIS'},
   'Szafa SN-1 ma przełącznik kluczykowy SERWIS/PRACA. W trybie SERWIS nadajnik ignoruje polecenia z K1 i z K3 (ochrona osób pracujących na maszcie). Każde przełączenie zapisuje się w dzienniku zdarzeń SN-1 razem z oznaczeniem klucza.'],
   start=True),
 ev('e06', 'Dokument', 'Regulamin serwisowy SYRION-4', 'Zasady okien serwisowych i kluczy.', [
   {'log': ['§2   Prace przy SN-1 wymagają zgłoszenia okna serwisowego w systemie MW.',
            '§4   Okno zatwierdza administrator systemu (kierownik Referatu Zarządzania Kryzysowego).',
            '§4.3 Zastępca może zatwierdzić okno tylko wtedy, gdy administrator jest nieobecny dłużej niż 72 godziny.',
            '§5   Klucz SERWIS i kartę serwisową otrzymuje wyłącznie serwisant z wykazu.',
            '§6   W trybie SERWIS blokowane są polecenia K1 i K3.',
            '§7   Po wyjściu z trybu SERWIS nadajnik wysyła zaległe polecenia z kolejki (do 6 godzin wstecz).']},
   {'note': 'Klucze SERWIS: UM-1 (miasto, w sejfie na stacji) oraz SYR-1 (pula serwisowa firmy Syreon Polska).'}],
   start=True),

 # ---------- STACJA NADAWCZA KOLONIA ----------
 ev('e07', 'Oględziny', 'Ciało przy szafie SN-1', 'Bogdan Lasota, pomieszczenie nadajnika.', [
   'Lasota leży na plecach przy otwartej szafie SN-1, głową ku ścianie, prawa ręka wyciągnięta, dłoń na szynach rozdzielni 400 V. Rękaw prawej ręki przepalony przy nadgarstku, skóra dłoni z oparzeniami. Pod potylicą niewielka kałuża zaschniętej krwi.',
   'Na podłodze, kilkadziesiąt centymetrów od ciała, brak krwi poza kałużą pod głową. Kurtka zapięta, lekko wilgotna od deszczu, rękawiczki w kieszeni. Karta LAS-01 w portfelu.',
   {'note': 'Oparzenia są ostre, ale okolica oparzeń jest sucha i blada. Technik zaznacza, że wygląda to „na czyste, bez reakcji skóry” — do oceny lekarza.'}]),
 ev('e08', 'Przedmiot', 'Zegarek Lasoty', 'Smartwatch z urwanym paskiem, pod szafą.', [
   'Zegarek leżał pod szafą, około 30 cm od ciała. Pasek urwany przy zapięciu, ekran pęknięty, urządzenie nie reaguje. Technik nie włączał go ani nie ustawiał godziny.',
   {'note': 'Dane z zegarka można odzyskać tylko przez producenta (zapytanie służbowe).'}]),
 ev('e09', 'Dziennik', 'Dziennik zdarzeń SN-1', 'Wydruk lokalnego dziennika nadajnika, pamięć zabezpieczona przed zapisem.', [
   {'log': ['27.11 01:03:22   MODE SERWIS ON            key=SYR-1',
            '27.11 01:03:23   K1 EXEC SUSPENDED',
            '27.11 01:03:25   K3 FAILOVER BLOCKED       (SERWIS)',
            '27.11 01:47:09   K1 CMD AL-2611-0147 IGN   (SERWIS)',
            '27.11 01:47:09   QUEUE ADD AL-2611-0147    pending',
            '27.11 03:01:50   QUEUE CLEAR (MANUAL)      key=SYR-1',
            '27.11 03:02:11   MODE PRACA                key=SYR-1',
            '27.11 03:02:12   K1 EXEC RESTORED']},
   {'note': 'Dziennik zapisuje się w pamięci, do której nie ma dostępu z poziomu panelu serwisowego. Jego zegar synchronizuje GPS.'}],
   time=[T(1, 3, 'SN-1 przechodzi w tryb SERWIS (klucz SYR-1)', 'Dziennik SN-1'), T(1, 47, 'SN-1 ignoruje polecenie alarmu AL-2611-0147 (tryb SERWIS)', 'Dziennik SN-1'), T(3, 2, 'SN-1 wraca do trybu PRACA (klucz SYR-1)', 'Dziennik SN-1')]),
 ev('e10', 'Oględziny', 'Przełącznik SERWIS/PRACA', 'Szafa SN-1, panel przełącznika.', [
   'Przełącznik w pozycji PRACA, kluczyka brak. Obudowa wytarta do czysta, w szczelinie tarcia kilka drobin talku z lateksowych rękawiczek. Daktyloskopii nie udało się zabezpieczyć.',
   {'note': 'Kluczyk UM-1 leży w sejfie stacji, plomba nienaruszona.'}]),
 ev('e11', 'Oględziny', 'Skrzynka kablowa K3', 'Złącze anteny rezerwowej na SN-1.', [
   'Do złącza K3 w szafie podłączono sztuczne obciążenie 50 Ω (obudowa z napisem ATR-50, nalepka serwisowa: „Syreon — czerwiec 2024”). Kabel prowadzący na maszt do anteny rezerwowej jest zaślepiony i zwinięty za szafą, bez śladów użycia.',
   {'note': 'Kanał K3 według schematu ma być autonomicznym torem rezerwowym. Przy takim podłączeniu nie wypromieniowałby żadnego sygnału.'}]),
 ev('e12', 'Wydruk', 'Wydruk z czytnika kart (drzwi D1)', 'Wejścia i wyjścia, 26–27.11.', [
   {'log': ['26.11 14:05:18   IN   MAZ-03   konserwator',
            '26.11 14:49:02   OUT  MAZ-03',
            '27.11 00:41:10   IN   SRV-07   pula serwisowa Syreon',
            '27.11 02:31:40   IN   LAS-01   administrator systemu',
            '27.11 03:09:50   OUT  SRV-07',
            '27.11 06:07:30   IN   MAZ-03']},
   'Obowiązują czytniki z obu stron drzwi: wyjście wymaga odbicia karty. Drzwi D1 zatrzaskują się samoczynnie.',
   {'note': 'Brak zapisu wyjścia karty LAS-01. Karta SRV-07 nie należy do konkretnej osoby, tylko do puli serwisowej firmy Syreon.'}],
   time=[T(0, 41, 'Karta SRV-07 (pula serwisowa Syreon) wchodzi na stację', 'Czytnik D1'), T(2, 31, 'Karta LAS-01 (Lasota) wchodzi na stację', 'Czytnik D1'), T(3, 9, 'Karta SRV-07 wychodzi ze stacji', 'Czytnik D1')]),
 ev('e13', 'Przedmiot', 'Klucz dynamometryczny SY-TW-17', 'Znaleziony w kanale kablowym za szafą.', [
   'Klucz dynamometryczny 40–200 Nm, wytarty, z nalepką inwentarzową „SY-TW-17”. W rowku przy głowicy zaschnięta rdzawa substancja. Klucz leżał w kanale kablowym tuż za szafą, poza zasięgiem wzroku od drzwi.',
   {'note': 'Nalepki SY- noszą narzędzia firmy Syreon Polska. Stacja nie ma własnych narzędzi tej klasy.'}]),
 ev('e14', 'Oględziny', 'Brama i droga dojazdowa', 'Żwirowy dojazd i kamera przy bramie.', [
   'Przy bramie na żwirze ślady opon dostawczego pojazdu (rozstaw kół typowy dla furgonu typu Ducato) oraz ślady dwóch samochodów osobowych, wyraźnie starsze.',
   'Kamera nad bramą nie rejestruje od wtorku. Zgłoszenie usterki wisi w systemie od 24.11, naprawa „odroczona”.',
   {'note': 'Brama zamykana na kłódkę, klucze mają miasto i serwisant.'}]),
 ev('e44', 'Przedmiot', 'Telefon Lasoty', 'Znaleziony w wewnętrznej kieszeni kurtki.', [
   'Telefon bez blokady ekranu (tryb pracy), 38% baterii. Na ekranie powiadomienia aplikacji SYRION-Mobile (dla administratora).',
   {'log': ['27.11 02:12   push SYRION-Mobile   SN-1 w trybie SERWIS od 01:03 (MW-2611). Alarm AL-2611-0147: brak potwierdzenia z syren.',
            '27.11 02:14   odczytano powiadomienie',
            '27.11 02:34   połączenie wychodzące   L. Hajduk   0:22']},
   {'note': 'Lasota został powiadomiony o trybie SERWIS i o niewysłanym alarmie dopiero o 2:12, bo aplikacja zgłasza brak potwierdzenia z syren po 25 minutach od żądania alarmu. Wcześniej żadne powiadomienie do niego nie dotarło.'}],
   time=[T(2, 12, 'Lasota dostaje powiadomienie: SN-1 w trybie SERWIS, alarm niewysłany', 'Telefon Lasoty'), T(2, 34, 'Lasota dzwoni do L. Hajduk (22 s)', 'Telefon Lasoty')]),
 ev('e45', 'Zeznanie', 'Protokół zeznań Henryka Mazura', 'Konserwator stacji, piątek 7:30.', [
   {'quote': 'O szóstej siedem odbiłem kartę i zobaczyłem pana Lasotę na podłodze przy szafie. Drzwi były zamknięte, zatrzaskują się same. Na stację jeżdżę dwa razy w tygodniu, nigdy nie widziałem tu nocą nikogo.', 'by': 'Henryk Mazur'},
   {'quote': 'Klucz UM-1 jest w sejfie na ścianie i nikt go nie ruszał, plomba cała. Drugi klucz, SYR-1, mają tylko ludzie z Syreon.', 'by': 'Henryk Mazur'}],
   testimony=True, start=True),

 # ---------- CENTRUM ZARZĄDZANIA KRYZYSOWEGO ----------
 ev('e16', 'Wydruk', 'Historia zdarzeń konsoli CZK (noc)', 'Pasek zdarzeń z konsoli dyżurnej, 0:00–4:00.', [
   {'log': ['27.11 00:12:04   TEST LINK SN-1                OK',
            '27.11 00:41:20   MW-2611 WINDOW OPEN SN-1       Syreon Polska',
            '27.11 01:03:30   STATUS SN-1                   SERWIS (MW-2611)',
            '27.11 03:02:20   STATUS SN-1                   PRACA',
            '27.11 03:02:21   TEST LINK SN-1                OK']},
   {'note': 'Konsola zapisuje tylko zmiany statusu łączy, a zdarzenia alarmowe trzyma archiwum alarmów. Między 1:03:30 a 3:02:20 historia konsoli jest pusta. Czerwony pasek „brak potwierdzenia” widać wyłącznie na żywo i nie jest archiwizowany.'}]),
 ev('e17', 'Notatka', 'Notatka z kosza w sali dyżurnej', 'Połowa żółtej karteczki, wyrzucona do kosza.', [
   {'quote': '01:49 — Kopeć (Syreon): serwis, to ich test czujnika?? „Nie ruszaj”. 112? — przekreślone', 'by': 'pismo operatorki, ołówek'},
   'Karteczka została przedarta na pół. Druga połowa, z napisem „Chemrud?”, leży obok.']),
 ev('e18', 'Nagranie', 'Zapis z kamery sali dyżurnej', 'CZK, kamera nad konsolą, 1:30–3:00.', [
   {'log': ['01:30–01:47   operatorka (plakietka: BURDA A.) przy konsoli, sama w sali',
            '01:47:40       operatorka zwraca się do ekranu, wstaje',
            '01:49:10       rozmowa telefoniczna, ok. 40 s, rozmówczyni stoi tyłem do kamery',
            '01:52:00       zapisuje coś na karteczce, siada',
            '02:00–03:00    operatorka cały czas w sali, sama']},
   {'note': 'Od 2023 roku w sali dyżurnej CZK pracuje jedna osoba na nocną zmianę.'}]),
 ev('e19', 'Dokument', 'Grafik dyżurów CZK', 'Noc z czwartku na piątek.', [
   {'kv': [['Zmiana nocna', '18:00–6:00'], ['Operator', 'A. Burda (jedyna osoba w sali)'], ['Nadzór zdalny', 'B. Lasota — telefon, powiadomienia aplikacji']]},
   'Przy alarmie operator uruchamia procedurę „A”: wysyła polecenie z konsoli i zgłasza zdarzenie do 112.']),
 ev('e20', 'Dokument', 'Procedura archiwum CZK', 'Usuwanie zapisów z archiwum alarmów.', [
   'Usunięcie zapisu z archiwum wymaga PIN-u operatora zmiany albo administratora. Operator może usuwać wyłącznie zapisy oznaczone jako testowe.',
   {'note': 'Każde usunięcie zostawia wpis w dzienniku audytu (tylko do odczytu, dostęp ma informatyk CZK).'}]),

 # ---------- ZAKŁAD CHEMRUD ----------
 ev('e21', 'Dziennik', 'Dziennik czujników GasNet', 'Wydruk wydziału chloru, linia Cl-3.', [
   {'log': ['27.11 01:41:20   Cl-3   spadek ciśnienia',
            '27.11 01:46:40   Cl-3   1,2 ppm     OSTRZEŻENIE',
            '27.11 01:47:00   Cl-3   3,4 ppm     ALARM',
            '27.11 01:47:05   ALARM REQ AL-2611-0147 -> CZK   przyjęto przez serwer CZK 01:47:06',
            '27.11 02:05:00   Cl-3   38 ppm      MAX',
            '27.11 02:50:00   Cl-3   0,8 ppm']},
   {'note': 'Brak potwierdzenia z syren. Żądanie alarmu zostało przyjęte przez serwer CZK jedną sekundę po wysłaniu.'}],
   time=[T(1, 47, 'Czujniki Chemrud wysyłają żądanie alarmu AL-2611-0147, serwer CZK je przyjmuje', 'Dziennik GasNet')]),
 ev('e22', 'Dziennik', 'Dziennik zmiany wydziału chloru', 'Nocna zmiana, kierownik zmiany J. Orlik.', [
   {'log': ['01:41   awaria zaworu Cl-3, wyciek',
            '01:47   czujniki: alarm',
            '01:52   kierownik zmiany dzwoni do prezesa W. Pyki; polecenie: bez zgłoszeń na zewnątrz, opanować własnymi siłami',
            '02:20   prezes Pyka na zakładzie, do 03:30',
            '02:26   straż pożarna (wezwana przez mieszkańców, nie przez zakład)']}],
   time=[T(1, 52, 'Kierownik zmiany Chemrud informuje prezesa Pykę o wycieku', 'Dziennik zmiany'), T(2, 20, 'Prezes Pyka przyjeżdża do zakładu', 'Dziennik zmiany')]),
 ev('e23', 'Raport', 'Raport z awarii zaworu Cl-3', 'Przyczyna wycieku.', [
   'Zawór Cl-3 wymieniono w 2025 roku na tańszy zamiennik, na polecenie prezesa (cena niższa o 40%). Zawór pękł na uszczelce w nocy z czwartku na piątek, około 1:41.',
   {'note': 'W 2025 roku czujniki GasNet wysłały cztery fałszywe alarmy, zakład uznał je za usterki oprogramowania.'}]),
 ev('e24', 'Dokument', 'Szkic oświadczenia prezesa Chemrud', 'Plik z gabinetu prezesa, zapis 2:40.', [
   {'quote': 'W nocy doszło do niewielkiej nieszczelności, bez zagrożenia dla mieszkańców. Zakład działał zgodnie z procedurami.', 'by': 'szkic oświadczenia, zapisany 27.11 o 2:40'}]),

 # ---------- SZPITAL MIEJSKI ----------
 ev('e25', 'Rejestr', 'Rejestr przyjęć SOR', 'Noc 26/27.11, Szpital Miejski.', [
   {'kv': [['Pierwszy pacjent', '2:19'], ['Łącznie', '23 osoby, w tym 3 w stanie ciężkim'], ['Powód', 'ekspozycja na chlor, mieszkańcy osiedla Zielone']]},
   {'note': 'Pierwszy telefon do szpitala od mieszkańców: 2:11.'}]),
 ev('e26', 'Opinia', 'Opinia toksykologa', 'Szpital Miejski, piątek 9:00.', [
   'Stężenie chloru w rejonie osiedla Zielone przekroczyło dawkę niebezpieczną po 8–12 minutach od 1:47. Ostrzeżenie syrenami w ciągu kilku minut pozwoliłoby zamknąć okna i wyjść na wzgórze. Zdecydowana większość poszkodowanych przebywała w tym czasie w łóżkach.']),

 # ---------- URZĄD MIASTA ----------
 ev('e27', 'Notatka', 'Kalendarz i notatki Lasoty', 'Gabinet kierownika referatu.', [
   {'kv': [['Pt 27.11, 9:00', 'NIK — spotkanie otwierające kontrolę SYRION-4'], ['Cz 26.11, 24:00', 'Kolonia, parking — L.H.']]},
   {'quote': 'PIN do sejfu: dzień i miesiąc odbioru systemu. Tego nie zapomnę.', 'by': 'karteczka na monitorze, pismo B. Lasoty'},
   'Na marginesie kalendarza: „K3 — porównać telemetrię z protokołem. Jeśli się nie zgadza, ktoś nas oszukał.”']),
 ev('e28', 'Dokument', 'Protokół odbioru SYRION-4 (2024)', 'Odbiór systemu przez miasto, czerwiec 2024.', [
   {'kv': [['Data odbioru', '14.06.2024'], ['Wykonawca', 'Syreon Polska Sp. z o.o.'], ['Wartość', '4 800 000 zł']]},
   {'log': ['K1  test łączności               pozytywny',
            'K3  test nadawania, moc 25 W      pozytywny (wymagane ≥ 20 W)',
            'Syreny S01–S14  test akustyczny   pozytywny']},
   {'kv': [['Za wykonawcę', 'D. Kopeć, inżynier wdrożenia'], ['Za zamawiającego', 'P. Szczerba, wiceprezydent'], ['Administrator systemu', 'pole puste (urlop B. Lasoty)']]}],
   mark='I'),
 ev('e29', 'Notatka', 'Teczka „K3” Lasoty', 'Sejf w gabinecie, robocze notatki do kontroli NIK.', [
   'Roboczy konspekt wystąpienia dla NIK: protokół odbioru twierdzi, że kanał K3 przeszedł test mocy. Telemetria z nadajnika mówi co innego. Do wyjaśnienia: kto zlecił zmianę zakresu w 2024 i kto podpisał odbiór pod nieobecność administratora.',
   {'quote': 'Dostanie to dziennikarka. NIK dostanie to samo o 9:00. Jeśli komuś zależy, żeby tego nie było, ma czas do rana.', 'by': 'B. Lasota, dopisek odręczny'}]),
 ev('e30', 'Dane', 'Telemetria K3 (eksport z SN-1)', 'Pamięć zdarzeń nadajnika, wpisy z 2024 roku.', [
   {'log': ['14.06.2024 11:20   TEST K3   FWD 0,3 W   REFL 0,0 W   WYNIK: NEG (brak mocy)',
            '14.06.2024 11:26   TEST K3   FWD 0,2 W   REFL 0,0 W   WYNIK: NEG (brak mocy)',
            '14.06.2024 11:41   K3 TEST PASS   wpis ręczny, panel serwisowy, key=SYR-1']},
   {'note': 'Wpis „PASS” dodano ręcznie z panelu serwisowego. Oba pomiary urządzenia dały wynik negatywny.'}]),
 ev('e31', 'Dokument', 'Zamówienie i aneks nr 2', 'Archiwum zamówień publicznych.', [
   {'log': ['Moduł nadajnika rezerwowego K3 (kpl.)        wykreślony aneksem nr 2',
            'Antena rezerwowa K3 z osprzętem              wykreślona aneksem nr 2',
            'Oszczędność wg aneksu nr 2 (28.05.2024)      612 000 zł']},
   {'kv': [['Aneks podpisali', 'Syreon Polska (D. Kopeć) i Urząd Miasta (P. Szczerba)'], ['Uzasadnienie', 'zmiana sprzętu na równoważny']]},
   {'note': 'Aneks z maja 2024 usuwa K3 z zakresu dostawy. Protokół odbioru z czerwca 2024 podaje K3 jako przetestowany.'}]),
 ev('e32', 'Rejestr', 'Zgłoszenie serwisowe MW-2611', 'System wniosków serwisowych.', [
   {'kv': [['Wnioskodawca', 'Syreon Polska — D. Kopeć'], ['Zakres', 'wymiana modułu K3 na SN-1'], ['Okno', '27.11, 0:00–3:00'],
           ['Zatwierdził', 'P. Szczerba, 26.11, 22:05, „w zastępstwie administratora”'], ['Powiadomienie do administratora', 'wstrzymane (zatwierdzenie w zastępstwie)']]},
   {'note': 'Administrator systemu, Lasota, był w pracy w czwartek do 18:30 i nie był nieobecny dłużej niż 72 godziny.'}],
   time=[T(22, 5, 'Szczerba zatwierdza okno serwisowe MW-2611 „w zastępstwie” Lasoty', 'System MW', day=D)]),
 ev('e33', 'Dokument', 'Faktura Alfa-Doradztwo', 'Kopia z szuflady wiceprezydenta.', [
   {'kv': [['Wystawca', 'Alfa-Doradztwo Sp. z o.o.; prezes zarządu: Karolina Szczerba'], ['Płatnik', 'Syreon Polska Sp. z o.o.'],
           ['Kwota', '310 000 zł netto'], ['Tytuł', 'doradztwo strategiczne'], ['Data', '15.07.2024']]},
   {'note': 'Płatnikiem nie jest miasto. Wystawcą jest firma żony wiceprezydenta.'}]),

 # ---------- PARKING LEŚNY ----------
 ev('e34', 'Nagranie', 'Fotopułapka leśnictwa', 'Zdjęcia z parkingu pod wzgórzem Kolonia.', [
   {'log': ['27.11 00:03   Skoda Octavia  SRS 4RX11   wjazd',
            '27.11 00:07   VW Golf        SRS 55K2   wjazd',
            '27.11 00:44   VW Golf        SRS 55K2   wyjazd',
            '27.11 00:46   Skoda Octavia  SRS 4RX11   wyjazd',
            '27.11 02:20   Skoda Octavia  SRS 4RX11   wjazd',
            '27.11 03:05   VW Golf        SRS 55K2   wjazd',
            '27.11 03:19   VW Golf        SRS 55K2   wyjazd']},
   {'note': 'Zegar fotopułapki synchronizowany z GPS. Octavia, która wjechała o 2:20, nie wyjechała do rana. Lasota mieszkał przy drodze na Kolonię, około sześciu minut jazdy od parkingu. Skoda Octavia SRS 4RX11 to samochód służbowy referatu Lasoty; VW Golf SRS 55K2 jest zarejestrowany na Lenę Hajduk.'}],
   time=[T(0, 7, 'Golf L. Hajduk wjeżdża na parking pod Kolonią, 4 minuty po aucie Lasoty', 'Fotopułapka'), T(3, 5, 'Golf L. Hajduk ponownie na parkingu pod Kolonią', 'Fotopułapka')]),
 ev('e35', 'Oględziny', 'Ślady przy parkingu', 'Parking leśny, piątek 9:30.', [
   'Wokół miejsca postoju dwóch aut ślady butów w rozmiarach około 43 i 38. Na pniaku dwa kubki po kawie z jednej stacji paliw i pusta koperta z logo „Głos Rudy”.']),

 # ---------- REDAKCJA „GŁOS RUDY” ----------
 ev('e36', 'Notatka', 'Notatki Leny Hajduk', 'Plan artykułu „Syreny na papierze”.', [
   'Notatnik reporterki. Hasło „Syreny na papierze”: źródło B.L. zapewnia, że kanał rezerwowy K3 jest atrapą, a protokół odbioru podrobiony. Dowód: telemetria z nadajnika, kopia na pendrive.',
   {'quote': 'Spotkanie 00:05 pod Kolonią. Ma przynieść kopię telemetrii. Nie wiem, kto jeszcze wie.', 'by': 'L. Hajduk, notatnik'},
   'Na ostatniej stronie, starszy wpis innym długopisem: „VESPER, Wrocław — »ekspertyzy« starych dokumentów. Kto to zamawia i ile płaci? Temat na później.”']),
 ev('e37', 'Korespondencja', 'E-mail Lasota — Hajduk', 'Czwartek 21:15.', [
   {'quote': 'Spotkajmy się o północy na parkingu pod Kolonią. Dam Pani, co trzeba. Jutro o dziewiątej NIK. Niech Pani niczego nie publikuje przed południem.', 'by': 'B. Lasota do L. Hajduk, 26.11 21:15'}],
   time=[T(21, 15, 'Lasota umawia się z Leną Hajduk na północ pod Kolonią', 'E-mail', day=D)]),

 # ---------- SYREON POLSKA (GLIWICE) ----------
 ev('e39', 'Rejestr', 'Rejestr kart i kluczy serwisowych Syreon', 'Gliwice, wydania z 26.11.', [
   {'log': ['26.11 16:10   karta SRV-07 + klucz SYR-1   pobrał: D. Kopeć   zwrot: jutro rano   uwagi: MW-2611']}]),
 ev('e40', 'Dokument', 'Grafik serwisantów Syreon', 'Dostępność w tygodniu 23–29.11.', [
   {'log': ['J. Wolak    urlop (Chorwacja) 24.11–07.12',
            'T. Tarka    zwolnienie lekarskie od 20.11',
            'D. Kopeć    dyżur nocny serwisowy 26/27.11']}]),
 ev('e41', 'Oględziny', 'Bus Syreon (Ducato) — wnętrze', 'Garaż firmy, piątek 13:00.', [
   'W skrzyni narzędziowej puste gniazdo w pianie z etykietą „SY-TW-17”, a obok zwitek niebieskich rękawic lateksowych. W kabinie trzy zaślepki oporowe 50 Ω.']),
 ev('e42', 'Wykaz', 'Wykaz narzędzi Syreon z przypisaniem', 'Narzędzia z przydziałem do osób.', [
   {'log': ['SY-TW-17   klucz dynamometryczny 40–200 Nm   przypisany: D. Kopeć   wydano 02.01.2025']}]),
 ev('e43', 'Dokument', 'Anulowanie zamówienia modułu K3', 'Archiwum zamówień Syreon.', [
   'Zamówienie modułu nadajnika rezerwowego K3 u producenta nadajników anulowano 03.06.2024 na polecenie D. Kopecia, przed odbiorem systemu.']),

 # ---------- ZEZNANIA PO KONFRONTACJACH (testimony) ----------
 ev('t01', 'Zeznanie', 'Uzupełnienie zeznań D. Kopecia (obecność na stacji)', 'Po konfrontacji.', [
   {'quote': 'Dobrze. Byłem na Kolonii. Okno serwisowe było moje, wymieniałem moduł K3. Wszedłem o 00:41, wyszedłem około drugiej. Lasoty nie widziałem na oczy.', 'by': 'Dariusz Kopeć'}], testimony=True),
 ev('t02', 'Zeznanie', 'Uzupełnienie zeznań D. Kopecia (godzina wyjścia)', 'Po konfrontacji.', [
   {'quote': 'Dobrze, przeciągnęło się do trzeciej. Antena, konfiguracja. Ale Lasoty tam nie było, przysięgam.', 'by': 'Dariusz Kopeć'}], testimony=True),
 ev('t03', 'Zeznanie', 'Uzupełnienie zeznań D. Kopecia (Lasota)', 'Po konfrontacji.', [
   {'quote': 'Zjawił się koło wpół do trzeciej. Pokłóciliśmy się o K3. Wyszedł na dwór zadzwonić, a ja zostałem przy szafie. Więcej go nie widziałem.', 'by': 'Dariusz Kopeć'}], testimony=True),
 ev('t04', 'Zeznanie', 'Uzupełnienie zeznań D. Kopecia (telefony)', 'Po konfrontacji.', [
   {'quote': 'Dzwoniła operatorka, potem wiceprezydent. Obojgu powiedziałem, że to fałszywy alarm z Chemrudu i że za chwilę wyjdę z serwisu. Nie wyszedłem.', 'by': 'Dariusz Kopeć'}], testimony=True),
 ev('t05', 'Zeznanie', 'Uzupełnienie zeznań D. Kopecia (koniec)', 'Po konfrontacji z sekcją i narzędziem.', [
   {'quote': 'Chciał to zgłosić, rano, wszystko. Złapałem klucz, jedno uderzenie. Potem ułożyłem go przy szynach. Alarm wisiał w kolejce — skasowałem go, zanim wyszedłem z serwisu, bo wyszłoby, że spóźniony.', 'by': 'Dariusz Kopeć'}], testimony=True),
 ev('t06', 'Zeznanie', 'Uzupełnienie zeznań A. Burdy (alarm)', 'Po konfrontacji.', [
   {'quote': 'Widziałam czerwony pasek „brak potwierdzenia”. Zadzwoniłam do serwisu. Kopeć powiedział, że to ich test czujnika, żebym niczego nie ruszała. Uwierzyłam mu.', 'by': 'Agnieszka Burda'}], testimony=True),
 ev('t07', 'Zeznanie', 'Uzupełnienie zeznań A. Burdy (archiwum)', 'Po konfrontacji.', [
   {'quote': 'Pan Szczerba kazał skasować zapis jako testowy, żeby nie robić paniki w mediach. Wpisałam swój PIN. Nie wiedziałam, że ktoś zginął.', 'by': 'Agnieszka Burda'}], testimony=True),
 ev('t08', 'Zeznanie', 'Uzupełnienie zeznań P. Szczerby (telefony)', 'Po konfrontacji.', [
   {'quote': 'Pyka dzwonił koło drugiej, pytał, czy syreny wyły. Zadzwoniłem do Kopecia, potem nad ranem do operatorki. Chciałem tylko uniknąć paniki.', 'by': 'Piotr Szczerba'}], testimony=True),
 ev('t09', 'Zeznanie', 'Uzupełnienie zeznań P. Szczerby (zatwierdzenie okna)', 'Po konfrontacji.', [
   {'quote': 'Zatwierdziłem okno sam, bo Kopeć prosił, a Lasota zawsze się certolił. Do dziś nie sprawdzałem, czy K3 działa. Podpisałem odbiór, bo serwis mówił, że działa.', 'by': 'Piotr Szczerba'}], testimony=True),
 ev('t10', 'Zeznanie', 'Uzupełnienie zeznań L. Hajduk (parking)', 'Po konfrontacji.', [
   {'quote': 'Spotkałam się z nim o północy. Dał mi pendrive z telemetrią K3 i protokół. Powiedział, że rano wszystko wyjdzie. Nie powiedziałam, bo chronię źródło.', 'by': 'Lena Hajduk'}], testimony=True),
 ev('t11', 'Zeznanie', 'Uzupełnienie zeznań L. Hajduk (druga wizyta)', 'Po konfrontacji.', [
   {'quote': 'Zadzwonił o drugiej trzydzieści cztery: „Przyjedź, to pilne”. Wjechałam w las o trzeciej pięć, pod bramą byłam kilka minut później. Brama zamknięta, w stacji światło. O dwunastej po trzeciej wyjechał stamtąd biały bus z drabiną na dachu i naklejką, widać było „SYREO…”.', 'by': 'Lena Hajduk'}], testimony=True),
 ev('t12', 'Zeznanie', 'Uzupełnienie zeznań W. Pyki (wiedza o wycieku)', 'Po konfrontacji.', [
   {'quote': 'Wiedziałem od 1:52. Orlik zadzwonił, uznałem, że zakład opanuje to sam. Nie wezwałem straży, bo nie chciałem kolejnej kontroli.', 'by': 'Witold Pyka'}], testimony=True),
 ev('e38', 'Nagranie', 'Zapis z kamerki w samochodzie (Golf)', 'Rejestrator jazdy Leny Hajduk, 3:05–3:20.', [
   {'log': ['03:05:10   wjazd na leśną drogę pod Kolonię',
            '03:09:20   pod bramą stacji: brama zamknięta, w oknie światło',
            '03:12:08   przy bramie od strony stacji mija biały furgon z drabiną na dachu, naklejka „SYREO…”, tablica częściowo: SGL 4…',
            '03:13:40   furgon znika za zakrętem w stronę drogi, bez świateł']},
   {'note': 'Nagranie otrzymaliście od Leny Hajduk dopiero po jej konfrontacji. Czas rejestratora zsynchronizowany z GPS.'}],
   time=[T(3, 12, 'Biały furgon z drabiną i naklejką „SYREO…” opuszcza stację', 'Rejestrator Hajduk')]),
 ev('t13', 'Zeznanie', 'Uzupełnienie zeznań W. Pyki (rozmowa z urzędem)', 'Po konfrontacji.', [
   {'quote': 'Dzwoniłem do wiceprezydenta, bo zobaczyłem, że miasto milczy. Zapytałem, czy syreny wyły. Powiedział: „Zajmę się tym”.', 'by': 'Witold Pyka'}], testimony=True),

 ev('t14', 'Zeznanie', 'Uzupełnienie zeznań D. Kopecia (K3)', 'Po konfrontacji.', [
   {'quote': 'K3 nie było w dostawie. Aneks wykreślił je z umowy, a Szczerba go podpisał. Nic więcej nie powiem bez adwokata.', 'by': 'Dariusz Kopeć'}], testimony=True),

 # ---------- TAJNE AKTA / CENTRALA ----------
 ev('x1', 'Wydruk', 'Billing połączeń (wyciąg operatora)', 'Telefony osób związanych ze sprawą, noc 26/27.11.', [
   {'log': ['27.11 01:49:12   A. Burda        ->  D. Kopeć       38 s',
            '27.11 01:52:30   Chemrud (zmiana) ->  W. Pyka        71 s',
            '27.11 01:58:40   W. Pyka         ->  P. Szczerba    112 s',
            '27.11 02:03:40   P. Szczerba     ->  D. Kopeć       57 s',
            '27.11 02:34:10   B. Lasota       ->  L. Hajduk      22 s',
            '27.11 03:35:20   P. Szczerba     ->  A. Burda       66 s']},
   {'note': 'Czas wg centrali operatora, zsynchronizowany. Wyciąg nie zawiera treści rozmów.'}],
   private=True, time=[T(1, 49, 'Burda dzwoni do Kopecia', 'Billing'), T(1, 58, 'Pyka dzwoni do Szczerby', 'Billing'), T(2, 3, 'Szczerba dzwoni do Kopecia', 'Billing'), T(3, 35, 'Szczerba dzwoni do Burdy', 'Billing')]),
 ev('x2', 'Dane', 'Dane lokalizacyjne operatora (BTS)', 'Rejestracje telefonów w komórkach, wybrane chwile.', [
   {'h': 'Pokrycie komórek'},
   {'log': ['Kolonia-1    stacja nadawcza i parking pod wzgórzem',
            'Droga-5      droga Ruda–Kolonia, bez zabudowy',
            'Centrum-2    śródmieście (CZK, urząd, redakcja i część mieszkań)',
            'Parkowe-7    osiedle Parkowe (domy jednorodzinne)',
            'Zielone-4    osiedle Zielone oraz zakład Chemrud']},
   {'h': 'Rejestracje'},
   {'log': ['              01:47        02:41',
            'D. Kopeć      Kolonia-1    Kolonia-1',
            'A. Burda      Centrum-2    Centrum-2',
            'P. Szczerba   Parkowe-7    Parkowe-7',
            'L. Hajduk     Parkowe-7    Droga-5',
            'W. Pyka       Zielone-4    Zielone-4']}],
   private=True),
 ev('x3', 'Dane', 'Telematyka busa Syreon', 'Wyciąg z GPS floty, pojazd Ducato.', [
   {'log': ['26.11 16:34   garaż Gliwice            wyjazd',
            '27.11 00:38   stacja Kolonia, brama    postój',
            '27.11 03:11   stacja Kolonia, brama    ruch',
            '27.11 04:20   garaż Gliwice            postój']},
   {'note': 'Pojazd w dyspozycji pracownika, który pobrał kartę SRV-07. Kierowca nie jest zapisywany przez system.'}],
   private=True),
 ev('x4', 'Opinia', 'Sekcja zwłok B. Lasoty — wnioski', 'Zakład medycyny sądowej, piątek 14:00.', [
   {'kv': [['Przyczyna zgonu', 'uraz czaszkowo-mózgowy po uderzeniu ciężkim narzędziem w potylicę'],
           ['Oparzenia', 'pośmiertne — brak odczynu żywotnego w skórze'],
           ['Ślad na kości', 'wgłębienie okrągłe o średnicy ok. 38 mm, zgodne z głowicą dużego klucza']]},
   'Śmierć nastąpiła w ciągu kilku minut od uderzenia. Do porażenia prądem doszło po śmierci.'],
   private=True),
 ev('x5', 'Wydruk', 'Dziennik audytu archiwum CZK', 'Odczyt informatyka CZK.', [
   {'log': ['27.11 03:41:07   DEL AL-2611-0147   user=abur   reason=ZAPIS TESTOWY   PIN ok']},
   {'note': 'Zapis alarmu został usunięty z poziomu stanowiska operatora, własnym PIN-em. Wpis audytu nie podlega usunięciu.'}],
   private=True, time=[T(3, 41, 'Z archiwum CZK usunięto zapis AL-2611-0147 (użytkownik abur)', 'Dziennik audytu')]),
 ev('x6', 'Dane', 'Eksport danych zegarka Lasoty', 'Dane odzyskane od producenta zegarka.', [
   {'log': ['zegarek   02:27   połączenie wychodzące   L. Hajduk   0:22',
            'zegarek   02:34   tętno 134   gwałtowne przyspieszenie',
            'zegarek   02:34   zdjęto z nadgarstka (urwany pasek)',
            'zegarek   02:34   koniec zapisu']},
   {'note': 'Zegar zegarka nie był synchronizowany z siecią od kilku tygodni.'}],
   private=True),
]
