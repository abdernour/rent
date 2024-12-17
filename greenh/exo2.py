import tkinter as tk 

def somme():
    num1 = int(entry_num1.get())
    num2 = int(entry_num2.get())
    Label_result.config(text="leur somme est " + str(num1 + num2))

fenetre = tk.Tk()
fenetre.title("hello")
fenetre.geometry("300x300")  

label_title1 = tk.Label(fenetre, text="entre number 1")
label_title1.pack(pady=10)
entry_num1 = tk.Entry(fenetre)
entry_num1.pack(pady=10)

label_title2 = tk.Label(fenetre, text="entre number 2")
label_title2.pack(pady=10)
entry_num2 = tk.Entry(fenetre)
entry_num2.pack(pady=10)

Label_result = tk.Label(fenetre, text="")  # Changed from tk.Entry to tk.Label
Label_result.pack(pady=10)

button_valider = tk.Button(fenetre, text="valider", command=somme)
button_valider.pack(pady=10)

fenetre.mainloop()
