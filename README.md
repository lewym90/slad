# ŚLAD — Archiwum spraw niewyjaśnionych

Kooperacyjna gra detektywistyczna dla 2–6 osób przy jednym ekranie (telefon, tablet, komputer). Instaluje się jak aplikacja (PWA) i po pierwszym uruchomieniu działa offline.

Gotowe sprawy: 001 „Dom, który pamięta”, 002 „Ostatni pociąg”, 003 „Cisza w sanatorium”, 004 „Martwy kanał”, 005 „Pokój bez okien”. Sprawy 006–009 są w przygotowaniu (widoczne w archiwum jako zapieczętowane). Aktualny numer wersji: Ustawienia → „Wersja gry”.

## Tryby gry (wybór po otwarciu sprawy)
- **Wspólny stół** — jeden ekran (laptop, telewizor, tablet). Wszyscy widzą wszystko. Informacje, które w drugim trybie są tajnymi aktami, trzeba zdobyć w śledztwie (m.in. w miejscu „Centrala wydziału”). Najlepszy we dwoje.
- **Telewizor + telefony** — gra na wspólnym ekranie, a każdy gracz skanuje swój kod QR i ma tajne akta tylko w swoim telefonie. Dokument ujawnia się zespołowi, wpisując na wspólnym ekranie jego 4-znakowy kod z telefonu. Działa bez serwera — kod QR zawiera adres teczki. Gracz bez telefonu może zajrzeć do teczki na wspólnym ekranie (zabezpieczone pieczęcią).

**Tryb telewizora** (Ustawienia ⚙ albo przełącznik na ekranie wyboru trybu) powiększa tekst, karty i przyciski tak, by były czytelne z kanapy. Skaluje się do rozdzielczości: laptop, Full HD, 4K.

## Jak się gra
1. Przeszukujcie **miejsca** i przesłuchujcie **osoby**. Każdy ruch jest liczony (norma ruchów wpływa na wynik).
2. Świadkowie kłamią. W **protokole zeznań** podważajcie zeznania dowodami (konfrontacja). Nietrafiona konfrontacja kosztuje punkty.
3. **Zagadki** wymagają połączenia kilku dokumentów — odpowiedzi nie ma w pytaniu.
4. **Szkic miejsca zdarzenia** (zakładka Miejsca) pokazuje rozkład pomieszczeń; żółte tabliczki pojawiają się na przeszukanych punktach, obrys ciała — po oględzinach.
5. **Tablica** (korkowa, z czerwoną nitką), **oś czasu** i **notatki** pomagają poukładać fakty.
6. **Akt oskarżenia**: pytania o sprawcę, sposób, czas, motyw i tło sprawy, kolejność zdarzeń + wskazanie dowodów. Wynik 0–100, ranga, epilog i decyzja zespołu.

