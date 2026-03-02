def log_call(function):
    def wrapper(*args, **kwargs):
        print(f"Volání funkce: {function.__name__} s argumenty: {args} a klíčovými argumenty: {kwargs}")
        result = function(*args, **kwargs)
        print(f"Funkce {function.__name__} vrátila: {result}")
        return result

@log_call
def add(a, b):
    return a + b

vysledek = add(3, 5)
print(f"Výsledek: {vysledek}")