# ŚLAD — Archiwum spraw niewyjaśnionych

Kooperacyjna gra detektywistyczna dla 2–6 osób przy jednym ekranie (telefon, tablet, komputer). Instaluje się jak aplikacja (PWA) i po pierwszym uruchomieniu działa offline.

Wersja **2.1.0** — nowy silnik, nowa oprawa, sprawa 001 „Dom, który pamięta” przepisana od zera. Sprawy 002–009 są w przygotowaniu (widoczne w archiwum jako zapieczętowane).

## Tryby gry (wybór po otwarciu sprawy)
- **Wspólny stół** — jeden ekran (laptop, telewizor, tablet). Wszyscy widzą wszystko. Informacje, które w drugim trybie są tajnymi aktami, trzeba zdobyć w śledztwie (m.in. w miejscu „Centrala wydziału”). Najlepszy we dwoje.
- **Telewizor + telefony** — gra na wspólnym ekranie, a każdy gracz skanuje swój kod QR i ma tajne akta tylko w swoim telefonie. Dokument ujawnia się zespołowi, wpisując na wspólnym ekranie jego 4-znakowy kod z telefonu. Działa bez serwera — kod QR zawiera adres teczki. Gracz bez telefonu może zajrzeć do teczki na wspólnym ekranie (zabezpieczone pieczęcią).

**Tryb telewizora** (Ustawienia ⚙ albo przełącznik na ekranie wyboru trybu) powiększa tekst, karty i przyciski tak, by były czytelne z kanapy. Skaluje się do rozdzielczości: laptop, Full HD, 4K.

## Jak się gra
1. Przeszukujcie **miejsca** i przesłuchujcie **osoby**. Każdy ruch jest liczony (norma ruchów wpływa na wynik).
2. Świadkowie kłamią. W **protokole zeznań** podważajcie zeznania dowodami (konfrontacja). Nietrafiona konfrontacja kosztuje punkty.
3. **Zagadki** wymagają połączenia kilku dokumentów — odpowiedzi nie ma w pytaniu.
4. **Tablica** (korkowa, z czerwoną nitką), **oś czasu** i **notatki** pomagają poukładać fakty.
5. **Akt oskarżenia**: sprawca, narzędzie, godzina, motyw, tożsamość, przeszłość, kolejność zdarzeń + wskazanie dowodów. Wynik 0–100, ranga, epilog i decyzja zespołu.

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
- `tools/cut_sheet.py` — cięcie plansz z grafikami na pojedyncze pliki.

## Testy
```bash
node tools/validate.js
MODE=table node tools/e2e.mjs http://localhost:8000/ phone    # MODE: table | phones; urządzenie: phone | tablet | desktop
node tools/audit.mjs http://localhost:8000/ /tmp/state.json
```

## Zapis
Postęp zapisuje się automatycznie na urządzeniu (localStorage). Ustawienia → Eksportuj/Importuj zapis pozwala przenieść grę na inne urządzenie.

Wszystkie postacie, miejsca i zdarzenia są fikcyjne.
