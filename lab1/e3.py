# Write a program to find all factors of the numbers in the list l
def print_factor(x):
    for i in range(2, x):
        if x % i == 0:
            print(i)

l = [52633, 8137, 1024, 999]

for num in l:
    print(f"Factors of {num}:")
    print_factor(num)
