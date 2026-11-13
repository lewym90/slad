# Sprawa 005 „Pokój bez okien” — miejsca, zagadki, raport, zakończenia, bazy (część skryptu build_005.py)
from b005_evidence import T, D, F

def spot(id, name, text, gives, requires=None, lockedText=None):
    d = {'id': id, 'name': name, 'text': text, 'gives': gives}
    if requires: d['requires'] = requires; d['lockedText'] = lockedText
    return d

locations = [
 {'id': 'room', 'name': 'Pokój 214', 'kind': 'Hotel „Gryf”, II piętro, skrzydło B',
  'desc': 'Wąski pokój bez okien, oświetlony tylko lampami. Łóżko, biurko, szafa wnękowa i łazienka. Drzwi z przeciętą zasuwą stoją otworem.',
  'spots': [
   spot('sp-suitcase', 'Walizka na stojaku', 'Szara walizka na kółkach, zamknięta na suwak.', ['e09']),
   spot('sp-bed', 'Łóżko i łazienka', 'Zasłane łóżko, za nim drzwi do łazienki.', ['e10']),
   spot('sp-desk', 'Biurko', 'Koperta z recepcji, notes, długopis.', ['e12']),
   spot('sp-wardrobe', 'Szafa wnękowa', 'Głęboka szafa na całą ścianę. Kilka pustych wieszaków.', ['e11'], requires={'all': ['e24']},
        lockedText='Zwykła hotelowa szafa: wieszaki, półka, sejf bez zawartości. Bez konkretnego powodu nie będziecie rozbierać mebli.'),
  ]},
 {'id': 'reception', 'name': 'Recepcja i hol', 'kind': 'Parter hotelu „Gryf”',
  'desc': 'Długa lada z ciemnego drewna, za nią ekran systemu hotelowego i skaner dokumentów. W holu fotele, z boku wejście do baru.',
  'spots': [
   spot('sp-card', 'Karta meldunkowa i skaner', 'Dokumenty z zameldowania gościa z 214.', ['e13', 'e14']),
   spot('sp-register', 'Księga gości', 'Wyciąg z systemu: kto nocował w hotelu.', ['e15']),
   spot('sp-phone', 'Centrala telefoniczna', 'Dziennik połączeń wewnętrznych.', ['e16']),
   spot('sp-booking', 'Skrzynka rezerwacji', 'Korespondencja w sprawie pokoju dla biegłego.', ['e17']),
   spot('sp-locks', 'System zamków', 'Eksport zdarzeń zamków na kartę.', ['e27']),
  ]},
 {'id': 'hall', 'name': 'Sala „Bursztynowa”', 'kind': 'Sala konferencyjna, I piętro',
  'desc': 'Stół na dwanaście osób, karafki z wodą, rzutnik. Na krzesłach teczki uczestników. Posiedzenie przerwano o 9:40.',
  'spots': [
   spot('sp-files', 'Akta komisji', 'Segregator z wnioskiem i kopiami dokumentów.', ['e19', 'e22']),
   spot('sp-rules', 'Regulamin komisji', 'Oprawiony regulamin przy miejscu przewodniczącego.', ['e20']),
   spot('sp-minutes', 'Notatki protokolanta', 'Zapis pierwszych czterdziestu minut posiedzenia.', ['e21']),
  ]},
 {'id': 'tech', 'name': 'Dział techniczny', 'kind': 'Piwnica hotelu',
  'desc': 'Pokój kierownika technicznego, regały z segregatorami i szafka na klucze. Zbigniew Wrona pracuje w hotelu od trzydziestu lat.',
  'spots': [
   spot('sp-plans', 'Archiwum planów', 'Teczki z planami budynku i dokumentacją remontów.', ['e23', 'e24']),
   spot('sp-invoice', 'Archiwum faktur', 'Segregatory z fakturami za remonty.', ['e25']),
   spot('sp-exit', 'Kontroler drzwi służbowych', 'Panel z dziennikiem wyjść personelu.', ['e26']),
   spot('sp-keys', 'Szafka z kluczami', 'Klucze techniczne i zeszyt wydań.', ['e28']),
  ]},
 {'id': 'service', 'name': 'Korytarz gospodarczy i klatka B', 'kind': 'Zaplecze hotelu',
  'desc': 'Wąski korytarz wzdłuż ściany od podwórza, za pokojem 214: rury pod sufitem, stare drzwi rewizyjne. Na końcu klatka schodowa personelu, a na dole palarnia przy wyjściu służbowym.',
  'spots': [
   spot('sp-m2', 'Drzwi M2 od korytarza', 'Stalowe drzwi w ścianie korytarza, dokładnie za pokojem 214.', ['e29']),
   spot('sp-stairs', 'Klatka schodowa B', 'Betonowe schody, kaloryfery na podestach.', ['e31']),
   spot('sp-smoke', 'Palarnia personelu', 'Mała wiata przy wyjściu B.', ['e30']),
  ]},
 {'id': 'bar', 'name': 'Bar „Kotwica”', 'kind': 'Parter hotelu',
  'desc': 'Ciemne drewno, mosiężne lampy, kilka stolików. Z baru widać kawałek holu.',
  'spots': [
   spot('sp-bills', 'Kasa fiskalna', 'Rachunki z czwartkowego wieczoru.', ['e32']),
   spot('sp-barman', 'Barman', 'Rafał Czajka miał czwartkową zmianę.', ['e33']),
   spot('sp-rs', 'Zamówienia room service', 'Kuchnia prowadzi zeszyt zamówień do pokojów.', ['e34']),
  ]},
 {'id': 'archive', 'name': 'Archiwum w Koszalinie', 'kind': 'Wideorozmowa z gabinetem dr. Szulca',
  'desc': 'Na ekranie gabinet z regałami teczek i lampą z zieloną szybką. Przy biurku zastępczyni dr. Szulca, Joanna Kurek, pokazuje wam to, o co poprosicie.',
  'spots': [
   spot('sp-notes', 'Biurko dr. Szulca', 'Monitor obklejony karteczkami.', ['e35']),
   spot('sp-catalog', 'Kartoteka znaków wodnych', 'Szuflady z kartami katalogowymi papierni.', ['e45']),
   spot('sp-mail', 'Skrzynka służbowa', 'Wysłane wiadomości i załączniki.', ['e36', 'e38']),
   spot('sp-sign', 'Teczka korespondencji', 'Pisma podpisane przez dr. Szulca.', ['e37']),
   spot('sp-pdf', 'Projekt opinii', 'Plik otwarty hasłem.', ['e39'], requires={'puzzle': 'p-pdf'}, lockedText='Plik jest zaszyfrowany. Bez czterocyfrowego hasła go nie otworzycie.'),
  ]},
 {'id': 'parking', 'name': 'Parking za hotelem', 'kind': 'Szlaban z kamerą ANPR',
  'desc': 'Kilkanaście miejsc za budynkiem, szlaban z kamerą odczytującą tablice. Wzdłuż ściany wąska alejka do wyjścia służbowego.',
  'spots': [
   spot('sp-anpr', 'Szlaban i kamera', 'Rejestr wjazdów i wyjazdów.', ['e18']),
   spot('sp-lane', 'Alejka za hotelem', 'Trzydzieści metrów do wyjścia B.', ['e41']),
   spot('sp-car', 'Samochód Iwony Kraski', 'Granatowa toyota na miejscu numer 7.', ['e40'], requires={'all': ['lie:k-l1']},
        lockedText='Samochód sekretarz komisji. Bez podstaw prokurator nie zgodzi się na przeszukanie. Najpierw wykażcie, że jego właścicielka kłamie o czwartkowym wieczorze.'),
  ]},
]

