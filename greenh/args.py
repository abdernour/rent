import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def calcule():
    try:
        num1 = float(entrynum1.get())
        num2 = float(entrynum2.get())
        operation = combobox1.get()

        if operation == "A+B":
            Labelresult.config(text="Le résultat est : " + str(num1 + num2))
        elif operation == "A-B":
            Labelresult.config(text="Le résultat est : " + str(num1 - num2))
        elif operation == "A*B":
            Labelresult.config(text="Le résultat est : " + str(num1 * num2))
        elif operation == "A/B":
            if num2 != 0:
                Labelresult.config(text="Le résultat est : " + str(num1 / num2))
            else:
                Labelresult.config(text="Erreur : Division par zéro")
        else:
            Labelresult.config(text="Veuillez sélectionner une opération.")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des nombres valides.")

def effacer():
    entrynum1.delete(0, tk.END)
    entrynum2.delete(0, tk.END)
    Labelresult.config(text="Le résultat ")
    combobox1.set("")


fenetr = tk.Tk()
fenetr.geometry("400x400")
fenetr.title("Calculatrice")


Labelnom1 = tk.Label(fenetr, text="Entrez le nombre 1 :")
Labelnom1.pack(pady=10)
entrynum1 = tk.Entry(fenetr)
entrynum1.pack(pady=10)

Labelnom2 = tk.Label(fenetr, text="Entrez le nombre 2 :")
Labelnom2.pack(pady=10)
entrynum2 = tk.Entry(fenetr)
entrynum2.pack(pady=10)

labelstat = tk.Label(fenetr, text="Opération :")
labelstat.pack(pady=10)
combobox1 = ttk.Combobox(fenetr, values=["A+B", "A-B", "A*B", "A/B"], state="readonly")
combobox1.pack(pady=10)

button_calculate = tk.Button(fenetr, text="Calculer", command=calcule,bg="green")
button_calculate.pack(pady=10)

button_clear = tk.Button(fenetr, text="Effacer", command=effacer,bg="red")
button_clear.pack(pady=10)

Labelresult = tk.Label(fenetr, text="Le résultat sera affiché ici.")
Labelresult.pack(pady=10)

fenetr.mainloop()

    