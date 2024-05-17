def fact(n):
    if n < 0:
        raise ValueError
    elif n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return n * fact(n - 1)

try:
    print(fact(-1))
except ValueError:
    print("Factorial is not defined for negative numbers")
