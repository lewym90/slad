#!/usr/bin/env python3
"""Sprawa 003 „Cisza w sanatorium” — źródło danych. Uruchomienie zapisuje cases/003.json
(zachowuje istniejącą sekcję "plan", którą dopisuje tools/plans.py)."""
import json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
P = os.path.join(ROOT, 'cases', '003.json')
old = json.load(open(P, encoding='utf-8')) if os.path.exists(P) else {}

def img(kind, name):
    p = f'assets/{kind}/003-{name}.webp'
    return p if os.path.exists(os.path.join(ROOT, p)) else None

def ev(id, type, title, summary, body, **kw):
    d = {'id': id, 'type': type, 'title': title, 'summary': summary, 'body': body}
    d.update({k: v for k, v in kw.items() if v is not None})
    return d

D = '2026-11-20'; S = '2026-11-21'

evidence = [
 ev('e01', 'Raport', 'Raport z miejsca zdarzenia', 'Sobota, 8:05. Pierwsze ustalenia patrolu.', [
   {'kv': [['Miejsce', 'Sanatorium „Jodła”, Jaworzyn Zdrój — klatka gospodarcza wschodniego skrzydła, parter'],
           ['Zgłoszenie', 'sobota 21.11, 7:41, Zenon Kubik (stróż obiektu), telefon komórkowy'],
           ['Przyjazd patrolu', '8:05'], ['Zmarły', 'dr Adam Wilk, 71 l., były dyrektor sanatorium']]},
   'Budynek jest zamknięty od 2018 roku. Właściciel: gmina Jaworzyn. Teren pilnuje stróż mieszkający w stróżówce przy bramie. Adam Wilk mieszkał z córką w willi przylegającej do parku sanatorium od wschodu.',
   'W nocy z piątku na sobotę padał śnieg. Technik zabezpieczył ślady wokół budynku, zanim ktokolwiek po nich przeszedł.',
   {'note': 'Stróż zgłosił, że o 7:35, na porannym obchodzie, zastał uchylone boczne drzwi klatki gospodarczej, a w środku ciało.'}],
   start=True, time=[[f'{S} 07:41', 'Zenon Kubik zgłasza znalezienie ciała', 'Raport']]),
 ev('e02', 'Opinia', 'Wstępna opinia lekarza', 'Oględziny o 9:10, przed przewiezieniem ciała.', [
   {'kv': [['Obrażenia', 'liczne złamania kończyn i miednicy, uraz czaszkowo-mózgowy'],
           ['Mechanizm', 'upadek z dużej wysokości'], ['Czas zgonu', 'piątek 23:00 – sobota 1:00 (wstępnie)']]},
   'Zgon nastąpił na miejscu, w chwili upadku. Ciała nie przemieszczano.',
   {'note': 'Prawa dłoń zaciśnięta. Lekarz zostawia zawartość dłoni technikowi.'}], start=True),
 ev('e03', 'Plan', 'Plan wschodniego skrzydła (2018)', 'Inwentaryzacja gminy przy zamknięciu sanatorium.', [
   {'h': 'Skrzydło wschodnie — inwentaryzacja, wrzesień 2018'},
   {'log': ['Parter      ±0,00   kuchnia, magazyny', 'I piętro    +4,10   pokoje kuracjuszy', 'II piętro   +8,20   pokoje kuracjuszy, sale 1–8', 'Poddasze            nieużytkowe, bez dostępu']},
   'Klatka gospodarcza na końcu skrzydła: od parteru do II piętra. Boczne drzwi z klatki prowadzą na zewnątrz, od strony parku.',
   {'note': 'Szczyt skrzydła od strony doliny: trzy rzędy okien pokoi (parter, I i II piętro), a nad nimi małe okienko poddasza.'}], start=True),
 ev('e04', 'Nagranie', 'Zwiastun kanału „Zapomniane”', 'Opublikowany w piątek o 18:00.', [
   {'kv': [['Kanał', '„Zapomniane” — Kamil Duda'], ['Tytuł', '„PIĘTRO, KTÓREGO NIE MA — Sanatorium Jodła, cz. 1”'], ['Wyświetlenia do rana', '142 tys.']]},
   {'quote': 'Znaleźliśmy pomieszczenie, którego nie ma na żadnym planie. Jutro o 20:00 pokażemy, co dyrektor trzymał w szafie.', 'by': 'opis filmu'},
   'Kadr końcowy: żelazne drzwi z wizjerem w świetle lampy. Tabliczka na drzwiach zamazana.'],
   start=True, time=[[f'{D} 18:00', 'Publikacja zwiastuna „Piętro, którego nie ma”', 'YouTube']]),
 ev('e05', 'Notatka', 'Notatka dzielnicowego: światło w sanatorium', 'Rozmowa z Haliną Mrozek, czwartek i sobota.', [
   'Czwartek 19.11. Pani Halina Mrozek (77 l.) mieszka po drugiej stronie doliny; jej okna wychodzą na szczyt wschodniego skrzydła sanatorium.',
   {'quote': 'Od niedzieli co noc się tam pali, do pierwszej, drugiej. Szczyt ma cztery rzędy okien. Świeci się w najwyższym — w tym małym okienku pod samym dachem. Jak sanatorium działało, czasem się tam paliło po nocach. Potem zamknęli i osiem lat było ciemno.', 'by': 'Halina Mrozek'},
   'Dopisek, sobota 8:50, telefonicznie:',
   {'quote': 'W piątek zgasło nagle o 23:52 — patrzyłam na zegar. Zaraz potem jakieś małe światełko schodziło niżej, w oknach klatki, i znikło.', 'by': 'Halina Mrozek'}],
   start=True, time=[[f'{D} 23:52', 'Światło w najwyższym okienku gaśnie nagle', 'Halina Mrozek']]),
 ev('e06', 'Oględziny', 'Ciało u podnóża klatki', 'Adam Wilk, parter klatki gospodarczej.', [
   'Adam Wilk leży na wznak na posadzce parteru, u podnóża duszy klatki — w miejscu, nad którym schody okrążają otwartą przestrzeń. Puchowa kurtka, kalosze w rozmiarze 43, rękawiczki w kieszeni.',
   'W kieszeni kurtki telefon z włączoną latarką (bateria wyczerpana) i stary klucz z przywieszką „Klatka gosp.”. Na kurtce i we włosach zardzewiałe okruchy drutu.']),
 ev('e07', 'Przedmiot', 'Guzik z dłoni ofiary', 'Wyrwany z czyjegoś ubrania.', [
   'W zaciśniętej prawej dłoni — mosiężny guzik o średnicy 2 cm, z wytłoczonym liściem dębu. W uszku guzika zostały wyrwane nitki z zielonej wełny.',
   {'note': 'Ubranie Adama Wilka nie ma takich guzików.'}]),
 ev('e08', 'Oględziny', 'Ślady na śniegu', 'Pomiary technika, sobota 8:20.', [
   'Przed bocznymi drzwiami klatki gospodarczej zbiegają się ślady. Technik zmierzył, ile świeżego śniegu nasypało się do wnętrza każdego odcisku:',
   {'log': ['A  od furtki w parkanie willi Wilków do drzwi    kalosze ok. 43, gładkie     3,5 cm   brak powrotu',
            'B  od drzwi do furtki przy bramie i drogą do wsi  buty sportowe ok. 42        4,5 cm',
            'C  od stróżówki do drzwi                          filcowe buty ok. 44, łata   2 cm',
            'D  od drzwi do stróżówki                          te same filcowe buty        1 cm',
            'E  stróżówka → drzwi → stróżówka                  te same filcowe buty        0 cm (świeże)']},
   {'note': 'Łata na prawej pięcie filcowych butów odciska się wyraźnie. Innych śladów na terenie nie ma.'}]),
 ev('e09', 'Obserwacja', 'Siatka w duszy klatki', 'Rozdarta od góry.', [
   'Patrząc z parteru w górę duszy klatki: na wysokości stropu II piętra rozpięta jest stalowa siatka zabezpieczająca. Pośrodku jest rozdarta, a druty wygięte w dół.',
   'Nad siatką światło latarki ginie w ciemności.',
   {'note': 'Ktoś spadł na siatkę z góry i przerwał ją.'}]),
 ev('e10', 'Obserwacja', 'Boczne drzwi klatki', 'Otwarte kluczem.', [
   'Zamek bez śladów włamania — drzwi otwierano kluczem. Rano zastano je uchylone. Za progiem kałuże z roztopionego śniegu.']),
 ev('e11', 'Obserwacja', 'Podest II piętra', 'Według planu — najwyższy poziom klatki.', [
   'Podest II piętra kończy się gładką, szarą ścianą. Balustrada z 2018 roku, wysokość 110 cm. Kurz na poręczy nienaruszony.',
   {'note': 'Z tego podestu nikt tej nocy nie spadał.'}]),
 ev('e12', 'Obserwacja', 'Tablica z kluczami w stróżówce', 'Brakuje jednego klucza.', [
   'Na tablicy w sieni stróżówki brak drugiego klucza do bocznych drzwi klatki gospodarczej. Pierwszy Zenon Kubik nosi przy sobie.']),
 ev('e13', 'Przedmiot', 'Filcowe buty stróża', 'Pokazał je dobrowolnie.', [
   'Filcowe buty z gumową podeszwą, rozmiar 44. Na prawej pięcie naklejona łata z dętki. Podeszwy jeszcze wilgotne.',
   {'quote': 'Chodzę w nich od lat. Innych zimowych butów nie mam.', 'by': 'Zenon Kubik'}]),
 ev('e14', 'Obserwacja', 'Ściana na końcu podestu', 'To nie jest ściana.', [
   'Szara „ściana” na końcu podestu II piętra to płyta pilśniowa pomalowana na kolor tynku, przykręcona czterema wkrętami. Za nią — zamurowanie z cegieł z wybitym otworem i świeżym gruzem. Za otworem strome schody prowadzą w górę.',
   {'note': 'Na krawędziach cegieł ślady łomu.'}]),
 ev('e15', 'Oględziny', 'Izolatorium na poddaszu', 'Sala, której nie ma na planie.', [
   'Długa sala pod dachem: osiem żelaznych łóżek ze skórzanymi pasami, stojak na kroplówki, stalowa szafa lekarska. Małe okienko w szczycie budynku wychodzi na dolinę.',
   'Szafa otwarta. Na środkowej półce prostokąt bez kurzu, ok. 30 × 22 cm — niedawno coś stąd zabrano.',
   'Na podłodze przewrócona lampa LED na statywie, z rozbitym kloszem.']),
 ev('e16', 'Przedmiot', 'Kamera na statywie', 'Nagrywała całą noc, klatka po klatce.', [
   {'kv': [['Tryb', 'poklatkowy (timelapse), kadr na szafę'], ['Pierwsza klatka', 'piątek 20.11, 20:14:00'], ['Interwał', '30 sekund'], ['Klatek na karcie', '1 001 — potem wyczerpała się bateria']]},
   'Technik przegląda miniatury. Na początku nagrania przy szafie widać dwie osoby: mężczyznę i kobietę. Potem długo nikogo. Później przy szafie znów jedna postać w ciemnej kurtce — przez wiele klatek przegląda papiery. Od pewnego momentu wszystkie klatki są czarne.',
   {'note': 'Miniatury są zbyt małe, by rozpoznać twarze. Pełną rozdzielczość technik może wyciągnąć tylko dla kilku wskazanych klatek.'}]),
 ev('e17', 'Oględziny', 'Podest pod izolatorium', 'Stara balustrada, kurz i ślady.', [
   'Podest przed salą: oryginalna balustrada z 1936 roku, wysokość 80 cm. Na poręczy świeże otarcie, kurz starty na odcinku pół metra. Pod podestem dusza klatki opada aż na parter.',
   'W kurzu na podeście odciski: gładkie kalosze ok. 43 oraz filcowe buty ok. 44 z łatą na prawej pięcie. Ślady się przenikają, kurz rozmazany jak po szamotaninie.']),
 ev('e18', 'Kadry', 'Klatki 0435–0437', 'Pełna rozdzielczość z karty kamery.', [
   {'h': 'Klatka 0435'}, 'Starszy mężczyzna w puchowej kurtce przy otwartej szafie, w ręku gruby zeszyt. W drzwiach sali, na skraju kadru, ramię drugiej osoby.',
   {'h': 'Klatka 0436'}, 'Obraz rozmazany, lampa na statywie przechyla się. Na pierwszym planie rękaw ciemnego płaszcza z okrągłymi metalowymi guzikami; dłoń zaciśnięta na puchowej kurtce.',
   {'h': 'Klatka 0437'}, 'Czarny kadr.'],
   time=[[f'{D} 23:51', 'Kamera: szamotanina przy szafie w izolatorium (klatki 0435–0436)', 'Kamera (ustalone)']], wide=True),
 ev('e19', 'Przedmiot', 'Płaszcz z szafy stróża', 'Zielona wełna, mosiężne guziki.', [
   'Zielony płaszcz leśnika z mosiężnymi guzikami z liściem dębu. Przy prawym mankiecie brakuje jednego guzika — wyrwano go razem z kawałkiem materiału, zostały postrzępione nitki. Dół płaszcza wilgotny.']),
 ev('e20', 'Dokument', 'Dziennik izolatorium', 'Zawinięty w ręcznik na dnie szafy stróża.', [
   'Gruby zeszyt w płóciennej oprawie. Na okładce: „Izolatorium — kuracja insulinowa 2016–2018. A.W.”. Wpisy pismem Adama Wilka: inicjały pacjentów, dawki insuliny, godziny śpiączki.',
   {'log': ['2.03.2018  E.R., 34 l., depresja lekooporna', '  22:00  insulina 30 j.', '  23:10  śpiączka', '  01:40  przerwanie glukozą — bez reakcji', '  04:10  zgon']},
   {'quote': 'Przenieść na II, sala 7. Karta zleceń: 3 j. Dyżur — K.B.', 'by': 'dopisek pismem A. Wilka pod wpisem'},
   {'note': 'Śpiączki insulinowe jako leczenie psychiatryczne porzucono w Polsce kilkadziesiąt lat temu.'}]),
 ev('e21', 'Obserwacja', 'Gabinet Adama Wilka', 'Laptop i telefon.', [
   {'log': ['pt 18:41  zwiastun „Zapomniane” — odtworzony w całości', 'pt 19:10  telefon stacjonarny: połączenie wychodzące do K. Duda, 6 min', 'pt 22:31  zwiastun — odtworzony ponownie']},
   {'quote': 'Klucz? Kubik?!', 'by': 'kartka na biurku, pismo A. Wilka'}],
   time=[[f'{D} 18:41', 'Adam Wilk ogląda zwiastun', 'Laptop A. Wilka'], [f'{D} 19:10', 'Adam Wilk dzwoni do Kamila Dudy (6 min)', 'Telefon A. Wilka']]),
 ev('e22', 'Obserwacja', 'Przedpokój willi', 'Brak kaloszy i kurtki.', [
   'Na wieszaku brak puchowej kurtki doktora, na półce brak jego kaloszy. Drzwi na taras nie są zamknięte na klucz. Z tarasu ścieżka prowadzi przez park do furtki w parkanie sanatorium — pięć minut spacerem.']),
 ev('e23', 'Notatka', 'Właścicielka pensjonatu', 'Bożena Nowacka, „Pod Jaworem”.', [
   {'quote': 'Pan Kamil wrócił za dziesięć jedenasta, cały w śniegu. Zrobiłam mu herbatę, siedział w jadalni do północy i coś montował na laptopie. Potem poszedł na górę. Schody u mnie skrzypią — słyszałabym, gdyby jeszcze wychodził.', 'by': 'Bożena Nowacka'},
   {'note': 'Pensjonat stoi w centrum wsi, ok. 25 minut pieszo od bramy sanatorium.'}],
   time=[[f'{D} 22:50', 'Kamil Duda wraca do pensjonatu', 'Bożena Nowacka']]),
 ev('e24', 'Fotografia', 'Zdjęcia z laptopa Kamila', 'Zrobione w czwartek wieczorem.', [
   'Seria zdjęć z czwartku 19.11, 21:40: stalowa szafa w sali z żelaznymi łóżkami. Na środkowej półce gruby zeszyt w płóciennej oprawie. Na okładce: „Izolatorium — kuracja insulinowa 2016–2018. A.W.”.']),
 ev('e25', 'Wydruk', 'Przelew z konta Kamila', 'Historia rachunku.', [
   {'kv': [['Data', 'sobota 14.11'], ['Kwota', '1 500 zł'], ['Odbiorca', 'Zenon Kubik'], ['Tytuł', '„klucz”']]}],
   time=[['2026-11-14 12:00', 'Kamil Duda przelewa stróżowi 1 500 zł („klucz”)', 'Bank']]),
 ev('e26', 'Dokument', 'Wyrok w sprawie Krystyny Bober', 'Sąd Rejonowy w Jaworzynie, 12.10.2018.', [
   'Krystyna Bober uznana winną nieumyślnego spowodowania śmierci pacjentki Ewy Rudnickiej z domu Kubik (34 l.) przez podanie w nocy 2/3 marca 2018 r. 30 jednostek insuliny zamiast zleconych 3 jednostek. Pacjentka leżała na II piętrze, w sali 7.',
   {'kv': [['Kara', '2 lata pozbawienia wolności w zawieszeniu na 4 lata'], ['Środek karny', 'zakaz wykonywania zawodu pielęgniarki na 5 lat'], ['Kluczowy dowód', 'karta zleceń podpisana przez dyr. A. Wilka: „insulina 3 j.”']]}],
   time=[['2018-03-03 04:10', 'Śmierć Ewy Rudnickiej w sanatorium „Jodła”', 'Wyrok']]),
 ev('e27', 'Przedmiot', 'Kurtka Kamila', 'Wojskowa, z mosiężnymi guzikami.', [
   'Zielona kurtka wojskowa z demobilu, mosiężne guziki z kotwicą. Wszystkie guziki na miejscu.']),
 # tajne akta
 ev('x1', 'Komunikat', 'Dane IMGW — opad śniegu', 'Stacja Jaworzyn, noc 20/21 listopada.', [
   {'log': ['do 22:10      bez opadu, −6 °C', '22:10–00:40   śnieg, natężenie równomierne: ok. 2 cm na godzinę', 'po 00:40      bez opadu']},
   {'note': 'Przyrost pokrywy: 5 cm. Wiatr słaby — śnieg nie był nawiewany.'}], private=True),
 ev('x2', 'Plan', 'Projekt sanatorium z 1936 roku', 'Z archiwum budowlanego.', [
   'Przekrój wschodniego skrzydła: parter, I piętro, II piętro, a nad nimi III piętro w mansardzie — „izolatorium, 8 łóżek”. Dostęp wyłącznie klatką gospodarczą. W szczycie od strony doliny: cztery rzędy okien.'], private=True),
 ev('x3', 'Akta osobowe', 'Kwestionariusz stróża', 'Kadry gminy Jaworzyn.', [
   {'kv': [['Zenon Kubik', 'ur. 1963'], ['Zatrudniony', 'marzec 2019, stróż obiektu „Jodła”'], ['Poprzednio', 'leśniczy, Nadleśnictwo Jaworzyn (do 2018)'], ['Stan cywilny', 'wdowiec']]},
   {'note': 'Adnotacja kadrowej: „Sam zgłosił się na to stanowisko, choć płaca jest niska. Zrezygnował dla niego z pracy w lesie.”'}], private=True),
 ev('x4', 'Opinia', 'Uzupełnienie opinii lekarza', 'Po wstępnej sekcji, sobota 13:00.', [
   {'kv': [['Wysokość upadku', '11–13 m (charakter złamań, energia uderzenia)']]},
   'Na obu ramionach świeże sińce od silnego chwytu palcami. Ktoś mocno trzymał ofiarę krótko przed upadkiem.'], private=True),
 ev('x5', 'Akt', 'Odpis aktu zgonu Ewy Rudnickiej', 'Urząd Stanu Cywilnego w Jaworzynie.', [
   {'kv': [['Zmarła', 'Ewa Rudnicka z domu Kubik'], ['Urodzona', '14.06.1983 w Jaworzynie'], ['Zmarła', '3.03.2018, sanatorium „Jodła”'], ['Imię ojca', 'Zenon'], ['Imię i nazwisko rodowe matki', 'Maria Górska']]}], private=True),
 ev('x6', 'Dokument', 'Zlecenie remontu z kwietnia 2018', 'Z archiwum gminy.', [
   'Zleceniodawca: dyrektor sanatorium dr Adam Wilk. Zakres: zamurowanie przejścia na poddasze na podeście II piętra klatki gospodarczej; nowa balustrada podestu II piętra; montaż stalowej siatki zabezpieczającej w duszy klatki na wysokości stropu II piętra.',
   {'quote': 'Poddasze nieużytkowe, zagrożenie wypadkiem.', 'by': 'uzasadnienie zlecenia'}], private=True,
   time=[['2018-04-16 08:00', 'Wilk zleca zamurowanie wejścia na poddasze', 'Archiwum gminy']]),
 # zeznania po konfrontacjach
 ev('t1', 'Zeznanie', 'Stróż: nocne wyjście', 'Po okazaniu śladów.', ['Zenon Kubik przyznaje, że w nocy poszedł do klatki gospodarczej, bo w najwyższym okienku zobaczył ruch przy lampie, a Kamil wyszedł już o 22:20. Twierdzi, że w środku nikogo nie widział i wrócił.'], testimony=True),
 ev('t2', 'Zeznanie', 'Stróż: klucz za pieniądze', 'Po okazaniu przelewu.', ['Zenon Kubik przyznaje, że za 1 500 zł dał Kamilowi Dudzie drugi klucz do bocznych drzwi.'], testimony=True),
 ev('t3', 'Zeznanie', 'Stróż: był w izolatorium', 'Po okazaniu śladów w kurzu.', ['Zenon Kubik przyznaje, że w czwartek, po wyjściu Kamila, wszedł na poddasze, widział łóżka z pasami i szafę.'], testimony=True),
 ev('t4', 'Zeznanie', 'Stróż: „Ewka była moją córką”', 'Po okazaniu aktu zgonu.', ['Zenon Kubik przyznaje, że Ewa Rudnicka była jego córką. Wziął pracę stróża w sanatorium, w którym zmarła.'], testimony=True),
 ev('t5', 'Zeznanie', 'Stróż: spotkał Wilka', 'Po okazaniu płaszcza i kadrów.', ['Zenon Kubik przyznaje, że w izolatorium zastał Adama Wilka i powiedział mu, kim jest. Dalszych wyjaśnień odmawia do czasu rozprawy.'], testimony=True),
 ev('t6', 'Zeznanie', 'Kamil: klucz od stróża', 'Po okazaniu przelewu.', ['Kamil Duda przyznaje, że do budynku wchodził kluczem kupionym od stróża za 1 500 zł.'], testimony=True),
 ev('t7', 'Zeznanie', 'Kamil: nie był sam', 'Po okazaniu miniatur z kamery.', ['Kamil Duda przyznaje, że w piątek była z nim Krystyna Bober — przyszła o 20:30 i wyszła przed 22:00. To ona powiedziała mu o izolatorium.'], testimony=True,
    time=[[f'{D} 20:30', 'Krystyna Bober przychodzi do sanatorium (do 22:00)', 'Kamil Duda']]),
 ev('t8', 'Zeznanie', 'Krystyna: piątkowy wieczór', 'Po konfrontacji.', ['Krystyna Bober przyznaje, że w piątek od 20:30 do 22:00 była z Kamilem w izolatorium i pokazała mu szafę. Wyszła przed śniegiem. Adama Wilka nie widziała.'], testimony=True,
    time=[[f'{D} 22:00', 'Krystyna Bober wychodzi z sanatorium (przed śniegiem)', 'Krystyna Bober']]),
 ev('t9', 'Zeznanie', 'Joanna: ojciec wyszedł', 'Po okazaniu śladów i przedpokoju.', ['Joanna Wilk przyznaje, że o 22:50 słyszała, jak ojciec wychodzi. Powiedział: „Muszę coś zabrać, zanim to pokażą”. Nie zatrzymała go.'], testimony=True,
    time=[[f'{D} 22:50', 'Adam Wilk wychodzi z willi', 'Joanna Wilk']]),
]

