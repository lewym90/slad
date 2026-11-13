#!/usr/bin/env python3
# Buduje cases/005.json z modułów b005_*.py (rekordy bazy: b005_db.py → data/baza/sprawa-005.json)
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from b005_evidence import evidence
from b005_people import people
import b005_rest as R

case = {
 'id': '005', 'title': 'Pokój bez okien', 'subtitle': 'Zamknięty od środka. Pusty od rana.',
 'genre': 'Zagadka psychologiczna', 'duration': '100–140 min', 'players': '2–6', 'difficulty': 'Trudna',
 'cover': 'assets/cases/005-cover.webp', 'art': 'assets/art/005-keyart.webp', 'ambience': 'assets/audio/case-005.mp3', 'par': 86,
 'voiceDir': 'assets/voice/005', 'introVideo': 'assets/video/005-intro.mp4', 'voice': {'brief': 'assets/voice/005-brief.mp3'},
 'intro': {
  'lead': 'Piątek, 13 marca, 10:40. Hotel „Gryf” w Szczecinie, II piętro. Drzwi pokoju 214 stoją otworem, zasuwa jest przecięta. Pokój nie ma okien.',
  'brief': [
   'Dr Edward Szulc, 63-letni archiwista z Koszalina, miał o 9:00 przedstawić komisji ugodowej opinię o dokumencie, od którego zależy zwrot kamienicy wartej 38 milionów złotych.',
   'Według recepcji zameldował się w czwartek o 23:05. O 23:13 zamek zarejestrował zasunięcie zasuwy od środka. O 23:50 z jego skrzynki wyszedł mail: rezygnuje i prosi, żeby go nie szukać. Rano jego nazwiska nie było już na liście uczestników.',
   'O 9:47 technik przeciął zasuwę. Pokój był pusty. W walizce została insulina.',
   'Żona mówi, że bez insuliny mąż jest w niebezpieczeństwie. Prokurator chce raportu do wieczora. Macie hotel, sześć osób do przesłuchania i dostęp do ogólnopolskich baz danych.'],
  'task': [
   'Gdzie jest dr Edward Szulc?',
   'Kto zorganizował jego zniknięcie i kto podszył się pod niego w hotelu?',
   'Jak ktoś wyszedł z pokoju zamkniętego od środka?',
   'Dlaczego jego nazwisko zniknęło z listy uczestników?'],
  'rules': [
   'Każde przeszukanie, każde pytanie i każde okazanie dowodu to jeden ruch. Ruchów nie brakuje, ale najlepsze zespoły zamykają sprawę oszczędnie.',
   'Nowość: zakładka Bazy. Ogólnopolskie rejestry PESEL, CEPiK, KRS i EKW. Wyszukiwanie jest bezpłatne, ale dane trzeba wpisać dokładnie. Żeby użyć wyniku w śledztwie, dołączcie wydruk do akt (1 ruch).',
   'Nowość: Okaż dowód. Każdej osobie możecie pokazać dowód i zobaczyć jej reakcję. To nie konfrontacja — nie tracicie punktów, a jedno zdjęcie potrafi otworzyć nowy wątek.',
   'Świadkowie kłamią, czasem kilka razy z rzędu. Gdy dowód przeczy zeznaniu, użyjcie konfrontacji. Nietrafiona konfrontacja kosztuje punkty.'],
  'modeRules': {
   'table': 'Wszystko widzicie razem. Dane operatorów, taksówek i urzędu zdobędziecie w Centrali wydziału — każde zapytanie to ruch.',
   'phones': 'Każdy gracz ma w telefonie tajne akta i własny terminal baz danych. Szukajcie równolegle, a wydruki dołączajcie na wspólnym ekranie.'}},
 'unlocks': ['db', 'show'],
 'unlockNote': {'text': 'Od dziś wydział ma dostęp do ogólnopolskich rejestrów, a prokuratura zgodziła się, żebyście pokazywali świadkom dowody już na pierwszym przesłuchaniu. Tę sprawę rozwiążecie tylko wtedy, gdy zrobicie z tego użytek.', 'by': 'szef wydziału'},
 'people': people, 'locations': R.locations, 'evidence': evidence,
 'privateClues': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'],
 'puzzles': R.puzzles, 'tableMode': R.tableMode, 'breakthroughs': R.breakthroughs,
 'hintTrail': R.hintTrail, 'report': R.report, 'solution': R.solution, 'endings': R.endings, 'db': R.db,
}
# --- media ---
EVIMG = {'e14': 'assets/evidence/005-szulc-id.webp', 'e42': 'assets/evidence/005-szulc-feb.webp', 'e09': 'assets/evidence/005-suitcase.webp', 'e11': 'assets/evidence/005-wardrobe.webp',
         'e29': 'assets/evidence/005-m2.webp', 'e40': 'assets/evidence/005-ticket.webp', 'e12': 'assets/evidence/005-desk.webp', 'e22': 'assets/evidence/005-act.webp',
         'e35': 'assets/evidence/005-note.webp', 'e28': 'assets/evidence/005-keys.webp', 'e31': 'assets/evidence/005-card.webp'}
for e in evidence:
    if e['id'] in EVIMG: e['img'] = EVIMG[e['id']]
for pr in people: pr['img'] = f"assets/people/005-{pr['id']}.webp"
for l in R.locations: l['img'] = f"assets/places/005-{l['id']}.webp"
BT = {'b-beard': ('beard', EVIMG['e14']), 'b-door': ('door', EVIMG['e11']), 'b-pass': ('pass', EVIMG['e40']), 'b-ring': ('ring', 'assets/people/005-kraska.webp')}
for b in R.breakthroughs:
    n, im = BT[b['id']]; b['video'] = f'assets/video/005-bt-{n}.mp4'; b['img'] = im
vl = os.path.join(os.path.dirname(__file__), 'voice', 'lines.json')
VL = json.load(open(vl)); NL = json.load(open(os.path.join(os.path.dirname(__file__), 'voice', '005-lines.json')))
for k, v in NL.items():
    VL[k] = {'name': v['name'], 'lines': [{x: y for x, y in l.items() if x != 'n'} for l in v['lines']]}
json.dump(VL, open(vl, 'w'), ensure_ascii=False, indent=1)
out = os.path.join(os.path.dirname(__file__), '..', 'cases', '005.json')
json.dump(case, open(out, 'w'), ensure_ascii=False, indent=1)
print('005:', len(evidence), 'dowodów,', len(people), 'osób,', len(R.locations), 'miejsc')
