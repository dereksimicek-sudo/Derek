# Derel Šimíček 1.C 8.12.2025
"""
Cvičení: Datové struktury - sklad elektroniky
Datová struktura pro sklad elektroniky
"""

# 1. Datová struktura (seznam slovníků):

sklad_elektroniky = [
    {"kategorie": "Notebook", "vyrobce": "Dell", "model": "XPS 15",
     "rok_vyroby": 2023, "cena": 45000.00, "skladem": True},
    {"kategorie": "Telefon", "vyrobce": "Apple", "model": "iPhone 15 Pro",
     "rok_vyroby": 2023, "cena": 32000.00, "skladem": True},
    {"kategorie": "Monitor", "vyrobce": "Samsung", "model": "Odyssey G9",
     "rok_vyroby": 2022, "cena": 28000.00, "skladem": False},
    {"kategorie": "Notebook", "vyrobce": "Apple", "model": "MacBook Air M2",
     "rok_vyroby": 2022, "cena": 29990.00, "skladem": True},
    {"kategorie": "Sluchátka", "vyrobce": "Sony", "model": "WH-1000XM5",
     "rok_vyroby": 2023, "cena": 8990.00, "skladem": True},
    {"kategorie": "Klávesnice", "vyrobce": "Logitech", "model": "MX Keys",
     "rok_vyroby": 2021, "cena": 2500.00, "skladem": True},
    {"kategorie": "Tablet", "vyrobce": "Samsung", "model": "Galaxy Tab S9",
     "rok_vyroby": 2023, "cena": 21000.00, "skladem": False},
    {"kategorie": "Fotoaparát", "vyrobce": "Canon", "model": "EOS R6",
     "rok_vyroby": 2021, "cena": 55000.00, "skladem": True},
    {"kategorie": "Myš", "vyrobce": "Razer", "model": "Viper V2 Pro",
     "rok_vyroby": 2022, "cena": 3500.00, "skladem": True},
    {"kategorie": "Telefon", "vyrobce": "Google", "model": "Pixel 8",
     "rok_vyroby": 2023, "cena": 20000.00, "skladem": True}
]

# 2. Tisk informací o položkách

print("\nSklad elektroniky:")
print("=" * 91) # Celková šířka tabulky

# --- Definice formátování ---
# Definujeme šířky sloupců na jednom místě pro snadnou úpravu
SIRKA_KAT = 12
SIRKA_VYR = 10
SIRKA_MODEL = 20  
SIRKA_ROK = 8
SIRKA_CENA = 15
SIRKA_SKLADEM = 8
  # doplň šířku pro ostatní sloupce a spočítej kolik činí CELKOVA_SIRKA

# Např.: Celková šířka: 12 ..... + 3 + 8 = nějaké číslo
CELKOVA_SIRKA = 91      # uprav dle skutečného součtu šířek a mezer

# --- Tisk hlavičky tabulky ---
# Použijeme stejné šířky jako pro data, aby vše sedělo pod sebou
hl_kat = "Kategorie"
hl_vyr = "Výrobce"
hl_model = "Model"
hl_rok = "Rok"
hl_cena = "Cena"
hl_skladem = "Skladem"

# Zápis f"..." f"..." umožňuje rozdělit dlouhý f-string na více řádků
# Zarovnání: '<' = vlevo (default), '>' = vpravo
print(f"{hl_kat:<{SIRKA_KAT}} | "
      f"{hl_vyr:<{SIRKA_VYR}} |"
      f"{hl_model:<{SIRKA_MODEL}} | "
      f"{hl_rok:>{SIRKA_ROK}} | "
      f"{hl_cena:>{SIRKA_CENA}} | "
      f"{hl_skladem:<{SIRKA_SKLADEM}}"
      )
      # doplň další sloupce dle vzoru

# --- Tisk oddělovače ---
print("-" * CELKOVA_SIRKA)

# --- Tisk dat (jeden cyklus pro všechny položky) ---
# Tímto dodržujeme princip DRY (Don't Repeat Yourself)
for polozka in sklad_elektroniky:
    # Získání a formátování dat z aktuálního slovníku 'polozka'
    kategorie = polozka["kategorie"]
    vyrobce = polozka["vyrobce"]
    model = polozka["model"]
    rok_vyroby = polozka["rok_vyroby"]
    cena = polozka["cena"]
    skladem = polozka["skladem"]
      # doplň další proměnné dle vzoru, model a rok_vyroby
    
    # Formátování ceny s oddělovači tisíců a dvěma des. místy
    cena = "CZK {:>11,.2f}".format(polozka["cena"])
    
    # Ternární operátor pro převod boolean na text
    skladem = "ano" if polozka["skladem"] else "ne"

    # Tisk řádku s daty
    print(f"{kategorie:<{SIRKA_KAT}} | "
          f"{vyrobce:<{SIRKA_VYR}} | "
          f"{model:<{SIRKA_MODEL}} | "
          f"{rok_vyroby:>{SIRKA_ROK}} | "
          f"{cena:>{SIRKA_CENA}} | "
          f"{skladem:<{SIRKA_SKLADEM}}    "
          )
    

print("-" * CELKOVA_SIRKA)
print("\n")