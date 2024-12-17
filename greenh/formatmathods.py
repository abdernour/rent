# string.format :is a methode is used by the user the gain more control over the outputs
#like you can have a string that can have diffrent values like the one down in the exemple and you can change it according to what you wanna display 

print("the {} jumped over the {}".format("man","bitch"))
print("the {1} jumped over the {0}".format("man","bitch"))# positional argument you can use the numbers to put the output you want (the computer start always counting from 0)
print("the {theuser} jumped over the {object}".format(theuser="man",object="bitch"))  # keyword argumrnt  just using keywords and put them in correct position 