import os
import json

script_dir = os.path.dirname(__file__)
NAZEV_SOUBORU = os.path.join(script_dir, "inventar.json")

print(f"cesta a nazev souboru je: {NAZEV_SOUBORU}")

try:
    with open(NAZEV_SOUBORU, "r", encoding="utf-8") as f:
        inventar_knih = json.load(f)
    print(f"==== INVENTAR KNIH ZE SOUBORU : {NAZEV_SOUBORU} ==== \n")
    for kniha in  inventar_knih:
        print(f"{kniha["nazev"]},{kniha["autor"]}")
except FileNotFoundError:
    print(f"soubor nenalezen - {NAZEV_SOUBORU}")
except json.JSONDecodeError :
    print(f"neplatny soubor JSON - {NAZEV_SOUBORU}")
except Exception as e:
    print(f"Došlo k neočekavane chybě {e}")