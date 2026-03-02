import random
""""
print("generejume nahodne čislo")

cislo = random.randint(1,10)
print(cislo)
"""
rozsah = 10
min_cislo = 1
max_cislo = 6

for i in range(rozsah): 
    cislo = random.randint(min_cislo,max_cislo)
    print (f"Nahodne cislo je: , {cislo}")