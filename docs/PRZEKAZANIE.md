# ŚLAD — przekazanie projektu (stan na 14.11.2026, 14:05, wersja 2.18.0)

Ten dokument pozwala kontynuować pracę **dokładnie od tego miejsca** na dowolnym koncie Claude. Bez spoilerów — rozwiązania spraw i ukryty wątek są w osobnym pliku `docs/PRZEKAZANIE_DLA_CLAUDE_SPOILERY.md`, którego **autor gry nie czyta** (sam o to prosi: „staram się wiedzieć jak najmniej”).

---

## 1. Pierwsza wiadomość na nowym koncie (do skopiowania przez autora)

```
Kontynuujemy projekt gry detektywistycznej ŚLAD. Repozytorium GitHub: lewym90/slad (gra: https://lewym90.github.io/slad/).
Podłącz repozytorium (add_repo z prawem zapisu), sklonuj je, a potem przeczytaj w całości:
1) docs/PRZEKAZANIE.md — zasady współpracy, stan prac i lista zadań,
2) docs/PRZEKAZANIE_DLA_CLAUDE_SPOILERY.md — tylko dla Ciebie, mi nie streszczaj i nie cytuj,
3) docs/ROZWOJ_UNIWERSUM.md — wszystkie decyzje projektowe,
4) README.md.
Pracuj dokładnie według tych dokumentów. Zacznij od krótkiego potwierdzenia (bez spoilerów), na czym skończyliśmy i co jest następne.
```

---

## 2. Kim jest autor i jak z nim pracować (obowiązuje zawsze)

- Autor pisze po polsku; odpowiedzi po polsku, zwięźle, często czyta z telefonu.
- **Żadnych spoilerów.** Autor gra w sprawy. Nie zdradzać fabuły, sprawców, rozwiązań, zarysów, opisów treści mediów. W raportach z pracy pisać ogólnie („poprawiłem daty w dokumentach 006”, a nie „faktura faksymile”).
- **Prompty mediów** podaje się w czacie jako bloki kodu do skopiowania, oznaczone **wyłącznie cyframi**, pogrupowane w sekcje **GRAFIKI / VIDEO / DŹWIĘK**. W każdym prompcie wpisana najwyższa jakość i rozdzielczość (grafiki ≥4K, najlepiej 6144×4096 lub 8K; wideo 4K; audio WAV 48 kHz 24-bit) — autor niczego nie zmienia, tylko kopiuje. Przy głosach postaci uprzedzić: „kopiuj przyciskiem, nie czytaj treści”.
- Gdy trzeba coś wygenerować ponownie — podawać **tylko** te prompty, które trzeba zrobić od nowa (nie całą listę; autora to zdezorientowało).
- Gdy autor pisze „nie przerywaj / nic nie rób, póki nie napiszę, że to już wszystko” — tylko potwierdzać odbiór i czekać na „to już wszystko”.
- Gdy autor prosi o omówienie — **najpierw omówić i dostać zgodę**, potem budować. Propozycje w formie numerowanej listy z rekomendacją; autor odpowiada np. „1. Zgoda, 2. …”.
- Każdy plik mediów od autora **audytować pod kątem zgodności z fabułą** (np. coś mokre, gdy nie powinno — dla gracza to dowód). Niezgodne → poprawić tekst gry albo dać nowy prompt.
- „Pilnuj wszystkiego jak oka w głowie”: logika i dedukcja bez luk, niespójności tylko celowe (kłamstwo, pomyłka świadka), walidator bez błędów, przejścia testowe na wszystkich urządzeniach.
- Push **bezpośrednio na `main`** (bez PR). Commit kończyć linijkami atrybucji wymaganymi przez aktualną sesję.
- Adres e-mail autora (z kontekstu konta) jest prywatny — nigdzie go nie wpisywać.
- Autor gra we dwoje z partnerką, czasem więcej osób; gra musi działać dla 1–6 graczy (jedna osoba tylko w trybie „Wspólny stół”).

