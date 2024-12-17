import random
def roll():
    max_value = 6
    min_value = 1
    roll = random.randint(min_value,max_value)
    
    return roll
while True:
 player = input("how many players are in?(2-4)")
 if player.isdigit():
      player = int(player)
      if 2 <= player <= 4:
          break
 else:
       print("invalid value")
       
max_score = 50
player_score = [ 0 for _ in range(player)]


while max(player_score) < max_score:
    for player_idx in range(player):
      print("\n player number ",player_idx+1,"turn has just statrted!\n")
      current_score = 0
     
      while True:
           want_roll = input("would you like to roll again ? (yes or no)")
           if want_roll.lower() != "yes":
              break
            
            
           value = roll()
           if value == 1:
              print(" you rolled 1! turn done!")
              current_score =0
              break
           else:
              current_score += value
              print("you rolled a :",value)
          
           print("your corrent score is:",current_score)
           
      player_score[player_idx] += current_score
      print("your total score is: ",player_score[player_idx])