def Q(id, q, a, **kw):
    d = {'id': id, 'q': q, 'a': a}
    d.update({k: v for k, v in kw.items() if v is not None})
    d.setdefault('claims', [])
    return d
def ST(id, text, contradicts=None, response=None, gives=None, truth=None, **kw):
    d = {'id': id, 'text': text}
    if truth: d['truth'] = True
    if contradicts: d['contradicts'] = contradicts
    if response: d['response'] = response
    if gives: d['gives'] = gives
    d.update(kw)
    return d

people = [
 {'id': 'zenon', 'name': 'Zenon Kubik', 'role': 'Stróż sanatorium', 'revealRole': 'Stróż — ojciec Ewy Rudnickiej', 'revealOn': ['z-l5'], 'age': 63,
  'desc': 'Duży, z siwą brodą, w swetrze i filcowych butach. Mieszka w stróżówce przy bramie. Odpowiada krótko i patrzy w okno.',
  'deflect': ['Ja tu tylko pilnuję płotu.', 'Pytajcie gminę, nie mnie.', 'Nie wiem, o co wam chodzi.'],
  'questions': [
   Q('z-q1', 'Co pan robił w piątek wieczorem i w nocy?', 'O dziesiątej obszedłem teren, wszystko było zamknięte. Wróciłem do stróżówki, zjadłem, położyłem się. Rano o wpół do ósmej poszedłem na obchód. Boczne drzwi były uchylone, w środku leżał doktor.', claims=['z-l1'],
     time=[[f'{D} 22:00', 'Wieczorny obchód stróża (według niego ostatni tej nocy)', 'Zenon Kubik'], [f'{S} 07:35', 'Zenon Kubik znajduje ciało', 'Zenon Kubik']]),
   Q('z-q2', 'Czy w tym tygodniu wpuszczał pan kogoś do budynku?', 'Nie. Budynek jest zamknięty, klucze mam ja i gmina.', claims=['z-l2']),
   Q('z-q3', 'Czy w tym tygodniu widział pan nocą światło w budynku?', 'Nie. Stróżówka stoi przy bramie, okna mam na drogę.'),
   Q('z-q4', 'Po co pana zdaniem doktor Wilk przyszedł w nocy do sanatorium?', 'Pewnie po ten swój dziennik. Żeby go nikt nie zobaczył.'),
   Q('z-q5', 'Czy był pan kiedykolwiek wyżej niż na podeście II piętra klatki gospodarczej?', 'Wyżej? Wyżej nic nie ma. Wejście na poddasze zamurowali, zanim tu przyszedłem.', requires=['p-floor'], claims=['z-l4']),
   Q('z-q6', 'Czy znał pan Ewę Rudnicką?', 'Nie. Słyszałem, że ktoś tu umarł przed zamknięciem. Ludzie gadali.', requiresAny=['e26', 'x5', 'e20', 'kb-q3'], claims=['z-l5']),
  ],
  'statements': [
   ST('z-l1', 'Po obchodzie o 22:00 nie wychodził ze stróżówki aż do rana.', ['e08'],
      'Dobra. Koło wpół do dwunastej zobaczyłem, że w tym okienku na górze ktoś się rusza przy lampie. Chłopak wyszedł o dwadzieścia po dziesiątej, widziałem go przy bramie. Poszedłem. Drzwi były otwarte, w środku cicho. Nikogo nie widziałem. Postałem i wróciłem. Nie mówiłem, bo bym się musiał tłumaczyć, czemu nie zadzwoniłem.',
      ['t1'], reveals=['z-l6']),
   ST('z-l2', 'W tym tygodniu nikogo nie wpuszczał do budynku.', ['e25'],
      'Chłopak chciał nagrywać. Dał półtora tysiąca, dałem mu drugi klucz do bocznych drzwi. Budynek i tak stoi pusty.', ['t2']),
   ST('z-l4', 'Nigdy nie był wyżej niż na podeście II piętra.', ['e17'],
      'Byłem. W czwartek, jak chłopak poszedł. Chciałem zobaczyć, co tam znalazł. Łóżka z pasami. I tę szafę.', ['t3']),
   ST('z-l5', 'Nie znał Ewy Rudnickiej.', ['x5', 'st:kb-c1'],
      '(długo milczy) Ewka była moją córką. Po rozwodzie zostawiła nazwisko męża. Przyjechała tu się leczyć z depresji, a wróciła w trumnie. Powiedzieli, że pielęgniarka pomyliła dawkę. Wziąłem tę robotę, żeby… żeby być blisko. Tylko tyle.', ['t4']),
   ST('z-l6', 'W nocy w budynku nikogo nie spotkał.', ['e19', 'e18'],
      '(patrzy na guzik, potem na swoje ręce) Był tam. Stał przy szafie z jej… z tym zeszytem. Powiedziałem mu, kim jestem. Resztę powiem przed sądem.', ['t5']),
  ], 'img': img('people', 'zenon')},
 {'id': 'kamil', 'name': 'Kamil Duda', 'role': 'Autor kanału „Zapomniane”', 'age': 29,
  'desc': 'Szczupły, w wojskowej kurtce, z kamerą na szyi nawet na przesłuchaniu. Mówi szybko i ciągle sprawdza telefon.',
  'deflect': ['Ja tylko nagrywam opuszczone miejsca.', 'Mam to wszystko na nagraniach, sprawdźcie.'],
  'questions': [
   Q('k-q1', 'Od kiedy nagrywał pan w sanatorium?', 'Od niedzieli. Co noc po kilka godzin, do serii o opuszczonych szpitalach.', time=[['2026-11-15 20:00', 'Kamil Duda zaczyna nocne nagrania w sanatorium', 'Kamil Duda']]),
   Q('k-q2', 'Jak wchodził pan do zamkniętego budynku?', 'Boczne drzwi były otwarte. Ktoś musiał je kiedyś wyłamać.', claims=['k-l1']),
   Q('k-q3', 'O której wyszedł pan z budynku w piątek?', 'Około 22:20. Kamerę i lampę zostawiłem na całą noc.', time=[[f'{D} 22:20', 'Kamil Duda wychodzi z budynku', 'Kamil Duda']]),
   Q('k-q4', 'Czy w piątek był pan w budynku sam?', 'Tak. Zawsze nagrywam sam.', claims=['k-l2']),
   Q('k-q5', 'Co było w szafie w izolatorium?', 'Gruby zeszyt w płóciennej oprawie. Na okładce: „Izolatorium — kuracja insulinowa 2016–2018”. W czwartek zrobiłem zdjęcia, w sobotę miałem go pokazać. Nie ma go tam?', requires=['e15']),
   Q('k-q6', 'Czy komuś mówił pan, co jest w szafie?', 'Nikomu. W zwiastunie napisałem tylko o szafie — specjalnie, żeby nikt nie uprzedził premiery. Stróż nie wiedział nawet, którędy wchodzę na górę.'),
   Q('k-q8', 'Kto zasłonił przejście na podeście II piętra płytą?', 'Ja. W niedzielę wybiłem otwór łomem, a płytę pomalowałem i przykręciłem, żeby nikt mnie nie uprzedził przed premierą.', requires=['e14']),
   Q('k-q7', 'Czy rozmawiał pan z doktorem Wilkiem?', 'Tak. Zadzwonił w piątek koło siódmej wieczorem. Krzyczał, że mnie pozwie, jeśli pokażę choć jedną stronę. Rozłączyłem się.'),
  ],
  'statements': [
   ST('k-l1', 'Wchodził przez boczne drzwi, które były otwarte.', ['e25', 'e10'],
      'Zapłaciłem stróżowi półtora tysiąca za klucz. Nie chciałem, żeby miał przeze mnie kłopoty.', ['t6']),
   ST('k-l2', 'W piątek był w budynku sam.', ['e16'],
      'Była ze mną pani Krystyna Bober. To ona powiedziała mi o izolatorium i o szafie. Przyszła wpół do dziewiątej, wyszła przed dziesiątą, zanim zaczął padać śnieg. Nie chciałem jej w to mieszać — ona już raz przez nich straciła wszystko.', ['t7']),
  ], 'img': img('people', 'kamil')},
 {'id': 'krystyna', 'name': 'Krystyna Bober', 'role': 'Była pielęgniarka sanatorium', 'age': 58,
  'desc': 'Drobna, siwe włosy spięte gumką, ręce schowane w rękawach swetra. Odpowiada cicho i bardzo dokładnie.',
  'deflect': ['Osiem lat temu też nikt mnie nie słuchał.', 'Proszę mnie nie pytać o to, czego nie wiem.'],
  'questions': [
   Q('kb-q1', 'Czym się pani teraz zajmuje?', 'Pracuję w aptece w Jaworzynie, na zapleczu. Do pacjentów nie mam prawa wrócić.'),
   Q('kb-q2', 'Kiedy ostatnio była pani w sanatorium?', 'W marcu 2018 roku. Tej nocy, kiedy umarła pani Ewa.', claims=['kb-l1']),
   Q('kb-q3', 'Co wydarzyło się w nocy z 2 na 3 marca 2018 roku?', 'Umarła pani Ewa Rudnicka. Sąd uznał, że podałam jej trzydzieści jednostek insuliny zamiast trzech. Karta zleceń mówiła: trzy. Kartę wypisywał doktor Wilk.'),
   Q('kb-q4', 'Gdzie leżała pani Ewa Rudnicka tamtej nocy?', 'Według akt — na II piętrze, w sali 7. Znalazłam ją tam nad ranem, już nie żyła. O dziesiątej wieczorem, kiedy robiłam obchód, jej łóżko było puste.', requires=['kb-q3']),
   Q('kb-q5', 'Czy ktoś z rodziny pani Ewy przychodził na rozprawy?', 'Ojciec. Na każdą. Duży mężczyzna z siwą brodą, w zielonym płaszczu leśnika. Siedział z tyłu i nigdy się nie odezwał.', requires=['kb-q3'], claims=['kb-c1']),
   Q('kb-q6', 'Gdzie była pani w piątek po 22:00?', 'W domu. Sama. Nikt tego nie potwierdzi.'),
  ],
  'statements': [
   ST('kb-c1', 'Na każdej rozprawie siedział ojciec Ewy: duży mężczyzna z siwą brodą, w zielonym płaszczu leśnika.', truth=True),
   ST('kb-l1', 'Nie była w sanatorium od marca 2018 roku.', ['t7'],
      'Byłam. W piątek, od wpół do dziewiątej do dziesiątej. Zaprowadziłam chłopaka na poddasze i pokazałam szafę. Osiem lat czekałam, aż ktoś tam wejdzie. Wyszłam, zanim zaczął padać śnieg. Doktora nie widziałam.', ['t8']),
  ], 'img': img('people', 'krystyna')},
 {'id': 'joanna', 'name': 'Joanna Wilk', 'role': 'Córka zmarłego', 'age': 46,
  'desc': 'Wysoka, w czarnym swetrze, z kubkiem herbaty, której nie pije. Mówi spokojnie, ale co chwilę poprawia włosy.',
  'deflect': ['Mój ojciec nie żyje, a wy pytacie mnie o takie rzeczy?', 'Nie wiem. Nie rozmawialiśmy o pracy.'],
  'questions': [
   Q('j-q1', 'Co robił pani ojciec w piątek wieczorem?', 'Po kolacji zamknął się w gabinecie. O dziesiątej powiedział dobranoc i poszedł do sypialni. Rano jego łóżko było nietknięte.', claims=['j-l1']),
   Q('j-q2', 'Czy ojciec oglądał w piątek nagranie z sanatorium?', 'Tak. Wieczorem, w gabinecie. Zrobił się szary na twarzy. Potem do kogoś dzwonił i krzyczał.'),
   Q('j-q3', 'Czy ojciec na coś chorował?', 'Na serce. Brał leki. W śnieg nie powinien wychodzić nawet do furtki.'),
   Q('j-q4', 'Kto dziedziczy po ojcu?', 'Ja. Dom i kredyt pod jego hipotekę. Od lat żyliśmy na kredyt.'),
   Q('j-q5', 'Co pani robiła w piątek po 23:00?', 'Byłam w swoim pokoju na piętrze. Czytałam do pierwszej.'),
  ],
  'statements': [
   ST('j-l1', 'Ojciec poszedł spać o 22:00 i tej nocy nie wychodził z domu.', ['e08', 'e22', 'e21'],
      'Słyszałam, jak wychodził, za dziesięć jedenasta. Zapytałam z góry, dokąd idzie. Powiedział: „Muszę coś zabrać, zanim to pokażą”. Nie zeszłam. Byłam na niego zła — od wieczora nie chciał powiedzieć, co jest w tym filmie.', ['t9']),
  ], 'img': img('people', 'joanna')},
]
for p in people:
    if not p.get('img'): p.pop('img', None)

