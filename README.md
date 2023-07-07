# PathXML - KONVERZIA VYSTUPU ZO SAP3 DO XML 


## Účel projektu:

Konverzia exportovaných dát zo SAP3 pre potreby účtovných výkazov pre Daňové riaditeľstvo vo formáte XML v špecifikovanom
formáte. Bohužiaľ SAP exportuje iba XLS v binárnom formáte. Preto je potrebné využiť moduly tretích strán ako aj konverziu Excelovských dátumov na štandardný ISO formát. 

## Inštalácia

Program sa inštaluje v dvoch fázach:
1. Je potrebné mať nainštalovaný Python 3.11 z Microsoft Store:
	https://www.microsoft.com/store/productId/9NRWMJP3717K

2. je potrebné stiahnuť repozitár z githubu

https://github.com/fortisauris/XLSconvertXML.git

**Mozete ho stiahnut ako zip**

3. program odporúčame spúšťať z virtuálnej obálky ale nie je to podmienkou.

4. Treba doinštalovať všetky DEPENDENCIES (potrebné moduly a knižnice tretích strán) pomocou súboru
	`requirements.txt`

``` powershell
	python.exe -m pip install -r requirements.txt
```

## Použitie programu

1. Otvorte Powershell v adresari PathXML malo by Vám svietiť:

``` powershell
	C:\Users\...\PathXML\
```

2. Program berie výstupný xls zo SAP3 ako Argument:

``` powershell
	python.exe main.py VYSTUP_ZO_SAPU.xls
```
3. Program vytvori súbor `output.xml`, ktorý možno prehliadať v ľubovoľnom textovom editore. NIE VO WORDE !!!

 
## Ďalšie plánované funkcie:

*CONFIG* - Upravovať výstup pomocou CONFIG.py suboru
*BATCH PROCESSING*  
*VALIDATORY*