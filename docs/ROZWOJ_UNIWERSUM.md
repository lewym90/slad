# ŚLAD — plan rozwoju uniwersum

Dokument roboczy z decyzjami autora gry (właściciel repo). Służy do kontynuacji prac w dowolnej sesji/koncie Claude.
Stan na: 14.11.2026, wersja aplikacji 2.18.0. Sprawy 001–006 gotowe, 007 zbudowana (czeka na media), 008–010 zapieczętowane. Bieżący stan i lista zadań: `docs/PRZEKAZANIE.md`.

## 0. Zasady nadrzędne (obowiązują zawsze)

1. Wszystko musi być logiczne i spójne jak w rzeczywistości. Każda niespójność w sprawie jest **celowa** (trop, kłamstwo, pomyłka świadka) — nigdy błąd gry.
2. Dedukcja na najwyższym poziomie: rozwiązanie wynika wyłącznie z materiałów, jedna jednoznaczna odpowiedź, walidator bez błędów.
3. Autor gra w sprawy — **nie zdradzać fabuły**, nie pokazywać zarysu, rozwiązań ani opisów mediów (prompty oznaczane tylko cyframi, podział GRAFIKI / VIDEO / DŹWIĘK).
4. Grafiki i media muszą być zgodne z fabułą w każdym szczególe (np. coś mokre, gdy nie powinno — to dla gracza dowód). Każdy obraz jest audytowany po wygenerowaniu.
5. Duże, osobne grafiki lokacji (wyświetlanie na telewizorze). Żadnych skrótów. Od sprawy 005 każdy prompt wymaga NAJWYŻSZEJ możliwej rozdzielczości i jakości wpisanej w treść (grafiki ≥4K, idealnie 6144×4096 / 8K; wideo 4K; audio WAV 48 kHz 24-bit) — autor niczego nie zmienia, tylko kopiuje.
6. Nowości wprowadzamy **stopniowo i zmiennie**: raz jedna nowość, raz kilka, raz sprawa krótka, raz duża. Nie wszystko naraz. Kierunek: coraz bogatsza rozgrywka, docelowo mega-sprawa 4–5 h, a uniwersum może mieć znacznie więcej niż 9 spraw.
7. Nie tworzymy edytora spraw dla autora (zna by fabułę przed grą).

## 1. Lista pomysłów i decyzje

Legenda: ✅ robimy · 🔶 robimy, ale wymaga doprecyzowania · ⏸ na później · ❌ raczej nie

