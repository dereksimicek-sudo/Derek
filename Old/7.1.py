# Super()

class Zvire:
    def __init__(self, jmeno, druh):
        self.jmeno = jmeno
        print(f"Zvire {self.jmeno} bylo vytvořeno.")

class Pes(Zvire):
    def __init__(self, jmeno, rasa):
        super().__init__(jmeno, "Pes")
        self.rasa = rasa
        print(f"Pes: {self.jmeno}, rasa: {self.rasa} byl vytvořen.")

muj_cokl = Pes("Rex", "Český čokl")
print(f" Pes: {muj_cokl.jmeno}")