---

## 3. Projekt w skrócie

- **Czysta aplikacja PWA** bez serwera: `index.html`, `app.js`, `styles.css`, `sw.js`, `manifest.webmanifest`, `cases/*.json`, `cases/index.json` (lista spraw, `ready`), `data/baza/*.json` (ogólnopolska fikcyjna baza: tło + rekordy spraw + `uniwersum.json`), `assets/` (art, cases, people, places, evidence, video, audio, voice, print, plan).
- Wersja w dwóch miejscach: `VERSION` w `app.js` i `sw.js` (obecnie **2.18.0**), `BUILD` w `app.js` (data). Każda zmiana plików gry → podbić wersję.
- Tryby: „Wspólny stół” (jeden ekran/TV, Centrala wydziału zamiast tajnych akt) i „Telefony” (każdy gracz ma tajne akta i terminal baz). Role graczy z mocami, poziomy trudności, tropy, przełomy (filmy), tablica śledcza, kronika wydziału, raport końcowy z punktami.
- Mechaniki odblokowywane kampanijnie (zostają na zawsze): bazy danych PESEL/CEPiK/KRS/EKW (od 005), okazywanie dowodów (od 005), oględziny na zdjęciu (od 006). Mechaniki per sprawa: podarty dokument, zeznania-pomyłki, materiały do druku (006), zegar w grze, mapa szlaków, dowód dźwiękowy (007).
- Szczegóły formatu danych: `README.md` (sekcje „Nowe mechaniki”) i walidator `tools/validate.js`.
- Tła bazy (`tools/gen_db.py`) **nie generować ponownie** — rekordy tła są stałe.

---

## 4. Narzędzia i polecenia (repo w `/home/claude/slad` albo gdzie sklonowano)

- Walidacja: `node tools/validate.js` (wszystkie gotowe sprawy) albo `node tools/validate.js cases/NNN.json`. Cel: **zero błędów i ostrzeżeń**.
- Budowa spraw skryptami (nie edytować JSON-ów ręcznie dla 003–007): `python3 tools/build_00N.py` (moduły `tools/b00N_*.py`; bazy: `python3 tools/b00N_db.py`). 001–002 nie mają skryptów — edycja bezpośrednio w `cases/001.json`, `cases/002.json`.
- Prompty: `python3 tools/prompts_00N.py` → `docs/PROMPTY_*_00N.md`, `tools/voice/00N-lines.json` (podział nagrań na części), `tools/voice/00N-media-order.json` / `00N-graphics-order.json` (kolejność plików).
- PDF-y do druku: `python3 tools/gen_print.py` → `assets/print/NNN.pdf` (dla spraw z `print` w `cases/index.json`).
- Przejścia testowe (Playwright): skopiować repo do `/tmp/run`, w kopii ustawić `ready: true` dla testowanej zapieczętowanej sprawy, uruchomić `cd /tmp/run && python3 -m http.server 8871` w tle, potem
  `CASE=NNN MODE=table|phones node tools/e2e.mjs http://localhost:8871/ phone|tablet|desktop` (zrzuty w `/home/claude/audit/e2e-NNN-urządzenie-tryb/`; Playwright: `/opt/npm-tools/node_modules/playwright/index.mjs`). Oczekiwane: `ERRORS none`, `missing evidence none`, komplet przełomów.
  Dla 007 bez grafik: w kopii testowej podstawić zastępcze obrazki `assets/places/007-dry.webp` i `007-shelter.webp` i dopisać je do `cases/007.json` (oględziny wymagają zdjęć).
