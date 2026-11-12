#!/usr/bin/env python3
# Buduje cases/004.json z modułów b004_*.py
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from b004_evidence import evidence
from b004_people import people
import b004_rest as R

case = {
 'id': '004', 'title': 'Martwy kanał', 'subtitle': 'Syreny milczały. Ktoś skasował dowód.',
 'genre': 'Thriller techniczny', 'duration': '110–150 min', 'players': '2–6', 'difficulty': 'Wymagająca',
 'cover': 'assets/cases/004-cover.webp', 'par': 73,
 'intro': {
  'lead': 'Piątek, 27 listopada, 10:00. Centrum Zarządzania Kryzysowego w Rudzie. Za oknem mgła, na ścianie monitorów żadnego alarmu.',
  'brief': [
   'O 6:10 konserwator znalazł w stacji nadawczej „Kolonia” ciało Bogdana Lasoty, miejskiego administratora systemu ostrzegania. Wygląda na porażenie prądem przy rozdzielni.',
   'W nocy o 1:47 czujniki chloru w zakładzie Chemrud zażądały alarmu. Syreny w mieście nie zawyły. Do rana 23 osoby trafiły do szpitala z podrażnieniem dróg oddechowych, a z archiwum Centrum zniknął zapis tego alarmu.',
   'O 9:00 w urzędzie miała się zacząć kontrola NIK. Lasota figurował w kalendarzu jako uczestnik tego spotkania.',
   'Burmistrz wydał dwa polecenia: ustalić, co się stało na wzgórzu, i wyjaśnić, dlaczego system, za który miasto zapłaciło miliony, milczał. Pięć osób ma coś do ukrycia.'],
  'task': [
   'Kto zabił Bogdana Lasotę, jak i kiedy?',
   'Dlaczego syreny nie zawyły o 1:47?',
   'Kto jeszcze był w to zamieszany?',
   'Co jest nie tak z kanałem K3 i dlaczego zniknął zapis alarmu?'],
  'rules': [
   'Każde przeszukanie miejsca i każde pytanie zadane świadkowi to jeden ruch. Ruchów nie brakuje, ale najlepsze zespoły zamykają sprawę oszczędnie.',
   'Świadkowie kłamią, a w tej sprawie część z nich jest ze sobą powiązana. Gdy dowód przeczy zeznaniu, użyjcie konfrontacji. Nietrafiona konfrontacja kosztuje punkty.',
   'W tej sprawie oprócz sprawcy działali pomocnicy. Raport zapyta o to osobno i oceni każdy wniosek.',
   'Część miejsc jest zamknięta, dopóki nie wykażecie, że ktoś skłamał, albo nie otworzycie sejfu. Nie wszystko da się obejrzeć od razu.'],
  'modeRules': {
   'table': 'Wszystko widzicie razem. Część informacji zdobędziecie tylko w Centrali wydziału — zapytania do centrali też kosztują ruchy.',
   'phones': 'Każdy gracz ma w telefonie tajne akta, których nie widzi reszta. Od was zależy, kiedy i czy podzielicie się nimi z zespołem.'}},
 'people': people, 'locations': R.locations, 'evidence': evidence,
 'privateClues': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'],
 'puzzles': R.puzzles, 'tableMode': R.tableMode, 'breakthroughs': R.breakthroughs,
 'hintTrail': R.hintTrail, 'report': R.report, 'solution': R.solution, 'endings': R.endings,
}
out = os.path.join(os.path.dirname(__file__), '..', 'cases', '004.json')
json.dump(case, open(out, 'w'), ensure_ascii=False, indent=1)
print('zapisano', out, len(evidence), 'dowodów')
