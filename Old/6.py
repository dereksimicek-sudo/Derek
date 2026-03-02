import random
import string

delka = 8
znaky = string.ascii_lowercase

heslo = ""
for i in range(delka):
    heslo += random.choice(znaky)

print("Zkušební heslo:", heslo)

vstup_delka = input("Zadejte délku hesla: ")
delka = int(vstup_delka)