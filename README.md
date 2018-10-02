# Detektiranje trčanja poomoću strojnog učenja
Projekt za uporabu računala u nastavi.
Sastoji se od dvije komponente:

### Klijent - micro:bit + ESP8266
Što klijent trenutno radi:
1. micro:bit čita podatke sa senzora i šalje ih preko UART-a na ESP8266.
2. ESP, preko wifi-a šalje na server sve podatke koje primi preko UART-a


### Server
Postoje dva programa za server:

primanjePodataka.py
>Sluša podatke koji dolaze preko mreže na port 5005 i sprema ih u datoteku "podaci"

learn.py
>Istrenira neuron prema spremljenim podacima i pokrene server koji prima nove podatke.
>Prema novim podacima predviđa naučeno i ispisuje ako detektira pozitivnu klasu.



## Korištenje

MicroPython kod za micro:bit se nalazi u [client/microbit](client/microbit)  
Za flashanje koristimo [mu editor](https://codewith.mu/)

Kod za ESP8266 se nalazi u [clent/esp8266](client/esp8266)  
Mogu se koristiti dvije verzije firmwarea: [NodeMCU](https://nodemcu.readthedocs.io/en/master/) ~~i [MicroPython](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html)~~
Za uploadavanje file-ova na NodeMCU koristimo [nodemcu-uploader](https://github.com/kmpm/nodemcu-uploader).
Još nema programa za MicroPython

### upload.py
Skripta koja uploadava sve relevantne fajlove na microbit ili ESP8266.  
Ovisno o opcijama, traži programe u [client/](client/) direktoriju i uploada/flasha ih s odgovarajućim alatima na uređaj.  
Alati za uploadavanje (npr. nodemcu-uploader.py) trebaju bit dostupni putem PATH ili PYTHONPATH environment varijabli.

Upotreba:
upload.py {esp|microbit}
upload.py esp {micropython|nodemcu}
>Trenutno radi samo `upload.py esp nodemcu`\



<div class="paragraph"><p> <br>
 <br></p></div>
<div class="paragraph"><p> <br>
 <br></p></div>

# Detaljnije upute
Kratak opis
===========

Strojno učenje je trenutno jedno od najaktivnijih područja računarske
znanosti. Iako sami algoritmi za učenje iza sebe imaju naprednu
statistiku (i općenito matematiku), neke jednostavne modele je moguće
shvatiti na intuitivnoj razini.\
U ovom projektu radimo jednostavan i grubi sustav za prepoznavanje
trčanja pomoću strojnog učenja pod nadzorom.\
Da bismo to ostvarili, radimo dvije stvari:

1.  Uređaj za mjerenje akceleracije, koju algoritam koristi kao podatke
    za učenje i prepoznavanje

2.  Server i algoritam s *jednim neuronom* za učenje trčanja.

**Napomena:** predviđeno vrijeme za izradu cijelog projekta je nekoliko
mjeseci

![uredaj](https://raw.githubusercontent.com/termistotel/microbitML/readmeAssets/imgs/Uredaj.jpg)
Uređaj za mjerenje i slanje akceleracije

Potrebna predznanja
-------------------

Za izradu ovog projekta potrebno je dobro znanje srednjoškolske
matematike, spajanja strujnih krugova i osnova programskog jezika
Python. S obzirom da se u projektu koristi komunikacija između više
uređaja, potrebno je poznavanje osnovnih principa računalnih mreža i
komunikacije, te pojmova kao što su *router* i *IP adresa*.\
Preporuča se poznavanje osnova matričnog računa, jer dobro dođe kod
pokušavanja optimizacije koda.\
U ovom projektu su podaci raspoređeni u velik broj dimenzija, pa ih neće
biti lako vizualizirati pomoću grafova. Zbog toga je korisno (ali ne i
nužno) prijašnje iskustvo s projekatima vezanih uz strojno učenje,
baratanje podacima i statistiku.

Naučene vještine
----------------

Ovim projektom se stječe razumijevanje osnovnih principa *supervised*
strojnog učenja i mogućnost implementiranja jednostavne klasifikacije za
svakidašnju upotrebu.\
Stječe se bolji osjećaj za komunikaciju među raznim uređajima i osnovni
alati za korištenje. Konkretno, nauči se baratati UART protokolom i
osnovnom računalnom mrežom koristeći TCP.\
Unaprijeđuje se znanje i razumijevanje matematike u područjima koje
koriste sve prirodne znanosti.\
Ostala stječena zananja kroz ovaj projekt ukljućuje osnovno korištenje
dretvi u Python-u, paketa Numpy, osnove programskog jezika Lua i
programiranja pogonjenog događajima.

Popis opreme
------------

Potrebna oprema:

-   BBC micro:bit i oprema koja dolazi uz njega

-   ESP8266 201 wifi modul

-   USB-TTL adapter za arduino

-   Gumb

-   Žice za spajanje, *jumper wire*

-   Računalo s wifi-om (Po mogučnosti prijenosno)

-   Ruter s mogučnošču wifi pristupne točke (Za ovo može poslužiti
    većina mobitela)

Opcionalna oprema:

-   Break-out board za BBC micro:bit

-   Odstojnici za wifi modul

-   Lemilica

-   Veroboard za učvrstiti i zalemiti komponente

-   Torba za nošenje uređaja prilikom trčanja

Uređaj za mjerenje akceleracije
===============================

Za učenje prepoznavanja trčanja, trebamo izmjeriti podatke prema kojima
će algoritam naučiti raspoznavati trčanje od ostalih aktivnosti. S
obzirom da očekujemo dosta veliku razliku između akceleracije prilikom
trčanja i mirovanja, kao podatke za učenje ćemo mjeriti akceleraciju s
microbitovim unutarnjim akcelerometrom.\
Uređaj će slati mjerene podatke na računalo za obradu. Sustav za slanje
radimo po uzoru na projekt \"Microbit i WiFi modul\":
Imamo microbit koji mjeri akceleraciju i te podatke šalje preko UART-a
na wifi modul. Wifi modul će sve što primi automatski proslijediti na
računalo.

Programiranje i spajanje micro:bit-a
------------------------------------

Gumb spajamo na pin 16 i 3.3V na
microbitu.\
Gumb nam služi da pritiskom na njega označimo trčimo li trenutno ili ne.
Sa y označavamo stanje trčanja, gdje 1 označava da trčimo, a 0 da ne
trčimo.\
Svakih 25 milisekunda (proizvoljno vrijeme) pošaljemo preko UARTa
podatke: komponente vektora akceleracije, njegov iznos i vrijednost y.
Na kraju dodajemo znak \"\\r\" koji koristimo da nam označava kraj
komunikacije kod UART-a.

*Flashanje* NodeMCU na ESP8266
------------------------------
<div>
<img align="left" src="https://raw.githubusercontent.com/termistotel/microbitML/readmeAssets/imgs/normalno.png" width="45%">      
<img align="right" src="https://raw.githubusercontent.com/termistotel/microbitML/readmeAssets/imgs/flashanje.png" width="45%">
</div>
/

**Lijevo:** Shema za normalan način rada s microbitom/

**Desno:** Spajanje za *flashanje*, odnosno instalaciju NodeMCU sustava. Za
prebacivanje datoteka na instalirani sustav, **odspojiti pin
IO-0**/

Na wifi modul prvo instaliramo NodeMCU sustav[@NodeMCU] koji nam
omogućava da ga programiramo u programskom jeziku Lua. Za izgradnju
datoteke NodeMCU koristimo cloud servis[@cloud]. Označimo da želimo
izgradnju sustava za verziju od 512KB sa modulima: node, net, timer,
UART i WiFi. Ostavimo naš e-mail i kliknemo \"Start your build\". Nakon
što je izgradnja gotova, datoteka nam je poslana na e-mail.\
Prije instaliravanja, moramo spojiti pinove modula prema shemi na
slici desno te
USB-TTL adapter ukopčamo u računalo preko kojeg ćemo instalirati sustav
na wifi modul. Za instaliranje sustava i stavljanje datoteka na uređaj
može se koristiti bilo koji alat koji piše u dokumentaciji za
NodeMCU[@NodeMCU]. Prilikom testiranja smo koristili alat
*nodemcu-pyflasher*[@pyflasher] za instalaciju sustava i
*nodemcu-uploader*[@uploader] za stavljanje datoteka.

Programiranje i spajanje ESP8266
--------------------------------

Nakon uspješne instalacije sustava, uređaj spojimo kao na
slici lijevo.
NodeMCU funkcionira tako da čim priključimo napajanje na uređaj, on
počne izvršavati Lua kod koji je zapisan u init.lua datoteci. U prilogu
su priložene datoteke *init.lua* i *application.lua*. U init.lua se samo
vrši preporučeno početno spajanje na pristupnu točku, kao što je
preporučeno u dokumentaciji za NodeMCU. Da bismo ostvarili komunikaciju
s računalom, moramo ga spojiti na istu pristupnu točku i saznati
pridjeljenu IP adresu.\
Glavni dio programa se nalazi u application.lua datoteci. Njegov zadatak
je da sve podatke koje primi preko UART-a, odmah proslijedi preko mreže
na IP adresu od našeg računala.

Server
======

Na računalu želimo napraviti dva različita programa. U prilogu su
priloženi pod nazivom primanjePodataka.py i learn.py. Prvi program
jednostavno prima podatke sa wifi modula i sprema ih u posebnu datoteku.
Te podatke drugi program čita, oblikuje te iz njih nauči prepoznavati
trčanje. Odmah nakon učenja, ponovno se pokreće server za čekanje
podataka koje onda algoritam prepoznaje kao trčanje ili ne.

Prikupljanje podataka za učenje
-------------------------------

Prije nego što je naš algoritam sposoban učiti, mora imati
iskustvo(odnosno podatke) iz kojeg će naučiti prepoznavati trčanje. Te
podatke zovemo *training data* ili podaci za treniranje. Da bismo
uređaju osigurali te podatke, moramo staviti uređaj u neku torbu i
trčati.\
Konkretno, nakon što pravilno isprogramiramo ESP8266 i spojimo računalo
na istu pristupnu točku, pokrenemo primanjePodataka.py i spojimo
baterije na microbit. Ubrzo nakon što se uređaji spoje, naš bi server
trebao primati podatke sa uređaja.\
Dok trčimo trebamo držati gumb pritisnutim, a prekinuti ga kada hodamo
ili mirujemo. Koliko dugo trebamo skupljati podatke može ovisiti o mnogo
čimbenika. Ideja je da pomoću pokušaja i pogreške dođemo do tog
zaključka. U našem testu je trebalo ukupno oko minutu trčanja i oko 10
minuta hodanja i mirovanja.\
U datoteci u kojoj smo spremili podatke za treniranje svaki red
predstavlja jedno mjerenje. Prvi stupci predstavljaju komponente
akceleracije i iznos akceleracije, dok je zadnji stupac y.

Osnovna ideja algoritma za učenje
---------------------------------

<img src="https://raw.githubusercontent.com/termistotel/microbitML/readmeAssets/imgs/neuron.png">\
Model neurona. Na ulazu prima podatke mjerenja, a na izlazu daje
predivđanje h prema koeficijentima θ koje pamti

Kao model našeg algoritma za učenje klasifikacije trčanja koristimo
jedan neuron kao na slici. Ovaj neuron prima na svom ulazu naše podatke o
akceleraciji za jedno mjerenje (x1, x2,...) i na izlazu nam daje
predviđanje, odnosno broj između 0 i 1 koji ćemo označavati sa **h**.
Potpuna h=0 na izlazu označava da neuron misli da podaci na ulazu ne
označavaju trčanje, a h=1 na izlazu bi označavao da podaci na ulazu
označavaju trčanje. Neki broj između 0 i 1 možemo interpretirati kao
vjerojatnost da je naša trenutna akcija trčanje.\
Ono što želimo postići je da za većinu mjerenja označenih sa y = 1,
neuron na izlazu vrati otprilike 1, a za one označene sa y=0,
vrati oko 0.

Matematika iza modela
---------------------

Funkcija koju ćemo fitat na izmjerene podatke zove se logistička
funkcija:\
<img src="https://raw.githubusercontent.com/termistotel/microbitML/readmeAssets/imgs/jednadbe/prva.png">\
Gdje su x-evi naši podaci za jedno mjerenje, a θ težinski
parametri koje moramo naučiti.\
Ako svakom mjerenju ručno unesemo podatak x0 koji definiramo tako da
je uvijek x0 = 1, onda možemo olakšati notaciju:\
<img src="https://raw.githubusercontent.com/termistotel/microbitML/readmeAssets/imgs/jednadbe/druga.png">\
Gdje je **xi** vektor s podacima za i-to mjerenje, a hi
predviđanje za vrijednost y.

Učenje
------

Originalno komplicirani koncept učenja smo uspjeli svesti na traženje
najpovoljnijih parametra **θ** koji opisuju naše podatke za
treniranje. Za traženje optimalnih parametara možemo koristiti
iterativno pravilo za učenje jednog neurona:\
<img src="https://raw.githubusercontent.com/termistotel/microbitML/readmeAssets/imgs/jednadbe/treca.png">\
gdje je j redni broj iteracije, a m je broj mjerenja. Parametar α
se zove *learning rate* ili faktor učenja. Iteraciju ponavljamo sve dok
razlike ne postanu dovoljno male:\
<img src="https://raw.githubusercontent.com/termistotel/microbitML/readmeAssets/imgs/jednadbe/cetvrta.png">\
Da bismo na ovaj
način ostvarili učenje, moramo zadati dva parametra: α i η.
Faktor učenja, α, može jako varirati ovisno o načinu učenja i
nemožemo na jednostavan način unaprijed znati koliko bi trebao iznositi.
Ako ga zadamo previsokog, učenje nam neće nikada konvergirati, ali ako
je prenizak, učenje će biti presporo. Najbolji pristup zadavanju tih
parametara je isprobavanje sa različitim vrijednostima dok se ne dobije
konvergencija i zadovoljavajući rezultati u razumnom vremenu.

skaliranje
----------

Ako isprobamo gornji algoritam za učenje na spremljenim podacima,
primjetili bismo da je jako teško naštimati parametre α i η
za dobru konvergenciju. To se događa jer nam različiti stupci poprimaju
jako različite vrijednosti.\
Da bismo riješili taj problem, trebamo primjeniti osnovno
pret-procesiranje podataka za treniranje. To ćemo postići skaliranjem.\
Za svaki stupac nađemo srednju vrijednost i standardnu deviaciju
σ. Nakon toga, od svake vrijednosti u tom stupcu oduzmemo srednju
vrijednost i podijelimo sa standardnom deviaijom:\
<img src="https://raw.githubusercontent.com/termistotel/microbitML/readmeAssets/imgs/jednadbe/peta.png">\
Time smo postigli da nam
podaci u svakom stupcu postižu vrijednosti otprilike između -1 i 1.
Nakon toga će lakše biti naštimati parametre učenja.

prepoznavanje
-------------

Ako pokrenemo learn.py, neuron će početi učiti iz podataka za
treniranje. Kada je učenje završeno, pokrenut će server koji čeka nove
podatke sa uređaja. Za svako primljeno mjerenje će izračunati
predviđanje h, te ako je veći od 0.5 ga ispiše na zaslon.\
Kada krenemo trčati, neuron bi to trebao detektirati kao pozitivno
mjerenje i ispisati.

Prijedlozi za nadogradnju
=========================

Nakon uspješno izvedenog projekta, ovladali smo jednim od osnovnih
algoritma za klasifikaciju. Za one koji žele nadograditi svoj projekt i
nastaviti razvijati razumijevanje strojnog učenja i baratanje podacima,
preporučamo neke ideje za nastavak:

-   Napraviti bolje pret-procesiranje i čišćenje podataka na ulazu i
    prije slanja. Npr. uzimati srednju vrijednost nekoliko uzastopnih
    mjerenja sa senzora

-   Postavljanje vanjskih senzora, kao npr. žiroskop, za skupljanje više
    podataka koji bi omogučili algoritmu bolje klasificiranje

-   Implementirati model neuralne mreže, u kojemu više neurona ima
    međusobno povezane ulaze i izlaze. Time bismo mogli trenirati
    prepoznavanje nekih finijih kretnji kao što je sjedenje i ustajanje.

-   Agregirati susjede: u pret-procesiranju podataka, spojiti određeni
    broj susjednih podataka oko svakog mjerenja u nova mjerenja. Ovo bi
    omogučilo bolje klasificiranje vremenski promijenjivih radnji
    (uključujući i trčanje).