- Pisownia: słownik LibreOffice `pl_PL.dic/.aff` + `spylls` (pip) — skrypt sprawdzający teksty spraw trzeba w razie potrzeby odtworzyć.
- Git: `git fetch -q && git rebase -q origin/main && git push -q origin HEAD:main`.
- Pułapki środowiska: z powłoki nie ma dostępu do github.io (allowlista; raw.githubusercontent.com działa); procesy w tle giną kilka minut po odpowiedzi — długie testy uruchamiać na pierwszym planie; nigdy `rm -rf` z globami (blokada bezpieczeństwa) — używać nowych katalogów.

---

## 5. Potok mediów (jak dotąd — autor generuje, Claude obrabia)

Autor generuje grafiki w **ChatGPT**, filmy i dźwięki w **Groku**, a potem powiększa grafiki ×4 w programie **Upscayl** (na swoim komputerze) i przysyła paczki ZIP.

1. **Portrety** (plansza 3×2): `python3 tools/cut_sheet.py plansza.png 3 2 assets/people/NNN-a.webp … --ratio 4:5`.
2. **Dowody** (plansza 3×2, kwadraty): `cut_sheet.py … 3 2 assets/evidence/…`.
3. **Miejsca**: pojedyncze 3:2 → `assets/places/NNN-id.webp` (po Upscaylu szer. ok. 3072 px). Dla oględzin na zdjęciu po wstawieniu grafiki **ustawić pozycje śladów** (`search.spots: {spotId: [x, y, r]}` w module `b00N_rest.py`; względne współrzędne), sprawdzić podglądem, że każdy ślad trafia w wyraźny przedmiot.
4. **Filmy**: ffmpeg → `assets/video/NNN-intro.mp4` (pętla ping-pong, bez dźwięku, libx264 veryfast crf 20) i `NNN-bt-*.mp4` (przełomy), plakaty `.webp` z pierwszej klatki.
5. **Dźwięk tła**: pętla z przenikaniem 4 s (osobne pliki głowa/ciało, `acrossfade`), `loudnorm I=-28 TP=-6` + `alimiter 0.35` (średnio ok. −29 dB jak w 005) → `assets/audio/case-NNN.mp3` (007 ma też `case-007-storm.mp3` — tło po śnieżycy).
6. **Głosy**: `python3 tools/cut_voices.py NNN katalog_z_wav` — tnie po ciszy (`silencedetect -45 dB, d=2`), `loudnorm I=-17`, mp3 112k → `assets/voice/NNN/<id>.mp3` (identyfikatory: pytania, odpowiedzi po konfrontacji, reakcje `show`, `<osoba>-deflect-i`, `<osoba>-show-i`); narrator → `assets/voice/NNN-brief.mp3`. Liczba kwestii musi się zgadzać z `tools/voice/NNN-lines.json` (nagrania podzielone na części po maks. 5 kwestii, bo generator gubił kwestie w długich plikach). Walidator porównuje teksty z nagraniami (bez interpunkcji).
7. **Powiększone grafiki**: `python3 tools/import_upscaled.py paczka.zip` (podgląd `/tmp/up-sheet.jpg`, kontrola skali i kompozycji), potem `--apply`.
8. Przebudować sprawę (`build_00N.py` dopisuje pola mediów tylko dla istniejących plików), dopisać pliki sprawy do precache w `sw.js`, walidacja, przejścia testowe, `ready: true` w `cases/index.json`, PDF druku, podbicie wersji, commit, push.