def SP(id, name, text, gives, requires=None, lockedText=None):
    d = {'id': id, 'name': name, 'text': text, 'gives': gives}
    if requires: d['requires'] = requires; d['lockedText'] = lockedText
    return d
LOCK_ATTIC = 'Według planu z 2018 roku nad II piętrem jest tylko nieużytkowe poddasze bez dostępu. Najpierw ustalcie, czy to prawda.'
locations = [
 {'id': 'stairwell', 'name': 'Klatka gospodarcza', 'kind': 'Miejsce znalezienia ciała', 'desc': 'Wąska klatka na końcu wschodniego skrzydła. Schody okrążają otwartą duszę. Od strony parku boczne drzwi.',
  'img': img('places', 'stairwell'), 'spots': [
   SP('sp-body', 'Ciało', 'Adam Wilk leży na posadzce parteru, u podnóża duszy klatki. Prawa dłoń zaciśnięta.', ['e06', 'e07']),
   SP('sp-well', 'Dusza klatki', 'Świecicie latarką w górę, wzdłuż schodów.', ['e09']),
   SP('sp-door', 'Boczne drzwi', 'Drzwi od strony parku, rano zastane uchylone.', ['e10']),
   SP('sp-landing2', 'Podest II piętra', 'Najwyższy podest klatki według planu.', ['e11']),
   SP('sp-panel', 'Ściana na końcu podestu', 'Szara ściana zamykająca schody na II piętrze.', ['e14'], {'puzzle': 'p-floor'}, 'Zwykła szara ściana. Nie macie powodu jej rozbierać — jeszcze.'),
  ]},
 {'id': 'attic', 'name': 'Poddasze', 'kind': 'Według planu nieużytkowe', 'desc': 'Przestrzeń pod dachem wschodniego skrzydła. Na planie z 2018 roku — bez dostępu.',
  'img': img('places', 'attic'), 'spots': [
   SP('sp-ward', 'Sala pod dachem', 'Długa sala z żelaznymi łóżkami. W rogu stalowa szafa.', ['e15'], {'puzzle': 'p-floor'}, LOCK_ATTIC),
   SP('sp-camera', 'Kamera na statywie', 'W kącie sali, skierowana na szafę. Dioda już nie świeci.', ['e16'], {'puzzle': 'p-floor'}, LOCK_ATTIC),
   SP('sp-landing4', 'Podest przed salą', 'Stary podest nad duszą klatki.', ['e17'], {'puzzle': 'p-floor'}, LOCK_ATTIC),
   SP('sp-sd', 'Karta pamięci kamery', 'Technik wyciąga wskazane klatki w pełnej rozdzielczości.', ['e18'], {'puzzle': 'p-frame'}, 'Ponad tysiąc klatek, miniatury wielkości paznokcia. Technik wyciągnie w pełnej rozdzielczości tylko kilka — wskażcie które.'),
  ]},
 {'id': 'grounds', 'name': 'Teren wokół budynku', 'kind': 'Park, śnieg, ślady', 'desc': 'Zaśnieżony park między bramą, stróżówką, wschodnim skrzydłem i parkanem willi Wilków.',
  'img': img('places', 'grounds'), 'spots': [
   SP('sp-tracks', 'Ślady przed bocznymi drzwiami', 'Technik pokazuje zabezpieczone ślady i miarkę.', ['e08']),
  ]},
 {'id': 'gatehouse', 'name': 'Stróżówka', 'kind': 'Mieszkanie stróża', 'desc': 'Mały domek przy bramie. Sień z tablicą kluczy, pokój z piecem, łóżko, szafa. Na stole kubek i stary modlitewnik.',
  'img': img('places', 'gatehouse'), 'spots': [
   SP('sp-keys', 'Tablica z kluczami', 'W sieni wiszą klucze do wszystkich drzwi sanatorium.', ['e12']),
   SP('sp-boots', 'Buty przy piecu', 'Zenon zgadza się pokazać buty, w których chodzi.', ['e13']),
   SP('sp-wardrobe', 'Szafa', 'Prokurator wydał nakaz przeszukania. Technik otwiera szafę.', ['e19', 'e20'], {'all': ['lie:z-l1']}, 'Stróżówka to mieszkanie Zenona Kubika. Bez jego zgody albo nakazu prokuratora szafy nie otworzycie.'),
  ]},
 {'id': 'villa', 'name': 'Willa Wilków', 'kind': 'Dom ofiary', 'desc': 'Dom za parkanem sanatorium, od wschodu. Gabinet doktora na parterze, pokój córki na piętrze.',
  'img': img('places', 'villa'), 'spots': [
   SP('sp-wstudy', 'Gabinet doktora', 'Laptop, telefon stacjonarny, kartki na biurku.', ['e21']),
   SP('sp-hall', 'Przedpokój', 'Wieszak, półka na buty, drzwi na taras.', ['e22']),
  ]},
 {'id': 'inn', 'name': 'Pensjonat „Pod Jaworem”', 'kind': 'Pokój Kamila Dudy', 'desc': 'Drewniany pensjonat w centrum wsi. Kamil wynajmuje pokój na poddaszu od niedzieli.',
  'img': img('places', 'inn'), 'spots': [
   SP('sp-owner', 'Właścicielka', 'Bożena Nowacka pamięta piątkowy wieczór.', ['e23']),
   SP('sp-klaptop', 'Laptop Kamila', 'Kamil zgadza się pokazać zdjęcia i historię konta.', ['e24', 'e25']),
   SP('sp-kjacket', 'Kurtka na wieszaku', 'Wojskowa kurtka Kamila, ta sama, w której nagrywa.', ['e27']),
  ]},
 {'id': 'flat', 'name': 'Mieszkanie Krystyny Bober', 'kind': 'Blok przy aptece', 'desc': 'Dwa pokoje na parterze. Na stole segregator z dokumentami sprzed ośmiu lat.',
  'img': img('places', 'flat'), 'spots': [
   SP('sp-kpapers', 'Segregator', 'Krystyna sama podaje wam akta swojej sprawy.', ['e26']),
  ]},
]
for l in locations:
    if not l.get('img'): l.pop('img', None)