puzzles = [
 {'id': 'p-pdf', 'kind': 'Hasło', 'title': 'Projekt opinii dr. Szulca',
  'prompt': 'Projekt opinii jest zaszyfrowany czterocyfrowym hasłem. Jakie hasło ustawił dr Szulc? Sam zostawił wskazówkę.',
  'requires': ['e35', 'e45', 'e38'], 'input': 'digits4', 'answers': ['1051'],
  'hints': ['Kartka na monitorze mówi, z czego składa się hasło. Potrzebujecie nazwy papierni ze znaku wodnego.',
            'Znak wodny na akcie to „WIEPRZA”. Kartoteka znaków wodnych podaje datę uruchomienia tej papierni. Hasło to miesiąc i dwie ostatnie cyfry roku.',
            'Papiernia „Wieprza” ruszyła 3 października 1951: miesiąc 10, rok 51. Hasło: 1051.'],
  'solution': 'Hasło to miesiąc i rok uruchomienia papierni „Wieprza”, której znak wodny jest na akcie z 1946 roku: październik 1951, czyli 1051. Szulc wybrał je celowo — to sedno jego opinii.',
  'reward': {'spots': ['sp-pdf']}},
 {'id': 'p-where', 'kind': 'Macierz alibi', 'title': 'Kto gdzie był',
  'prompt': 'Gdzie była każda z pięciu osób o 22:15, gdy dr Szulc powinien już być w hotelu, i o 23:20, gdy ktoś zniknął z zamkniętego pokoju? Wybierzcie miejsce dla każdej osoby w obu kolumnach.',
  'requires': ['e18', 'x3', 'e32', 'x4', 'st:l-c2', 'e15', 'lie:l-l1', 'e34', 'e16'], 'input': 'grid',
  'grid': {
   'rows': [{'id': 'kraska', 'label': 'Iwona Kraska'}, {'id': 'kosowski', 'label': 'Adrian Kosowski'}, {'id': 'dabrowska', 'label': 'Ewa Dąbrowska'}, {'id': 'lis', 'label': 'Bartosz Lis'}, {'id': 'morawiec', 'label': 'Lech Morawiec'}],
   'cols': [{'id': 't1', 'label': '22:15'}, {'id': 't2', 'label': '23:20'}],
   'options': [{'id': 'hol', 'label': 'Hol i recepcja'}, {'id': 'bar', 'label': 'Bar'}, {'id': 'pok', 'label': 'Własny pokój'}, {'id': 'zap', 'label': 'Palarnia'}, {'id': 'out', 'label': 'Poza hotelem'}],
   'constraints': [
    {'t': 'is', 'r': 'kraska', 'c': 't1', 'v': 'out', 'src': ['e18'], 'why': 'Jej toyota ZS 3K118 wyjechała z parkingu o 21:36 i wróciła o 22:41.'},
    {'t': 'is', 'r': 'kraska', 'c': 't2', 'v': 'pok', 'src': ['x3'], 'why': 'Od 23:03 do rana jej telefon był w punkcie AP-3B, na piętrze jej pokoju 305.'},
    {'t': 'is', 'r': 'kosowski', 'c': 't1', 'v': 'bar', 'src': ['e32', 'x3'], 'why': 'Rachunki baru na jego pokój od 21:04 do 0:22, a telefon cały czas na parterze (AP-1A).'},
    {'t': 'is', 'r': 'kosowski', 'c': 't2', 'v': 'bar', 'src': ['e32', 'x3'], 'why': 'Rachunki o 22:31 i 23:47, telefon na parterze do 0:31.'},
    {'t': 'is', 'r': 'dabrowska', 'c': 't1', 'v': 'hol', 'src': ['x4', 'st:l-c2'], 'why': 'Taksówka przywiozła ją o 22:12, a recepcjonista widział ją w holu od 22:15.'},
    {'t': 'is', 'r': 'dabrowska', 'c': 't2', 'v': 'out', 'src': ['x4'], 'why': 'Odjechała taksówką o 22:52.'},
    {'t': 'is', 'r': 'lis', 'c': 't1', 'v': 'hol', 'src': ['e15'], 'why': 'O 22:20 meldował w recepcji gościa z pokoju 216.'},
    {'t': 'is', 'r': 'lis', 'c': 't2', 'v': 'zap', 'src': ['lie:l-l1'], 'why': 'Sam przyznał: od 23:15 do około 23:35 był w palarni.'},
    {'t': 'is', 'r': 'morawiec', 'c': 't1', 'v': 'pok', 'src': ['e34'], 'why': 'Zamówił kolację z pokoju o 22:10 i odebrał ją w pokoju o 22:18.'},
    {'t': 'is', 'r': 'morawiec', 'c': 't2', 'v': 'pok', 'src': ['e16'], 'why': 'O 23:22 dzwonił do recepcji z telefonu w pokoju 118.'},
   ]},
  'answers': [{'kraska': {'t1': 'out', 't2': 'pok'}, 'kosowski': {'t1': 'bar', 't2': 'bar'}, 'dabrowska': {'t1': 'hol', 't2': 'out'}, 'lis': {'t1': 'hol', 't2': 'zap'}, 'morawiec': {'t1': 'pok', 't2': 'pok'}}],
  'hints': ['Zacznijcie od twardych zapisów: szlaban parkingu, rachunki baru, room service i centrala telefoniczna.',
            'O 22:15 tylko jedna z tych osób była poza hotelem. O 23:20 też tylko jedna, ale już ktoś inny.',
            'Kraska: poza hotelem, potem pokój. Kosowski: bar i bar. Dąbrowska: hol, potem poza hotelem. Lis: hol, potem palarnia. Morawiec: pokój i pokój.'],
  'solution': 'O 22:15 Kraska jeździła po mieście (21:36–22:41), Dąbrowska czekała w holu, Lis był w recepcji, Kosowski w barze, Morawiec w pokoju. O 23:20, gdy ktoś wychodził z 214 drzwiami za szafą, Lis był w palarni, Dąbrowska już w domu, Kosowski w barze, Morawiec w pokoju, a Kraska u siebie na III piętrze. Żadna z tych osób nie była w pokoju 214.',
  'reward': {'time': [[f'{D} 23:20', 'Nikt z piątki nie był przy 214: Lis w palarni, Kosowski w barze, Morawiec i Kraska w pokojach, Dąbrowska poza hotelem', 'Macierz alibi']]}},
]