| # | Pomysł | Decyzja | Uwagi autora |
|---|--------|---------|--------------|
| 1 | Terminal śledczy — bazy danych (PESEL, CEPiK, KRS, KRK, księgi wieczyste, broń, archiwum spraw), na telefonie, m.in. przez QR | 🔶 | Musi działać jak prawdziwa baza — patrz §2 |
| 2 | Własne pytania (tematy wpisywane przez graczy, parser deterministyczny, bez AI) | 🔶 | Autor prosi o szczegółowe wyjaśnienie — patrz §3 |
| 3 | Wnioski do prokuratora (nakazy uzasadniane dowodami) | ✅ | |
| 4 | Pokaż dowód dowolnej osobie → reakcja | ✅ | |
| 5 | Laboratorium z kolejką i opóźnionymi wynikami | ✅ | |
| 6 | Telefon ofiary (odblokowanie kodem, SMS, galeria, lokalizacje, połączenia) | ✅ | |
| 7 | Komputer i poczta podejrzanego | ✅ | |
| 8 | Media społecznościowe i OSINT (geolokalizacja zdjęć, godziny postów) | ✅ | |
| 9 | Analiza monitoringu | 🔶 | Autor: serie klatek z generatora są nierealne — zamiast tego monitoring jako dane i schemat generowany kodem (§4) |
| 10 | Billingi i analiza powiązań | ✅ | |
| 11 | Oględziny w powiększeniu (szukanie szczegółów na dużym zdjęciu) | ✅ | Bardzo szczegółowe prompty, by błędy generowania nic nie zepsuły — §4 |
| 12 | Mapa miasta z czasem dojazdu | ✅ | |
| 13 | Dokumenty do odtworzenia (podarty list, szyfr, nadpalona kartka, pismo) | ✅ | |
| 14 | Dowody dźwiękowe (tło nagrania zdradza miejsce/czas) | ✅ | |
| 15 | Obserwacja (kogo śledzić w nocy) | ⏸ | Na razie nie (13.11.2026) |
| 16 | Presja i adwokat w przesłuchaniu | ✅ | |
| 17 | Ponowne przesłuchanie po nowym dowodzie | ✅ | |
| 18 | Konfrontacja dwóch osób naraz | ✅ | |
| 19 | Świadek, który się myli, a nie kłamie | ✅ | |
| 20 | Zegar w grze zamiast ruchów, wydarzenia o ustalonych godzinach | 🔶 | Nie może biec w czasie rzeczywistym (przerwa na obiad ≠ przegrana) — §5 |
| 21 | 48 godzin zatrzymania | 🔶 | Autor prosi o rozwinięcie — §6 |
| 22 | Nieodwracalne decyzje, rozgałęzienia | ✅ | |
| 23 | Wydarzenia na żywo / powiadomienie „SMS” do konkretnego gracza | 🔶 | Jeśli technicznie możliwe; ustalić, który telefon dostaje wiadomość (gra w parze i u innych osób) — §7 |
| 24 | Role z asymetryczną wiedzą (technik, analityk, profiler, prokurator) | ✅ | |
| 25 | Wspólne wnioski w trakcie gry (łączenie faktów) | ✅ | |
| 26 | Tryb rywalizacji drużyn | ⏸ | Na razie nie (13.11.2026) |
| 27 | Rozprawa w sądzie jako finał | ✅ | |
| 28 | Kilka poziomów prawdy (np. zleceniodawca) | ✅ | |
| 29 | Odwrócony kryminał (Columbo) | ✅ | |
| 30 | Sprawa obrony (udowodnić niewinność) | ✅ | |
| 31 | Zaginięcie zamiast morderstwa | ✅ | |
| 32 | Sprawca spoza obsady (szukany w bazach) | ✅ | |
| 33 | Dwie sprawy przemieszane | ❌ | |
| 34 | Seryjny sprawca w odcinkach | ✅ | |
| 35 | Szybkie zgłoszenia 15–20 min | ✅ | |
| 36 | Sprawa historyczna (PRL, międzywojnie) | ✅ | |
| 37 | Kampania: kartoteka zespołu, ranga, odblokowywane narzędzia | ✅ | |
| 38 | Powracające postaci | ✅ | |
| 39 | Ukryty wątek nadrzędny łączący sprawy, finałowa wielka sprawa | ✅ | |
| 40 | Powrót do zamkniętej sprawy (nowy dowód podważa wyrok) | ✅ | |
| 41 | Archiwum dawnych spraw jako baza | ✅ | |
| 42 | Kronika miasta i odznaki | ❌ | |
| 43 | Materiały do druku | ✅ | Zawsze opcjonalne — patrz §10 |
| 44 | Edytor spraw | ❌ | Autor znałby fabułę przed grą |

## 2. Terminal śledczy (#1) — wymagania autora i ustalenia

Wymagania autora (dosłownie w duchu):
- Ma działać jak prawdziwa baza danych. Wpisanie samego nazwiska „Kowalski” zwraca **wszystkich** Kowalskich (każde imię). „Jan Kowalski” zwraca tylko Janów Kowalskich.
- Nie może być sytuacji, że gracz zna dane, ale „zgaduje”, w jakiej formie baza je przyjmie.
- Każdy identyfikator (rejestracja, KRS, NIP, PESEL, nr księgi wieczystej, telefon, adres) występuje w całej grze **w jednej, identycznej formie**. Jeśli w aktach jest „124-15”, to wszędzie jest „124-15” i tylko ta forma działa w bazie. Ewentualna inna forma jest wyłącznie celowym zabiegiem fabularnym.
- Literówka lub błędna forma (np. „ul.” zamiast „al.”) = brak wyników, jak w rzeczywistości.

