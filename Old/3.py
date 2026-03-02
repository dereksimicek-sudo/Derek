import datetime
dnesje = datetime.date.today()
print(f"Dneska je: {dnesje}")

ted = datetime.datetime.now()
print(ted)

cesky_format = dnesje.strftime("%d.%m.%Y")
print(cesky_format)

aktualni_cas = ted.time()
print(aktualni_cas)
cas_format =  aktualni_cas.strftime("%H%M%S")