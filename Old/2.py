cislo = 10
if cislo > 0:
    print("Kladné číslo")

if cislo % 2 == 0 :
    print("Sude")
else:
    print("Kiche")

věk = 15 
if věk >= 13 and věk <= 20:
    print("teenager")
else:
    print("Není teenager")

povolené_ovoce = ["jablko","banan","ananas","pomeranc"]
moje_ovoce = "kokos"

if moje_ovoce in povolené_ovoce:
    print(f"{moje_ovoce.upper()} je povolene ovoce.")
else:
    print(f"{moje_ovoce.upper()} je zakázané ovoce.")

heslo = "TajneHeslo5248"
limit = 8
if (delka:= len(heslo)) >= limit:
    print("Heslo je dostatecne dlouhe {delka}")