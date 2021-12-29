import random
target = random.randint(0, 10)
'''
guess = int(input('Enter your guess:'))
guess2 = int(input('Enter your guess:'))
guess3 = int(input('Enter your guess:'))

while (target != guess1) or (target != guess2) or (target != guess3):
    print('You lose!')
    
print('You win!)
'''
count = 0
while count < 3:
    guess = int(input('Enter your guess:'))
    if guess == target:
        print("You win!")
        break
    count = count + 1

if count >= 3:
    print("You lose!")