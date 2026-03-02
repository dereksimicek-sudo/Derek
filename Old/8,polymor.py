class Pes:
    def vydej_zvuk(self):
        return "Haf haf!"
    
class Kocka:
    def vydej_zvuk(self):
        return "Mňau mňau!"

class Kachna:
    def vydej_zvuk(self):
        return "Kvak kvak!"
    
zvirata = [Pes(), Kocka(), Kachna()]
for zvire in zvirata:
    print(zvire.vydej_zvuk())