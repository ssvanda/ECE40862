#Python program to generate Fibonacci series until 'n' value
n = int(input("How many Fibonacci numbers would you like to generate? "))
a = 1
b = 1
sum = 0
count = 0

print("The Fibonacci Sequence is: ", end = " ")

while(count <= n):
    if (sum != 0):
        print(sum, end = " ")
    count += 1
    a = b
    b = sum
    sum = a + b
