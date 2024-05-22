def fact(n):
    if n < 0:
        raise ValueError
    elif 0<=n<=1:
        return 1
    else:
        return n * fact(n - 1)

try:
    print(fact(-1))
except ValueError:
    print("Factorial is not defined for negative numbers")