hintTrail = [
 {'unless': ['sp-suitcase'], 'text': 'Zacznijcie od pokoju 214. Co zostało, a czego brakuje?'},
 {'unless': ['sp-locks'], 'when': ['sp-suitcase'], 'text': 'Zamek pokoju zapisuje zdarzenia. Sprawdźcie, co działo się z drzwiami w nocy.'},
 {'unless': ['sp-card'], 'when': ['sp-locks'], 'text': 'Kto właściwie zameldował się w 214? Zobaczcie kartę meldunkową i skan dowodu.'},
 {'unless': ['m-q2'], 'when': ['sp-card'], 'text': 'Żona dr. Szulca jest w hotelu. Zapytajcie, jak dziś wygląda jej mąż.'},
 {'unless': ['show:l-s1'], 'when': ['e42', 'e14'], 'text': 'Macie aktualne zdjęcie dr. Szulca. Pokażcie je osobie, która widziała gościa z 214.'},
 {'unless': ['sp-anpr'], 'when': ['sp-card'], 'text': 'Parking ma szlaban z kamerą. Kto przyjeżdżał i odjeżdżał w czwartek wieczorem?'},
 {'unless': ['d01'], 'when': ['e18'], 'text': 'Jeden samochód z rejestru szlabanu nie pasuje do żadnego gościa. Sprawdźcie go w CEPiK.'},
 {'unless': ['d02'], 'when': ['d01'], 'text': 'Właścicielem samochodu jest spółka. KRS powie, kto nią kieruje i gdzie ma siedzibę.'},
 {'unless': ['lie:k-l6'], 'when': ['d02'], 'text': 'Prezes spółki ma PESEL w rejestrze KRS. Ewidencja ludności powie o nim więcej — także o rodzinie.'},
 {'unless': ['sp-wardrobe'], 'when': ['e23'], 'text': 'Plan z 1974 roku pokazuje magazyn z dwojgiem drzwi. Co się stało z drugimi drzwiami przy remoncie w 2019?'},
 {'unless': ['p-pdf'], 'when': ['e35', 'e38'], 'text': 'Szulc zapisał, czym jest hasło do projektu opinii. Kartoteka znaków wodnych zna odpowiedź.'},
 {'unless': ['lie:k-l1'], 'when': ['e18'], 'text': 'Toyota ZS 3K118 należy do jednej z uczestniczek posiedzenia. Gdzie była między 21:36 a 22:41?'},
 {'unless': ['p-where'], 'when': ['lie:l-l1', 'x3'], 'text': 'Zbierzcie, gdzie kto był o 22:15 i o 23:20. Macierz alibi uporządkuje noc.'},
 {'text': 'Macie dość, by złożyć raport. Pamiętajcie: najważniejsze pytanie brzmi, gdzie jest dr Szulc.'},
]

