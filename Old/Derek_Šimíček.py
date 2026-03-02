# Cvičení L1-L10: Souhrnné opakování
# jmeno, příjmení, třída: DOPLNIT !!!
# soubor pojmenuj: jmeno_prijmeni.py

import math # Příklad importu pro použití v cvičení
print("=== ČÁST 1: Proměnné a řetězce ===")

# ÚKOL 1:
# Vytvořte proměnné `jmeno` (str) a `vek` (int) s libovolnými hodnotami.
# Pomocí f-stringu vytiskněte větu: "Ahoj, jmenuji se [jmeno] a je mi [vek] let."
# TODO: Váš kód zde
jmeno = "Derek"
vek = 15
print(f"Ahoj, jmenuji se {jmeno} a je mi {vek} let.")


print("\n=== ČÁST 2: Seznamy a práce s nimi ===")
numbers = [10, 5, 20, 1, 8, 15]
# ÚKOL 2:
# 1. Přidejte na konec seznamu `numbers` číslo 15.
# 2. Seřaďte seznam vzestupně.
# 3. Vytiskněte první a poslední prvek seřazeného seznamu.
# TODO: Váš kód zde
print(f"První prvek: {numbers[0]}, Poslední prvek: {numbers[-1]}")


print("\n=== ČÁST 3: Slovníky a množiny ===")
# ÚKOL 3:
# 1. Přidejte do slovníku `student` nový klíč "vek" s hodnotou 16.
# 2. Přidejte do seznamu "predmety" další předmět "Informatika".
# 3. Vytiskněte aktualizovaný slovník.

student = {
    "jmeno": "Jan",
    "predmety": ["Matematika", "Čeština", "informatika"],
    "vek": 16
}

# TODO: Váš kód zde
print(student)



print("\n=== ČÁST 4: Řízení toku (Podmínky a Cykly) ===")
# ÚKOL 4:
# Máte seznam s duplicitami. Vytvořte z něj množinu pro získání unikátních hodnot a vytiskněte ji.
raw_data = [1, 2, 2, 3, 1, 4, 5, 5]
# TODO: Váš kód zde
print(set(raw_data))


print("\n=== ČÁST 5: Funkce ===")
# ÚKOL 5:
# Napište cyklus `for`, který projde čísla od 1 do 10 (včetně).
# Pokud je číslo dělitelné 3, vytiskněte "Fizz".
# Pokud je číslo dělitelné 5, vytiskněte "Buzz".
# Jinak vytiskněte samotné číslo.
# TODO: Váš kód zde
for i in range(1, 11):
    if i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)


print("\n=== ČÁST 6: Výjimky (Error Handling) ===")
# ÚKOL 6:
# Definujte funkci `vypocet_obvodu_obdelnika(a, b)`, která vrátí obvod obdélníka.
# Pokud uživatel nezadá `b`, použijte implicitní hodnotu stejnou jako `a` (čtverec).
# Zavolejte funkci pro strany 5 a 3 a výsledek vytiskněte.
# Zavolejte funkci pouze pro stranu 5 a výsledek vytiskněte.

# TODO: Definice funkce
def vypocet_obvodu_obdelnika(a, b=None):
    if b is None:
        b = a
    return 2 * (a + b)
# TODO: Volání funkce
print(vypocet_obvodu_obdelnika(5, 3))
print(vypocet_obvodu_obdelnika(5))

print("\n=== ČÁST 7: Pokročilejší výrazy a Importy ===")
# ÚKOL 7:
# Napište kód, který se zeptá uživatele na zadání čísla (funkce `input` - zde simulujte nebo odkomentujte).
# Použijte blok `try-except` pro ošetření chyby, kdy uživatel nezadá číslo (ValueError).
# Pokud uživatel zadá 0 a program by měl dělit, ošetřete ZeroDivisionError.
# Pro účely tohoto automatického testu pracujte s předdefinovanou proměnnou `vstup_od_uzivatele`, místo input().

vstup_od_uzivatele = "abc" # Zkuste změnit na "0", "10", "abc" pro testování

# TODO: Váš kód zde (napište funkci 'vydej_podil(vstup)', která zkusí vydělit 100 / int(vstup))
def vydej_podil(vstup):
    try:
        cislo = int(vstup)
        vysledek = 100 / cislo
        print(f"Výsledek dělení je: {vysledek}")
    except ValueError:
        print("Chyba: Nezadal jsi číslo.")
    except ZeroDivisionError:
        print("Chyba: Nelze dělit nulou.")
vydej_podil(vstup_od_uzivatele)

print("\n=== ČÁST 8: Pokročilejší výrazy ===")
# ÚKOL 8:
# Použijte modul `math` (importován na začátku) k výpočtu druhé odmocniny z čísla 256.
# Výsledek vytiskněte.
# Dále převeďte číslo 255 do hexadecimální (šestnáctkové) soustavy a výsledek vytiskněte.
# TODO: Váš kód zde
odmocnina = math.sqrt(256)
print(f"Druhá odmocnina z 256 je: {odmocnina}")
hexadecimal = hex(255)
print(f"255 v hexadecimální soustavě je: {hexadecimal}")

print("\n=== HOTOVO ===")

"""
Cvičení L1-L10: Souhrnné opakování
==================================

Cvičení N00 až N10.
Místa pro váš kód jsou označena komentářem # TODO.

Témata:
- Proměnné, datové typy, f-stringy
- Seznamy, ntice, slovníky, množiny
- Řízení toku (podmínky, cykly)
- Funkce
- Výjimky
- Importy (standardní knihovna)
"""