puzzles = [
 {'id': 'p-floor', 'kind': 'Analiza miejsca', 'title': 'Okienko pod dachem',
  'prompt': 'Na której kondygnacji paliło się światło, które widziała Halina Mrozek? Podajcie numer, licząc parter jako 0.',
  'requires': ['e03', 'e05', 'e09'], 'input': 'number', 'answers': ['3'],
  'hints': ['Świadek liczy rzędy okien w szczycie skrzydła od dołu. Ile rzędów okien klatki pokazuje plan z 2018 roku?',
            'Plan zna parter, I i II piętro. Świadek widzi światło w czwartym rzędzie. Siatka w klatce jest rozdarta od góry, nad II piętrem.',
            'Czwarty rząd to kondygnacja nad II piętrem: parter (0), I (1), II (2), poddasze (3). Tego piętra „nie ma” — trzeba znaleźć do niego wejście.'],
  'solution': 'Światło paliło się na kondygnacji 3 — nad II piętrem, gdzie według planu z 2018 roku nie ma nic. Plan kłamie: na poddaszu jest pomieszczenie, a wejście ukryto na podeście II piętra.',
  'reward': {'spots': ['sp-panel', 'sp-ward', 'sp-camera', 'sp-landing4']}},
 {'id': 'p-snow', 'kind': 'Analiza śladów', 'title': 'Śnieg w odciskach',
  'prompt': 'O której godzinie ktoś przeszedł od stróżówki do bocznych drzwi klatki (ślad C)?',
  'requires': ['e08', 'x1'], 'input': 'time', 'answers': ['23:40'],
  'hints': ['Im wcześniej ktoś przeszedł, tym więcej śniegu zdążyło nasypać się do jego odcisków.',
            'Śnieg padał równo, ok. 2 cm na godzinę, i przestał o 00:40. W odciskach śladu C są 2 cm.',
            '2 cm to godzina padania. Ślad C powstał godzinę przed 00:40, czyli o 23:40.'],
  'solution': 'Do odcisków śladu C nasypały się 2 cm śniegu, czyli godzina opadu przed jego końcem o 00:40: ktoś szedł od stróżówki o 23:40. Tak samo: ślad D (1 cm) — powrót o 00:10, ślad A (3,5 cm) — 22:55, ślad B (4,5 cm) — 22:25.',
  'reward': {'time': [[f'{D} 22:25', 'Ślad B: buty sportowe od drzwi do bramy (ustalone ze śniegu)', 'Analiza śladów'],
                      [f'{D} 22:55', 'Ślad A: kalosze od furtki willi do drzwi (ustalone ze śniegu)', 'Analiza śladów'],
                      [f'{D} 23:40', 'Ślad C: filcowe buty od stróżówki do drzwi (ustalone ze śniegu)', 'Analiza śladów'],
                      [f'{S} 00:10', 'Ślad D: filcowe buty od drzwi do stróżówki (ustalone ze śniegu)', 'Analiza śladów']]}},
 {'id': 'p-frame', 'kind': 'Analiza nagrania', 'title': 'Którą klatkę wyciągnąć',
  'prompt': 'Technik wyciągnie w pełnej rozdzielczości klatkę z chwili, w której według świadka zgasło światło, i dwie poprzednie. Podajcie numer tej klatki.',
  'requires': ['e16', 'e05'], 'input': 'number', 'answers': ['436-437'],
  'hints': ['Halina zna dokładną godzinę, o której zgasło światło. Kamera robi jedną klatkę co 30 sekund od pierwszej klatki.',
            'Od 20:14:00 do 23:52:00 mijają 3 godziny i 38 minut, czyli 13 080 sekund.',
            '13 080 : 30 = 436 odstępów. Klatka nr 1 to 20:14:00, więc 23:52:00 to klatka nr 437.'],
  'solution': 'Od pierwszej klatki (20:14:00) do 23:52:00 mija 436 odstępów po 30 sekund, więc światło gaśnie na klatce 437. Technik wyciąga klatki 0435–0437.',
  'reward': {'spots': ['sp-sd']}},
]