report = {'questions': [
 {'id': 'r-who', 'q': 'Kto zorganizował zniknięcie dr. Edwarda Szulca?', 'type': 'single', 'points': 12,
  'options': [['kraska', 'Iwona Kraska, sekretarz komisji'], ['kosowski', 'Adrian Kosowski, pełnomocnik wnioskodawczyni'], ['dabrowska', 'Ewa Dąbrowska, radca prawny Gminy'],
              ['lis', 'Bartosz Lis, nocny recepcjonista'], ['morawiec', 'Lech Morawiec, biegły zastępczy'], ['self', 'Nikt — dr Szulc odszedł sam, zdezorientowany']],
  'correct': 'kraska',
  'proof': {'count': 3, 'each': 4, 'valid': ['d03', 'd06', 'e18', 'e05', 'x3', 'e40', 'e17', 'x2', 'x6', 'e44'], 'label': 'Wskażcie trzy dowody, które najmocniej łączą tę osobę ze zniknięciem biegłego.'}},
 {'id': 'r-imp', 'q': 'Kto zameldował się w czwartek o 23:05 jako Edward Szulc?', 'type': 'single', 'points': 12,
  'options': [['pietras', 'Damian Pietras, prezes Restytucji Pomorskiej'], ['szulc', 'Sam dr Edward Szulc'], ['morawiec', 'Lech Morawiec'], ['kosowski', 'Adrian Kosowski'], ['banas', 'Marek Banaś, gość z pokoju 216']],
  'correct': 'pietras'},
 {'id': 'r-where', 'q': 'Gdzie należy natychmiast szukać dr. Szulca?', 'type': 'single', 'points': 12,
  'options': [['jag', 'Szczecin, ul. Jagiellońska 12/4 — lokal Restytucji Pomorskiej'], ['szafera', 'Szczecin, ul. Szafera 8 — dom Pietrasa i Kraski'], ['police', 'Police, ul. Fabryczna 3 — siedziba PB Pietras Budownictwo'],
              ['urzad', 'Urząd Miasta, pl. Armii Krajowej 1 — biuro komisji'], ['hotel', 'W hotelu, w zaplombowanej części zaplecza']],
  'correct': 'jag'},
 {'id': 'r-how', 'q': 'Jak fałszywy gość opuścił pokój 214 zamknięty od środka?', 'type': 'single', 'points': 10,
  'options': [['m2', 'Drzwiami rewizyjnymi M2 za tylną ścianą szafy, do korytarza gospodarczego i klatki B'], ['master', 'Ktoś otworzył drzwi kartą MASTER, a zasuwę załączył potem z zewnątrz'],
              ['vent', 'Przez kratkę wentylacyjną pod sufitem'], ['never', 'Nigdy nie wszedł do pokoju — zasuwę załączono zdalnie'], ['morning', 'Wyszedł rano, w zamieszaniu przy otwieraniu drzwi']],
  'correct': 'm2'},
 {'id': 'r-list', 'q': 'Dlaczego nazwisko dr. Szulca zniknęło z listy uczestników?', 'type': 'single', 'points': 10,
  'options': [['plan', 'Kraska usunęła je w nocy, osiem minut po „rezygnacji” wysłanej z telefonu Szulca, by komisja przyjęła opinię Morawca'], ['real', 'Szulc sam zrezygnował mailem, a lista to tylko formalność'],
              ['error', 'Hotelowa drukarka wydrukowała starą wersję pliku'], ['kos', 'Kosowski zażądał wykreślenia biegłego na posiedzeniu']],
  'correct': 'plan'},
 {'id': 'r-motive', 'q': 'Jaki był motyw?', 'type': 'single', 'points': 10,
  'options': [['claim', 'Opinia Szulca dowodziła, że akt z 1946 roku jest falsyfikatem, a roszczenie do kamienicy za 38 mln zł należało do spółki męża Kraski'],
              ['fee', 'Kosowski bał się utraty honorarium od wnioskodawczyni'], ['revenge', 'Zemsta za dawny spór o archiwum'], ['career', 'Morawiec chciał zająć miejsce Szulca na liście biegłych']],
  'correct': 'claim'},
 {'id': 'r-signs', 'q': 'Które ustalenia dowodzą, że w 214 zameldował się ktoś inny niż dr Szulc?', 'type': 'multi', 'points': 10,
  'hint': 'Zaznaczcie wszystkie właściwe odpowiedzi. Każda błędna odejmuje punkty za trafną.',
  'options': [['beard', 'Gość miał brodę, a Szulc od trzech lat jej nie nosi'], ['sign', 'Podpis „E. Szulc” nakreśliła inna ręka niż wzory podpisów Szulca'],
              ['foot', 'Gość przyszedł pieszo, bez samochodu'], ['bed', 'Łóżko było nietknięte, a ręczniki suche'], ['insulin', 'Insulina została w walizce']],
  'correct': ['beard', 'sign']},
 {'id': 'r-order', 'q': 'Ułóżcie wydarzenia czwartkowego wieczoru we właściwej kolejności.', 'type': 'order', 'points': 12,
  'items': [['call', 'Kraska prosi Morawca, by został w Szczecinie'], ['train', 'Szulc wysiada z pociągu i pisze do żony o pani Kraskiej'], ['off', 'Telefon Szulca zostaje wyłączony w rejonie ul. Jagiellońskiej'],
            ['back', 'Toyota Kraski wraca na parking hotelu'], ['check', 'Fałszywy „Szulc” melduje się w recepcji'], ['latch', 'W pokoju 214 zostaje załączona zasuwa'],
            ['exit', 'Ktoś wychodzi wyjściem służbowym B'], ['mail', 'Z telefonu Szulca na III piętrze wychodzi mail z rezygnacją'], ['list', 'Kraska zapisuje listę uczestników bez Szulca']],
  'correct': ['call', 'train', 'off', 'back', 'check', 'latch', 'exit', 'mail', 'list']},
]}