**Ustalenia o automatyzacji generowania (14.11.2026):**
- Wtyczka **Krea** (jest podłączona, ma Nano Banana Pro 4K, Veo 3.1, Kling 4, ElevenLabs, Topaz) — **odrzucona przez autora jako za droga** (konto darmowe, 44 jednostki; grafika 4K ≈ 220 j., film Veo 8 s ≈ 1185 j. Full HD / 2370 j. 4K, kwestia głosowa ≈ 10 j.; cała sprawa 10–17 tys. j. ≈ plan Pro 35 $/mies.).
- Higgsfield (podłączony, wymaga ponownego logowania) — też drożej. Wtyczek do ChatGPT i Groka **nie ma**; ich API jest płatne osobno i niedostępne ze środowiska Claude.
- **Plan uzgodniony do sprawdzenia:** Claude sam obsługuje ChatGPT (grafiki) i Groka (filmy, dźwięki) w przeglądarce autora (Claude in Chrome albo wbudowana przeglądarka aplikacji Claude na komputerze — preferowana w ustawieniach: wbudowana), na kontach autora, w ramach jego abonamentów — ta sama jakość. Warunki: autor przy komputerze, zalogowany w obu serwisach (hasła wpisuje sam), aplikacja Claude z udostępnionym folderem Pobrane (pliki zabierane przez most urządzenia), jednorazowa zgoda autora na pobieranie wygenerowanych plików („Pobieraj wszystkie pliki wygenerowane dla gry”); CAPTCHA klika autor. Zacząć od **jednej grafiki 007 jako testu jakości**. Spróbować też przejąć powiększanie (Upscayl na komputerze autora przez sterowanie komputerem albo Real-ESRGAN w środowisku Claude).
- Do czasu testu obowiązuje dotychczasowy tryb: prompty w czacie → autor generuje → przysyła.

---

## 6. Stan prac (14.11.2026)

| Sprawa | Stan |
|---|---|
| 001 „Dom, który pamięta” | gotowa, otwarta |
| 002 „Ostatni pociąg” | gotowa |
| 003 „Cisza w sanatorium” | gotowa |
| 004 „Martwy kanał” | gotowa |
| 005 „Pokój bez okien” | gotowa (debiut baz danych i okazywania dowodów) |
| 006 „Ostatni seans” | gotowa (oględziny na zdjęciu, podarty list, świadek-pomyłka, PDF do druku), wszystkie grafiki po Upscaylu |
| 007 „Biała cisza” | **zbudowana i przetestowana, zapieczętowana — czeka na media** |
| 008 „Cień w galerii” | w archiwum jako zapieczętowana, do zbudowania |
| 009 „Czarna skrzynka” | w archiwum jako zapieczętowana, do zbudowania |
| 010 „Palimpsest” | finał kampanii 1, okładka jest, do zaprojektowania |

Ostatnie wersje: 2.17.9 (pełny audyt: poprawki językowe, gra w pojedynkę przy wspólnym stole, czytelniejszy podarty list, porządki), 2.18.0 (silnik: zegar, mapa szlaków, dowód dźwiękowy, nowości sprawy; sprawa 007).

### Sprawa 007 — co jest, czego brak
- Dane: `tools/build_007.py` + `b007_evidence.py`, `b007_people.py`, `b007_rest.py`, `b007_db.py` (rekordy → `data/baza/sprawa-007.json`). 6 osób, 10 miejsc, 53 dowody, 2 zagadki, 4 przełomy, 3 zdarzenia zegara (12:00, 13:00 śnieżyca, 15:00), mapa 4 punktów.
- Testy: walidator bez błędów logiki (zostały tylko 2 błędy „brak zdjęcia” dla oględzin `dry` i `shelter` — znikną po wstawieniu grafik), przejścia testowe stół/telefony/komputer: komplet dowodów i przełomów, bez błędów aplikacji. Norma czasu: raport do 19:50 (stół +80 min).
- **Prompty mediów: `docs/PROMPTY_007.md`** (GRAFIKI 1–13, VIDEO 1–5, DŹWIĘK 1–30 — dokładnie te same, które autor dostał w czacie 14.11.2026). Kolejność i nazwy plików: `tools/voice/007-media-order.json`. Autor **jeszcze ich nie wygenerował**.
- Nagranie `assets/audio/007-call.mp3` jest **tymczasowe (syntetyczne)** — do zastąpienia nagraniem złożonym z dźwięków DŹWIĘK 3–6 (szczegóły montażu: plik ze spoilerami, §007).

---

## 7. Lista zadań (kolejność)

