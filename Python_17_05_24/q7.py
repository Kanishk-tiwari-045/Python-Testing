import random
n = random.randint(1,100)
guess = int(input("Guess the number:"))
if(guess>n):
    print("too high")
elif(guess<n):
    print("too low")
else:
    print("correct")
