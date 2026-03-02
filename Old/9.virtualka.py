class Vozidlo:
    def __init__(self, typ):
        self.typ = typ

    def zvuk(self):
        return "Neznámý zvuk"
    
class Auto(Vozidlo):
    def __init__(self, znacka):
        Vozidlo.__init__(self, "Auto")
        self.znacka = znacka

    def zvuk(self):
        return "Brrr Brrr!"
    
class Motorka(Vozidlo):
    def __init__(self, model):
        super().__init__("Motorka")
        self.model = model

    def zvuk(self):
        return "Vrmmm Vrrrrm!"
    
Vozidloa = [Auto("Toyota"), Motorka("Harley-Davidson")]
for vozidlo in Vozidloa:
    print(f"{vozidlo.typ} zvuk: {vozidlo.zvuk()}")