solution = {
 'summary': 'Dr Edwarda Szulca uprowadzili Iwona Kraska, sekretarz komisji, i jej mąż Damian Pietras, prezes Restytucji Pomorskiej — spółki, która przejęła roszczenie do kamienicy przy Wielkopolskiej 21. Kraska odebrała biegłego z dworca i zawiozła do lokalu spółki przy ul. Jagiellońskiej 12/4. Pietras zameldował się w hotelu jako Szulc, na jego dowodzie z brodą na zdjęciu, załączył zasuwę i wyszedł drzwiami za szafą, które sam zostawił w 2019 roku. Kraska wysłała z telefonu Szulca mail z „rezygnacją” i usunęła go z listy.',
 'steps': [
  {'h': 'Pokój, w którym nikt nie spał', 'p': 'Zasuwa w 214 została załączona o 23:13:40 i do rana drzwi niczego nie zarejestrowały. Łóżko nietknięte, ręczniki suche, kosmetyczka z insuliną zamknięta. Brakowało płaszcza, kapelusza, telefonu, dowodu i teczki.'},
  {'h': 'Broda', 'p': 'Recepcjonista zameldował mężczyznę z brodą, zgodnego ze zdjęciem z dowodu wydanego w 2018 roku. Żona: Szulc od trzech lat się goli. Na zdjęciu z lutego jest gładko ogolony. Podpis „E. Szulc” różni się od wszystkich wzorów — Szulc zawsze podpisywał się pełnym imieniem.'},
  {'h': 'Druga droga z pokoju', 'p': 'Plan z 1974 roku pokazuje magazyn bielizny z drzwiami M2 do korytarza gospodarczego. Przy adaptacji w 2019 drzwi zostawiono za płytą szafy, zamykane kluczem od korytarza. Za szafą świeży pył, przy M2 starty kurz, na klatce B karta 214-A, o 23:24 wyjście służbowe otwarte przyciskiem od środka, o 23:31 z parkingu wyjeżdża ZS 7PR04.'},
  {'h': 'Samochód, spółka, małżeństwo', 'p': 'ZS 7PR04 należy do Restytucji Pomorskiej (CEPiK). Jej jedynym wspólnikiem i prezesem jest Damian Pietras (KRS), z PESEL-em, pod którym ewidencja ludności podaje żonę: Iwonę Kraską. Ten sam Pietras jako kierownik robót zostawił w 2019 drzwi M2 za szafą.'},
  {'h': 'Pasażerka', 'p': 'O 21:49 Szulc napisał żonie, że pani Kraska czeka przed dworcem. Kierownik pociągu widział kobietę z parasolem. Toyota Kraski była poza hotelem od 21:36 do 22:41, a pod fotelem pasażera leżał bilet Szulca. Telefony Szulca i Kraski były od 21:58 w tej samej komórce Śródmieście-14, obejmującej ul. Jagiellońską. Telefon Szulca zgasł tam o 22:03. Urząd Miasta był tej nocy zamknięty.'},
  {'h': 'Rezygnacja z cudzego telefonu', 'p': 'O 23:48 telefon Szulca na cztery minuty połączył się z Wi-Fi na III piętrze (AP-3B), piętrze pokoju Kraski — a nigdy z punktem przy 214. O 23:50 wyszedł z niego mail „Proszę mnie nie szukać. E.S.”, o 23:58 Kraska zapisała listę bez Szulca, a już o 19:32 prosiła Morawca, żeby został w Szczecinie.'},
  {'h': 'Motyw', 'p': 'Projekt opinii Szulca: papier aktu z 1946 roku pochodzi z papierni uruchomionej w 1951. Akt to falsyfikat, a roszczenie warte 38,4 mln zł należało do spółki męża Kraski. Szulc miał wypaść z gry do podpisania ugody, a potem wrócić jako zdezorientowany starszy pan, który w nocy „zrezygnował” i zniknął.'},
  {'h': 'Fałszywe tropy', 'p': 'Kosowski próbował kupić biegłego listem, ale całą noc spędził w barze. Dąbrowska ukryła wieczorną wizytę, bo spotkanie z biegłym przed posiedzeniem nie wypadało. Lis ukrył przerwę na papierosa. Morawiec ukrył telefon z czwartku, bo dał się wciągnąć w zastępstwo, nie pytając dlaczego.'},
 ]}

