import random

choices = ["rock","paper","scissors"]

computer = random.choice(choices)
player = None

while player  not in choices:
    player = input("enter a choice")
if player == computer:
     print("computer : ",computer)
     print("player :",player)
     print("tie")
elif player == "rock":
       if computer == "scissors":
             print("computer : ",computer)
             print("player :",player)
             print("player win")
       if computer == "paper":
             print("computer : ",computer)
             print("player :",player)
             print("computer win")
elif player == "scissors":
       if computer == "rock":
             print("computer : ",computer)
             print("player :",player)
             print("computer win")
       if computer == "paper":
             print("computer : ",computer)
             print("player :",player)
             print("player win")
elif player == "paper":
       if computer == "rock":
             print("computer : ",computer)
             print("player :",player)
             print("player win")
       if computer == "scissors":
             print("computer : ",computer)
             print("player :",player)
             print("computer win")