hq = {'id': 'hq', 'name': 'Centrala wydziału', 'kind': 'Zapytania przez radio', 'desc': 'Wóz dowodzenia przed bramą sanatorium. Każde zapytanie to jeden ruch — odpowiedzi przychodzą od razu.',
      'img': 'assets/places/001-hq.webp', 'spots': [
  SP('sp-hq-imgw', 'Dane pogodowe', 'Zamawiacie z IMGW przebieg opadów z ostatniej nocy.', ['x1']),
  SP('sp-hq-arch', 'Archiwum budowlane', 'Prosicie o oryginalny projekt sanatorium.', ['x2']),
  SP('sp-hq-hr', 'Kadry gminy', 'Prosicie o akta osobowe stróża.', ['x3']),
  SP('sp-hq-med', 'Zakład medycyny sądowej', 'Prosicie o uzupełnienie opinii po sekcji.', ['x4']),
  SP('sp-hq-usc', 'Urząd Stanu Cywilnego', 'Prosicie o odpis aktu zgonu Ewy Rudnickiej.', ['x5']),
  SP('sp-hq-gmina', 'Archiwum gminy', 'Prosicie o dokumenty remontów sanatorium z 2018 roku.', ['x6']),
 ]}

hintTrail = [
 {'unless': ['sp-body'], 'text': 'Zacznijcie od klatki gospodarczej: ciało i to, co ofiara trzyma w dłoni.'},
 {'unless': ['sp-well'], 'when': ['sp-body'], 'text': 'Lekarz mówi o upadku z dużej wysokości. Spójrzcie w górę klatki.'},
 {'unless': ['p-floor'], 'when': ['e09'], 'text': 'Siatka nad II piętrem jest rozdarta od góry, a plan twierdzi, że wyżej nic nie ma. Policzcie rzędy okien, o których mówi świadek.'},
 {'unless': ['sp-tracks'], 'text': 'Zanim śnieg stopnieje: obejrzyjcie ślady przed bocznymi drzwiami.'},
 {'unless': ['lie:z-l1'], 'when': ['e08'], 'text': 'Stróż mówi, że w nocy nie wychodził. Ślady od stróżówki mówią co innego.'},
 {'unless': ['p-snow'], 'when': ['e08'], 'text': 'W każdym odcisku jest inna ilość świeżego śniegu. Dane IMGW o tym, jak szybko padało, są w tajnych aktach albo w centrali.'},
 {'unless': ['k-q6'], 'when': ['z-q4'], 'text': 'Stróż mówi o „dzienniku”. W zwiastunie była mowa tylko o szafie. Zapytajcie Kamila, komu mówił, co w niej jest.'},
 {'unless': ['lie:k-l2'], 'when': ['e16'], 'text': 'Na miniaturach z kamery są dwie osoby. Kamil twierdzi, że był sam.'},
 {'unless': ['p-frame'], 'when': ['e16'], 'text': 'Świadek podała dokładną godzinę, o której zgasło światło. Kamera robi klatkę co 30 sekund.'},
 {'unless': ['sp-wardrobe'], 'when': ['lie:z-l1'], 'text': 'Stróż skłamał w sprawie nocnego wyjścia. Prokurator zgodzi się na przeszukanie stróżówki.'},
 {'unless': ['lie:z-l5'], 'when': ['z-q6'], 'text': 'Ewa Rudnicka nosiła po rozwodzie nazwisko męża. Sprawdźcie, jak nazywała się z domu i kim był jej ojciec.'},
 {'text': 'Macie dość, by złożyć raport. Upewnijcie się, że każdy wniosek umiecie podeprzeć dowodem.'},
]

