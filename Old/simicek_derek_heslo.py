
## Derek Šimíček, 3.C, 24.11.2025
# Soubor pojmenuješ: prijmeni_jmeno_heslo.py
## například: novak_jan_heslo.py

import random
import string

# Získání parametrů od uživatele
def generujHeslo():
    print("-" * 30)
    print("Generátor hesel")
    print("-" * 30)
# Ošetřit vstup uživatele

while True:
    try:
        delka = int(input("Zadejte požadovanou délku hesla (např. 12): "))
        if delka <= 0:
            print("Délka musí být kladné číslo.")
        else:
            break
        # zde se ptame uzivatele a pote kontrolujeme vstup
    except ValueError:
        print("Neplatný vstup. Zadejte prosím číslo.")
        # zde osetrujeme chybny vstup
        

# zde je konec smyčky ================================================
# nadefinujeme si co chce uzivatel v hesle mít: velka pismena, cisla a specialni znaky - zeptaeme se jej
#  - a ulozime do promennych
print("Chcete zahrnout do hesla velká písmena? (a/n): ")
include_upper = input().strip().lower() == 'a'
# sestavime sadu znaku pro generovani hesla
znaky = "string.ascii_lowercase"      # vzdy zahrneme mala pismena 
if include_upper:
    znaky += string.ascii_uppercase

# zde konotrola a varovani ze zadal pouze mala pismena, tzn na vse odpovedel ne
if not znaky:
    print("Varování: Zadané parametry neumožňují vytvoření hesla. Použijí se malá písmena.")
    znaky = string.ascii_lowercase

# generovani hesla neco jako heslo = "".join....
heslo = ""  # doplnit kod pro generovani hesla

# vypis vygenerovaneho hesla
print("\nVygenerované heslo: ", heslo)
print("-" * 30)

# spusteni generatoru, hlavní část programu bude v funkci generujHeslo()
generujHeslo()