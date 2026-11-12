# Sprawa 004 „Martwy kanał” — osoby, pytania i zeznania (część skryptu build_004.py)
from b004_evidence import T, D, F

def Q(id, q, a, claims=None, requires=None, requiresAny=None, time=None):
    d = {'id': id, 'q': q, 'a': a}
    if claims: d['claims'] = claims
    if requires: d['requires'] = requires
    if requiresAny: d['requiresAny'] = requiresAny
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

people = [
 {'id': 'kopec', 'name': 'Dariusz Kopeć', 'role': 'Inżynier serwisowy, Syreon Polska', 'age': 49,
  'desc': 'Szczupły, w granatowej kurtce firmowej, spokojny. Mówi technicznie i rzeczowo, a gdy pytania stają się osobiste, patrzy w bok.',
  'deflect': ['To pytanie do działu prawnego.', 'Proszę nie mylić serwisu z winą.', 'Mam dokumentację. Dla mnie sprawa jest jasna.'],
  'questions': [
   Q('k-q1', 'Gdzie pan spędził noc z czwartku na piątek?', 'W domu, w Zabrzu. Skończyłem pracę o szesnastej, położyłem się przed północą. Żona to potwierdzi.', ['k-l1']),
   Q('k-q2', 'Jaka jest pana rola w systemie SYRION-4?', 'Jestem inżynierem Syreon Polska. W 2024 wdrażałem ten system i podpisałem odbiór za wykonawcę. Dziś prowadzę serwis i gwarancję.', ['k-c1']),
   Q('k-q3', 'Zgłoszenie MW-2611 jest na pana. Kto zatwierdził to okno serwisowe?', 'Wiceprezydent Szczerba. Szybciej niż czekać na pana Lasotę. Zatwierdzenie miałem w systemie jeszcze wieczorem.', ['k-c2'], requires=['e32']),
   Q('k-q4', 'Co pan robił na stacji od 0:41?', 'Wymieniałem moduł K3. Tryb SERWIS włączyłem tylko na jakieś dwadzieścia minut, żeby podłączyć kabel, potem wróciłem do PRACA.', ['k-l4'], requires=['lie:k-l1']),
   Q('k-q5', 'Czy ktoś do pana dzwonił tej nocy?', 'Nikt. Telefon miałem wyciszony, bo pracowałem przy antenie.', ['k-l7'], requiresAny=['x1', 'e17']),
   Q('k-q6', 'Okno miało trwać do trzeciej, a tryb SERWIS trwał prawie dwie godziny. Dlaczego tak długo?', 'K3 to skomplikowana konfiguracja i nie wszystko zależy od mnie. Nie widzę tu niczego dziwnego.', requires=['p-service']),
   Q('k-q7', 'W szafie do złącza K3 podłączono sztuczne obciążenie zamiast anteny. Dlaczego?', 'To była tymczasowa atrapa na czas wymiany modułu. Tak się robi w serwisie, żeby nie uszkodzić nadajnika.', ['k-l8'], requires=['e11']),
  ],
  'statements': [
   S('k-l1', 'Całą noc spędził w domu w Zabrzu.', contradicts=['e12', 'x2', 'x3'],
     response='Dobrze. Byłem na Kolonii. Zgłoszenie było moje, wymieniałem moduł K3. Wszedłem o 0:41, wyszedłem koło drugiej. Lasoty nie widziałem na oczy.', gives=['t01'], reveals=['k-l2', 'k-l3']),
   S('k-c1', 'W 2024 roku wdrażał SYRION-4 i podpisał protokół odbioru za wykonawcę.', truth=True),
   S('k-c2', 'Okno serwisowe MW-2611 zatwierdził wiceprezydent Szczerba.', truth=True),
   S('k-l2', 'Wyszedł ze stacji około drugiej w nocy.', contradicts=['e12', 'e09', 'x3'],
     response='Dobrze, przeciągnęło się do trzeciej. Antena, konfiguracja. Ale Lasoty tam nie było, przysięgam.', gives=['t02']),
   S('k-l3', 'Lasoty tej nocy nie widział.', contradicts=['e12', 'e44'],
     response='Zjawił się koło wpół do trzeciej. Pokłóciliśmy się o K3. Wyszedł na dwór zadzwonić, a ja zostałem przy szafie.', gives=['t03'], reveals=['k-l5']),
   S('k-l5', 'Lasota wyszedł ze stacji żywy.', contradicts=['e12', 'x4'],
     response='Doszło do szarpaniny. Złapał za szyny i rąbnęło go. To był wypadek, nieszczęśliwy wypadek.', reveals=['k-l6']),
   S('k-l6', 'Lasota zginął w nieszczęśliwym wypadku, dotknąwszy szyn rozdzielni.', contradicts=['x4', 'e13', 'e42'],
     response='Chciał to zgłosić rano. Wszystko, K3, aneks. Złapałem klucz. Jedno uderzenie. Potem ułożyłem go przy szynach.', gives=['t05']),
   S('k-l4', 'Tryb SERWIS trwał około dwudziestu minut.', contradicts=['e09', 'e16'],
     response='Dobrze, trwał dłużej. Nie chciałem wychodzić z trybu, dopóki nie skończę konfiguracji.'),
   S('k-l7', 'Nikt nie dzwonił do niego tej nocy.', contradicts=['x1', 'st:b-c1'],
     response='Dzwoniła operatorka, potem wiceprezydent. Obojgu powiedziałem, że to fałszywy alarm z Chemrudu.', gives=['t04']),
   S('k-l8', 'Sztuczne obciążenie przy K3 było tylko tymczasowe, na czas wymiany modułu.', contradicts=['e31', 'e43', 'e30'],
     response='Nie było czego wymieniać. K3 wykreślono z dostawy, żeby zmieścić się w budżecie. Odbiór podpisał wiceprezydent.', gives=['t14']),
  ]},

 {'id': 'burda', 'name': 'Agnieszka Burda', 'role': 'Operatorka dyżurna CZK', 'age': 38,
  'desc': 'Drobna, w służbowym polarze, z opuchniętymi oczami po nocnej zmianie. Mówi szybko i nerwowo skubie rękaw.',
  'deflect': ['Jestem tylko operatorem, nie administratorem.', 'Robiłam to, co mówi procedura.', 'Proszę mnie nie przesłuchiwać na korytarzu.'],
  'questions': [
   Q('b-q1', 'Proszę opisać swoją zmianę.', 'Dyżur od osiemnastej. W nocy cisza, test łącza o 0:12 w porządku. Żądanie alarmu z Chemrud do mnie nie dotarło, system niczego nie pokazał.', ['b-l1']),
   Q('b-q2', 'Czy w nocy było otwarte okno serwisowe na nadajniku?', 'Tak, MW-2611, od północy. Widziałam na konsoli status SERWIS od 1:03.', ['b-c2']),
   Q('b-q3', 'Czy kasowała pani coś z archiwum alarmów?', 'Nie. Mogę usuwać tylko zapisy testowe, a testowych tej nocy nie było. Niczego nie usuwałam.', ['b-l2'], requires=['x5']),
   Q('b-q4', 'Dlaczego nie zgłosiła pani żądania do 112, tylko zadzwoniła do serwisanta?', 'Procedura mówi: najpierw serwis. Kopeć powiedział, że to test. Nie chciałam fałszywego alarmu na własną rękę.', requires=['lie:b-l1']),
   Q('b-q5', 'O czym rozmawiała pani z wiceprezydentem o 3:35?', 'O tym, żeby usunąć zapis. Powiedział, że to błąd czujnika i że rano zgłosimy usterkę. Nie wiedziałam, że ludzie trafili do szpitala.', ['b-c3'], requiresAny=['x1', 'lie:b-l2']),
  ],
  'statements': [
   S('b-l1', 'Żądanie alarmu nie dotarło do centrum, system niczego nie pokazał.', contradicts=['e17', 'e18', 'x1'],
     response='Widziałam czerwony pasek „brak potwierdzenia”. Zadzwoniłam do serwisu. Kopeć powiedział, że to ich test czujnika, żebym niczego nie ruszała.', gives=['t06'], reveals=['b-c1']),
   S('b-c1', 'Kopeć powiedział jej przez telefon, że to test czujnika i żeby niczego nie ruszała.', truth=True),
   S('b-c2', 'Konsola pokazywała SN-1 w trybie SERWIS od 1:03.', truth=True),
   S('b-l2', 'Niczego nie usuwała z archiwum alarmów.', contradicts=['x5'],
     response='Wiceprezydent kazał skasować zapis jako testowy, żeby nie robić paniki w mediach. Wpisałam swój PIN. Nie wiedziałam, że ktoś zginął.', gives=['t07']),
   S('b-c3', 'O 3:35 wiceprezydent Szczerba polecił jej usunąć zapis alarmu.', truth=True),
  ]},

 {'id': 'szczerba', 'name': 'Piotr Szczerba', 'role': 'Wiceprezydent miasta', 'age': 51,
  'desc': 'Gładko ogolony, w drogim płaszczu, uprzejmy i zdystansowany. Zaczyna zdania od słów „jak państwo wiedzą”.',
  'deflect': ['Proszę kierować pytania do biura prasowego.', 'Jestem do dyspozycji, ale nie będę zgadywał.', 'To sprawa operacyjna, nie polityczna.'],
  'questions': [
   Q('s-q1', 'Co pan robił w nocy z czwartku na piątek?', 'Spałem. Położyłem się o 23:30, o niczym nie wiedziałem do rana. O wycieku dowiedziałem się z radia.', ['s-l1']),
   Q('s-q2', 'Okno MW-2611 zatwierdzone jest pana nazwiskiem. Dlaczego nie administrator?', 'Okno zatwierdził pan Lasota. Wpis przy moim nazwisku to błąd systemu.', ['s-l2'], requires=['e32']),
   Q('s-q3', 'Podpisał pan protokół odbioru SYRION-4. Czy kanał K3 był przetestowany?', 'Oczywiście. Protokół jest jednoznaczny: test pozytywny, 25 watów. Nie mam powodu wątpić.', ['s-l3'], requires=['e28']),
   Q('s-q4', 'Faktura Alfa-Doradztwo wystawiona została dla Syreon. Kim jest prezes tej spółki?', 'Nie znam tej firmy ani jej prezesa. Syreon ma wielu doradców.', ['s-l4'], requires=['e33']),
   Q('s-q5', 'Kto zdecydował o wykreśleniu K3 z dostaw w 2024 roku?', 'Kopeć zaproponował oszczędność. Podpisałem aneks, bo wyglądał rozsądnie. Resztę załatwiał serwis.', ['s-c2'], requires=['lie:s-l3']),
  ],
  'statements': [
   S('s-l1', 'Spał od 23:30 do rana i o niczym nie wiedział.', contradicts=['x1'],
     response='Pyka dzwonił koło drugiej, pytał, czy syreny wyły. Zadzwoniłem do Kopecia, potem nad ranem do operatorki. Chciałem uniknąć paniki.', gives=['t08'], reveals=['s-c1']),
   S('s-c1', 'Pyka zadzwonił do niego około drugiej z pytaniem, czy syreny wyły.', truth=True),
   S('s-l2', 'Okno MW-2611 zatwierdził Lasota; wpis z jego nazwiskiem to błąd systemu.', contradicts=['e32', 'st:k-c2'],
     response='Zatwierdziłem sam. Kopeć prosił, a Lasota zawsze się certolił. Uznałem, że to formalność.'),
   S('s-l3', 'Kanał K3 został poprawnie przetestowany przy odbiorze.', contradicts=['e30', 'e31', 'e11'],
     response='Podpisałem, co dał serwis. Do dziś nie sprawdzałem, czy K3 działa. Serwis mówił, że działa.', gives=['t09']),
   S('s-c2', 'K3 wykreślono z dostaw z inicjatywy Kopecia, a Szczerba podpisał aneks.', truth=True),
   S('s-l4', 'Nie zna firmy Alfa-Doradztwo ani jej prezesa.', contradicts=['e33'],
     response='To firma mojej żony. Usługa doradcza była legalna. Nie widzę związku ze sprawą.'),
  ]},

 {'id': 'hajduk', 'name': 'Lena Hajduk', 'role': 'Dziennikarka „Głosu Rudy”', 'age': 33,
  'desc': 'Szczupła, w skórzanej kurtce, z notatnikiem w kieszeni. Odpowiada uprzejmie, ale z dystansem, jak ktoś przyzwyczajony do pytań z drugiej strony.',
  'deflect': ['Chronię źródła informacji.', 'Tajemnica dziennikarska nie podlega negocjacjom.', 'Nie jestem podejrzana.'],
  'questions': [
   Q('h-q1', 'Czy rozmawiała pani w nocy z Lasotą albo widziała się z nim?', 'Nie. Ani w czwartek, ani w piątek. Znam go zawodowo, to wszystko.', ['h-l1']),
   Q('h-q2', 'Gdzie pani była po północy?', 'W domu, na osiedlu Parkowe. Pracowałam nad tekstem. Nigdzie nie jeździłam.', ['h-l2']),
   Q('h-q3', 'Co pani widziała pod stacją nadawczą?', 'Biały bus z drabiną na dachu wyjechał z bramy o 3:12. Kierowcy nie widziałam, było ciemno.', ['h-c2'], requires=['lie:h-l2']),
   Q('h-q4', 'Co dostała pani od Lasoty o północy?', 'Pendrive z telemetrią K3 i kopię protokołu odbioru. Mówił, że kanał rezerwowy to atrapa i że rano NIK dostanie to samo.', ['h-c1'], requires=['lie:h-l1']),
  ],
  'statements': [
   S('h-l1', 'Tej nocy nie rozmawiała z Lasotą ani się z nim nie widziała.', contradicts=['e34', 'e37', 'x1'],
     response='Spotkałam się z nim o północy. Dał mi pendrive z telemetrią K3 i protokół. Powiedział, że rano wszystko wyjdzie. Nie mówiłam, bo chronię źródło.', gives=['t10']),
   S('h-c1', 'Lasota dał jej pendrive z telemetrią K3 i powiedział, że kanał rezerwowy to atrapa.', truth=True),
   S('h-l2', 'Po północy była w domu i nie jeździła na Kolonię.', contradicts=['e34', 'x2'],
     response='Zadzwonił o drugiej trzydzieści cztery: „Przyjedź, to pilne”. Wjechałam w las o trzeciej pięć, pod bramą byłam kilka minut później. Brama zamknięta, w stacji światło.', gives=['t11', 'e38']),
   S('h-c2', 'O 3:12 z bramy stacji wyjechał biały bus z drabiną na dachu.', truth=True),
  ]},

 {'id': 'pyka', 'name': 'Witold Pyka', 'role': 'Prezes Chemrud S.A.', 'age': 60,
  'desc': 'Potężny, w kamizelce i szytej na miarę koszuli, głos jak z mównicy. Odpowiada, jakby wygłaszał oświadczenie.',
  'deflect': ['Moi prawnicy zajmą się wszystkimi pytaniami.', 'Zakład działał zgodnie z procedurami.', 'To nie jest miejsce na takie insynuacje.'],
  'questions': [
   Q('y-q1', 'Kiedy dowiedział się pan o wycieku?', 'Rano, z telefonu od zastępcy. Noc spędziłem w domu, spałem.', ['y-l1']),
   Q('y-q2', 'Czy wyciek był groźny dla mieszkańców?', 'Nie. To była niewielka nieszczelność. Alarm syren nie był potrzebny.', ['y-l2']),
   Q('y-q3', 'Czy rozmawiał pan tej nocy z kimś z urzędu miasta?', 'Nie. Z nikim.', ['y-l3'], requires=['x1']),
   Q('y-q4', 'Dlaczego wymienił pan zawór Cl-3 na tańszy zamiennik?', 'To decyzja ekonomiczna, zgodna z normami. Nie będę jej tłumaczył w tonie śledztwa.', requires=['e23']),
  ],
  'statements': [
   S('y-l1', 'O wycieku dowiedział się dopiero rano.', contradicts=['e22', 'x1'],
     response='Wiedziałem od 1:52. Orlik zadzwonił, uznałem, że zakład opanuje to sam. Nie wezwałem straży, bo nie chciałem kolejnej kontroli.', gives=['t12']),
   S('y-l2', 'Wyciek był niewielki i alarm syren nie był potrzebny.', contradicts=['e21', 'e25', 'e26'],
     response='Czujniki dawały u nas fałszywe alarmy. Byłem przekonany, że sytuacja jest pod kontrolą.'),
   S('y-l3', 'Tej nocy z nikim z urzędu miasta nie rozmawiał.', contradicts=['x1', 'st:s-c1'],
     response='Dzwoniłem do wiceprezydenta, bo zobaczyłem, że miasto milczy. Zapytałem, czy syreny wyły. Powiedział: „Zajmę się tym”.', gives=['t13']),
  ]},
]
