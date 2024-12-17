#its so easy its just a code used to creat a program to ready anyfile you have in your device just put the file path
try:
   with open('aymen') as file :
      print(file.read())
except FileNotFoundError:
    print("file was not found(:")
    
    