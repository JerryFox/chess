# chess
## Cvičná webová aplikace

Cvičné prostředí s Pythonem na backendu (zatím Bottle) i frontendu (Brython).

Funkční by to mělo být tady:
http://vysoky.pythonanywhere.com/chessboard

Backend umí vygenerovat stránku s libovolnou pozicí na šachovnici. Příklady:
- http://vysoky.pythonanywhere.com/chessboard/blank
- http://vysoky.pythonanywhere.com/chessboard/base
- http://vysoky.pythonanywhere.com/chessboard/RN-KQ-NR48r6r

Přidávat a ubírat figurky na šachovnici:
- http://vysoky.pythonanywhere.com/chessboard/blank/set/K00k77R07r70
- http://vysoky.pythonanywhere.com/chessboard/3K/set/Q04
- http://vysoky.pythonanywhere.com/chessboard/base/reset/00077077

Při přidávání a ubírání figur je také možno používat souřadnice v notaci a1 - h8:
- http://vysoky.pythonanywhere.com/chessboard/base/reset/a1
- http://vysoky.pythonanywhere.com/chessboard/base/reset/h8
- http://vysoky.pythonanywhere.com/chessboard/blank/set/ra1Ra8


## Jak to spustit na lokále

- požadavky: python 3, Bottle framework - https://bottlepy.org/docs/dev/
- naklonovat tento repositář
- upravit config.py
- v adresáři projektu spustit Python (3)
- import bottle_chess
- from bottle import run
- run(host='localhost', port=8080, debug=True)
- v browseru http://localhost:8080/chessboard

## Brython na frontendu

Veškerý frontend je napsán v [Brythonu](https://brython.info/) - javascriptové implementaci jazyka Python. 
Na začátku jsem použil javascript, abych viděl, že vše funguje, jak má, 
nyní už i pro nové věci používám výhradně Brython. 

Motivace k použití Brythonu je dána tím, že tato aplikace je zamýšlena jako cvičná (výuková) 
pro výuku programování v Pythonu, primárně určená pro studenty IT semináře na SŠ. 
Proto jsem chtěl, aby i na frontendu, který je většinou pro studenty pochopitelnější 
a atraktivnější, mohli studenti pracovat v Pythonu. 
K mému překvapení je běh těchto skriptů jak z hlediska rychlosti tak i spolehlivosti bezproblémový, 
z mého pohledu je tak Brython použitelný i pro běžné aplikace. 

Základem aplikace je hra - v tomto případě šachy sloužící jako pískoviště, na němž je předpřipravena 
určitá sada objektů s nějakou funkcionalitou, která se postupně vyvíjí. 
Běžný uživatel má možnost přistupovat k těmto objektů a využívat jejich funkcionalitu pomocí 
pythoní konzole, která je převzata z projektu Brython 3.5, drobně upravena a doplněna o ukládání 
historie příkazů do local storage. Dále je možno využívat vestavěný editor (ACE, součást Brythonu), 
do kterého je možno natahovat a spouštět existující skripty ze serveru, a dále psát vlastní skripty 
a ukládat je do local storage. 

## PythonAnywhere

## Jupyter notebooks

Výukové lekce vytvářim (respektive chtěl bych vytvářet) formou Jupyter notebooků. 
Určitou komplikací je, že studenti, kteří mají pouze free účet na PythonAnywhere, 
zde nemohou s notebooky pracovat přímo. To je velká škoda, i když práce s lokální 
instalací Jupyteru není obtížná. 

- https://github.com/JerryFox/chess/blob/master/chess_exercise01.ipynb
- https://github.com/JerryFox/chess/blob/master/chess_exercise02.ipynb
- https://github.com/JerryFox/chess/blob/master/chess_exercise_decorator.ipynb


 

