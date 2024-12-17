name2 = "aymen2"  #global scope is declared outside the fonction

def display_name() :
    name = "aymen"
    print(name)  #local scope is known inside his fonction
    
    
print(name2)
display_name()