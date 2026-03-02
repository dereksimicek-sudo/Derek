def faktorial(n):
    if n <= 1:
        return 1
    else:
        return n * faktorial(n - 1)


n = 8
print(f"faktorial čísla{n} je roven: {faktorial(n)}")