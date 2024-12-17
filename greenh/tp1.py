import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox
def fonc1():
    print("mrghwn")
    messagebox.showerror("mrmot","sido")
def window():
    
    fenetre = tk.Tk()
    fenetre.title("Premier projet Tkinter")
    fenetre.geometry("300x300")  
    
    tk.Label(fenetre, text="Nom:").place(x=20, y=10)
    tk.Entry(fenetre).place(x=120, y=10, width=150)
    
    tk.Label(fenetre, text="Code:").place(x=20, y=40)
    tk.Entry(fenetre,show="*").place(x=120, y=40, width=150)
    
    tk.Label(fenetre, text="Prix unitaire HT:").place(x=20, y=70)
    tk.Entry(fenetre).place(x=120, y=70, width=150)
    
    tk.Label(fenetre, text="Prix unitaire TTC:").place(x=20, y=100)
    tk.Entry(fenetre).place(x=120, y=100, width=150)
    
    tk.Label(fenetre, text="Status:").place(x=20, y=130)
    ttk.Combobox(fenetre, values=["Offline", "Online"],state="readonly").place(x=120, y=130, width=150)
    
    tk.Label(fenetre, text="Date creation:").place(x=20, y=160)
    tk.Entry(fenetre).place(x=120, y=160, width=150)
    
    
    tk.Button(fenetre, text="Creer",command=fonc1).place(x=120, y=200) 
    fenetre.mainloop()
    
window()