## Funkcje dodatkowe (2.9)
- **Poziomy trudności:** Rekrut, Śledczy, Weteran — zmieniają normę ruchów i koszty podpowiedzi, tropów i pomyłek.
- **Role ze zdolnościami:** każda rola ma jedną zdolność na sprawę (Analiza → Zespół).
- **Przełomy:** pełnoekranowe sceny po kluczowych odkryciach (`breakthroughs` w JSON: zdjęcie albo wideo).
- **Konfrontacje świadek kontra świadek:** kłamstwo można podważyć prawdziwym zeznaniem innej osoby (token `st:<id>`).
- **Tabela podejrzanych** i **głosowanie zespołu** (głosowanie tylko w trybie telewizor + telefony).
- **Powiększanie zdjęć** gestem lub kółkiem myszy — reszta interfejsu jest zablokowana przed przypadkowym powiększaniem.
- **Lektor briefingu** (`voice.brief`) i **głosy świadków** (`voiceDir`: `<id pytania/zeznania>.mp3`, odmowy `<osoba>-deflect-<n>.mp3`) — muzyka cichnie, gdy ktoś mówi; przełącznik w ustawieniach i w oknie przesłuchania.
- **Filmy** — `introVideo` i `breakthroughs[].video` (`assets/video`, plakat `.webp` o tej samej nazwie). Nagrania i filmy sprawy zapisują się do pamięci offline po rozpoczęciu gry; Service Worker odpowiada na zapytania Range (wymóg iPhone'a).
- Teksty lektorów: `tools/voice_scripts.py` → `tools/voice/lines.json`.
- **Kronika wydziału** z odznakami, **akt oskarżenia do druku/PDF** i **pieczęcie Archiwisty** (litera w jednym dowodzie każdej sprawy).

## Tablica śledcza (2.11)
- **Karty z treścią:** przypięty dowód pokazuje zdjęcie i początek treści (tabele, logi, cytaty, adnotacje), przycisk „Rozwiń” otwiera go w całości, „Akta” otwiera dokument. „Rozwiń wszystko / Zwiń wszystko” działa na całej tablicy.
- **Fragmenty:** w otwartym dokumencie przy każdym akapicie, wierszu tabeli, linii logu, cytacie i adnotacji jest pinezka — przypina tylko ten fragment jako karteczkę z podanym źródłem. Pinezek nie ma w teczce tajnych akt na wspólnym ekranie.
- **Porządek:** nowe karty trafiają w wolne miejsce, „Uporządkuj” układa całą tablicę bez nakładania, notatki można edytować, nitki łączą pinezki. Stare zapisy są jednorazowo porządkowane, jeśli karty by się nakładały.
- Działa automatycznie w każdej sprawie — treść bierze z pola `body` dowodu, więc nowe sprawy nie wymagają żadnych dodatkowych danych.

## Aktualizacje
Gra sama sprawdza nową wersję przy każdym otwarciu, powrocie z tła i co 15 minut, po czym przeładowuje się w tym samym miejscu. Numer wersji: Ustawienia → „Wersja gry” (przycisk „Sprawdź”).

## Publikacja na GitHub Pages
1. Wgraj zawartość tego katalogu do głównego katalogu repozytorium (gałąź `main`).
2. Settings → Pages → Deploy from a branch → `main` / `(root)`.
3. Otwórz adres `https://<użytkownik>.github.io/<repozytorium>/` i dodaj grę do ekranu głównego:
   - **iPhone/iPad (Safari):** Udostępnij → „Do ekranu początkowego”.
   - **Android (Chrome):** menu ⋮ → „Zainstaluj aplikację”.
   - **Windows/macOS (Chrome/Edge):** ikona instalacji w pasku adresu.

Ścieżki są względne — gra działa także w podkatalogu repozytorium. Plik `.nojekyll` wyłącza przetwarzanie Jekyll.

## Lokalnie
```bash
python3 -m http.server 8000   # potem http://localhost:8000
```
Nie otwieraj przez `file://` (Service Worker wymaga HTTP/HTTPS).

## Nowe mechaniki (2.12)
- **Macierz alibi (`input: "grid"` w zagadce):** tabela osoba × chwila, w każdej komórce lista miejsc. Walidator rozwiązuje ją wyczerpująco: warunki logiczne (`is`, `not`, `in`, `same`, `diff`, `forbid`, `exactly`) muszą dawać dokładnie jedno rozwiązanie zgodne z `answers[0]`, każdy ma `src` (dowód z listy `requires`) i `why`.
- **Pytanie wielokrotnego wyboru w raporcie (`type: "multi"`):** zaznaczacie wszystkie właściwe osoby; błędny wybór odejmuje punkty za trafny (`points × max(0, trafione − błędne) / liczba poprawnych`).
- **Dwa akty przez bramkowanie:** miejsca i pytania zależne od wykazanych kłamstw (`requires: {all: ["lie:…"]}`) otwierają się dopiero po przełomach, więc sprawa 004 rozkręca się w drugiej połowie.
- Sprawa 004 „Martwy kanał” jest gotowa (grafiki, głosy, filmy i ambient dodane). Prompty użyte do mediów: `docs/PROMPTY_GRAFIK_004.md`, `docs/PROMPTY_GLOSY_004.md`, `docs/PROMPTY_FILMY_DZWIEK_004.md` (generuje je `tools/prompts_004.py`).
- Plan rozwoju uniwersum, decyzje autora i zasady: `docs/ROZWOJ_UNIWERSUM.md` (czytać przed pracą nad kolejnymi sprawami).

## Nowe mechaniki (2.15)
- **Terminal baz danych (zakładka „Bazy”, `case.db`):** ogólnopolska baza wspólna dla całego uniwersum — `data/baza/index.json` wylicza pliki: tło (`tlo-*.json`, wygenerowane raz przez `tools/gen_db.py`, ziarno stałe — NIE generować ponownie po wydaniu sprawy z bazą) i rekordy spraw (`sprawa-NNN.json`, z `tools/bNNN_db.py`). Rejestry: `osoby` (PESEL), `pojazdy` (CEPiK), `firmy` (KRS), `ksiegi` (EKW). Wyszukiwanie dokładne jak w prawdziwym systemie: bez znaczenia są tylko wielkość liter i spacje na brzegach; nazwisko zwraca wszystkich o tym nazwisku, nazwisko + imię tylko pasujących; nazwy firm po całych słowach (skróty form prawnych typu „sp. z o.o.” są rozwijane). Ponad 30 wyników → „zawęźcie kryteria”.
- Widoczność rekordu: `from`/`to` względem `db.date` sprawy; `case: "NNN"` = widoczny tylko w tej sprawie i w innych dopiero po jej rozwiązaniu na urządzeniu; `neutral: true` = zawsze; `afterSolved` = dopiero po rozwiązaniu wskazanej sprawy.
- Dołączenie wydruku do akt kosztuje 1 ruch. `db.attach` mapuje rekordy na dowody sprawy (`dNN`, pole `db` w dowodzie — treść generuje aplikacja z rekordu) i opisuje ścieżki dojścia (`paths: [{q, from}]`). Inne rekordy trafiają do akt jako wydruki `db:<id>` (bez znaczenia dla bramek — nic nie zdradzają). W trybie z telefonami terminal jest też w każdej teczce (bez dołączania).
- Walidator: sumy kontrolne PESEL/NIP/KW/nr dowodu, unikalność, powiązania (małżonkowie, zarządy, właściciele), osiągalność dowodów z bazy, czy każde zapytanie ze ścieżki zwraca rekord i czy jego dane występują DOSŁOWNIE w dowodzie-źródle, imiennicy nie do rozróżnienia, oraz czy każdy identyfikator w tekstach sprawy (tablice, PESEL, KRS, NIP, KW, dowody) istnieje w bazie w tej samej formie (`db.ignore` na wyjątki, np. numer pociągu).
- **Okazywanie dowodów (zakładka „Okaż dowód” u osoby):** `shows: [{id, ev, a, requires?, claims?, gives?}]` i `showDefault: [...]` (odpowiedź na wszystko inne). 1 ruch. Token `show:<id>` do bramek i przełomów. Głosy: `<voiceDir>/<id>.mp3` i `<osoba>-show-<i>.mp3`.
- **Nowe uprawnienia i oględziny na zdjęciu (2.16):** `case.unlocks` (+ `unlockNote`) pokazuje ekran „Nowe uprawnienia wydziału”; katalog uprawnień `FEATURES` w `app.js`; `offline: {db: 'powód'}` wyłącza zakładkę z fabularnym wyjaśnieniem. `location.search = {aspect, spots: {spotId: [x, y, r]}}` zamienia listę punktów w oględziny zdjęcia (licznik, wskazanie po przybliżeniu ≥2×, pudło bez kosztu, trafienie 1 ruch). Walidator sprawdza położenia, nachodzenie obszarów i ciągłość odblokowanych uprawnień.
- Sprawa 005 „Pokój bez okien” jest gotowa (media dodane). Prompty: `docs/PROMPTY_GRAFIK_005.md`, `docs/PROMPTY_GLOSY_005.md`, `docs/PROMPTY_FILMY_DZWIEK_005.md` (`tools/prompts_005.py`); źródło: `tools/build_005.py` + `b005_*.py`.

## Struktura
- `index.html`, `styles.css`, `app.js` — aplikacja (bez zależności i bez budowania).
- `sw.js`, `manifest.webmanifest` — PWA i tryb offline. Przy każdej zmianie podnieś `VERSION` w `sw.js` i `app.js`.
- `cases/index.json` — katalog spraw; `cases/NNN.json` — treść sprawy (dane, nie kod). Sekcja `tableMode` opisuje, gdzie w trybie „Wspólny stół” leżą informacje z tajnych akt; `intro.modeRules` — zasady zależne od trybu.
- `assets/` — czcionki (wbudowane, offline), tekstury, ikony, okładki, grafiki, audio.
- `tools/validate.js` — walidator logiki spraw (referencje, osiągalność każdego dowodu, łamliwość kłamstw, brak odpowiedzi w treści zagadek, suma punktów).
- `tools/e2e.mjs` — pełne przejście sprawy przez interfejs w Chrome (Playwright) na telefonie, tablecie i komputerze.
- `tools/board_test.mjs` — test tablicy: karty z treścią, fragmenty, rozwijanie, układanie bez nakładania, migracja starego zapisu, prywatność tajnych akt (CASE, MODE, urządzenie jak w e2e).
- `tools/audit.mjs` — audyt techniczny: pliki offline, tryb offline, przycisk Wstecz, prywatność tajnych akt, błędne raporty, przepełnienia na 7 rozmiarach ekranu.
- `tools/gen_audio.py` — generator ambientu (bezszwowa pętla) i efektów dźwiękowych, normalizacja głośności (LUFS).
- `tools/cut_sheet.py` — cięcie plansz z grafikami na pojedyncze pliki.
- `tools/plans.py` — szkice miejsc zdarzenia (sekcja `plan` w plikach spraw).
- `tools/build_003.py` — źródło danych sprawy 003 (generuje `cases/003.json`).
- `tools/build_004.py` (+ `b004_evidence.py`, `b004_people.py`, `b004_rest.py`) — źródło danych sprawy 004; `tools/prompts_004.py` — generator promptów medialnych.

## Testy
```bash
node tools/validate.js
CASE=001 MODE=table node tools/e2e.mjs http://localhost:8000/ phone    # CASE: 001…005 (sprawa zapieczętowana wymaga kopii z ready:true); MODE: table | phones; urządzenie: phone | tablet | desktop
node tools/audit.mjs http://localhost:8000/ /tmp/state.json
CASE=001 MODE=table node tools/board_test.mjs http://localhost:8000/ phone
```

## Zapis
Postęp zapisuje się automatycznie na urządzeniu (localStorage). Ustawienia → Eksportuj/Importuj zapis pozwala przenieść grę na inne urządzenie.

Wszystkie postacie, miejsca i zdarzenia są fikcyjne.
