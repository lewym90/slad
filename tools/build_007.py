#!/usr/bin/env python3
# Buduje cases/007.json z modułów b007_*.py (rekordy bazy: b007_db.py → data/baza/sprawa-007.json)
# Pola mediów dopisywane tylko wtedy, gdy pliki istnieją — sprawa może być budowana przed dostarczeniem grafik.
import json, sys, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from b007_evidence import evidence
from b007_people import people
import b007_rest as R

ROOT = os.path.join(os.path.dirname(__file__), '..')
ex = lambda p: os.path.exists(os.path.join(ROOT, p))

case = {
 'id': '007', 'title': 'Biała cisza', 'subtitle': 'Głos w radiu mówił, że wszystko gra.',
 'genre': 'Zimowa ekspedycja', 'duration': '100–140 min', 'players': '1–6', 'difficulty': 'Trudna',
 'cover': 'assets/cases/007-cover.webp', 'par': 60,
 'intro': {
  'lead': 'Sobota, 16 stycznia, 8:00. Schronisko „Hala Szronów” w Karkonoszach, 1220 m n.p.m. Wiatr przewiewa śnieg przez taras, a w jadalni nikt nie rusza śniadania.',
  'brief': [
   'Od wtorku w Karkonoszach trenowała wyprawa „Północ 2028”, która za rok chce zimą przejść Grenlandię. Cztery noce spędziła w starym kamiennym schronie na Przełęczy Mglistej, od 2019 roku zamkniętym dla turystów.',
   'W piątek po południu zespół zjechał na noc do schroniska. Na przełęczy został tylko łącznościowiec, Krystian Lis — miał przez dobę testować w mrozie radiostację i baterie. O 22:05 zgłosił się przez radio. Po północy radio w schronisku odezwało się jeszcze raz.',
   'O szóstej rano Krystian nie odpowiedział. O 7:10 kierownik wyprawy i ratownik GOPR znaleźli go martwego pod skałą z masztem antenowym, piętnaście metrów od schronu.',
   'Prokurator nie wierzy w nieszczęśliwy wypadek. Wszyscy, którzy byli w nocy w schronisku, zostali na miejscu. Macie mapę, ratownika do pomocy i dzień, który nie będzie na was czekał: od południa idzie śnieżyca.',
   'Jeśli wolicie notować na papierze, w ustawieniach, w części „Do wydruku”, czeka plan sprawy: osoby, miejsca i arkusze na oś czasu. To nieobowiązkowe.'],
  'task': [
   'Jak zginął Krystian Lis — wypadek czy zbrodnia? Jeśli zbrodnia: kto za nią stoi?',
   'Kiedy naprawdę został zaatakowany i kto nadał łączność po północy?',
   'Jak sprawca dotarł na przełęcz i wrócił na czas?',
   'Dlaczego Krystian musiał zginąć właśnie tej nocy?'],
  'rules': [
   'Nowość: zegar. Zamiast ruchów liczy się czas. Pytanie i okazanie dowodu trwają 5 minut, przeszukanie punktu i konfrontacja — 10, dołączenie wydruku z bazy — 5. Zegar stoi, kiedy nic nie robicie.',
   'Nowość: mapa szlaków. Przeszukujecie tylko miejsca w punkcie mapy, w którym jesteście, i przesłuchujecie tylko osoby, które są obok. Przejście trwa tyle, ile pokazuje mapa.',
   'Nowość: dowód dźwiękowy. Nagranie łączności możecie odsłuchać i zaznaczyć dźwięki w tle. Pudło nic nie kosztuje, rozpoznany dźwięk to 5 minut.',
   'O ustalonych godzinach dzieją się rzeczy, na które nie macie wpływu. Niektórych śladów nie da się zbadać po czasie — ale sprawę zawsze da się rozwiązać.',
   'Wynik zależy od godziny, o której złożycie raport. Normę zobaczycie po stuknięciu zegara.'],
  'modeRules': {
   'table': 'Wszystko widzicie razem. Dane od meteorologów, operatora komunikatora i sponsora zdobędziecie w Centrali wydziału — każde zapytanie to 15 minut.',
   'phones': 'Każdy gracz ma w telefonie tajne akta i własny terminal baz danych. Mapa, zegar i analiza nagrania są na wspólnym ekranie.'}},
 'novelties': R.novelties,
 'clock': R.clock, 'map': R.MAP,
 'people': people, 'locations': R.locations, 'evidence': evidence,
 'privateClues': ['x1', 'x2', 'x3', 'x4', 'x5'],
 'puzzles': R.puzzles, 'tableMode': R.tableMode, 'breakthroughs': R.breakthroughs,
 'hintTrail': R.hintTrail, 'report': R.report, 'solution': R.solution, 'endings': R.endings, 'db': R.db,
}
# --- media (tylko istniejące pliki) ---
for k, p in [('art', 'assets/art/007-keyart.webp'), ('ambience', 'assets/audio/case-007.mp3'), ('ambienceStorm', 'assets/audio/case-007-storm.mp3'), ('introVideo', 'assets/video/007-intro.mp4')]:
    if ex(p): case[k] = p