report = {'questions': [
 {'id': 'r-who', 'q': 'Kto spowodował śmierć Adama Wilka?', 'type': 'single', 'points': 13,
  'options': [['zenon', 'Zenon Kubik, stróż'], ['kamil', 'Kamil Duda, autor kanału'], ['krystyna', 'Krystyna Bober, była pielęgniarka'], ['joanna', 'Joanna Wilk, córka'], ['accident', 'Nikt — to był nieszczęśliwy wypadek']],
  'correct': 'zenon',
  'proof': {'count': 3, 'each': 4, 'valid': ['e07', 'e19', 'e18', 'e08', 'e13', 'e17', 'x4', 't1', 't5', 't3', 'e20', 'x5', 't4', 'x3'],
            'label': 'Wskażcie trzy dowody, które najmocniej łączą sprawcę ze zdarzeniem.'}},
 {'id': 'r-place', 'q': 'Skąd spadł Adam Wilk?', 'type': 'single', 'points': 10,
  'options': [['attic', 'Z podestu na poddaszu, nad II piętrem'], ['second', 'Z podestu II piętra'], ['stairs', 'Ze schodów między parterem a I piętrem'], ['moved', 'Nie spadł tutaj — ciało przeniesiono']], 'correct': 'attic'},
 {'id': 'r-when', 'q': 'Kiedy doszło do upadku?', 'type': 'single', 'points': 10,
  'options': [['2225', 'Ok. 22:25'], ['2255', 'Ok. 22:55'], ['2340', 'Ok. 23:40'], ['2352', 'Ok. 23:52']], 'correct': '2352'},
 {'id': 'r-light', 'q': 'Kto przez cały tydzień zapalał światło w okienku pod dachem?', 'type': 'single', 'points': 10,
  'options': [['kamil', 'Kamil Duda — lampa do nagrań'], ['wilk', 'Adam Wilk'], ['zenon', 'Zenon Kubik'], ['krystyna', 'Krystyna Bober']], 'correct': 'kamil'},
 {'id': 'r-motive', 'q': 'Jaki był motyw?', 'type': 'single', 'points': 15,
  'options': [['daughter', 'Śmierć córki sprawcy, którą Wilk zatuszował w 2018 roku'], ['lawsuit', 'Wilk groził sprawcy pozwem za nagrania'], ['inherit', 'Spadek po Wilku'], ['nurse', 'Zemsta za niesłuszny wyrok i utratę zawodu']], 'correct': 'daughter'},
 {'id': 'r-past', 'q': 'Jak naprawdę zginęła Ewa Rudnicka w 2018 roku?', 'type': 'single', 'points': 15,
  'options': [['therapy', 'Zmarła na poddaszu podczas nielegalnej kuracji insulinowej Wilka; winę zrzucono na pielęgniarkę'], ['nurse', 'Pielęgniarka pomyliła dawkę na II piętrze'], ['heart', 'Zmarła na serce, a dokumenty zaginęły'], ['self', 'Sama wstrzyknęła sobie insulinę']], 'correct': 'therapy'},
 {'id': 'r-order', 'q': 'Ułóżcie wydarzenia piątkowej nocy we właściwej kolejności.', 'type': 'order', 'points': 15,
  'items': [['krystyna', 'Krystyna Bober pokazuje Kamilowi szafę'], ['kamil', 'Kamil wychodzi z budynku'], ['wilk', 'Wilk wchodzi od strony willi'], ['zenon', 'Ktoś idzie od stróżówki do klatki'], ['fall', 'Szamotanina i upadek Wilka'], ['back', 'Powrót do stróżówki']],
  'correct': ['krystyna', 'kamil', 'wilk', 'zenon', 'fall', 'back']},
]}