endings = {
 'correct': {'title': 'Pokój bez okien', 'text': 'O 13:20 policja wchodzi do lokalu przy ul. Jagiellońskiej 12/4. Dr Edward Szulc leży na kanapie w pokoju bez okien, otumaniony lekiem nasennym, z cukrem na granicy śpiączki. Karetka zabiera go do szpitala, a żona jedzie za nią. Pietras zostaje zatrzymany godzinę później w domu przy ul. Szafera, Kraska — przy stole komisji, gdy próbuje wznowić posiedzenie. Skórzana teczka z oryginałem opinii leży w szafie lokalu.',
  'decision': {'q': 'Szulc przeżył, a komisja czeka. Co zrobicie z ugodą i aktem z 1946 roku?', 'options': [
   {'id': 'law', 'label': 'Zawiadomić prokuraturę o fałszerstwie aktu i wnieść o unieważnienie postępowania ugodowego', 'text': 'Prokuratura zabezpiecza oryginał aktu w Koszalinie. Komisja umarza postępowanie, a cesja dla Restytucji trafia do sądu jako element oszustwa. Szulc po dwóch tygodniach wraca do archiwum i sam kończy opinię.'},
   {'id': 'press', 'label': 'Udostępnić projekt opinii dziennikarzom, zanim ktokolwiek spróbuje go podważyć', 'text': 'Tekst „Akt z papieru, którego nie było” ukazuje się w sobotę. Prezydent miasta zawiesza prace komisji. Obrona Kraski i Pietrasa grzmi o nagonce medialnej, ale sprawa reprywatyzacyjna wraca do sądów pod lupą opinii publicznej.'},
   {'id': 'audit', 'label': 'Zażądać audytu wszystkich ugód komisji z udziałem Kraski z ostatnich trzech lat', 'text': 'Audyt obejmuje jedenaście postępowań. W dwóch pojawia się ta sama kancelaria notarialna i ten sam papier. Proces o uprowadzenie Szulca przeciąga się, ale miasto odzyskuje dwie kamienice.'},
  ]}},
 'wrong': {
  'kosowski': {'title': 'Pełnomocnik', 'text': 'Kosowski skłamał o liście do biegłego i chciał kontynuować posiedzenie, więc oskarżacie go. Tymczasem całą noc przesiedział w barze, co potwierdzają rachunki, barman i hotelowa sieć. Szulca znajduje dopiero w sobotę rano sprzątaczka biura przy Jagiellońskiej — w ciężkim stanie.'},
  'dabrowska': {'title': 'Radca prawny', 'text': 'Dąbrowska ukryła, że była w hotelu w czwartek. Ale to ona żądała otwarcia pokoju, a o 22:52 odjechała taksówką do domu. Zanim śledztwo wraca na właściwy tor, mija noc. Szulc przeżywa, ale ze znacznym uszczerbkiem na zdrowiu.'},
  'lis': {'title': 'Recepcjonista', 'text': 'Lis zostawił recepcję i skłamał, więc wydaje się wspólnikiem. W rzeczywistości zameldował człowieka, którego dowód się zgadzał, i palił papierosa, gdy ten wychodził. Prawdziwi sprawcy zdążą wypuścić Szulca w niedzielę na dworcu — bez pamięci i bez wiarygodności.'},
  'morawiec': {'title': 'Biegły zastępczy', 'text': 'Morawiec skłamał o porze telefonu i zyskiwał na nieobecności Szulca. Ale nie wiedział, dlaczego ma zostać w Szczecinie, a w nocy jadł kolację w swoim pokoju. Ugoda zostaje wstrzymana, a Szulc odnaleziony dopiero następnego dnia.'},
  'self': {'title': 'Zagubiony staruszek', 'text': 'Uznajecie, że zdezorientowany diabetyk napisał w nocy dziwny mail i wyszedł w deszcz. Dokładnie tak miało to wyglądać. Komisja przyjmuje opinię Morawca, a Szulc pojawia się w niedzielę na dworcu w Szczecinie — otumaniony, bez teczki i bez wiarygodności. Nikt nie słucha, co ma do powiedzenia o papierni „Wieprza”.'},
 },
 'partial': 'Wskazaliście właściwą osobę, ale część wniosków jest błędna lub niepoparta dowodami. Szulc zostaje odnaleziony, choć później, niż mógł, a obrona będzie miała o co walczyć.',
}

