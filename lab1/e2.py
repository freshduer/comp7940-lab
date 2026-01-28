# Write a function that prints all factors of the given parameter x
def print_factor(x):
    for i in range(2, x):
        if x % i == 0:
            print(i)
    