solution = {'summary': 'Adama Wilka zepchnął z podestu na poddaszu Zenon Kubik, stróż sanatorium i ojciec Ewy Rudnickiej, ok. 23:52, po szamotaninie przy szafie z dziennikiem.',
 'steps': [
  {'h': 'Piętro, którego nie ma', 'p': 'Lekarz: upadek z dużej wysokości, a uzupełnienie opinii mówi o 11–13 m. Podest II piętra jest na 8,2 m, ma wysoką balustradę i nietknięty kurz. Siatka nad II piętrem jest rozdarta od góry. Świadek widzi światło w czwartym rzędzie okien szczytu — plan z 2018 roku zna tylko trzy. Za pomalowaną płytą na podeście II piętra są schody na poddasze.'},
  {'h': 'Izolatorium', 'p': 'Na poddaszu jest sala z ośmioma łóżkami z pasami. Wilk prowadził tam nielegalne śpiączki insulinowe. Po śmierci Ewy Rudnickiej przeniósł jej ciało do sali 7, wpisał w kartę „3 j.” i zrzucił winę na pielęgniarkę, a w kwietniu 2018 roku zamurował wejście i wpisał w plan „poddasze nieużytkowe”.'},
  {'h': 'Światło', 'p': 'Przez tydzień w okienku paliła się lampa Kamila Dudy, który kupił od stróża klucz i nagrywał serię. W piątek zostawił lampę i kamerę na noc.'},
  {'h': 'Ślady na śniegu', 'p': 'Śnieg padał równo 2 cm na godzinę do 00:40. Ślad B (Kamil) — 22:25, ślad A (Wilk, od willi) — 22:55, ślad C (filcowe buty z łatą, od stróżówki) — 23:40, ślad D (powrót do stróżówki) — 00:10. Krystyna wyszła o 22:00, przed śniegiem, i nie zostawiła śladów.'},
  {'h': 'Kamera', 'p': 'Światło zgasło o 23:52, czyli na klatce 437. Klatki 0435–0436: Wilk przy szafie z dziennikiem i rękaw zielonego płaszcza z mosiężnymi guzikami, dłoń zaciśnięta na jego kurtce. Lekarz znajduje na ramionach Wilka sińce od chwytu.'},
  {'h': 'Guzik', 'p': 'W dłoni Wilka — mosiężny guzik z liściem dębu i nitkami zielonej wełny. W szafie stróża — zielony płaszcz leśnika bez jednego guzika przy prawym mankiecie i dziennik izolatorium zawinięty w ręcznik. Kurtka Kamila ma guziki z kotwicą, wszystkie na miejscu.'},
  {'h': 'Wpadka', 'p': 'W zwiastunie była mowa tylko o szafie. Kamil nikomu nie mówił o dzienniku. A stróż, który „nigdy nie był wyżej niż II piętro”, sam z siebie powiedział, że Wilk przyszedł „po ten swój dziennik”.'},
  {'h': 'Motyw', 'p': 'Ewa Rudnicka była z domu Kubik, a akt zgonu podaje imię ojca: Zenon. Zenon Kubik rzucił pracę leśniczego, żeby pilnować budynku, w którym zmarła jego córka. W czwartek przeczytał dziennik i poznał prawdę. W piątek zastał Wilka, który przyszedł go zabrać.'},
  {'h': 'Fałszywe tropy', 'p': 'Kamil skłamał o kluczu i o tym, że był sam, ale o 22:50 był już w pensjonacie. Krystyna miała najsilniejszy motyw, ale wyszła przed śniegiem i nie ma jej śladów. Joanna skłamała, że ojciec nie wychodził — ze wstydu, nie z winy.'},
 ]}

