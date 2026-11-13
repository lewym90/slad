#!/usr/bin/env python3
# Buduje cases/006.json z modułów b006_*.py (rekordy bazy: b006_db.py → data/baza/sprawa-006.json)
# Pola mediów dopisywane tylko wtedy, gdy pliki istnieją — sprawa może być budowana przed dostarczeniem grafik.
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from b006_evidence import evidence
from b006_people import people
import b006_rest as R

ROOT = os.path.join(os.path.dirname(__file__), '..')
ex = lambda p: os.path.exists(os.path.join(ROOT, p))

case = {
 'id': '006', 'title': 'Ostatni seans', 'subtitle': 'Film poszedł do końca. Kinooperator — nie.',
 'genre': 'Kryminał klasyczny', 'duration': '80–110 min', 'players': '1–6', 'difficulty': 'Wymagająca',
 'cover': 'assets/cases/006-cover.webp', 'par': 72,
 'intro': {
  'lead': 'Niedziela, 6 grudnia, 9:00. Kino „Zorza” w Łodzi, kabina projekcyjna nad balkonem. Na podłodze zarys kredą, w projektorze wciąż zawieszona taśma.',
  'brief': [
   'W sobotę wieczorem kino „Zorza” pożegnało się z widzami. Sto dwanaście osób obejrzało z taśmy 35 mm film, od którego w 1958 roku wszystko się zaczęło. Projekcję prowadził Leon Barcz, kinooperator od pięćdziesięciu dwóch lat.',
   'Film poszedł do końca bez jednej przerwy. Na pożegnanie w foyer pan Leon już nie zszedł. O 22:41 kierowniczka i technik znaleźli go martwego w kabinie zamkniętej na klucz, z raną głowy i stalową puszką na taśmę obok.',
   'Patrol uznał, że to mógł być wypadek. Prokurator ma wątpliwości. Macie kino, podwórze, pięć osób do przesłuchania i sąsiada, który twierdzi, że coś widział ze swojego okna.',
   'Jeśli wolicie notować na papierze, w ustawieniach, w części „Do wydruku”, czeka plan sprawy: osoby, miejsca i arkusze na oś czasu. To nieobowiązkowe.'],
  'task': [
   'Czy Leon Barcz zginął w wypadku, czy został zabity — a jeśli zabity, to przez kogo?',
   'Jak sprawca dostał się do kabiny i jak z niej wyszedł?',
   'Kto i kiedy zmienił projektor w czasie seansu?',
   'Dlaczego kinooperator musiał zginąć właśnie tego wieczoru?'],
  'rules': [
   'Każde przeszukanie, każde pytanie i każde okazanie dowodu to jeden ruch. Wyszukiwanie w bazach jest bezpłatne, dołączenie wydruku do akt to ruch.',
   'Nowość: oględziny na zdjęciu. W niektórych miejscach sami szukacie śladów na fotografii z oględzin. Przybliżcie zdjęcie i wskażcie ślad. Licznik podpowiada, ile ich jest. Pudło nic nie kosztuje.',
   'Nowość: rekonstrukcja dokumentu. Podarte kartki składacie w zakładce Analiza, przeciągając skrawki na miejsce.',
   'Uwaga: świadek może się po prostu mylić. Pomyłka to nie kłamstwo — kiedy ją wyjaśnicie, protokół oznaczy zeznanie jako sprostowane.'],
  'modeRules': {
   'table': 'Wszystko widzicie razem. Dane od operatorów, banku i firmy ochrony zdobędziecie w Centrali wydziału — każde zapytanie to ruch.',
   'phones': 'Każdy gracz ma w telefonie tajne akta i własny terminal baz danych. Oględziny na zdjęciu i rekonstrukcja dokumentu odbywają się na wspólnym ekranie.'}},
 'unlocks': ['look'],
 'unlockNote': {'text': 'Technicy przysyłają od dziś zdjęcia z oględzin w pełnej rozdzielczości. Zanim kogoś zapytacie, przyjrzyjcie się sami — najmniejszy szczegół na zdjęciu bywa ważniejszy niż godzina przesłuchania.', 'by': 'szef wydziału'},
 'people': people, 'locations': R.locations, 'evidence': evidence,
 'privateClues': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'],
 'puzzles': R.puzzles, 'tableMode': R.tableMode, 'breakthroughs': R.breakthroughs,
 'hintTrail': R.hintTrail, 'report': R.report, 'solution': R.solution, 'endings': R.endings, 'db': R.db,
}
# --- media (tylko istniejące pliki) ---
for k, p in [('art', 'assets/art/006-keyart.webp'), ('ambience', 'assets/audio/case-006.mp3'), ('introVideo', 'assets/video/006-intro.mp4')]:
    if ex(p): case[k] = p
if ex('assets/voice/006'): case['voiceDir'] = 'assets/voice/006'
if ex('assets/voice/006-brief.mp3'): case['voice'] = {'brief': 'assets/voice/006-brief.mp3'}
EVIMG = {'e08': 'assets/evidence/006-can.webp', 'e09': 'assets/evidence/006-photo.webp', 'e13': 'assets/evidence/006-posters.webp',
         'e16': 'assets/evidence/006-coat.webp', 'e21': 'assets/evidence/006-wedge.webp',
         'e04': 'assets/evidence/006-leon.webp', 'e20': 'assets/evidence/006-scraps.webp'}
for e in evidence:
    if e['id'] in EVIMG and ex(EVIMG[e['id']]): e['img'] = EVIMG[e['id']]
for pr in people:
    p = f"assets/people/006-{pr['id']}.webp"
    if ex(p): pr['img'] = p
for l in R.locations:
    p = f"assets/places/006-{l['id']}.webp"
    if ex(p): l['img'] = p
BT = {'b-change': 'change', 'b-clock': 'clock', 'b-student': 'student', 'b-letter': 'letter'}
for b in R.breakthroughs:
    v = f"assets/video/006-bt-{BT[b['id']]}.mp4"
    if ex(v): b['video'] = v
    im = {'b-change': 'assets/places/006-booth.webp', 'b-clock': 'assets/evidence/006-clock.webp', 'b-student': EVIMG['e09'], 'b-letter': 'assets/places/006-yard.webp'}[b['id']]
    if ex(im): b['img'] = im
vlp = os.path.join(os.path.dirname(__file__), 'voice', '006-lines.json')
if os.path.exists(vlp):
    vl = os.path.join(os.path.dirname(__file__), 'voice', 'lines.json')
    VL = json.load(open(vl)); NL = json.load(open(vlp))
    for k, v in NL.items():
        VL[k] = {'name': v['name'], 'lines': [{x: y for x, y in l.items() if x != 'n'} for l in v['lines']]}
    json.dump(VL, open(vl, 'w'), ensure_ascii=False, indent=1)
out = os.path.join(ROOT, 'cases', '006.json')
json.dump(case, open(out, 'w'), ensure_ascii=False, indent=1)
# katalog
ip = os.path.join(ROOT, 'cases', 'index.json'); IX = json.load(open(ip))
for c in IX['cases']:
    if c['id'] == '006':
        c.update({'title': case['title'], 'tagline': 'Kino „Zorza”, kabina nad balkonem', 'genre': case['genre'], 'duration': case['duration'], 'players': case['players'],
                  'difficulty': case['difficulty'], 'teaser': 'Ostatni seans w historii kina poszedł bez jednej przerwy. Na pożegnanie nie zszedł tylko kinooperator.'})
json.dump(IX, open(ip, 'w'), ensure_ascii=False, indent=1)
print('006:', len(evidence), 'dowodów,', len(people), 'osób,', len(R.locations), 'miejsc')