breakthroughs = [
 {'id': 'b-beard', 'when': 'show:l-s1', 'title': 'Broda', 'text': 'Recepcjonista zameldował mężczyznę z brodą, bo taki był na zdjęciu w dowodzie. Edward Szulc od trzech lat się goli. W pokoju 214 nocował ktoś, kto miał jego dokument, ale nie jego twarz.'},
 {'id': 'b-door', 'when': 'sp-wardrobe', 'title': 'Drugie drzwi', 'text': 'Za tylną ścianą szafy są stalowe drzwi do korytarza gospodarczego. Pokój bez okien nigdy nie był zamknięty od środka — miał wyjście, o którym wiedzieli tylko ci, którzy go budowali.'},
 {'id': 'b-pass', 'when': 'lie:k-l2', 'title': 'Pasażer', 'text': 'Kraska przyznaje: Szulc wsiadł do jej samochodu na dworcu. Ostatnia osoba, która widziała go wolnego, siedzi przy stole komisji i poprawiała listę uczestników.'},
 {'id': 'b-ring', 'when': 'lie:k-l6', 'title': 'Obrączka', 'text': 'Damian Pietras, prezes spółki, która zarobi na ugodzie miliony, jest mężem sekretarz komisji. Różne nazwiska ukrywały to przez trzy lata.'},
]

