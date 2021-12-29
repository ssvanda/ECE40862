a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = []
print(a)
high = int(input("Enter number: "))
for i in a:
    if high > i:
        b.append(i)
print("The new list is " + str(b)) 

    