1. **Media 007**: test automatyzacji (ChatGPT/Grok w przeglądarce autora) albo czekanie na pliki od autora. Potem obróbka wg §5, w tym:
   - pocięcie plansz (portrety: adam, weronika, igor, natalia, hampel, kuznik; dowody: kolejność w `build_007.py` → `EVIMG`: ash, stove, frame, ladder, skins, body — patrz prompt GRAFIKI 2),
   - miejsca `assets/places/007-{office,dry,terrace,dining,room6,fork,shelter,rock,garage,notes}.webp`, grafika tytułowa `assets/art/007-keyart.webp`,
   - **pozycje śladów** dla oględzin `dry` i `shelter` (w `b007_rest.py`, teraz są wartości tymczasowe),
   - filmy `007-intro`, `007-bt-voice`, `007-bt-skis`, `007-bt-window`, `007-bt-cold`,
   - tła `case-007.mp3` i `case-007-storm.mp3`,
   - **montaż nagrania łączności** z DŹWIĘK 3–6 + syntetyczny sygnał cofania i trzaski radiowe, filtr radiowy, czasy znaczników zgodne z `tools/voice/007-call-marks.json` (lub poprawić znaczniki do nagrania), przebudowa (`build_007.py` liczy falę dźwięku),
   - głosy: `cut_voices.py 007 …` (części wg `tools/voice/007-lines.json`; kwestia Igora „Mam.” idzie do montażu nagrania, nie do gry),
   - audyt zgodności wszystkich plików z fabułą,
   - **strona z mapą w PDF-ie do druku** (`tools/gen_print.py` — obiecane autorowi, jeszcze niezrobione), `print` dla 007 w `cases/index.json`,
   - precache w `sw.js`, wersja 2.18.x, odpieczętowanie, testy, push.
2. **Sprawa 008 „Cień w galerii”** (60–90 min): sprawca znany od początku — trzeba to udowodnić (#29), nakazy prokuratora (#3), telefon podejrzanego (#6). Przed budową omówić z autorem szczegóły mechanik (bez fabuły), potem budowa, prompty.
3. **Sprawa 009 „Czarna skrzynka”** (ok. 2,5–3 h): 48 godzin zatrzymania (#21), presja i adwokat (#16), finał w sądzie (#27). Najpierw omówienie.
4. **Sprawa 010 „Palimpsest”** — finał kampanii 1 (4–5 h, akty, zapis postępu): wszystkie uprawnienia naraz, powroty postaci i miejsc, baza pokazuje skutki rozwiązanych spraw. Kandydaci na nowości (**do omówienia przed budową**): role w zespole i wspólne wnioski, decyzje nieodwracalne, powiadomienia dla ról, akty z raportami cząstkowymi i jednym końcowym.
5. Po finale: **planowanie kampanii 2 (011–020)**.

Zasady planowania kolejnych spraw: patrz `docs/ROZWOJ_UNIWERSUM.md` §0, §1 (lista pomysłów i decyzji), §8 (tempo nowości), §10 (1–6 graczy, ogólnopolska baza, druk), §12 (uprawnienia zostają na zawsze; od 005 każda sprawa ma `db` i `showDefault`).

---

## 8. Ostatnie rozmowy (dla pewności kontekstu)

- 14.11 rano: autor zlecił pełny audyt i poprawki → wersja 2.17.9.
- 14.11: omówienie 007 (zegar zamiast ruchów, mapa z pozycją zespołu, dowód dźwiękowy z analizą technika jako podpowiedzią, bazy przez radio za czas, 1–6 graczy) — autor: „Zgoda na wszystko. Działaj” → wersja 2.18.0 i prompty 007.
- 14.11 po południu: rozmowa o automatyzacji mediów (§5) — Krea odrzucona (koszt), plan: obsługa ChatGPT/Groka w przeglądarce autora, test przy komputerze.
- 14.11, 14:04: autor poprosił o ten dokument przekazania.
