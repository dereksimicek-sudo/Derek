# Datová struktura (seznam slovníků):
inventar_knih = [
    {"nazev": "Velké dobrodružství Pythonu", "autor": "Anna Nováková",
        "rok": 2023, "cena": 350.00, "skladem": True},
    {"nazev": "Základy datové analýzy", "autor": "Petr Dvořák",
        "rok": 2022, "cena": 450.50, "skladem": True},
    {"nazev": "Strojové učení v praxi", "autor": "Eva Černá",
        "rok": 2021, "cena": 599.00, "skladem": False},
    {"nazev": "Webové aplikace s Flaskem", "autor": "Tomáš Marek",
        "rok": 2023, "cena": 320.00, "skladem": True},
    {"nazev": "Dějiny programování", "autor": "Lucie Pokorná",
        "rok": 2019, "cena": 280.75, "skladem": True},
    {"nazev": "Kybernetická bezpečnost pro začátečníky",
        "autor": "Martin Kopecký", "rok": 2024, "cena": 410.00, "skladem": True},
    {"nazev": "Algoritmy a datové struktury", "autor": "Jan Svoboda",
        "rok": 2020, "cena": 515.00, "skladem": False},
    {"nazev": "Grafický design s GIMPem", "autor": "Veronika Veselá",
        "rok": 2022, "cena": 299.90, "skladem": True},
    {"nazev": "Úvod do SQL", "autor": "Pavel Novotný",
        "rok": 2021, "cena": 380.00, "skladem": True},
    {"nazev": "Automatizace s Ansible", "autor": "David Horák",
        "rok": 2023, "cena": 475.00, "skladem": True}
]
print("======================================")
print(" === PŘEHLED INVENTÁŘE (10 knih) ===")
print("====================================== ")
for kniha in inventar_knih:
    print(f"Nazev: {kniha['nazev']} Autor: {kniha['autor']} Cena: {kniha['cena']} Skladem: {kniha['skladem']}")