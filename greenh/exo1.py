import tkinter as tk 

def   nom():
    nomm = entry.get()
    Label.config(text = "hello"+ nomm+"!!")
    
fenetr = tk.Tk()
fenetr.geometry("300x300")
fenetr.title("hello")

Labelnom = tk.Label(fenetr, text= "entre ton nom")
Labelnom.pack(pady="10")

entry = tk.Entry(fenetr)
entry.pack(pady="10")


button = tk.Button(fenetr, text="press me",command=nom)
button.pack(pady="10")

Label = tk.Label(fenetr,text="")
Label.pack(pady="10")

fenetr.mainloop();