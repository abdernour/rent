import tkinter as tk 

def afficher():
    nom = entry_nom.get()
    lable_affichage.config(text="bonjour" + nom+" !!")

    
fenetre = tk.Tk()
fenetre.title("hello")
fenetre.geometry("300x300")  

lable_title = tk.Label(fenetre,text="entre your name")
lable_title.pack(pady=10)

entry_nom = tk.Entry(fenetre)
entry_nom.pack(pady=10)
button_valider =tk.Button(fenetre,text="valider",command=afficher)
button_valider.pack(pady=10)
lable_affichage =tk.Label(fenetre,text="")
lable_affichage.pack(pady=10)

fenetre.mainloop()