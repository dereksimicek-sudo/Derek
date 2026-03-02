# Derek Šimíček 1.C
destinace = "Kutná hora"
aktivity = []

print("Plánovač víkendového výletu!")
print(f"cíl cesty je: {destinace}")

kapesne = int(input("Zde zadej své planované kapesné v KČ: "))
doprava = int(input("Zadej dopravu: "))
ubytovani = int(input("Zadej ubytko: "))

print()

aktivita1 = input("První aktivita: ")
aktivity.append(aktivita1)
aktivita2 = input("Druhá aktivita: ")
aktivity.append(aktivita1)
aktivita3 = input("Třetí aktivita: ")
aktivity.append(aktivita1)
# Výpočty
celkove_naklady = doprava + ubytovani
zbyva = kapesne - celkove_naklady
# Výstup
print("\n-------------------------------------")
print("BOMBA PLÁN! ZDE JE SHRNUTÍ:")
print("-------------------------------------")
print(f"Cíl cesty: {destinace}")
print(f"Plánované aktivity: {aktivity}")
print(f"Celkové náklady na dopravu a ubytování: {celkove_naklady} Kč.")
print(f"Na jídlo a zábavu ti zbývá: {zbyva} Kč.")