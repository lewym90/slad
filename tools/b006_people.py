# Sprawa 006 „Ostatni seans” — osoby, pytania, zeznania i reakcje na okazane dowody (część skryptu build_006.py)
from b006_evidence import T, D, N

def Q(id, q, a, claims=None, requires=None, requiresAny=None, gives=None, time=None):
    d = {'id': id, 'q': q, 'a': a}
    if claims: d['claims'] = claims
    if requires: d['requires'] = requires
    if requiresAny: d['requiresAny'] = requiresAny
    if gives: d['gives'] = gives
    if time: d['time'] = time
    return d

def S(id, text, truth=False, contradicts=None, response=None, gives=None, reveals=None, mistake=False, time=None):
    d = {'id': id, 'text': text}
    if truth: d['truth'] = True
    if mistake: d['mistake'] = True
    if contradicts: d['contradicts'] = contradicts
    if response: d['response'] = response
    if gives: d['gives'] = gives
    if reveals: d['reveals'] = reveals
    if time: d['time'] = time
    return d

def SH(id, ev, a, requires=None, claims=None, gives=None):
    d = {'id': id, 'ev': ev, 'a': a}
    if requires: d['requires'] = requires
    if claims: d['claims'] = claims
    if gives: d['gives'] = gives
    return d

people = [
 {'id': 'ewa', 'name': 'Ewa Sitek', 'role': 'Kierowniczka kina „Zorza”', 'age': 52,
  'desc': 'Szczupła, w czarnym golfie, z perfekcyjnie upiętymi włosami. To ona wymyśliła „Ostatni seans”. Mówi spokojnie i rzeczowo, tylko co chwilę obraca obrączkę na palcu.',
  'deflect': ['Proszę mnie nie łapać za słowa.', 'Prowadzę to kino od dwudziestu lat. Nie wiem, do czego pan zmierza.', 'Wczoraj był najtrudniejszy wieczór w moim życiu. Proszę o fakty.'],
  'showDefault': ['Nie rozumiem, co to ma wspólnego z panem Leonem.', 'Widzę to pierwszy raz.'],
  'questions': [
   Q('ew-q1', 'Gdzie pani była w czasie seansu?', 'W biurze, od pięć po ósmej. Liczyłam utarg z biletów i układałam przemówienie na pożegnanie. Nie ruszałam się stamtąd do końca filmu.', ['e-l1']),
   Q('ew-q2', 'Jak znaleźliście pana Leona?', 'Nie zszedł na pożegnanie. O wpół do jedenastej poszłam z Damianem na górę. Drzwi zamknięte, pukałam, cisza. Otworzyłam zapasowym kluczem. Leżał przy przewijarce, obok ta puszka. Lampa w projektorze jeszcze świeciła.', ['e-c1']),
   Q('ew-q3', 'Dlaczego to pani zapaliła światło na sali?', 'Bo ekran zrobił się biały, a z kabiny nic. Pomyślałam, że pan Leon się wzruszył — ostatni seans w jego życiu. Ktoś musiał zapalić, ludzie siedzieli po ciemku.', ['e-c2']),
   Q('ew-q4', 'Kto w kinie umie zmienić projektor w trakcie seansu?', 'Pan Leon i Damian, którego pan Leon uczył. Ja się na tym nie znam. Nigdy w życiu nie obsługiwałam projektora, jestem od papierów i ludzi.', ['e-l7']),
   Q('ew-q5', 'Co z plakatami w gablocie, kiedy kino zostanie zamknięte?', 'To duma „Zorzy”. Cztery oryginały, wiszą tu od lat. Po zamknięciu trafią do muzeum kinematografii, już to uzgodniłam.', ['e-l5']),
   Q('ew-q6', 'Wiedziała pani, co pan Leon chciał powiedzieć po seansie?', 'Miał przemówić na pożegnaniu, jak wszyscy. Nie wiem, co przygotował. Nie pokazywał mi tekstu.', requiresAny=['st:j-c3', 'e12']),
   Q('ew-q7', 'Dlaczego od razu powiedziała pani, że puszka spadła z półki?', 'Bo tak to wyglądało. Leżała pod regałem. Co miałam pomyśleć? Że ktoś... Nie, wtedy nawet przez myśl mi to nie przeszło.', requires=['st:d-c4']),
  ],
  'statements': [
   S('e-c1', 'O 22:41 otworzyłam kabinę zapasowym kluczem i znalazłam pana Leona.', truth=True),
   S('e-c2', 'Pod koniec filmu zapaliłam światło na sali panelem przy drzwiach.', truth=True),
   S('e-l1', 'Przez cały seans nie wychodziłam z biura.', contradicts=['st:j-c2', 'x5'],
     response='Raz wyszłam. Około dziesięć po dziewiątej wyniosłam do kontenera kartony z baru. Kilka minut, nic ważnego. Zapomniałam o tym.', reveals=['e-l2']),
   S('e-l2', 'Na podwórku byłam kilka minut, tylko przy kontenerze, około 21:10.', contradicts=['x5', 'e16', 't4'],
     response='Wyszłam wcześniej, za dwadzieścia dziewiąta. Drzwi kabiny były otwarte, weszłam po schodach, żeby zamienić słowo z panem Leonem. On leżał na podłodze. Zamknęłam drzwi i zbiegłam. Potem stałam pod daszkiem i nie mogłam się ruszyć. Nie wiem, jak długo.',
     gives=['t5'], reveals=['e-l3']),
   S('e-l3', 'W kabinie byłam tylko chwilę i od razu zbiegłam.', contradicts=['e26', 'x5', 't4'],
     response='Byłam dłużej. Kiedy kończyła się pierwsza część, zmieniłam projektor. Pan Leon sam mnie tego nauczył, trzydzieści lat temu. Nie mogłam pozwolić, żeby ostatni seans się urwał. Wyszłam, kiedy zaczęło padać. Ale on już leżał, kiedy weszłam. Ja go nie zabiłam.',
     gives=['t6'], reveals=['e-l4']),
   S('e-l4', 'Nie zabiłam pana Leona. Kiedy weszłam, już leżał.', contradicts=['e27', 'x2'],
     response='Pokazał mi ten list. Powiedział, że po seansie wręczy go pani Wrzos, przy wszystkich, przy dziennikarzach. Dwadzieścia lat tego kina — i miałam wyjść na złodziejkę na jego pożegnaniu. Puszka stała na stole przewijarki. Nie pamiętam, kiedy ją chwyciłam. Potem myślałam już tylko o jednym: film musi iść. Póki szedł, wszyscy myśleli, że on żyje.',
     gives=['t7']),
   S('e-l5', 'W gablocie wiszą cztery oryginały.', contradicts=['e13', 'e17', 'e27'],
     response='Dwa to faksymile. Zamówiłam je, żeby oryginały nie blakły w świetle foyer. Oryginały są bezpieczne, leżą u mnie w domu.', reveals=['e-l6']),
   S('e-l6', 'Oryginały obu plakatów leżą bezpieczne u mnie w domu.', contradicts=['d02', 'd03'],
     response='Nie ma ich w domu. Mąż oddał je do aukcji przez swoją firmę. Kino zamykają, kolekcja i tak poszłaby do magazynu, a my toniemy w długach. Myślałam, że nikt nie zauważy różnicy. Nikt poza nim.',
     gives=['t8']),
   S('e-l7', 'Nigdy w życiu nie obsługiwałam projektora.', contradicts=['st:j-c6', 'd01', 't6'],
     response='Na zdjęciu jestem ja. Przed ślubem nazywałam się Kalinowska. Przez pięć lat siedziałam w tej kabinie obok pana Leona. Potem przeszłam do biura i nikt już o tym nie pamiętał.',
     gives=['t9']),
  ],
  'shows': [
   SH('ew-s1', 'e09', 'Stare zdjęcie. Pan Leon miał w kabinie mnóstwo pamiątek. Nie wiem, czemu mi je państwo pokazują.'),
   SH('ew-s2', 'e16', 'Mój płaszcz. Zahaczyłam o coś przy kontenerze. Na podwórku wszystko jest zardzewiałe.'),
   SH('ew-s3', 'x6', 'Plakaty z tych lat drukowano w tysiącach egzemplarzy. Na aukcjach jest ich pełno.'),
  ]},

 {'id': 'damian', 'name': 'Damian Wróbel', 'role': 'Technik projekcji', 'age': 31,
  'desc': 'Wysoki, w czarnej bluzie z logo „Zorzy” i z kucykiem. Od trzech lat uczył się u pana Leona projekcji z taśmy. Ma czerwone oczy i nie wypuszcza z ręki telefonu.',
  'deflect': ['Ja tylko obsługuję projektor. Nic więcej nie wiem.', 'Pan Leon był dla mnie jak dziadek. Naprawdę myślicie, że…', 'Nie pamiętam, serio. Byłem w szoku.'],
  'showDefault': ['Nie wiem, co mam o tym powiedzieć.', 'To nie moja działka.'],
  'questions': [
   Q('d-q1', 'Gdzie pan był w czasie seansu?', 'Przy barze z panią Joanną, szykowaliśmy pożegnanie. Za pięć dziewiąta wyszedłem zapalić na podwórko, wróciłem po kwadransie. Nikogo tam nie było.', ['d-l1']),
   Q('d-q2', 'Jak pan Leon prowadził projekcję z taśmy?', 'Jak zegarek. Każdą zmianę projektora wpisywał do dziennika, co do minuty. A pierwszą część przewijał od razu, kiedy szła druga. Mówił, że szpula na stole ma być gotowa, zanim film się skończy.', ['d-c1']),
   Q('d-q3', 'Kto poza panem Leonem umie zmienić projektor?', 'Ja. Uczył mnie od trzech lat. Wczoraj chciał zrobić wszystko sam, to był jego wieczór. Nie byłem w kabinie ani razu w czasie seansu.', ['d-c2']),
   Q('d-q4', 'Dlaczego drzwi pożarowe kabiny były otwarte w czasie seansu?', 'Pan Leon zawsze je klinował. Dwa projektory z lampami ksenonowymi — w kabinie jest jak w saunie. Miał taki stary drewniany klin na czerwonym sznurku.', ['d-c3']),
   Q('d-q5', 'Co pan zobaczył, kiedy weszliście do kabiny?', 'Pani Ewa otworzyła drzwi zapasowym kluczem. Pan Leon leżał przy przewijarce. W projektorze B jeszcze świeciła lampa, zgasiłem ją. Pani Ewa od razu powiedziała, że puszka musiała spaść z półki.', ['d-c4']),
  ],
  'statements': [
   S('d-c1', 'Pan Leon wpisywał każdą zmianę do dziennika i od razu przewijał pierwszą część.', truth=True),
   S('d-c2', 'W czasie seansu nie byłem w kabinie ani razu.', truth=True),
   S('d-c3', 'Pan Leon zawsze klinował drzwi pożarowe kabiny, bo lampy grzeją.', truth=True),
   S('d-c4', 'Pani Ewa od razu powiedziała, że puszka spadła z półki.', truth=True),
   S('d-c5', 'Pan Leon wpisywał do dziennika każdą zmianę projektora. Jeśli jej nie wpisał, to nie on ją zrobił.', truth=True),
   S('d-l1', 'Od 20:55 do 21:10 paliłem na podwórku i nikogo tam nie widziałem.', contradicts=['x4', 'x3', 'st:j-c5'],
     response='Dobra. Nie byłem na podwórku. Poszedłem do Żabki po wódkę i papierosy na po imprezie. Pani Ewa zakazała alkoholu, więc nie chciałem się przyznać. Wróciłem frontem, przez foyer.',
     gives=['t1']),
  ],
  'shows': [
   SH('d-s1', 'e06', 'Nie ma zmiany projektora. Pan Leon wpisał każdą od pięćdziesięciu lat, nawet na seansie dla trzech osób. Jeśli jej nie wpisał, to nie on ją zrobił.', claims=['d-c5']),
   SH('d-s2', 'e07', 'Pierwsza część nieprzewinięta? Pan Leon zabrałby się za to, gdy tylko ruszyła druga. Chyba że już nie mógł.'),
   SH('d-s3', 'e09', 'Nie wiem, kto to jest. Pan Leon mówił kiedyś, że przede mną miał tylko jedną uczennicę, dawno temu, i że była lepsza od niego.'),
  ]},

 {'id': 'grzegorz', 'name': 'Grzegorz Barcz', 'role': 'Syn kinooperatora', 'age': 46,
  'desc': 'Przyjechał z Warszawy na pożegnanie kina ojca. Drogi płaszcz, zmęczona twarz, telefon, który co chwilę wibruje. Odpowiada krótko i patrzy w podłogę.',
  'deflect': ['To był mój ojciec. Proszę o trochę szacunku.', 'Nie mam nic do dodania.', 'Pytajcie personel, ja tu tylko byłem gościem.'],
  'showDefault': ['Nie wiem. Dawno tu nie bywałem.', 'Nic mi to nie mówi.'],
  'questions': [
   Q('g-q1', 'Gdzie pan był podczas seansu?', 'Na sali, w piątym rzędzie. Cały film. Ostatni seans ojca — gdzie miałbym być?', ['g-l1']),
   Q('g-q2', 'O czym rozmawiał pan z ojcem przed seansem?', 'O filmie. O tym, że to koniec. Zwykła rozmowa.', ['g-l2']),
   Q('g-q3', 'Umie pan obsługiwać projektor?', 'Jako dzieciak spędzałem w tej kabinie każde popołudnie. Zmianę projektora zrobiłbym dziś z zamkniętymi oczami. Tylko że wczoraj nie miałem po co tam wchodzić.', ['g-c1']),
   Q('g-q4', 'Kto jest na zdjęciu z pana ojcem w kabinie?', 'Ojciec i jakaś praktykantka. Miałem wtedy osiemnaście lat i inne rzeczy w głowie. Ojciec miał paru uczniów, nie pamiętam ich.', requires=['e09']),
   Q('g-q5', 'Ojciec mówił panu o plakatach w gablocie?', 'W zeszłym tygodniu dzwonił i coś mamrotał, że „ktoś tu kręci”. Myślałem, że chodzi o sprzedaż budynku. Nie słuchałem go uważnie. Teraz żałuję.', requiresAny=['e13', 'st:j-c3']),
  ],
  'statements': [
   S('g-c1', 'Umiem zmienić projektor, nauczyłem się w dzieciństwie.', truth=True),
   S('g-c3', 'Ojciec zawsze stawiał pustą puszkę na stole przewijarki, nigdy na górnej półce.', truth=True),
   S('g-l1', 'Cały seans siedziałem na sali.', contradicts=['x3', 'st:j-c4'],
     response='Wyszedłem o dziewiątej zadzwonić. Do człowieka, któremu jestem winien pieniądze. Stałem przed kinem, aż skończyłem. Nie chciałem, żeby to wyszło na jaw — nie w taki dzień.',
     gives=['t2']),
   S('g-l2', 'Przed seansem rozmawiałem z ojcem tylko o filmie.', contradicts=['st:j-c1'],
     response='Pokłóciliśmy się. Prosiłem, żeby poręczył mi pożyczkę albo dał mieszkanie pod zastaw. Odmówił. Powiedziałem mu rzeczy, których nie da się cofnąć. To była nasza ostatnia rozmowa.',
     gives=['t3']),
  ],
  'shows': [
   SH('g-s1', 'e08', 'Ta puszka nie spadła z żadnej półki. Ojciec nigdy nie trzymał pustej puszki na górze. Zawsze stała na stole przewijarki, żeby od razu schować do niej przewiniętą szpulę.', claims=['g-c3']),
   SH('g-s2', 'e04', 'Ojciec czekał na ten wieczór pół roku. Mówił, że to będzie najlepsza projekcja w jego życiu.'),
  ]},

 {'id': 'joanna', 'name': 'Joanna Rak', 'role': 'Prowadzi bufet kina', 'age': 58,
  'desc': 'Pracuje za barem „Zorzy” od 1999 roku. Ciepła, gadatliwa, z ołówkiem wpiętym w rude loki. Zna wszystkich stałych widzów po imieniu i wszystko, co dzieje się w foyer.',
  'deflect': ['Ja tam stałam za barem, kochanie. Nic więcej nie wiem.', 'Nie będę gadać o ludziach za plecami.', 'Tego nie widziałam, nie będę zmyślać.'],
  'showDefault': ['Pierwszy raz widzę.', 'Nie znam się na tym, ja jestem od kawy i ciastek.'],
  'questions': [
   Q('j-q1', 'Co się działo przed seansem?', 'Pan Leon przyszedł o wpół do ósmej na herbatę. Przy barze pokłócił się z synem — o pieniądze, o mieszkanie, aż ludzie się oglądali. Potem poszedł na górę, cały czerwony.', ['j-c1']),
   Q('j-q2', 'Czy pan Leon mówił coś szczególnego?', 'Miał kopertę w kieszeni marynarki. Powiedział, że po seansie da coś pani konserwator i że wszyscy się zdziwią, co się dzieje z naszymi plakatami. Pytałam o co chodzi — machnął ręką.', ['j-c3']),
   Q('j-q3', 'Kto wychodził z foyer w czasie seansu?', 'Damian wyszedł frontem za pięć dziewiąta i wrócił z ulicy jakoś dziesięć po, z reklamówką. A syn pana Leona wyszedł z sali koło dziewiątej, przed kino, z telefonem przy uchu. Wrócił po kwadransie.', ['j-c5', 'j-c4']),
   Q('j-q4', 'Widziała pani kierowniczkę w czasie seansu?', 'Przyszła od zaplecza kwadrans po dziewiątej. Mokra, z płaszczem zarzuconym na ramiona, włosy jej się rozsypały. Powiedziała, że wynosiła śmieci. Zdziwiłam się, bo śmieci zawsze wynosi Damian.', ['j-c2']),
   Q('j-q5', 'Jak skończył się film?', 'Ostatnia scena, napisy i nagle biały ekran. Świecił tak z pięć minut. Ludzie bili brawo, myśleli, że pan Leon zaraz zejdzie się ukłonić. W końcu pani Ewa zapaliła światło panelem przy drzwiach sali.', ['j-c7']),
  ],
  'statements': [
   S('j-c1', 'Przed seansem pan Leon pokłócił się z synem o pieniądze i mieszkanie.', truth=True),
   S('j-c2', 'Kierowniczka przyszła od zaplecza kwadrans po dziewiątej, mokra, i mówiła, że wynosiła śmieci.', truth=True),
   S('j-c3', 'Pan Leon miał kopertę i zapowiedział, że po seansie powie coś o plakatach.', truth=True),
   S('j-c4', 'Syn pana Leona wyszedł przed kino koło dziewiątej i wrócił po kwadransie.', truth=True),
   S('j-c5', 'Damian wyszedł frontem za pięć dziewiąta i wrócił z ulicy z reklamówką.', truth=True),
   S('j-c6', 'Na zdjęciu z kabiny jest Ewa Sitek, z domu Kalinowska, która przed laty była kinooperatorką.', truth=True),
   S('j-c7', 'Po napisach ekran świecił na biało około pięciu minut, aż kierowniczka zapaliła światło.', truth=True),
  ],
  'shows': [
   SH('j-s1', 'e09', 'Przecież to Ewa! Pani Ewa, z domu Kalinowska. Kiedy zaczynałam tu pracować, ona jeszcze siedziała w kabinie z panem Leonem. Najlepsza, mówił o niej. Dopiero potem przeszła do biura.', claims=['j-c6']),
   SH('j-s2', 'e16', 'W tym płaszczu wtedy przyszła. Miała go na ramionach, cały mokry.'),
  ]},

 {'id': 'lipka', 'name': 'Stanisław Lipka', 'role': 'Sąsiad z oficyny naprzeciwko', 'age': 84,
  'desc': 'Emerytowany motorniczy tramwaju. Mieszka w oficynie od 1961 roku, z okna widzi tył kina. Przyszedł sam, w kapeluszu i krawacie, bo „jak się coś widziało, to trzeba powiedzieć”.',
  'deflect': ['Ja wiem, co widziałem, proszę pana.', 'Oczy mam jeszcze dobre, tylko nogi gorsze.', 'Tego to już nie wiem, nie będę zmyślał.'],
  'showDefault': ['A co ja mogę o tym wiedzieć?', 'Nie, tego nie widziałem.'],
  'questions': [
   Q('l-q1', 'Co pan widział w sobotę wieczorem?', 'Wstałem zamknąć okno, bo zaczęło kropić. Patrzę, a tu ktoś zbiega po tych żelaznych schodach z kina. Szybko, trzymał się poręczy. Długi jasny płaszcz. Zegar nad stołem pokazywał jakieś dziesięć po dziesiątej, od razu na niego spojrzałem.', ['l-m1', 'l-c2']),
   Q('l-q2', 'Widział pan twarz tej osoby?', 'Z tej odległości, w tym świetle? Nie. Kaptura nie miał. Włosy jasne albo siwe, nie wiem. Mogła to być i kobieta. Zszedł na podwórze i zniknął pod ścianą kina, tam gdzie tylne drzwi.', ['l-c3']),
   Q('l-q3', 'Czy drzwi kabiny były otwarte?', 'W czasie seansów zawsze są otwarte, pan Leon je podpiera, bo mu gorąco. Ale jak ten ktoś zbiegał, drzwi na górze były już zamknięte. Pamiętam, bo kiedy są otwarte, z kabiny bije światło od lamp, a wtedy na górze było już ciemno.', ['l-c4']),
   Q('l-q4', 'Kiedy ostatnio nastawiał pan zegar?', 'W czwartek, jak zmieniałem baterię. Nastawiłem z zegarka po bracie. Chodzi jak szwajcarski, codziennie rano go nakręcam.', ['l-c5'], requires=['e24']),
  ],
  'statements': [
   S('l-c2', 'Kiedy ta osoba zbiegała, zaczynało kropić.', truth=True),
   S('l-c3', 'Osoba w jasnym płaszczu zeszła na podwórze i zniknęła przy tylnych drzwiach kina.', truth=True),
   S('l-c4', 'Kiedy ta osoba zbiegała, drzwi kabiny były już zamknięte.', truth=True),
   S('l-c5', 'Zegar nastawiłem w czwartek z zegarka po bracie.', truth=True),
   S('l-m1', 'Kogoś na schodach pożarowych widziałem około dziesięć po dziesiątej wieczorem.', mistake=True, contradicts=['e24', 'e25'],
     response='Godzinę więcej? Mój Boże... Zegarek po Mietku. Przecież ja go w październiku nie przestawiłem — nakręcam go, ale wskazówek nie ruszam, kto by o tym pamiętał. A zegar nastawiłem z niego w czwartek. Czyli to było dziesięć po dziewiątej, nie po dziesiątej. Przepraszam państwa, nie chciałem nikogo zmylić.',
     gives=['t4']),
  ],
  'shows': [
   SH('l-s1', 'x5', 'Jedenaście po dziewiątej drzwi się zamknęły? Nie, to niemożliwe. Ja widziałem tego człowieka o dziesiątej, zegar miałem przed nosem.'),
   SH('l-s2', 'x1', 'Padać zaczęło akurat, jak on zbiegał. Tego jestem pewien. Dlatego wstałem do okna.'),
  ]},
]
