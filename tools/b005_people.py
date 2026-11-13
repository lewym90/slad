# Sprawa 005 „Pokój bez okien” — osoby, pytania, zeznania i reakcje na okazane dowody (część skryptu build_005.py)
from b005_evidence import T, D, F

def Q(id, q, a, claims=None, requires=None, requiresAny=None, gives=None, time=None):
    d = {'id': id, 'q': q, 'a': a}
    if claims: d['claims'] = claims
    if requires: d['requires'] = requires
    if requiresAny: d['requiresAny'] = requiresAny
    if gives: d['gives'] = gives
    if time: d['time'] = time
    return d

def S(id, text, truth=False, contradicts=None, response=None, gives=None, reveals=None):
    d = {'id': id, 'text': text}
    if truth: d['truth'] = True
    if contradicts: d['contradicts'] = contradicts
    if response: d['response'] = response
    if gives: d['gives'] = gives
    if reveals: d['reveals'] = reveals
    return d

def SH(id, ev, a, requires=None, claims=None, gives=None):
    d = {'id': id, 'ev': ev, 'a': a}
    if requires: d['requires'] = requires
    if claims: d['claims'] = claims
    if gives: d['gives'] = gives
    return d

people = [
 {'id': 'kraska', 'name': 'Iwona Kraska', 'role': 'Sekretarz Komisji Ugodowej', 'age': 47,
  'desc': 'Elegancka, w granatowym kostiumie, z teczką pełną kolorowych zakładek. Mówi szybko i uprzejmie, ale za każdym razem sprawdza, kto jeszcze słucha.',
  'deflect': ['Proszę pytać o fakty, a nie o domysły.', 'Ja tylko organizuję posiedzenia. Nic więcej.', 'Na to pytanie odpowie przewodniczący komisji.'],
  'showDefault': ['Nie wiem, co miałabym o tym powiedzieć.', 'To nie ma związku z moją pracą w komisji.'],
  'questions': [
   Q('k-q1', 'Co pani robiła w czwartek wieczorem?', 'Od ósmej siedziałam w centrum biznesowym nad materiałami na piątek, potem poszłam do siebie. Z hotelu nie wychodziłam, padało.', ['k-l1']),
   Q('k-q2', 'Miała pani odebrać doktora Szulca z dworca?', 'Proponowałam mu to SMS-em. Odpisał, że weźmie taksówkę, więc zostałam w hotelu.', ['k-l9']),
   Q('k-q3', 'Kiedy dowiedziała się pani, że doktor zrezygnował?', 'Rano, kwadrans po siódmej, kiedy otworzyłam pocztę. Od razu poprawiłam listę i wydrukowałam ją przed posiedzeniem.', ['k-l4']),
   Q('k-q4', 'Skąd na posiedzeniu wziął się doktor Morawiec?', 'Zadzwoniłam do niego rano, zaraz po przeczytaniu maila. Regulamin na to pozwala, a doktor akurat był w Szczecinie.', ['k-l5']),
   Q('k-q5', 'Kto wybrał dla doktora pokój 214?', 'Hotel. Ja tylko zarezerwowałam pokój dla biegłego, numer przydziela recepcja.', ['k-l7']),
   Q('k-q6', 'Znała pani wnioski z opinii doktora Szulca?', 'Projekt dostałam w środę, zaszyfrowany. Hasło doktor podał mi przez telefon, żebym przygotowała kopie dla komisji. Tak, znałam wnioski.', ['k-c1'], requiresAny=['e36', 'e39']),
   Q('k-q7', 'Co łączy panią ze spółką Restytucja Pomorska i jej prezesem?', 'Nic. Spółkę znam z akt sprawy. Pana Pietrasa nigdy nie spotkałam.', ['k-l6'], requires=['d02']),
  ],
  'statements': [
   S('k-l9', 'Szulc odpisał mi SMS-em, że weźmie taksówkę z dworca.', contradicts=['x1', 'x4'],
     response='Może nie odpisał. Może mi się pomyliło. Miałam tyle wiadomości tego wieczoru.'),
   S('k-l1', 'W czwartek wieczorem nie wychodziłam z hotelu.', contradicts=['e18', 'st:d-c2'],
     response='Dobrze. Pojechałam na dworzec, na wszelki wypadek. Doktora nie było, czekałam kwadrans i wróciłam. Nie mówiłam o tym, bo nie chciałam wyjść na kogoś, kto go zgubił.', reveals=['k-l2']),
   S('k-l2', 'Na dworcu doktora nie było. Czekałam kwadrans i wróciłam sama.', contradicts=['st:m-c3', 'e40', 'x6'],
     response='Wsiadł. Pojechaliśmy do biura komisji w urzędzie, po akta, które miał przejrzeć przed posiedzeniem. Potem podwiozłam go pod hotel i tyle go widziałam.', reveals=['k-l3']),
   S('k-l3', 'Z dworca zawiozłam doktora do biura komisji w urzędzie, a potem pod hotel.', contradicts=['x5', 'x1'],
     response='Więcej nic nie powiem. Doktor wysiadł pod hotelem. Co było dalej, nie wiem.'),
   S('k-l4', 'O rezygnacji doktora dowiedziałam się w piątek o 7:15.', contradicts=['e05'],
     response='Widziałam tego maila w nocy. Nie chciałam nikogo budzić. Poprawiłam listę od razu, żeby rano było mniej zamieszania.'),
   S('k-l5', 'Doktora Morawca poprosiłam w piątek rano, po przeczytaniu maila.', contradicts=['x2', 'st:o-c2'],
     response='Biegły zawsze powinien mieć zastępcę. Zadzwoniłam w czwartek, bo to zwykła ostrożność. Nic więcej w tym nie ma.'),
   S('k-l7', 'Pokój 214 przydzielił doktorowi hotel.', contradicts=['e17'],
     response='Prosiłam o 214, bo doktor chciał spokojnego pokoju. Tak mi powiedział przez telefon.', reveals=['k-l8']),
   S('k-l8', 'Doktor sam prosił o cichy pokój bez okien.', contradicts=['st:m-c4'],
     response='Może źle zrozumiałam. Proszę już o to nie pytać.'),
   S('k-l6', 'Damiana Pietrasa, prezesa Restytucji Pomorskiej, nie znam.', contradicts=['d03', 'd06'],
     response='To mój mąż. Mamy różne nazwiska, bo nie chciałam, żeby ktoś łączył moją pracę z jego interesami. Z tą sprawą nie ma to nic wspólnego.'),
   S('k-c1', 'Znałam wnioski z projektu opinii doktora Szulca od środy.', truth=True),
  ], 'shows': []},
 {'id': 'kosowski', 'name': 'mec. Adrian Kosowski', 'role': 'Pełnomocnik wnioskodawczyni', 'age': 52,
  'desc': 'Adwokat z Warszawy. Drogi garnitur, zmęczone oczy, telefon w ręku. Odpowiada pewnie i dodaje, czego nie musi mówić.',
  'deflect': ['Bez komentarza. Tajemnica adwokacka.', 'Proszę skierować to pytanie na piśmie.', 'Moja klientka ma prawo do ugody. Reszta to państwa problem.'],
  'showDefault': ['I co mam z tym zrobić?', 'Nie widzę tu niczego, co dotyczyłoby mojej klientki.'],
  'questions': [
   Q('a-q1', 'Gdzie pan był w czwartek wieczorem?', 'W barze na dole, od dziewiątej do zamknięcia. Ugoda nie załatwia się sama, miałem sporo telefonów.', ['a-c1']),
   Q('a-q2', 'Czy kontaktował się pan z doktorem Szulcem przed posiedzeniem?', 'Nigdy. Biegły jest niezależny. Pełnomocnikowi nie wolno się z nim kontaktować i nie robiłem tego.', ['a-l1']),
   Q('a-q3', 'Kim jest cesjonariusz roszczenia?', 'Restytucja Pomorska. W 2022 roku kupiła roszczenie od mojej klientki. Pani Rudnicka-Lange ma prawie osiemdziesiąt lat, nie chciała procesu na lata.', ['a-c2']),
   Q('a-q4', 'Co pan wie o znaku wodnym na akcie z 1946 roku?', 'Nic. Słyszę to pierwszy raz. Jeśli to prawda, ktoś oszukał moją klientkę, i to dawno przed mną.', requires=['e39']),
  ],
  'statements': [
   S('a-c1', 'W czwartek od 21:00 do zamknięcia baru siedziałem w barze „Kotwica”.', truth=True),
   S('a-l1', 'Z doktorem Szulcem nigdy się nie kontaktowałem.', contradicts=['e43'],
     response='Napisałem do niego raz. Propozycja konsultacji, wszystko legalne. Odmówił. Na tym sprawa się skończyła i więcej się nie odzywałem.'),
   S('a-c2', 'Restytucja Pomorska kupiła roszczenie od pani Rudnickiej-Lange w 2022 roku.', truth=True),
  ],
  'shows': [
   SH('a-s1', 'd02', 'Restytucja płaci moje faktury jako cesjonariusz. Prezesa, Pietrasa, znam z dwóch spotkań. Żona? Nie mam pojęcia, kim jest jego żona.'),
  ]},
 {'id': 'dabrowska', 'name': 'mec. Ewa Dąbrowska', 'role': 'Radca prawny Urzędu Miasta', 'age': 44,
  'desc': 'Szczupła, w czerwonym płaszczu przewieszonym przez krzesło. To ona nie pozwoliła rano zamknąć sprawy jednym mailem. Waży każde słowo.',
  'deflect': ['Reprezentuję Gminę. Nie mogę o tym mówić.', 'Proszę zapytać sekretariat komisji.', 'Nie będę spekulować.'],
  'showDefault': ['Nie wiem, co to ma wspólnego z doktorem.', 'Tego wcześniej nie widziałam.'],
  'questions': [
   Q('d-q1', 'Kiedy przyjechała pani do hotelu?', 'W piątek, za dwadzieścia dziewiąta. Posiedzenie było o dziewiątej.', ['d-l1']),
   Q('d-q2', 'Dlaczego nalegała pani na otwarcie pokoju?', 'Bo doktor Szulc nie jest człowiekiem, który rezygnuje mailem o północy. We wtorek napisał do mnie, że czuje presję.', ['d-c1']),
   Q('d-q3', 'Co wie pani o opinii doktora Szulca?', 'Tyle, że miała być niekorzystna dla wnioskodawczyni. Szczegółów mi nie podał. Projekt miała tylko sekretarz komisji.'),
  ],
  'statements': [
   S('d-l1', 'W hotelu byłam dopiero w piątek, o 8:40.', contradicts=['x4', 'st:l-c2'],
     response='Przyjechałam w czwartek, około dziesiątej wieczorem. Chciałam porozmawiać z doktorem przed posiedzeniem, sam o to prosił. Czekałam w holu prawie do jedenastej i nie przyszedł. Widziałam za to Iwonę. Za kwadrans jedenasta, może kilka minut wcześniej, weszła od strony parkingu, mokra, z kluczykami w ręku.', reveals=['d-c2']),
   S('d-c1', 'Doktor Szulc pisał mi, że ktoś wywiera na niego presję.', truth=True),
   S('d-c2', 'Około 22:45 Iwona Kraska weszła do hotelu od strony parkingu, mokra, z kluczykami w ręku.', truth=True),
  ],
  'shows': [
   SH('d-s1', 'd03', 'Pietras… Damian. Iwona mówiła kiedyś „mój Damian”, na wigilii w urzędzie. Nie wiedziałam, że to ten Pietras. Ona prowadzi protokoły tej komisji od trzech lat.'),
  ]},
 {'id': 'lis', 'name': 'Bartosz Lis', 'role': 'Nocny recepcjonista', 'age': 24,
  'desc': 'Wezwany z domu po nocnej zmianie. W hotelowej marynarce narzuconej na bluzę, z podkrążonymi oczami. Odpowiada grzecznie, ale za szybko.',
  'deflect': ['Nie pamiętam.', 'To trzeba sprawdzić w systemie.', 'Ja tylko meldowałem gości.'],
  'showDefault': ['Nie kojarzę.', 'Tego nie widziałem, przysięgam.'],
  'questions': [
   Q('l-q1', 'Kto zameldował się w pokoju 214?', 'Doktor Szulc, o 23:05. Przyszedł pieszo od strony parkingu, z walizką. Starszy pan, z brodą, w okularach, w szarym płaszczu i kapeluszu. Mówił mało, pokasływał. Dowód się zgadzał, zeskanowałem go.', ['l-c1']),
   Q('l-q2', 'Czy wieczorem ktoś czekał w holu?', 'Pani mecenas Dąbrowska, znam ją z posiedzeń komisji. Siedziała od kwadransa po dziesiątej prawie do jedenastej i pytała, czy doktor Szulc już jest.', ['l-c2']),
   Q('l-q3', 'Czy w nocy odchodził pan od recepcji?', 'Ani na chwilę. Do siódmej rano siedziałem przy ladzie.', ['l-l1']),
   Q('l-q4', 'Ile kart wydał pan do pokoju 214?', 'Dwie. 214-A gość wziął do ręki, 214-B włożyłem do koperty z mapką hotelu. Tak robimy zawsze.', requires=['e31']),
  ],
  'statements': [
   S('l-c1', 'Gość z 214 przyszedł o 23:05 pieszo od parkingu: starszy, z brodą, w okularach, płaszczu i kapeluszu.', truth=True),
   S('l-c2', 'W czwartek od 22:15 do prawie 23:00 w holu czekała mec. Dąbrowska.', truth=True),
   S('l-l1', 'Przez całą noc ani na chwilę nie odszedłem od recepcji.', contradicts=['e16', 'st:o-c3'],
     response='Wyszedłem na papierosa. Od kwadransa po jedenastej do mniej więcej za dwadzieścia pięć dwunasta byłem w palarni z tyłu. Koło dwudziestej trzeciej dwadzieścia pięć z wyjścia służbowego wyszedł facet w kapeluszu, z parasolem. Poszedł szybko na parking i chwilę później odjechał srebrnym autem. Myślałem, że to ktoś z obsługi.', reveals=['l-c3']),
   S('l-c3', 'Około 23:25 z wyjścia służbowego wyszedł mężczyzna w kapeluszu, z parasolem, i odjechał srebrnym samochodem.', truth=True),
   S('l-c4', 'Mężczyzna zameldowany w 214 miał brodę — taką jak na zdjęciu w dowodzie.', truth=True),
  ],
  'shows': [
   SH('l-s1', 'e42', 'To jest doktor Szulc? Ten pan nie ma brody. Nasz gość miał brodę, siwą, przyciętą. Taką jak na zdjęciu w dowodzie, dlatego się zgadzało. To… to nie był ten człowiek.', claims=['l-c4']),
   SH('l-s2', 'd01', 'Srebrna skoda… Tak, to mogła być ona. Duża, ciemne szyby z tyłu. Stała na końcu parkingu, przy alejce.', requires=['lie:l-l1']),
   SH('l-s3', 'e31', 'To karta 214-A, ta, którą dałem gościowi do ręki. Skąd ona na klatce B? Tamtędy chodzi tylko personel.'),
  ]},
 {'id': 'morawiec', 'name': 'dr Lech Morawiec', 'role': 'Biegły sądowy, badanie dokumentów', 'age': 61,
  'desc': 'Niski, w tweedowej marynarce, z lupą w kieszeni na piersi. Mówi o papierze z czułością, o pieniądzach niechętnie.',
  'deflect': ['To pytanie wykracza poza moją specjalność.', 'Opiniuję dokumenty, nie ludzi.', 'Proszę mnie w to nie mieszać.'],
  'showDefault': ['Mogę na to spojrzeć, ale nic mi to nie mówi.', 'Bez oryginału nie powiem nic pewnego.'],
  'questions': [
   Q('o-q1', 'Kiedy dowiedział się pan o tym posiedzeniu?', 'W piątek rano, za dwadzieścia ósma. Pani Kraska zadzwoniła, a ja przyjechałem prosto z dworca.', ['o-l1']),
   Q('o-q2', 'Czy widział pan oryginał aktu z 1946 roku?', 'Nie, tylko kopię z akt komisji. Na kopii nie ocenię papieru, mogę mówić o piśmie i pieczęci.', ['o-c1']),
   Q('o-q3', 'Co pan robił w czwartek wieczorem?', 'Zjadłem kolację w pokoju i oglądałem telewizję. Koło dwudziestej trzeciej dwadzieścia dzwoniłem do recepcji po dodatkową poduszkę. Nikt nie odebrał, więc dałem spokój.', ['o-c3'], requires=['lie:o-l1']),
  ],
  'statements': [
   S('o-l1', 'Pani Kraska zadzwoniła do mnie w piątek o 7:40, a ja przyjechałem prosto z dworca.', contradicts=['e15', 'x2'],
     response='Dobrze, powiem prawdę. W czwartek miałem rozprawę w sądzie okręgowym. O 19:32 zadzwoniła pani Kraska: proszę zostać w Szczecinie, ekspert może jutro nie dojechać. Zarezerwowałem pokój. Wtedy nie wydało mi się to dziwne.', reveals=['o-c2']),
   S('o-c1', 'Aktu z 1946 roku nie widziałem w oryginale, tylko na kopii.', truth=True),
   S('o-c2', 'W czwartek o 19:32 Kraska prosiła mnie, żebym został w Szczecinie, bo „ekspert może jutro nie dojechać”.', truth=True),
   S('o-c3', 'Około 23:20 dzwoniłem z pokoju do recepcji i nikt nie odebrał.', truth=True),
   S('o-c4', 'Podpis na karcie meldunkowej 214 nakreśliła inna ręka niż wzory podpisów doktora Szulca.', truth=True),
  ],
  'shows': [
   SH('o-s1', 'e13', 'Porównałem z wzorami z archiwum. To nie jest ręka doktora Szulca: inny nacisk, inne połączenia liter, zupełnie inaczej stawiane „z”. Doktor zawsze pisze pełne imię. Ktoś naśladował podpis, i to naprędce.', requires=['e37'], claims=['o-c4']),
   SH('o-s2', 'e39', 'Znak „Wieprza” na papierze z 1946 roku? Papiernia ruszyła w pięćdziesiątym pierwszym. To przesądza sprawę. Gdybym to wiedział rano, nie usiadłbym przy tym stole.'),
  ]},
 {'id': 'marta', 'name': 'Marta Szulc', 'role': 'Żona zaginionego', 'age': 59,
  'desc': 'Przyjechała z Koszalina w dwie godziny. Nauczycielka, ściska w dłoni telefon i torebkę z zapasową insuliną. Mówi cicho i bardzo konkretnie.',
  'deflect': ['Nie wiem. Edward nie opowiadał mi o szczegółach pracy.', 'Proszę go znaleźć. Tylko tyle.', 'Nie umiem na to odpowiedzieć.'],
  'showDefault': ['Nie wiem, co to jest.', 'Nigdy tego nie widziałam.'],
  'questions': [
   Q('m-q1', 'Kiedy ostatnio miała pani kontakt z mężem?', 'O 21:49 dostałam SMS-a: „Jestem. Pani Kraska już czeka przed dworcem, mam z nią jechać. Zadzwonię z hotelu.” Nie zadzwonił. Proszę, tu jest zrzut ekranu.', ['m-c3'], gives=['e44']),
   Q('m-q2', 'Jak mąż wygląda? Ma pani aktualne zdjęcie?', 'Od trzech lat nie nosi brody, goli się codziennie. To zdjęcie z jego urodzin, z lutego.', ['m-c1'], gives=['e42']),
   Q('m-q3', 'Jak groźny jest dla niego brak insuliny?', 'Bierze ją rano i wieczorem. Jeden wstrzykiwacz zawsze ma w teczce, zapasowe w kosmetyczce. Bez insuliny do wieczora może stracić przytomność. A jeśli ktoś dał mu coś na sen…', ['m-c2']),
   Q('m-q4', 'Czy ktoś naciskał na męża w tej sprawie?', 'Przyszedł list od adwokata, z propozycją pieniędzy. Edward był wściekły. Zrobiłam zdjęcie, zanim go schował.', gives=['e43']),
   Q('m-q5', 'Czy mąż bywał wcześniej w hotelu „Gryf”?', 'W październiku 2024 roku, na poprzednim posiedzeniu tej samej komisji. Narzekał na śniadania.', ['m-c5']),
   Q('m-q6', 'Według sekretariatu mąż prosił o pokój bez okien. To możliwe?', 'Nigdy w życiu. Edward ma klaustrofobię, w windzie jeździ z zamkniętymi oczami. Pokój bez okien to dla niego koszmar.', ['m-c4'], requires=['e17']),
  ],
  'statements': [
   S('m-c1', 'Mąż od trzech lat nie nosi brody.', truth=True),
   S('m-c2', 'Bez insuliny mąż może do wieczora stracić przytomność.', truth=True),
   S('m-c3', 'O 21:49 mąż napisał: „Jestem. Pani Kraska już czeka przed dworcem, mam z nią jechać.”', truth=True),
   S('m-c4', 'Mąż ma klaustrofobię. Nigdy nie prosiłby o pokój bez okien.', truth=True),
   S('m-c5', 'W październiku 2024 roku mąż nocował w hotelu „Gryf”.', truth=True),
  ],
  'shows': [
   SH('m-s1', 'e13', 'To nie jest jego podpis. Edward zawsze podpisuje się pełnym imieniem i nazwiskiem, od czterdziestu lat tak samo.'),
   SH('m-s2', 'x3', 'Gryf-Guest… W 2024 roku telefon sam się łączył z tą siecią, Edward się dziwił. Ale tu jest trzecie piętro. Edward miał pokój na drugim. To kto trzymał jego telefon?'),
   SH('m-s3', 'e14', 'To zdjęcie z dowodu z 2018 roku. Wtedy jeszcze nosił brodę. Ogolił się na sześćdziesiąte urodziny i już nie zapuścił.'),
  ]},
]
