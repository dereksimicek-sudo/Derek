class Ovoce:
    pass
class Hruska(Ovoce):
    # potomek třídy Ovoce
    def __repr__(self):
        return "Hruska"
    
class Jablko(Ovoce):
    # potomek třídy Ovoce
    def __repr__(self):
        return "Jablko"
    
# použití
ovoce_obj = Ovoce()
hruska_obj = Hruska()
jablko_obj = Jablko()

print(ovoce_obj)
print(hruska_obj)
print(jablko_obj)