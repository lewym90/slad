# ŚLAD — Archiwum spraw niewyjaśnionych

Kooperacyjna gra detektywistyczna dla 2–6 osób przy jednym ekranie (telefon, tablet, komputer). Instaluje się jak aplikacja (PWA) i po pierwszym uruchomieniu działa offline.

Gotowe sprawy: 001 „Dom, który pamięta”, 002 „Ostatni pociąg”, 003 „Cisza w sanatorium”. Sprawy 004–009 są w przygotowaniu (widoczne w archiwum jako zapieczętowane). Aktualny numer wersji: Ustawienia → „Wersja gry”.

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

## Struktura
- `index.html`, `styles.css`, `app.js` — aplikacja (bez zależności i bez budowania).
- `sw.js`, `manifest.webmanifest` — PWA i tryb offline. Przy każdej zmianie podnieś `VERSION` w `sw.js` i `app.js`.
- `cases/index.json` — katalog spraw; `cases/NNN.json` — treść sprawy (dane, nie kod). Sekcja `tableMode` opisuje, gdzie w trybie „Wspólny stół” leżą informacje z tajnych akt; `intro.modeRules` — zasady zależne od trybu.
- `assets/` — czcionki (wbudowane, offline), tekstury, ikony, okładki, grafiki, audio.
- `tools/validate.js` — walidator logiki spraw (referencje, osiągalność każdego dowodu, łamliwość kłamstw, brak odpowiedzi w treści zagadek, suma punktów).
- `tools/e2e.mjs` — pełne przejście sprawy przez interfejs w Chrome (Playwright) na telefonie, tablecie i komputerze.
- `tools/audit.mjs` — audyt techniczny: pliki offline, tryb offline, przycisk Wstecz, prywatność tajnych akt, błędne raporty, przepełnienia na 7 rozmiarach ekranu.
- `tools/gen_audio.py` — generator ambientu (bezszwowa pętla) i efektów dźwiękowych, normalizacja głośności (LUFS).
- `tools/cut_sheet.py` — cięcie plansz z grafikami na pojedyncze pliki.
- `tools/plans.py` — szkice miejsc zdarzenia (sekcja `plan` w plikach spraw).
- `tools/build_003.py` — źródło danych sprawy 003 (generuje `cases/003.json`).

## Testy
```bash
node tools/validate.js
CASE=001 MODE=table node tools/e2e.mjs http://localhost:8000/ phone    # CASE: 001|002|003; MODE: table | phones; urządzenie: phone | tablet | desktop
node tools/audit.mjs http://localhost:8000/ /tmp/state.json
```

## Zapis
Postęp zapisuje się automatycznie na urządzeniu (localStorage). Ustawienia → Eksportuj/Importuj zapis pozwala przenieść grę na inne urządzenie.

Wszystkie postacie, miejsca i zdarzenia są fikcyjne.
