# ŚLAD — plan rozwoju uniwersum

Dokument roboczy z decyzjami autora gry (właściciel repo). Służy do kontynuacji prac w dowolnej sesji/koncie Claude.
Stan na: 12.11.2026, wersja aplikacji 2.13.1. Sprawy 001–004 gotowe, 005–009 zapieczętowane.

## 0. Zasady nadrzędne (obowiązują zawsze)

1. Wszystko musi być logiczne i spójne jak w rzeczywistości. Każda niespójność w sprawie jest **celowa** (trop, kłamstwo, pomyłka świadka) — nigdy błąd gry.
2. Dedukcja na najwyższym poziomie: rozwiązanie wynika wyłącznie z materiałów, jedna jednoznaczna odpowiedź, walidator bez błędów.
3. Autor gra w sprawy — **nie zdradzać fabuły**, nie pokazywać zarysu, rozwiązań ani opisów mediów (prompty oznaczane tylko cyframi, podział GRAFIKI / VIDEO / DŹWIĘK).
4. Grafiki i media muszą być zgodne z fabułą w każdym szczególe (np. coś mokre, gdy nie powinno — to dla gracza dowód). Każdy obraz jest audytowany po wygenerowaniu.
5. Duże, osobne grafiki lokacji (wyświetlanie na telewizorze). Żadnych skrótów.
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
| 9 | Analiza monitoringu | 🔶 | Ograniczenia generatorów wideo (artefakty, ~15 s) — patrz §4 |
| 10 | Billingi i analiza powiązań | ✅ | |
| 11 | Oględziny w powiększeniu (szukanie szczegółów na dużym zdjęciu) | ✅ | Bardzo szczegółowe prompty, by błędy generowania nic nie zepsuły — §4 |
| 12 | Mapa miasta z czasem dojazdu | ✅ | |
| 13 | Dokumenty do odtworzenia (podarty list, szyfr, nadpalona kartka, pismo) | ✅ | |
| 14 | Dowody dźwiękowe (tło nagrania zdradza miejsce/czas) | ✅ | |
| 15 | Obserwacja (kogo śledzić w nocy) | ⏸ | Autor się zastanowi |
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
| 26 | Tryb rywalizacji drużyn | ⏸ | |
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
| 43 | Teczka do druku (PDF, koperty, QR) | ✅ | |
| 44 | Edytor spraw | ❌ | Autor znałby fabułę przed grą |

## 2. Terminal śledczy (#1) — wymagania autora i ustalenia

Wymagania autora (dosłownie w duchu):
- Ma działać jak prawdziwa baza danych. Wpisanie samego nazwiska „Kowalski” zwraca **wszystkich** Kowalskich (każde imię). „Jan Kowalski” zwraca tylko Janów Kowalskich.
- Nie może być sytuacji, że gracz zna dane, ale „zgaduje”, w jakiej formie baza je przyjmie.
- Każdy identyfikator (rejestracja, KRS, NIP, PESEL, nr księgi wieczystej, telefon, adres) występuje w całej grze **w jednej, identycznej formie**. Jeśli w aktach jest „124-15”, to wszędzie jest „124-15” i tylko ta forma działa w bazie. Ewentualna inna forma jest wyłącznie celowym zabiegiem fabularnym.
- Literówka lub błędna forma (np. „ul.” zamiast „al.”) = brak wyników, jak w rzeczywistości.

Ustalenia projektowe (do potwierdzenia):
- Formularze z osobnymi polami jak w prawdziwych systemach (np. Nazwisko / Imię / Data urodzenia; Nr rejestracyjny; KRS/NIP/nazwa). Puste pole = dowolna wartość.
- Normalizacja wyłącznie techniczna: wielkość liter i zbędne spacje na początku/końcu nie mają znaczenia. Wszystko inne (polskie znaki, myślniki, ukośniki, kolejność) — dokładnie.
- Rekordy „szumu” (inne osoby o tym samym nazwisku itd.) spójne z realiami sprawy.
- Walidator sprawdza, że każdy identyfikator ma w całej sprawie dokładnie jedną formę zapisu, i że każdy rekord bazy zgadza się z aktami.
- Zapytania kosztują ruch/czas; część baz wymaga nakazu (#3).

## 3. Własne pytania (#2) — do omówienia
Tematy wpisywane przez graczy, dopasowywane deterministycznie (odmiana, synonimy) do tematów znanych danej osobie; nieznane tematy → naturalna odmowa. Bez modelu AI w grze (ryzyko zmyślonych faktów, potrzeba internetu). Szczegóły w rozmowie z 12.11.2026.

## 4. Monitoring (#9) i oględziny w powiększeniu (#11)
- Kluczowe informacje nie mogą zależeć od generatora wideo. Monitoring jako sekwencja klatek/zdjęć; znacznik czasu, numer kamery i napisy nakłada aplikacja (kod), nigdy generator.
- Krótkie wideo tylko jako klimat, nie jako nośnik dowodu.
- Oględziny: szczegóły-dowody muszą być jednoznacznie widoczne i sprawdzone po wygenerowaniu; strefy (hotspoty) definiuje plik sprawy.

## 5. Zegar w grze (#20)
Czas gry płynie wyłącznie za akcje graczy (przeszukanie, dojazd, przesłuchanie), nigdy w czasie rzeczywistym. Pauza/odejście od gry nie zmienia niczego.

## 6. 48 godzin (#21) — do omówienia

## 7. Powiadomienia (#23) — do omówienia
Wiadomość w aplikacji (styl SMS), kierowana do roli/gracza, nie do numeru telefonu. Do ustalenia działanie przy jednym urządzeniu i przy kilku telefonach.

## 8. Tempo wprowadzania
Mieszanka: sprawy krótkie i duże, 1–3 nowości na sprawę, co jakiś czas sprawa bez nowości mechanicznych, za to z nowym formatem (#29–36). Szczegółowy przydział do spraw ustala Claude bez zdradzania fabuły autorowi.
