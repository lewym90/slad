# Sprawa 007 „Biała cisza” — osoby, pytania, zeznania i reakcje na okazane dowody (część skryptu build_007.py)

def Q(id, q, a, claims=None, requires=None, requiresAny=None, gives=None):
    d = {'id': id, 'q': q, 'a': a}
    if claims: d['claims'] = claims
    if requires: d['requires'] = requires
    if requiresAny: d['requiresAny'] = requiresAny
    if gives: d['gives'] = gives
    return d

def S(id, text, truth=False, contradicts=None, response=None, gives=None, reveals=None):
    d = {'id': id, 'text': text}
    if truth: d['truth'] = True
    if contradicts: d['contradicts'] = contradicts
    if response: d['response'] = response
    if gives: d['gives'] = gives
    if reveals: d['reveals'] = reveals
    return d

def SH(id, ev, a, claims=None, gives=None, requires=None):
    d = {'id': id, 'ev': ev, 'a': a}
    if claims: d['claims'] = claims
    if gives: d['gives'] = gives
    if requires: d['requires'] = requires
    return d

people = [
 {'id': 'adam', 'name': 'Adam Rogala', 'role': 'Kierownik wyprawy „Północ 2028”', 'age': 47, 'at': 'hs',
  'desc': 'Wysoki, ogorzały, z siwiejącą brodą i dawno odmrożonym czubkiem nosa. Autor książki „Dziennik Lodu” o samotnym przejściu Spitsbergenu. Mówi gładko i z przekonaniem, jak na konferencji prasowej.',
  'deflect': ['Prowadziłem wyprawy w gorszych warunkach niż to przesłuchanie.', 'Krystian był moim przyjacielem. Proszę o odrobinę taktu.', 'Nie będę komentował plotek.'],
  'showDefault': ['Nie wiem, co to ma znaczyć.', 'Pierwszy raz to widzę.'],
  'questions': [
   Q('a-q1', 'Jak znaleźliście Krystiana?', 'O szóstej nie zgłosił się przez radio. Wołaliśmy co dziesięć minut — cisza. Zadzwoniłem po GOPR, Tomek Kulig przyjechał skuterem i pojechaliśmy trasą zimową na przełęcz. Leżał pod skałą z masztem, przysypany śniegiem. Drzwi schronu zamknięte, w piecu zimno.', ['a-c1']),
   Q('a-q2', 'Po co Krystian został sam w schronie?', 'Test łączności i baterii w mrozie, dwadzieścia cztery godziny. Na Grenlandii od radia zależy życie. Krystian sam to wymyślił. Łączności o dwudziestej drugiej i o szóstej — tak się umówiliśmy.', ['a-c2']),
   Q('a-q3', 'Gdzie pan był w nocy?', 'Do jedenastej z minutami pisałem w jadalni przemówienie na poniedziałkową konferencję. Potem poszedłem spać. Wiatr mnie obudził, więc koło północy zszedłem na dół. Graliśmy w tysiąca z gospodarzem i Weroniką do wpół do drugiej.', ['a-c3']),
   Q('a-q4', 'Jakie stosunki miał pan z Krystianem?', 'Byliśmy jak bracia. Dziesięć lat wypraw. On siedział przy radiu w bazie, kiedy ja szedłem przez Spitsbergen. Nigdy się nie kłóciliśmy.', ['a-l1']),
   Q('a-q5', 'Słyszał pan łączność po północy?', 'Siedzieliśmy przy kartach, radio stoi w biurze za ścianą. Pan Hampel powiedział: o, Krystian się zgłasza. Słyszałem szum i jego głos. Ucieszyłem się, że wszystko gra.'),
   Q('a-q6', 'Jak wyglądało pana samotne przejście Spitsbergenu?', 'Trzydzieści cztery dni, sześćset czterdzieści kilometrów, sam, z pulką. Wszystko jest w moim dzienniku i w książce. Ekspertyza potwierdziła, że dziennik jest autentyczny.', ['a-l2'], requiresAny=['e25', 'st:n-c2']),
   Q('a-q7', 'Kto korzystał wieczorem z laptopa wyprawy?', 'Igor zgrywa na niego materiały. Koło wpół do dziesiątej siedziała przy nim Weronika — mówiła, że wybiera zdjęcia dla sponsora. Potem poszła na górę z migreną.', ['a-c4'], requires=['st:i-c3']),
  ],
  'statements': [
   S('a-c1', 'Krystian nie zgłosił się o 6:00; ciało znaleźliśmy z ratownikiem o 7:10 pod skałą z masztem.', truth=True),
   S('a-c2', 'Krystian miał dwie łączności z bazą: o 22:00 i o 6:00.', truth=True),
   S('a-c3', 'Do 23:20 pisałem w jadalni, potem spałem, od 0:15 grałem w karty z gospodarzem i Weroniką.', truth=True),
   S('a-c4', 'Około 21:30 przy laptopie wyprawy w jadalni siedziała Weronika.', truth=True),
   S('a-c6', 'Radiotelefon nr 04 zawsze zostaje w biurze schroniska; nikt nie brał go na przełęcz.', truth=True),
   S('a-l1', 'Z Krystianem nigdy się nie kłóciłem.', contradicts=['st:n-c1', 'st:i-c1'],
     response='Dobrze. W czwartek się pokłóciliśmy. Krystian wbił sobie do głowy, że w 2025 roku… Powiedział, że mam czas do poniedziałku, żeby sam wszystko wyznać. Ale ja go nie skrzywdziłem. W piątek wieczorem nie wyszedłem ze schroniska ani na krok.',
     gives=['t1'], reveals=['a-l2']),
   S('a-l2', 'Przeszedłem Spitsbergen sam, o własnych siłach, każdy kilometr.', contradicts=['e25', 'e29'],
     response='Szóstego dnia miałem odmrożone palce i pękniętą płozę pulki. Norweg z Longyearbyen zawiózł mnie skuterem dwieście dziesięć kilometrów na północ. Dziennik przepisałem potem w kraju, jakby tamte dni szedł ktoś inny. Weronika wiedziała od początku — to ona załatwiła ekspertyzę i premię. Krystian chciał to ujawnić w poniedziałek. Ale ja go nie zabiłem. Dla mnie skończyłoby się to wstydem, nie więzieniem.',
     gives=['t2']),
  ],
  'shows': [
   SH('a-s1', 'e07', 'Zero cztery? To zapasowy radiotelefon z biura. Krystian miał na górze stację i swój radiotelefon, dwójkę. Czwórki nikt nie brał na przełęcz, zawsze stoi w ładowarce w bazie.', claims=['a-c6']),
   SH('a-s2', 'e25', 'Skąd to macie? To prywatne papiery Krystiana. Proszę… to nie jest tak, jak wygląda.'),
  ]},

 {'id': 'weronika', 'name': 'Weronika Kos', 'role': 'Menedżerka wyprawy z ramienia sponsora', 'age': 41, 'at': 'hs',
  'desc': 'Drobna, w białej puchówce z logo Polar-Tex, z telefonem w obu dłoniach. Mówi szybko i uprzejmie, jakby prowadziła konferencję. Pod oczami ma cienie, których nie zakrył makijaż.',
  'deflect': ['Rozumiem, że to państwa praca, ale proszę mówić konkretnie.', 'Jestem tu z ramienia sponsora, nie jako śledcza.', 'Od wczoraj mam migrenę, naprawdę nie pamiętam szczegółów.'],
  'showDefault': ['Nie wiem, co mam na to odpowiedzieć.', 'To nie moja działka, proszę zapytać Adama.'],
  'questions': [
   Q('w-q1', 'Gdzie pani była w nocy?', 'Od za kwadrans dziesiąta w pokoju. Migrena, Natalia dała mi tabletkę. Spałam, aż obudził mnie wiatr. Kwadrans po północy zeszłam na dół i graliśmy w karty do wpół do drugiej. Od stołu się nie ruszałam.', ['w-l1', 'w-l5']),
   Q('w-q2', 'Kontaktował się z panią Krystian w piątek?', 'Nie. Ostatni raz rozmawialiśmy w czwartek na przełęczy, o zdjęciach do kampanii. W piątek nie miałam od niego żadnej wiadomości.', ['w-l3']),
   Q('w-q3', 'Jak pani jeździ na nartach?', 'Rekreacyjnie. Chodzę z zespołem na podejścia, bo tego wymaga kontrakt. Jestem z Warszawy i pierwszy raz w życiu jestem w Karkonoszach — w nocy nie znalazłabym tu drogi.', ['w-l0']),
   Q('w-q4', 'Czym zajmuje się pani w wyprawie?', 'Pilnuję kontraktu Polar-Tex: zdjęcia, media, rozliczenia. Za Grenlandię 2028 firma płaci dwa miliony czterysta tysięcy złotych. W poniedziałek mamy konferencję prasową.', ['w-c1']),
   Q('w-q5', 'Co pani wie o przejściu Spitsbergenu z 2025 roku?', 'Wspaniały wyczyn, na którym zbudowaliśmy markę. Poza kontraktem nie mam z tym nic wspólnego. Jeśli coś było nie tak, to sprawa Adama, nie moja.', ['w-l4'], requiresAny=['e25', 't1']),
   Q('w-q6', 'Korzystała pani wieczorem z laptopa wyprawy?', 'Wybierałam zdjęcia z treningu dla działu marketingu. Kilka minut. Niczego z niego nie kopiowałam.', ['w-l6'], requires=['st:a-c4']),
  ],
  'statements': [
   S('w-c1', 'Za wyprawę „Północ 2028” Polar-Tex płaci 2,4 mln zł; w poniedziałek jest konferencja prasowa.', truth=True),
   S('w-l0', 'Jeżdżę na nartach rekreacyjnie, w Karkonoszach jestem pierwszy raz; w nocy nie znalazłabym drogi.', contradicts=['st:i-c4', 'st:n-c4', 'd02'],
     response='Urodziłam się w Jeleniej Górze, w szkole średniej startowałam w zawodach skialpinistycznych — tu, na tych stokach. To było dawno. Nie chciałam, żeby to miało znaczenie.'),
   S('w-l1', 'Od 21:45 do 0:15 byłam w swoim pokoju.', contradicts=['e10', 'e11', 'e13'],
     response='Wyszłam na chwilę. Założyłam narty i doszłam do rozdroża, żeby przewietrzyć głowę po migrenie. Wróciłam przed północą. Nie chciałam, żeby Adam wiedział, że łamię zakaz nocnych wyjść.',
     gives=['t3'], reveals=['w-l2']),
   S('w-l2', 'Doszłam tylko do rozdroża; na przełęczy nie byłam.', contradicts=['x3', 'e18', 'e12'],
     response='Byłam na przełęczy. Chciałam porozmawiać z nim o tej wiadomości. Krzyczał, że w poniedziałek powie wszystko, o mnie też. Odepchnęłam go. Uderzył głową o róg pieca i przestał się ruszać. Nie oddychał, tak myślałam. Wyciągnęłam go pod skałę, żeby wyglądało, że spadł z masztu. Zabrałam jego komunikator i w nocy spaliłam go w suszarni.',
     gives=['t4'], reveals=['w-l5']),
   S('w-l3', 'W piątek nie dostałam od Krystiana żadnej wiadomości.', contradicts=['x2'],
     response='Dostałam. SMS-a z komunikatora, przy kolacji. Pisał, że ma logi z 2025 roku i moje maile, i że w poniedziałek powie wszystko. Wpadłam w panikę, ale to jeszcze niczego nie znaczy.',
     gives=['t5']),
   S('w-l4', 'Sprawa Spitsbergenu to sprawa Adama, nie moja.', contradicts=['e25', 't2'],
     response='Wiedziałam od kwietnia 2025. Krystian mi powiedział, a ja zamówiłam ekspertyzę dziennika, wypłaciłam premię i podpisałam raport dla zarządu, że wszystko sprawdzone. Gdyby to wyszło, straciłabym wszystko. Nie tylko pracę.',
     gives=['t6']),
   S('w-l5', 'Od 0:15 do 1:30 nie odchodziłam od stołu.', contradicts=['st:h-c3', 'e17'],
     response='Wyszłam na kilka minut. Wzięłam z biura zapasowy radiotelefon, stanęłam za tylnymi drzwiami i puściłam do niego z telefonu nagranie Igora — Krystian przy radiu, z czwartku. Chciałam, żeby wszyscy myśleli, że po północy on jeszcze żył.',
     gives=['t7']),
   S('w-l6', 'Z laptopa wyprawy niczego nie kopiowałam.', contradicts=['e14'],
     response='Skopiowałam jeden klip na telefon. Krystian przy radiu. Do filmu dla sponsora, nic więcej.'),
  ],
  'shows': [
   SH('w-s1', 'e13', 'Ktoś z nartami. Wszyscy tu mamy narty.'),
   SH('w-s2', 'e12', 'Popiół z pieca? Nie mam pojęcia, czemu mi to państwo pokazują.'),
  ]},

 {'id': 'igor', 'name': 'Igor Szadkowski', 'role': 'Operator kamery, film dla sponsora', 'age': 29, 'at': 'hs',
  'desc': 'Chudy, w czapce z pomponem, z aparatem na szyi nawet przy śniadaniu. Rzuca żartem, a potem patrzy, czy nikt się nie obraził. Unika wzroku Natalii.',
  'deflect': ['Ja tylko kręcę. Nie jestem od pytań.', 'Serio, nic więcej nie wiem.', 'Mogę pokazać materiał, ale zgadywać nie będę.'],
  'showDefault': ['Nie kojarzę.', 'To nie moje.'],
  'questions': [
   Q('i-q1', 'Gdzie pan był w nocy?', 'Od dziesiątej robiłem timelapse gwiazd na tarasie. Stałem przy aparacie do wpół do pierwszej, zmarzłem na kość. Nikogo nie widziałem.', ['i-l1']),
   Q('i-q2', 'Co działo się w czwartek w schronie?', 'Wieczorem Adam i Krystian pokłócili się przy piecu. Krystian powiedział coś w stylu: masz czas do poniedziałku. Adam trzasnął drzwiami i wyszedł na mróz. Potem obaj udawali, że nic się nie stało.', ['i-c1']),
   Q('i-q3', 'Nagrywał pan Krystiana przy radiu?', 'Jasne, kilka razy. W czwartek tuż przed północą nakręciłem całą łączność z bazą — świetny klip, mróz, para z ust. Plik C0112. Wszystko zgrywam na laptopa wyprawy w jadalni.', ['i-c3'], requires=['e07']),
   Q('i-q4', 'Kto z was najlepiej jeździ na nartach?', 'Weronika. Na nagraniach z treningu zjeżdża tak, że ledwo nadążam z kamerą. Mówiła kiedyś, że startowała w zawodach.', ['i-c4']),
   Q('i-q5', 'Co ustawił pan na tarasie?', 'Aparat na statywie, zdjęcie co trzydzieści sekund, od dziesiątej do wpół do pierwszej. Karta jest w aparacie, możecie obejrzeć klatki.'),
  ],
  'statements': [
   S('i-c1', 'W czwartek w schronie Adam i Krystian pokłócili się; Krystian powiedział Adamowi, że ma czas do poniedziałku.', truth=True),
   S('i-c3', 'W czwartek przed północą nagrał łączność Krystiana z bazą; klip C0112 jest na laptopie wyprawy w jadalni.', truth=True),
   S('i-c4', 'Weronika najlepiej z całego zespołu jeździ na nartach i startowała kiedyś w zawodach.', truth=True),
   S('i-c5', 'Głos z łączności o 0:40 pochodzi z jego czwartkowego klipu C0112.', truth=True),
   S('i-l1', 'Od 22:00 do 0:30 stałem przy aparacie na tarasie.', contradicts=['e13'],
     response='Nie stałem. Ustawiłem aparat i poszedłem do Natalii. Byłem u niej do wpół do pierwszej. Natalia ma narzeczonego, a Adam nie znosi romansów w zespole. Dlatego kłamałem.',
     gives=['t8']),
  ],
  'shows': [
   SH('i-s1', 'e34', 'Przecież to ja! Na końcu mówię „mam” — zawsze tak mówię, kiedy kończę ujęcie. To mój klip, C0112, czwartek przed północą. Skąd on się wziął w łączności z soboty?', claims=['i-c3', 'i-c5']),
  ]},

 {'id': 'natalia', 'name': 'Natalia Brandt', 'role': 'Lekarka wyprawy', 'age': 36, 'at': 'hs',
  'desc': 'Spokojna i rzeczowa, z włosami ściągniętymi w ciasny węzeł. Rano jako pierwsza obejrzała ciało. Mówi cicho, ale bez wahania — dopóki nie padnie pytanie o noc.',
  'deflect': ['Powiedziałam wszystko, co wiem jako lekarz.', 'Proszę nie mieszać mojego życia prywatnego do śledztwa.', 'Nie będę zgadywać.'],
  'showDefault': ['To nie moja specjalność.', 'Nic mi to nie mówi.'],
  'questions': [
   Q('n-q1', 'Co pani ustaliła, oglądając ciało?', 'Rana tłuczona z tyłu głowy, niezbyt głęboka. Ciało wychłodzone, stężenie pośmiertne. Nie żył od kilku godzin — więcej powie sekcja. Mróz bardzo utrudnia określenie godziny.'),
   Q('n-q2', 'Gdzie pani była w nocy?', 'W swoim pokoju. Od wpół do dziesiątej. Sama. Spałam.', ['n-l1']),
   Q('n-q3', 'Co działo się w czwartek w schronie?', 'Adam i Krystian się pokłócili. Krystian powiedział: masz czas do poniedziałku, potem ja to zrobię. Nie wiem, o co chodziło.', ['n-c1']),
   Q('n-q4', 'Jak zachowywała się Weronika w piątek?', 'Przy kolacji przeczytała coś w telefonie i zbladła. Koło wpół do dziesiątej poprosiła mnie o tabletkę na migrenę, a za kwadrans dziesiąta poszła na górę.', ['n-c5']),
   Q('n-q5', 'Kto najlepiej jeździ na nartach?', 'Weronika, bez dwóch zdań. Na treningu zostawiała nas wszystkich w tyle.', ['n-c4']),
   Q('n-q6', 'Co wiedziała pani o przejściu Spitsbergenu?', 'Krystian powiedział raz po kilku piwach, że „Dziennik Lodu” to najlepsza powieść, jaką czytał. Myślałam, że żartuje.', ['n-c2'], requiresAny=['e25', 'st:a-l2']),
  ],
  'statements': [
   S('n-c1', 'W czwartek w schronie Krystian powiedział Adamowi: masz czas do poniedziałku.', truth=True),
   S('n-c2', 'Krystian nazwał kiedyś „Dziennik Lodu” powieścią.', truth=True),
   S('n-c4', 'Weronika najlepiej z zespołu jeździ na nartach.', truth=True),
   S('n-c5', 'Przy kolacji Weronika przeczytała coś w telefonie i zbladła; o 21:45 poszła do pokoju.', truth=True),
   S('n-c6', 'Krystian zmarł z wychłodzenia; uraz głowy tylko go ogłuszył.', truth=True),
   S('n-c7', 'Rana głowy Krystiana pasuje do kantu pieca, a nie do skały.', truth=True),
   S('n-l1', 'W nocy byłam w pokoju sama.', contradicts=['t8'],
     response='Igor był u mnie od dziesiątej do wpół do pierwszej. Żadne z nas nie wychodziło. Proszę, niech to nie trafi do mojego narzeczonego… choć pewnie i tak trafi.',
     gives=['t9']),
  ],
  'shows': [
   SH('n-s1', 'e36', 'Plamy Wiszniewskiego… To znaczy, że zabił go mróz, a nie uderzenie. Uraz głowy go ogłuszył. Ktoś zostawił go nieprzytomnego na śniegu.', claims=['n-c6']),
   SH('n-s2', 'e19', 'Krew i włosy na kancie pieca… Kształt rany by pasował. Uderzył głową o piec, nie o skałę.', claims=['n-c7']),
  ]},

 {'id': 'hampel', 'name': 'Zdzisław Hampel', 'role': 'Gospodarz schroniska „Hala Szronów”', 'age': 63, 'at': 'hs',
  'desc': 'Krępy, w swetrze z reniferami, z fajką, której nie zapala, bo w schronisku nie wolno. Prowadzi schronisko od trzydziestu lat. U jego nóg śpi Bari, wielki kudłaty owczarek.',
  'deflect': ['Ja tu jestem od gotowania i od pieca, panie władzo.', 'Czego nie widziałem, tego nie powiem.', 'Bari może więcej wie, ale on nie gada.'],
  'showDefault': ['Nie znam się na tym.', 'Pierwszy raz widzę.'],
  'questions': [
   Q('h-q1', 'Co działo się w schronisku w piątek wieczorem?', 'Kolacja o szóstej, potem każdy w swoją stronę. Siedziałem w barze przy jadalni do jedenastej dwadzieścia, a pan Adam pisał przy stole — do tej samej godziny, bo razem gasiliśmy światło. Pani Weronika poszła na górę za kwadrans dziesiąta, pani doktor jeszcze wcześniej. Pan Igor kręcił się z aparatem.', ['h-c1']),
   Q('h-q2', 'Słyszał pan łączności Krystiana?', 'Radio stoi w biurze, za ścianą jadalni. O dziesiątej zgłosił się jak zawsze. Potem drugi raz w nocy, koło wpół do pierwszej — graliśmy wtedy w karty. Ucieszyłem się, bo wiało coraz mocniej.', ['h-c2']),
   Q('h-q3', 'Kto grał z panem w karty?', 'Od kwadrans po północy ja, pan Adam i pani Weronika. Do wpół do drugiej. Pani Weronika wyszła raz na kilka minut, koło wpół do pierwszej. Powiedziała, że do łazienki.', ['h-c3']),
   Q('h-q4', 'Czy w nocy coś pana zaniepokoiło?', 'Bari zaszczekał koło wpół do pierwszej, przy tylnych drzwiach. On tak ma, kiedy ktoś się kręci przy suszarni. Pomyślałem, że to ratrakowy.', ['h-c4']),
   Q('h-q5', 'Kto korzysta z suszarni?', 'Wszyscy z wyprawy: suszą tam buty, foki, rękawice. Jest tam piec, który czyszczę codziennie w południe, jak w zegarku.', ['h-c5']),
   Q('h-q6', 'Gdzie stoi zapasowy radiotelefon?', 'W ładowarce w biurze, obok bazowej. Biuro się nie zamyka, to schronisko, nie bank. Rano wszystko stało na swoim miejscu.', ['h-c6'], requiresAny=['e09', 'st:a-c6']),
   Q('h-q7', 'Czy Krystian zgłaszał się też w czwartek?', 'W czwartek cała wyprawa nocowała na górze, ale Krystian i tak zgłosił się do mnie przed północą, na próbę. Pamiętam, bo był straszny mróz i wiatr zupełnie ustał. Mówił tak samo jak zwykle: Baza, tu Mglista, wszystko gra.', ['h-c10'], requires=['e07']),
  ],
  'statements': [
   S('h-c1', 'Do 23:20 siedziałem w barze przy jadalni, a pan Adam pisał w jadalni.', truth=True),
   S('h-c2', 'Około 0:40 przez radio w biurze odezwał się głos Krystiana.', truth=True),
   S('h-c3', 'Około 0:35 pani Weronika na kilka minut odeszła od stołu.', truth=True),
   S('h-c4', 'Około 0:40 Bari zaszczekał przy tylnych drzwiach.', truth=True),
   S('h-c5', 'Piec w suszarni czyszczę codziennie w południe.', truth=True),
   S('h-c6', 'Zapasowy radiotelefon stoi w ładowarce w biurze, które się nie zamyka.', truth=True),
   S('h-c7', 'Żółta taśma odblaskowa na małym plecaku — to plecak pani Weroniki.', truth=True),
   S('h-c8', 'W piecu w suszarni palę tylko drewnem; plastik ktoś wrzucił w nocy.', truth=True),
   S('h-c9', 'Na nagraniu szczeka Bari — a Bari nigdy nie chodzi na przełęcz.', truth=True),
   S('h-c10', 'W czwartek przed północą Krystian zgłosił się przez radio przy mrozie i zupełnej ciszy.', truth=True),
  ],
  'shows': [
   SH('h-s1', 'e12', 'Popiół z pieca w suszarni? Ja tam palę drewnem i starymi gazetami, nie plastikiem. Ktoś tam coś spalił w nocy.', claims=['h-c8']),
   SH('h-s2', 'e13', 'To pod moim tarasem, idą do suszarni. Z nartami na ramieniu, o tej porze? Mały plecak z żółtą taśmą… Takie odblaski ma pani Weronika, sam jej pomagałem przyszyć, bo się odpruwały.', claims=['h-c7']),
   SH('h-s3', 'e33', 'Bari! Poznałbym go wszędzie — dwa razy, krótko, tak szczeka tylko przy tylnych drzwiach. Na przełęcz nie chodzi, stary już. Całą noc był tutaj, w korytarzu.', claims=['h-c9']),
  ]},

 {'id': 'kuznik', 'name': 'Mirosław Kuźnik', 'role': 'Operator ratraku', 'age': 52, 'at': 'gar',
  'desc': 'Barczysty, w kombinezonie poplamionym smarem, z wąsem jak szczotka. Ratrakiem jeździ od dwudziestu lat i zna tu każdy kamień. Mieszka w pokoiku przy garażu.',
  'deflect': ['Ja w nocy jeżdżę, nie gapię się na ludzi.', 'Pan pyta, ja mówię, ale zmyślać nie będę.', 'Przez szybę mało widać, jak sypie.'],
  'showDefault': ['Nie wiem, panie.', 'Nic mi to nie mówi.'],
  'questions': [
   Q('k-q1', 'Co pan robił w piątek wieczorem?', 'Od dziesiątej do za dwadzieścia jedenasta równałem drogę dojazdową poniżej schroniska. Potem przerwa w garażu. Od dwadzieścia po dwunastej do dziesięć po pierwszej równałem plac przed schroniskiem.', ['k-c1']),
   Q('k-q2', 'Widział pan kogoś na szlaku?', 'Koło dziesięć po dziesiątej czołówka szła w górę zielonym szlakiem za schroniskiem. Równo i szybko, jak ktoś, kto umie chodzić. A koło wpół do dwunastej, z okna garażu, światło zjechało z góry — tak szybko, że to musiał być narciarz.', ['k-c2', 'k-c3']),
   Q('k-q3', 'Czy ratrak wydaje jakieś sygnały?', 'Na wstecznym pika, jak każda maszyna. Kiedy równam plac, ciągle cofam, więc pika co chwilę. Ludzie się skarżą, ale przepisy to przepisy.', ['k-c4']),
   Q('k-q4', 'Czy ratrak zapisuje trasę?', 'GPS zapisuje wszystko, dla zarządu parku. Wydruk mam w kabinie.'),
  ],
  'statements': [
   S('k-c1', 'Od 22:00 do 22:40 równałem drogę poniżej schroniska, do 0:20 miałem przerwę w garażu, a od 0:20 do 1:10 równałem plac przed schroniskiem.', truth=True),
   S('k-c2', 'Około 22:10 czyjaś czołówka szła szybko w górę zielonym szlakiem.', truth=True),
   S('k-c3', 'Około 23:35 światło bardzo szybko zjechało z góry — jak narciarz.', truth=True),
   S('k-c4', 'Ratrak pika przy cofaniu; od 0:20 do 1:10 cofałem wiele razy na placu przed schroniskiem.', truth=True),
  ],
  'shows': [
   SH('k-s1', 'e35', 'To mój ratrak, na wstecznym. Tak pika tylko jedna maszyna w okolicy. W nocy cofałem tylko na placu przed schroniskiem, od dwadzieścia po dwunastej.', claims=['k-c4']),
  ]},
]