tableMode = {'parBonus': 6, 'locations': [
 {'id': 'hq', 'name': 'Centrala wydziału', 'kind': 'Zapytania przez radio i telefon',
  'desc': 'Wóz łączności przed hotelem. Każde zapytanie to jeden ruch, odpowiedzi przychodzą od razu.',
  'img': 'assets/places/001-hq.webp',
  'spots': [
   spot('sp-hq-op1', 'Operator: telefon Szulca', 'Prosicie o zdarzenia w sieci dla numeru dr. Szulca.', ['x1']),
   spot('sp-hq-op2', 'Operator: telefon Kraski', 'Prosicie o zdarzenia w sieci dla numeru sekretarz komisji.', ['x2']),
   spot('sp-hq-wifi', 'Firma obsługująca Wi-Fi hotelu', 'Prosicie o dziennik urządzeń w sieci „Gryf-Guest”.', ['x3']),
   spot('sp-hq-taxi', 'Dyspozytornie taxi', 'Prosicie o kursy spod dworca i pod hotel.', ['x4']),
   spot('sp-hq-um', 'Ochrona Urzędu Miasta', 'Prosicie o rejestr wejść do budynku przy pl. Armii Krajowej.', ['x5']),
   spot('sp-hq-pkp', 'PKP Intercity', 'Prosicie o rozmowę z kierownikiem pociągu IC 38170.', ['x6']),
  ]}], 'questions': {}}

db = {'date': F, 'bases': ['osoby', 'pojazdy', 'firmy', 'ksiegi'], 'ignore': ['IC 38170'], 'attach': [
 {'rec': 'V-005-rest', 'ev': 'd01', 'paths': [{'q': {'nr': 'ZS 7PR04'}, 'from': ['e18']}]},
 {'rec': 'F-005-rest', 'ev': 'd02', 'paths': [{'q': {'krs': '0000781264'}, 'from': ['d01']}, {'q': {'krs': '0000781264'}, 'from': ['d04']}, {'q': {'nazwa': 'Restytucja Pomorska'}, 'from': ['e19']}]},
 {'rec': 'O-005-pietras', 'ev': 'd03', 'paths': [{'q': {'pesel': '67082145713'}, 'from': ['d02']}, {'q': {'nazwisko': 'Pietras', 'imie': 'Damian'}, 'from': ['d02']}]},
 {'rec': 'K-005-claim', 'ev': 'd04', 'paths': [{'q': {'nr': 'SZ1S/00045218/0'}, 'from': ['e19']}]},
 {'rec': 'F-005-pb', 'ev': 'd05', 'paths': [{'q': {'nip': '8512047718'}, 'from': ['e25']}]},
 {'rec': 'O-005-kraska', 'ev': 'd06', 'paths': [{'q': {'nazwisko': 'Kraska', 'imie': 'Iwona'}, 'from': ['e04']}]},
 {'rec': 'O-005-szulc', 'ev': 'd07', 'paths': [{'q': {'nazwisko': 'Szulc', 'imie': 'Edward'}, 'from': ['e01']}]},
]}
