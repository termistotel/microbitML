# microbitML
Projekt za uporabu računala u nastavi.
Sastoji se od dvije komponente:

### Klijent - micro:bit + ESP8266
Što klijent trenutno radi:
1. micro:bit ~~čita podatke sa senzora i šalje ih preko UART-a na ESP8266.~~ Šalje "testinjola\r" preko UART-a 
2. Zatim se ti podaci šalju preko wifi-a na server.


### Server
>Server trenutno samo sluša podatke i ispiše što prima.



## Korištenje

MicroPython kod za micro:bit se nalazi u [client/microbit](client/microbit)  
Za flashanje koristimo [mu editor](https://codewith.mu/)

Kod za ESP8266 se nalazi u [clent/esp8266](client/esp8266)  
Mogu se koristiti dvije verzije firmwarea: [NodeMCU](https://nodemcu.readthedocs.io/en/master/) i [MicroPython](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html)  
Za uploadavanje file-ova na NodeMCU koristimo [nodemcu-uploader](https://github.com/kmpm/nodemcu-uploader).
Još nema programa za MicroPython

### upload.py
Skripta koja uploadava sve relevantne fajlove na microbit ili ESP8266.  
Ovisno o opcijama, traži programe u [client/](client/) direktoriju i uploada/flasha ih s odgovarajućim alatima na uređaj.  
Alati za uploadavanje (npr. nodemcu-uploader.py) trebaju bit dostupni putem PATH ili PYTHONPATH environment varijabli.

Upotreba:
```
upload.py {esp|microbit}
upload.py esp {micropython|nodemcu}
```  
>Trenutno radi samo `upload.py esp nodemcu`