Ustalenia projektowe (POTWIERDZONE przez autora 12.11.2026):
- Formularze z osobnymi polami jak w prawdziwych systemach (np. Nazwisko / Imię / Data urodzenia; Nr rejestracyjny; KRS/NIP/nazwa). Puste pole = dowolna wartość.
- Normalizacja wyłącznie techniczna: wielkość liter i zbędne spacje na początku/końcu nie mają znaczenia. Wszystko inne (polskie znaki, myślniki, ukośniki, kolejność) — dokładnie.
- Rekordy „szumu” (inne osoby o tym samym nazwisku itd.) spójne z realiami sprawy.
- Walidator sprawdza, że każdy identyfikator ma w całej sprawie dokładnie jedną formę zapisu, i że każdy rekord bazy zgadza się z aktami.
- Zapytania kosztują ruch/czas; część baz wymaga nakazu (#3).

## 3. Własne pytania (#2) — ZAAKCEPTOWANE
- Pole „Zapytaj o…”: gracz wpisuje temat (słowo, nazwisko, miejsce, godzinę). Dopasowanie deterministyczne: odmiana, synonimy, warianty. Bez modelu AI w grze.
- Nieznany temat → naturalna odpowiedź postaci; **nie kosztuje ruchu ani czasu** (wymóg autora). Kosztuje tylko trafione pytanie, tak jak zwykłe pytanie.
- Ochrona przed „wstrzeliwaniem się”: podpowiadanie (autouzupełnianie) z rzeczy, które gracze już znają — nazwiska, miejsca, dowody z akt. Bogate listy synonimów dla każdego tematu.
- Ochrona przed zgadywaniem na ślepo: temat działa dopiero wtedy, gdy gracze faktycznie o nim wiedzą (odblokowany dowodem/zeznaniem), więc wpisywanie wszystkich nazw z listy nic nie da.
- Lista tematów już poruszonych z każdą osobą.

## 4. Monitoring (#9) i oględziny w powiększeniu (#11)
Autor odrzucił serie klatek z generatora (niewykonalne: generator nie trzyma spójności nawet przy naklejce na aucie).
Rozwiązanie — monitoring bez generowanych serii:
- **Odtwarzacz zdarzeń rysowany przez aplikację**: plan budynku/ulicy (SVG), na którym kamery, czujniki, czytniki kart i ANPR zapalają się na osi czasu; gracz przewija, zatrzymuje, porównuje. Wszystko generowane kodem z danych sprawy — idealnie spójne.
- **Dzienniki**: ANPR (rozpoznawanie tablic), czujniki ruchu, kontrola dostępu, licznik wejść; protokół oględzin zapisu monitoringu (opis policjanta z godzinami).
- **Najwyżej 1–2 pojedyncze kadry na sprawę**, każdy niezależny (bez wymogu ciągłości z innymi), audytowany jak każda grafika; informacja kluczowa zawsze także w tekście protokołu.
- Wideo z generatora tylko jako klimat (przełomy), nigdy nośnik dowodu.
Oględziny w powiększeniu: na istniejących dużych grafikach lokacji gracz sam szuka miejsc; po trafieniu widzi zbliżenie i opis technika (opis jest wiążący). Kluczowe szczegóły duże i jednoznaczne; każdy obraz audytowany pod kątem fałszywych tropów; strefy definiuje plik sprawy.

## 5. Zegar w grze (#20)
Czas gry płynie wyłącznie za akcje graczy (przeszukanie, dojazd, przesłuchanie), nigdy w czasie rzeczywistym. Pauza/odejście od gry nie zmienia niczego.

## 6. 48 godzin (#21) — do omówienia

## 7. Powiadomienia (#23) — do omówienia
Wiadomość w aplikacji (styl SMS), kierowana do roli/gracza, nie do numeru telefonu. Do ustalenia działanie przy jednym urządzeniu i przy kilku telefonach.

## 8. Tempo wprowadzania
Mieszanka: sprawy krótkie i duże, 1–3 nowości na sprawę, co jakiś czas sprawa bez nowości mechanicznych, za to z nowym formatem (#29–36). Szczegółowy przydział do spraw ustala Claude bez zdradzania fabuły autorowi.

## 9. Poprawka UI: ekran konfrontacji (zgłoszona 12.11.2026) — WDROŻONE w 2.14.0: punkty 1, 3, 4, 6, 8 (wszystkie sprawy). Wyszukiwarka usunięta na życzenie autora w 2.14.1 („małe utrudnienia nie zaszkodzą”); punkty 5 i 7 nie wybrane.
Problem: płaska lista kafelków (dowody w kolejności znalezienia, notatki X, potem zeznania w innej formie); trzeba za każdym razem czytać wszystko.
Propozycja (do potwierdzenia przez autora):
1. Podważane zeznanie przypięte u góry (nie ucieka przy przewijaniu).
2. Pole wyszukiwania (tytuł, opis, nazwisko, numer dowodu).
3. Filtry-zakładki: Wszystko · Przypięte · Dowody rzeczowe i oględziny · Dokumenty i wykazy · Notatki zespołu · Zeznania.
4. Grupowanie dowodów według miejsca znalezienia (zwijane sekcje z nazwą lokacji), zeznania według osoby (z portretem).
5. Stały kolor kategorii (pasek z lewej + ikona), ten sam w Aktach, na Tablicy i w konfrontacji.
6. Pod tytułem jedna linia streszczenia; ikona „podgląd” otwiera dowód bez wychodzenia z konfrontacji, z przyciskiem „Okaż”.
7. Gwiazdka „przypnij” w Aktach — przypięte zawsze na górze listy w konfrontacji.
8. Dowody już nietrafione przeciw temu zeznaniu wyszarzone ze znakiem ✗.
Zasada: filtry i kolory są neutralne — niczego nie podpowiadają (żadnego wyróżniania właściwego dowodu).

## 10. Decyzje autora z 13.11.2026
1. **Liczba graczy i urządzenia — uniwersalnie.** Gra nie jest tylko dla autora (gra we dwoje z partnerką, czasem więcej osób, znajomi grają po swojemu). Każda mechanika musi działać przy 1–6 graczach, na jednym urządzeniu, na TV + telefonach i na samych telefonach.
2. **Role (#24): jedna osoba = jedna rola.** Zestaw ról skaluje się z liczbą graczy: przy małej liczbie graczy role łączą funkcje (np. przy 2 graczach dwie role „połączone”), przy większej dzielą się na węższe. Kluczowe informacje zawsze rozłożone tak, by każda liczba graczy miała pełny dostęp.
3. **Postęp kampanii (#37)** zapisywany na urządzeniu (bez przenoszenia kodem).
4. **Ukryty wątek nadrzędny (#39)** zaczyna się od sprawy 005. Sprawy 001–004 bez zmian (mogą wrócić jako cold case, #40).
5. **Sprawy dzieją się w całej Polsce.** Baza danych (#1) jest **jedna, ogólnopolska i wspólna dla wszystkich spraw** — z każdego miejsca widać osoby z całego kraju.
   Ustalenia do bazy: rekordy z datą obowiązywania (sprawa widzi bazę z dnia zdarzenia); rekordy zdradzające rozwiązanie widoczne dopiero po rozwiązaniu danej sprawy; kilka tysięcy stałych, fikcyjnych rekordów „tła” wygenerowanych raz i zapisanych (bez losowania w grze), walidowanych pod kątem kolizji; każda sprawa decyduje, które bazy są dostępne; w 001–004 terminal wyłączony lub tylko archiwum (nie były projektowane pod bazę).
6. **Druk (#43):** w Ustawieniach rozwijana sekcja „Do wydruku” z jednym linkiem (PDF) na każdą sprawę — można wydrukować z wyprzedzeniem na wiele spraw. Gdy sprawa ma materiały do druku, informacja jest na jej starcie, a szef wydziału wspomina o tym w odprawie. Druk **nigdy nie jest wymagany**: wszystko jest też w aplikacji (np. podarty list układany palcem).
7. Wyszukiwarka w konfrontacji — usunięta.
8. Obserwacja (#15) i rywalizacja (#26) — na razie nie.

## 11. Stan wdrożenia (13.11.2026)
- 2.15.0: terminal baz danych (#1) i okazywanie dowodów (#4) w silniku; ogólnopolska baza tła w `data/baza/`.
- Sprawa 005 „Pokój bez okien”: debiut #1, #4 i formatu zaginięcia (#31); logika zwalidowana, testy przejścia OK; czeka na media (prompty w `docs/PROMPTY_*_005.md`).
- Następne sprawy: kolejne nowości z listy, zmiennie (raz jedna, raz kilka; raz krótka sprawa, raz duża).

## 12. Decyzje autora z 13.11.2026 (przed południem)
1. **Ekran „Nowe uprawnienia wydziału”** na starcie sprawy, która coś odblokowuje (`case.unlocks`, opcjonalnie `unlockNote` — słowa szefa wydziału). Spis odblokowanych w Kronice wydziału (`S.unlocked`).
2. **Raz odblokowane uprawnienie zostaje** we wszystkich kolejnych sprawach. Wyjątek tylko z fabularnym powodem (np. awaria systemu, sprawa historyczna) — pole `offline: {db: 'powód'}`; zakładka pokazuje wtedy komunikat. Walidator pilnuje: od 005 każda sprawa ma `db` (albo `offline.db`) i każda osoba ma `showDefault` (albo `offline.show`).
3. **Oględziny na zdjęciu (#11) — zaakceptowane w tej formie:** licznik „Ślady: x z y”, ślad można wskazać dopiero po co najmniej 2× przybliżeniu, pudło bezpłatne, trafienie = 1 ruch (jak przeszukanie punktu), nieodkryte ślady jako „???”, zablokowane po trafieniu pokazują powód. Dane: `location.search = {aspect, img?, spots: {spotId: [x, y, r]}}` (współrzędne względne, r względem szerokości). Pozycje zaznacza Claude po wygenerowaniu grafiki i sprawdza; ślady muszą być wyraźnymi przedmiotami. Nie w każdym miejscu („raz tak, raz inaczej”). Silnik gotowy w 2.16.0; pierwsze użycie planowane od sprawy 006 (`FEATURES.look.since`).
4. **Ostrość na dużym ekranie:** generator autora daje maks. 1536×1024 (grafiki) i 1280×720 (wideo). Skalowanie AI ×4 (Real-ESRGAN) wyraźnie poprawia ostrość — autor zrobi je u siebie programem **Upscayl** (Claude poda instrukcję, gdy autor będzie przy komputerze). W chmurze to ok. 1 h na grafikę (brak GPU).
5. Dźwięk tła 005 wygenerowany ponownie (lepszy prompt ze zdarzeniami na osi czasu) — sprawa 005 odpieczętowana w 2.16.1.

## 13. Plan spraw 006–009 (zatwierdzony 13.11.2026: „Zgoda.”)
- **006 „Ostatni seans”** (średnia, 80–110 min): debiut oględzin na zdjęciu (#11), rekonstrukcji podartego dokumentu (#13), świadka, który się myli, a nie kłamie (#19), i materiałów do wydruku (#43). Baza i okazywanie dowodów działają dalej.
- **007 „Biała cisza”** (100–140 min): mapa z czasami przejść (#12), dowód dźwiękowy (#14), zegar gry liczony akcjami (#20).
- **008 „Cień w galerii”** (60–90 min): sprawca znany od początku — udowodnić (#29), nakazy prokuratora (#3), telefon podejrzanego (#6).
- **009 „Czarna skrzynka”** (ok. 2,5–3 h): 48 godzin zatrzymania (#21), presja i adwokat (#16), finał w sądzie (#27).
- Wątek przewodni uniwersum: zgodnie z decyzją autora od 005, a gdzie to możliwe bez komplikacji — od 003 (szczegóły tylko w plikach spraw, bez opisywania tutaj).

## 14. Stan wdrożenia 2.17 (13.11.2026)
- Silnik: zagadka „podarty dokument” (`input: "torn"`), zeznania-pomyłki (`mistake: true`), materiały do wydruku (`tools/gen_print.py`, Ustawienia → „Do wydruku”).
- 006: komplet mediów, ślady na zdjęciach rozmieszczone, walidacja bez błędów, przejścia testowe 100 pkt; otwarta w 2.17.1 (13.11.2026). Wszystkie grafiki 001–006 przeskalowane w Upscaylu (×4) i podmienione (2.17.6–2.17.8).

## 15. Sprawa 010 — finał pierwszej kampanii (decyzja 13.11.2026)
- Kampania pierwsza liczy 10 spraw: 001–006 gotowe, 007–009 według planu z §13, **010 to wielki finał** (4–5 h gry, z przerwami — postęp zapisuje się na urządzeniu, sprawa podzielona na akty).
- Tytuł roboczy: **„Palimpsest”**. Ma być najbardziej zaawansowaną rozgrywką ze wszystkich: wszystkie odblokowane uprawnienia działają jednocześnie, wracają postacie i miejsca z wcześniejszych spraw, a baza danych pokazuje skutki rozwiązanych spraw.
- Kandydaci na nowości finału (do omówienia przed budową): role w zespole i wspólne wnioski, decyzje nieodwracalne, powiadomienia dla ról, akty z osobnymi raportami cząstkowymi i jeden raport końcowy.
- Po finale: planowanie kampanii drugiej (sprawy 011–020).

## 16. Audyt całości (14.11.2026, wersja 2.17.9)
- Walidator: zero błędów i ostrzeżeń dla 001–006; przejścia testowe (stół i telefony) 100 pkt.
- Poprawki językowe w 001, 002 i 006 (formy czasowników, wielokropki, przecinki, jedno niezręczne zdanie, odsyłacz z identyfikatorem w treści sekcji).
- 006: daty faktury i oznaczenia faksymile ujednolicone z resztą osi czasu (faksymile zamówione tuż przed oddaniem oryginałów do komisu).
- Walidator porównuje teksty z nagraniami bez względu na interpunkcję i wielkość liter (poprawka przecinka nie wymaga nowego nagrania).
- Zagadka „Podarty list”: skrawki rozłożone równomierniej na stole, bez zbędnych komunikatów o próbach.

## 17. Sprawa 007 „Biała cisza” — budowa (14.11.2026, wersja 2.18.0)
- Zatwierdzone przez autora („Zgoda na wszystko”): zegar zamiast ruchów (wynik od godziny raportu), spóźnienie nigdy nie blokuje rozwiązania; mapa z pozycją zespołu i czasami przejść, śnieżyca wydłuża lub zamyka szlaki, mapa w PDF-ie do wydruku; dowód dźwiękowy z zaznaczaniem momentu i analizą technika jako podpowiedzią (nagranie składa Claude z pojedynczych dźwięków); bazy i okazywanie dowodów działają przez radio, kosztują czas; 1–6 graczy.
- Silnik 2.18: `clock`, `map`, `evidence.audio`, `novelties`, punkty `expires`; walidator: osiągalność mapy (także w śnieżycy), zdarzenia zegara, znaczniki nagrań, zakaz jedynych dróg przez ślady, które przepadają z czasem.
- Sprawa zbudowana skryptem `tools/build_007.py` (moduły `b007_*.py`), walidacja bez błędów logiki, przejścia testowe w obu trybach z kompletem dowodów i przełomów. Zapieczętowana do czasu mediów; nagranie łączności w repozytorium jest tymczasowe (syntetyczne) — do podmiany na złożone z wygenerowanych dźwięków.
- Prompty mediów: `docs/PROMPTY_007.md` (generuje `tools/prompts_007.py`, kolejność plików: `tools/voice/007-media-order.json`).

## 18. Media i przekazanie projektu (14.11.2026)
- Generowanie mediów wtyczką Krea odrzucone przez autora (za drogo). Wtyczek do ChatGPT i Groka nie ma. Uzgodniony kierunek do sprawdzenia: Claude obsługuje ChatGPT (grafiki) i Groka (filmy, dźwięki) w przeglądarce autora, na jego kontach — test na jednej grafice 007, gdy autor będzie przy komputerze. Szczegóły: `docs/PRZEKAZANIE.md` §5.
- Pełne przekazanie projektu na inne konto Claude: `docs/PRZEKAZANIE.md` (bez spoilerów) i `docs/PRZEKAZANIE_DLA_CLAUDE_SPOILERY.md` (tylko dla Claude).

