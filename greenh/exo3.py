import tkinter as tk 
from tkinter import messagebox
import math
def calcule():
    num1 = int(entrynum1.get())
    if num1<0:
        messagebox.showerror("erreur","le nombre est negative")
    else:
      Resultat = math.sqrt (num1)
      Labelreasult.config(text=" le resultat est :" +str(Resultat))
    
    
fenetr = tk.Tk()
fenetr.geometry("300x300")
fenetr.title("hello")

Labelnom = tk.Label(fenetr, text= "entre un num")
Labelnom.pack(pady="10")
entrynum1 = tk.Entry(fenetr)
entrynum1.pack(pady="10")

button = tk.Button(fenetr, text="calcule",command=calcule)
button.pack(pady="10")

Labelreasult = tk.Label(fenetr,text="")
Labelreasult.pack(pady="10")

fenetr.mainloop()