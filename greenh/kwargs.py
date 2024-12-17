# **kwargs to pack all the arguments into a dictionary, usefull so the fonction can accept a good amount of arguments

def hello(**kwargs):
    print("hello",end=" ")
    for key,value in kwargs.items():
        print(value,end=" ")
    

hello(midllename="rich",firstname="aymen",lastname="hafsaoui")

