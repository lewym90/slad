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
 'cover': 'assets/cases/005-cover.webp', 'par': 86,
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
 'people': people, 'locations': R.locations, 'evidence': evidence,
 'privateClues': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'],
 'puzzles': R.puzzles, 'tableMode': R.tableMode, 'breakthroughs': R.breakthroughs,
 'hintTrail': R.hintTrail, 'report': R.report, 'solution': R.solution, 'endings': R.endings, 'db': R.db,
}
out = os.path.join(os.path.dirname(__file__), '..', 'cases', '005.json')
json.dump(case, open(out, 'w'), ensure_ascii=False, indent=1)
print('005:', len(evidence), 'dowodów,', len(people), 'osób,', len(R.locations), 'miejsc')
