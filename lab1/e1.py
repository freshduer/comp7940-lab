# Find all the factors of x using a loop and the operator %
# % means find remainder, for example 10 % 2 = 0; 10 % 3 = 1
x = 52633
for i in range(2, x):
    if x % i == 0:
        print(i)