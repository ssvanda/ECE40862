#while(1):
first = print("Welcome to the birthday dictionary. We know the birthdays of:")
einstein = print("Albert Einstein")
franklin = print("Benjamin Franklin")
lovelace = print("Ada Lovelace")
name = (input("Who's birthday do you want to look up?\n"))
myDict = {"Benjamin Franklin" : "01/17/1706", "Albert Einstein" : "03/14/1879", "Ada Lovelace" : "12/10/1815"}
for k, v in myDict.items():
    if name == k:
        print(k + "'s birthday is " + v)
    