if ex('assets/voice/007'): case['voiceDir'] = 'assets/voice/007'
if ex('assets/voice/007-brief.mp3'): case['voice'] = {'brief': 'assets/voice/007-brief.mp3'}
EVIMG = {'e13': 'assets/evidence/007-frame.webp', 'e12': 'assets/evidence/007-ash.webp', 'e19': 'assets/evidence/007-stove.webp',
         'e10': 'assets/evidence/007-skins.webp', 'e26': 'assets/evidence/007-body.webp', 'e27': 'assets/evidence/007-ladder.webp'}
for e in evidence:
    if e['id'] in EVIMG and ex(EVIMG[e['id']]): e['img'] = EVIMG[e['id']]
for pr in people:
    p = f"assets/people/007-{pr['id']}.webp"
    if ex(p): pr['img'] = p
for l in R.locations:
    p = f"assets/places/007-{l['id']}.webp"
    if ex(p): l['img'] = p
BT = {'b-voice': 'voice', 'b-skis': 'skis', 'b-window': 'window', 'b-cold': 'cold'}
BTIMG = {'b-voice': 'assets/places/007-office.webp', 'b-skis': 'assets/places/007-fork.webp', 'b-window': 'assets/places/007-shelter.webp', 'b-cold': 'assets/places/007-rock.webp'}
for b in R.breakthroughs:
    v = f"assets/video/007-bt-{BT[b['id']]}.mp4"
    if ex(v): b['video'] = v
    if ex(BTIMG[b['id']]): b['img'] = BTIMG[b['id']]
# nagranie łączności: fala dźwięku liczona z pliku
CALL = 'assets/audio/007-call.mp3'
MARKS = json.load(open(os.path.join(os.path.dirname(__file__), 'voice', '007-call-marks.json')))
for e in evidence:
    if e['id'] == 'e08' and ex(CALL):
        raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', os.path.join(ROOT, CALL), '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True).stdout
        import array; a = array.array('h'); a.frombytes(raw[:len(raw) // 2 * 2]); n = 240; step = max(1, len(a) // n)
        pk = [max((abs(x) for x in a[i * step:(i + 1) * step]), default=0) for i in range(n)]; top = max(pk) or 1
        e['audio'] = {'src': CALL, 'dur': round(len(a) / 8000, 2), 'peaks': [round(min(1, (v / top) ** 0.8), 3) for v in pk],
                      'options': MARKS['options'], 'marks': MARKS['marks']}
vlp = os.path.join(os.path.dirname(__file__), 'voice', '007-lines.json')
if os.path.exists(vlp):
    vl = os.path.join(os.path.dirname(__file__), 'voice', 'lines.json')
    VL = json.load(open(vl)); NL = json.load(open(vlp))
    for k, v in NL.items():
        VL[k] = {'name': v['name'], 'lines': [{x: y for x, y in l.items() if x != 'n'} for l in v['lines']]}
    json.dump(VL, open(vl, 'w'), ensure_ascii=False, indent=1)
json.dump(case, open(os.path.join(ROOT, 'cases', '007.json'), 'w'), ensure_ascii=False, indent=1)
ip = os.path.join(ROOT, 'cases', 'index.json'); IX = json.load(open(ip))
for c in IX['cases']:
    if c['id'] == '007':
        c.update({'title': case['title'], 'tagline': 'Zimowa ekspedycja', 'genre': case['genre'], 'duration': case['duration'], 'players': case['players'],
                  'difficulty': case['difficulty'], 'teaser': 'Karkonosze, zamknięty schron i nadajnik, który pracował po północy.'})
json.dump(IX, open(ip, 'w'), ensure_ascii=False, indent=1)
print('007:', len(evidence), 'dowodów,', len(people), 'osób,', len(R.locations), 'miejsc')
