import random  #how to generate random numbers
mylist = ["house","money","wife"]
x = random.choice(mylist)

cards = ["1","h","g","7","e"]
random.shuffle(cards)
print(cards)
print(x)