endings = {
 'correct': {'title': 'Ojciec', 'text': 'Zenon Kubik czeka w stróżówce, w swetrze, z kubkiem zimnej herbaty. Nie próbuje uciekać. Zanim wsiądzie do radiowozu, prosi tylko, żeby zgasić światło w piecu. Prokurator stawia mu zarzut zabójstwa, a do akt trafia płócienny zeszyt z napisem „Izolatorium”.',
   'decision': {'q': 'Zostaje dziennik Adama Wilka — dowód w sprawie Zenona i jedyny dowód niewinności Krystyny Bober. Co zrobicie?', 'options': [
     {'id': 'law', 'label': 'Dziennik do prokuratury i wniosek o wznowienie sprawy Krystyny', 'text': 'Prokurator przyjmuje dziennik i składa wniosek o wznowienie postępowania z 2018 roku. Rok później sąd uniewinnia Krystynę Bober. Na rozprawie Zenona Kubika siada w ostatnim rzędzie, tam, gdzie on siadał przed laty. Sąd uznaje działanie w silnym wzburzeniu. Zenon dostaje osiem lat.'},
     {'id': 'show', 'label': 'Pozwolić Kamilowi pokazać dziennik w odcinku', 'text': 'Kamil publikuje odcinek z kadrami dziennika jeszcze przed aktem oskarżenia. Milion wyświetleń w dwa dni. Do prokuratury zgłaszają się rodziny trzech innych pacjentów izolatorium. Obrońca Zenona przez rok przekonuje sąd, że jego klient był ofiarą medialnej nagonki — i proces wlecze się bez końca.'},
     {'id': 'father', 'label': 'Pokazać Zenonowi wpis o córce, zanim go wywiozą', 'text': 'Kładziecie dziennik na stole w stróżówce i otwieracie na stronie z 2 marca 2018 roku. Zenon czyta długo, palcem pod linijką. Potem mówi: „Ona nie cierpiała. Śpiączka. Ona nie wiedziała”. I pierwszy raz od ośmiu lat płacze. Na przesłuchaniu u prokuratora mówi wszystko, od początku do końca.'},
   ]}},
 'wrong': {
  'kamil': {'title': 'Autor kanału', 'text': 'Oskarżacie Kamila, bo wszedł do budynku nielegalnie i miał konflikt z Wilkiem. Właścicielka pensjonatu i ślady na śniegu dają mu alibi od 22:25. Sprawa się sypie, a dziennik izolatorium zostaje w szafie stróża.'},
  'krystyna': {'title': 'Pielęgniarka po raz drugi', 'text': 'Krystyna Bober miała najsilniejszy motyw — i drugi raz w życiu słyszy zarzut, którego nie popełniła. Na śniegu nie ma jej śladów, a obrona rozbija akt oskarżenia na pierwszej rozprawie. Prawdziwy sprawca składa kondolencje Joannie Wilk.'},
  'joanna': {'title': 'Córka', 'text': 'Joanna skłamała o nocnym wyjściu ojca — i za to płaci. Ale z willi prowadzą tylko jedne ślady, a ona nie ruszyła się z domu. Sąd ją uniewinnia. Szafa w stróżówce nigdy nie zostaje otwarta.'},
  'accident': {'title': 'Nieszczęśliwy wypadek', 'text': 'Stary człowiek z chorym sercem poszedł nocą do opuszczonego budynku i spadł w ciemnej klatce. Sprawa zostaje umorzona. Kamil publikuje odcinek o „klątwie sanatorium”, a zeszyt z napisem „Izolatorium” znika z historii po raz drugi.'},
 },
 'partial': 'Wskazaliście właściwą osobę, ale część waszych wniosków jest błędna lub niepoparta dowodami. Prokurator przyjmuje sprawę, choć obrona będzie miała o co walczyć.'}

case = {
 'id': '003', 'title': 'Cisza w sanatorium', 'subtitle': 'Światło na piętrze, którego nie ma', 'genre': 'Mroczne mystery',
 'duration': '80–110 min', 'players': '2–6', 'difficulty': 'Wymagająca',
 'cover': 'assets/cases/003-cover.webp', 'art': 'assets/art/003-keyart.webp', 'ambience': 'assets/audio/case-003.mp3',
 'par': 53,
 'intro': {
  'lead': 'Sobota, 21 listopada, 9:30. Sanatorium „Jodła” w Jaworzynie Zdroju. W nocy spadł pierwszy śnieg.',
  'brief': ['Od niedzieli mieszkańcy dzwonili na posterunek: w zamkniętym od ośmiu lat sanatorium co noc pali się światło. W najwyższym okienku wschodniego skrzydła — tam, gdzie według planów nic nie ma.',
            'W piątek o 18:00 autor kanału „Zapomniane” opublikował zwiastun: „Piętro, którego nie ma”. Obiecał pokazać w sobotę, co dyrektor trzymał w szafie.',
            'Dziś o 7:35 stróż znalazł w klatce gospodarczej ciało dawnego dyrektora sanatorium, doktora Adama Wilka. Starszy człowiek z chorym sercem, nocą, w pustym budynku, w ciemnej klatce schodowej. Wygląda na wypadek.',
            'W 2018 roku, tuż przed zamknięciem, w tym sanatorium zmarła pacjentka. Za jej śmierć skazano pielęgniarkę. Wasz wydział dostał sprawę, bo prokurator nie wierzy w zbiegi okoliczności.'],
  'task': ['Jak zginął Adam Wilk — i czy ktoś mu w tym pomógł?', 'Skąd spadł i o której godzinie?', 'Kto zapalał światło w okienku pod dachem?', 'Co naprawdę stało się w sanatorium w marcu 2018 roku?'],
  'rules': ['Każde przeszukanie miejsca i każde pytanie zadane świadkowi to jeden ruch. Ruchów nie brakuje, ale najlepsze zespoły zamykają sprawę oszczędnie.',
            'Świadkowie kłamią — czasem ze strachu, czasem ze wstydu. Gdy dowód przeczy zeznaniu, użyjcie konfrontacji. Nietrafiona konfrontacja kosztuje punkty.',
            'Raport końcowy oceni wnioski i dowody, które na ich poparcie wskażecie.'],
  'modeRules': {'table': 'Wszystko widzicie razem. Część informacji zdobędziecie tylko w Centrali wydziału — zapytania do centrali też kosztują ruchy.',
                'phones': 'Każdy gracz ma w telefonie tajne akta, których nie widzi reszta. Od was zależy, kiedy i czy podzielicie się nimi z zespołem.'}},
 'people': people, 'locations': locations, 'evidence': evidence,
 'privateClues': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'], 'puzzles': puzzles,
 'tableMode': {'parBonus': 6, 'locations': [hq], 'questions': {}},
 'breakthroughs': [
  {'id': 'b-floor', 'when': 'p-floor', 'title': 'Piętro, którego nie ma', 'text': 'Czwarty rząd okien to poddasze, do którego według planu nie ma wejścia. A jednak ktoś tam co noc zapalał światło — i ktoś stamtąd spadł.', 'img': 'assets/evidence/003-panel.webp'},
  {'id': 'b-frame', 'when': 'e18', 'title': 'Klatka 0436', 'text': 'Kamera zarejestrowała szamotaninę przy szafie: rękaw ciemnego płaszcza z metalowymi guzikami i dłoń zaciśnięta na kurtce doktora.', 'img': 'assets/evidence/003-frames.webp'},
  {'id': 'b-father', 'when': 'lie:z-l5', 'title': 'Ewka była moją córką', 'text': 'Stróż sanatorium jest ojcem pacjentki, która zmarła tu w 2018 roku. Osiem lat pilnował budynku, w którym straciła życie.', 'img': 'assets/people/003-zenon.webp'}],
 'hintTrail': hintTrail, 'report': report, 'solution': solution, 'endings': endings,
}
MARKS = {'e26': 'M'}
for e in evidence:
    if e['id'] in MARKS: e['mark'] = MARKS[e['id']]
EVIMG = {'e07': 'button', 'e13': 'boots', 'e19': 'coat', 'e08': 'snow', 'e15': 'floodlight', 'e16': 'camera', 'e20': 'journal', 'e14': 'panel', 'e09': 'net', 'e18': 'frames'}
for e in evidence:
    if e['id'] in EVIMG and img('evidence', EVIMG[e['id']]): e['img'] = img('evidence', EVIMG[e['id']])
    if e['id'] == 'e01' and img('people', 'wilk'): e['img'] = img('people', 'wilk')
    if e['id'] == 'e05' and img('people', 'halina'): e['img'] = img('people', 'halina')
if 'plan' in old: case['plan'] = old['plan']
json.dump(case, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('zapisano', P)
