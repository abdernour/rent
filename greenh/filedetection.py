# here is just a methode you can use to verfiy if a path that is related to a sertine file is alredey existed in your device
import os

path = "C:\\Users\\sts\\Desktop\\hello.txt"

if os.path.exists(path):
    print("exists")
else:
    print("dosent exist")