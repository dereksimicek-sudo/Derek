def nacti_cislo():
    while True:
        try:
            vstup = input("zadej cele cislo ")
            cislo = int(vstup)
        except ValueError:
            print("Toto neni platne cele cislo, zkuz to znova")
        else:
            print("zadal jsi korektni čislo")
            break
        finally:
            print("tady tato cast bude provedena vzdy.")
    return cislo

print(f"\nzadal jis cislo {nacti_cislo()}")