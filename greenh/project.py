import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import messagebox
from pymysql import MySQLError
import pymysql
import re
from PIL import Image, ImageTk

CITY_COMMUNES = {
    'Alger': ['Bab El Oued', 'Hussein Dey', 'Bir Mourad Rais', 'El Harrach', 'Dar El Beida'],
    'Oran': ['Bir El Djir', 'Es Senia', 'Arzew', 'Ain Turk', 'Mers El Kebir'],
    'Constantine': ['El Khroub', 'Hamma Bouziane', 'Zighoud Youcef', 'Ibn Ziad', 'Didouche Mourad'],
    'Annaba': ['El Bouni', 'El Hadjar', 'Sidi Amar', 'Seraidi', 'Berrahal'],
    'Skikda': ['Azzaba', 'Collo', 'El Harrouch', 'Zitouna', 'Ramdane Djamel'],
    'Setif': ['Ain Arnat', 'El Eulma', 'Ain Oulmene', 'Bougaa', 'Ain Azel'],
    'Jijel': ['El Aouana', 'Ziama Mansouriah', 'Taher', 'El Milia', 'Sidi Marouf'],
    'Chlef': ['Tenes', 'Boukadir', 'Ouled Fares', 'Ain Merane', 'Benairia']
}

def connecter_bd():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="aptdemands"
        )
        return conn
    except MySQLError as e:
        messagebox.showerror("Database Error", f"Connection error: {str(e)}")
        return None

def communes(event):
    selected_city = city.get()
    com['values'] = CITY_COMMUNES.get(selected_city, [])
    com.set('')

def search_communes(event):
    selected_city = search_city.get()
    search_com['values'] = CITY_COMMUNES.get(selected_city, [])
    search_com.set('')

def executer_requete(conn, requete, valeurs=None):
    try:
        cursor = conn.cursor()
        if valeurs:
            cursor.execute(requete, valeurs)
        else:
            cursor.execute(requete)
        conn.commit()
    except MySQLError as e:
        messagebox.showerror("Database Error", f"Query execution error: {str(e)}")

def validate_name(value):
    if not value.strip():
        messagebox.showerror("Error", "Name cannot be empty")
        return False
    if not re.match(r'^[A-Za-zÀ-ÿ\s-]{2,50}$', value):
        messagebox.showerror("Error", "Name should contain only letters, spaces, and hyphens (2-50 characters)")
        return False
    return True

def validate_email(value):
    if not value.strip():
        messagebox.showerror("Error", "Email cannot be empty")
        return False
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        messagebox.showerror("Error", "Invalid email format")
        return False
    return True

def validate_phone(value):
    if not value.strip():
        messagebox.showerror("Error", "Phone number cannot be empty")
        return False
    if not re.match(r'^0[567][0-9]{8}$', value):
        messagebox.showerror("Error", "Phone number must start with 05, 06, or 07 followed by 8 digits")
        return False
    return True

def validate_nin(value):
    if not value.strip():
        messagebox.showerror("Error", "NIN cannot be empty")
        return False
    if not re.match(r'^[0-9]{18}$', value):
        messagebox.showerror("Error", "NIN must be exactly 18 digits")
        return False
    return True

def submit():
    firstname = name1.get()
    secondname = name2.get()
    date1 = date.get_date()
    NINf1 = NINf.get()
    email1 = email.get()
    phone1 = phone.get()
    com1 = com.get()
    city1 = city.get()
    apttype = apt.get()
    
    if not all([firstname, secondname, date1, NINf1, email1, phone1, city1, com1, apttype]):
        messagebox.showwarning("Warning", "Please fill all the fields to continue")
        return
    
    if not all([
        validate_name(firstname),
        validate_name(secondname),
        validate_email(email1),
        validate_phone(phone1),
        validate_nin(NINf1)
    ]):
        return

    conn = connecter_bd()
    if conn:
        try:
            query = """
            INSERT INTO rentals (first_name, second_name, date_of_birth, email, phone, nin, city, commune, apartment_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (firstname, secondname, date1, email1, phone1, NINf1, city1, com1, apttype)
            executer_requete(conn, query, values)
            messagebox.showinfo("Success", "Your rental request has been successfully submitted")
            delete()
        finally:
            conn.close()

def delete():
    name1.delete(0, tk.END)
    name2.delete(0, tk.END)
    date.set_date(None)
    email.delete(0, tk.END)
    phone.delete(0, tk.END)
    NINf.delete(0, tk.END)
    city.set('')
    com.set('')
    apt.set('')

def open_search():
    global search_city, search_com
    search = tk.Toplevel(fenetre)
    search.title("Search Requests")
    search.geometry("800x400")
    search.minsize(400, 300)
    search.transient(fenetre)
    search.grab_set()
    search.grid_columnconfigure(0, weight=1)
    search.grid_rowconfigure(0, weight=1)

    main_frame = ttk.Frame(search, padding="10")
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_columnconfigure(0, weight=1)

    # Form Fields
    ttk.Label(main_frame, text="Select City:").grid(row=0, column=0, pady=5, sticky="w")
    search_city = ttk.Combobox(main_frame, values=list(CITY_COMMUNES.keys()), state="readonly")
    search_city.grid(row=1, column=0, pady=5, sticky="ew")
    search_city.bind('<<ComboboxSelected>>', search_communes)

    ttk.Label(main_frame, text="Select Commune:").grid(row=2, column=0, pady=5, sticky="w")
    search_com = ttk.Combobox(main_frame, values=[], state="readonly")
    search_com.grid(row=3, column=0, pady=5, sticky="ew")

    ttk.Label(main_frame, text="Select Apartment Type:").grid(row=4, column=0, pady=5, sticky="w")
    search_apt = ttk.Combobox(main_frame, values=['F2', 'F3', 'F4'], state="readonly")
    search_apt.grid(row=5, column=0, pady=5, sticky="ew")

    # Results Frame
    result_frame = ttk.Frame(main_frame)
    result_frame.grid(row=6, column=0, pady=10, sticky="nsew")
    main_frame.grid_rowconfigure(6, weight=1)
    result_text = tk.Text(result_frame, height=10, wrap="word")
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # Make the text area unwritable
  

    scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.configure(yscrollcommand=scrollbar.set)

    def clear():
        search_city.set('')
        search_com.set('')
        search_apt.set('')
        result_text.delete("1.0", tk.END)

    def search():
        city = search_city.get()
        commune = search_com.get()
        apttype = search_apt.get()
        if not all([city, commune, apttype]):
            messagebox.showwarning("Warning", "Please select all fields: City, Commune, and Apartment Type")
            return
        conn = connecter_bd()
        if conn:
            try:
                query = """
                SELECT first_name, second_name, email, phone 
                FROM rentals
                WHERE city = %s AND commune = %s AND apartment_type = %s
                """
                cursor = conn.cursor()
                cursor.execute(query, (city, commune, apttype))
                results = cursor.fetchall()
                result_text.delete("1.0", tk.END)
                if results:
                    for row in results:
                        result_text.insert(tk.END, 
                            f"Name: {row[0]} {row[1]}\nEmail: {row[2]}\nPhone: {row[3]}\n{'='*40}\n")
                else:
                    result_text.insert(tk.END, "No results found.\n")
            except MySQLError as e:
                messagebox.showerror("Database Error", f"Error accessing database: {str(e)}")
            finally:
                conn.close()

  # Button frame at the bottom
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=8, column=0, columnspan=4, sticky="ew", pady=10)
    button_frame.grid_columnconfigure((0, 1, 2,3), weight=1)
    
    submit_btn = ttk.Button(button_frame, text="Search", command=search)
    submit_btn.grid(row=0, column=0, padx=5, sticky="ew")
    
    clear_btn = ttk.Button(button_frame, text="Clear", command=clear)
    clear_btn.grid(row=0, column=1, padx=5, sticky="ew")
    
    close_btn = ttk.Button(button_frame, text="Close", command=search.destroy)
    close_btn.grid(row=0, column=2, padx=5, sticky="ew")
    
    quit_btn = ttk.Button(button_frame, text="Quit", command=fenetre.quit, style='Red.TButton')
    quit_btn.grid(row=0, column=3, pady=10, padx=10, sticky="ew")

fenetre = tk.Tk()
fenetre.tk.call('tk', 'scaling', 2)
fenetre.title("Apartment Rental")
fenetre.geometry("800x600")  # Larger initial size
fenetre.minsize(600, 400)  

# Configure main window grid
fenetre.grid_columnconfigure((0, 1, 2, 3), weight=1)
fenetre.grid_rowconfigure(8, weight=1)  # Give extra space to the last row

# Create main container frame
main_frame = ttk.Frame(fenetre, padding="20")
main_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

try:
    background_image = Image.open("greenh/- (2).jpg")
    # Calculate aspect ratio for resizing
    aspect_ratio = background_image.width / background_image.height
    new_width = 1920
    new_height = int(new_width / aspect_ratio)
    background_image = background_image.resize((new_width, new_height))
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(fenetre, image=background_photo)
    background_label.image = background_photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Error loading background image: {e}")

title = tk.Label(fenetre, text="Rental Request", font=('helvetica', 14, 'normal'), bg='white', fg='black')
title.grid(row=0, column=0, columnspan=4, pady=20, sticky="ew")

tk.Label(fenetre, text="First Name:", bg='white', fg='black').grid(row=1, column=0, sticky='w', padx=10)
name1 = tk.Entry(fenetre)
name1.grid(row=1, column=1, pady=5)

tk.Label(fenetre, text="Second Name:", bg='white', fg='black').grid(row=2, column=0, sticky='w', padx=10)
name2 = tk.Entry(fenetre)
name2.grid(row=2, column=1, pady=5)

tk.Label(fenetre, text="Date of Birth:", bg='white', fg='black').grid(row=3, column=0, sticky='w', padx=10)
date = DateEntry(fenetre)
date.grid(row=3, column=1, pady=5)

tk.Label(fenetre, text="Email:", bg='white', fg='black').grid(row=4, column=0, sticky='w', padx=10)
email = tk.Entry(fenetre)
email.grid(row=4, column=1, pady=5)

tk.Label(fenetre, text="Phone number:", bg='white', fg='black').grid(row=5, column=0, sticky='w', padx=10)
phone = tk.Entry(fenetre)
phone.grid(row=5, column=1, pady=5)

tk.Label(fenetre, text="NIN:", bg='white', fg='black').grid(row=6, column=0, sticky='w', padx=10)
NINf = tk.Entry(fenetre)
NINf.grid(row=6, column=1, pady=5)

tk.Label(fenetre, text="City:", bg='white', fg='black').grid(row=1, column=2, sticky='w', padx=10)
city = ttk.Combobox(fenetre, values=list(CITY_COMMUNES.keys()), state="readonly")
city.grid(row=1, column=3, pady=5)
city.bind('<<ComboboxSelected>>', communes)

tk.Label(fenetre, text="Commune:", bg='white', fg='black').grid(row=2, column=2, sticky='w', padx=10)
com = ttk.Combobox(fenetre, values=[], state="readonly")
com.grid(row=2, column=3, pady=5)

tk.Label(fenetre, text="Apartment Type:", bg='white', fg='black').grid(row=3, column=2, sticky='w', padx=10)
apt = ttk.Combobox(fenetre, values=['F2', 'F3', 'F4'], state="readonly")
apt.grid(row=3, column=3, pady=5)

style = ttk.Style()
style.configure('Green.TButton', background='green')
style.configure('Red.TButton', background='red')
style.configure('Gray.TButton', background='gray')

submit_btn = ttk.Button(fenetre, text="Submit", command=submit, style='Green.TButton')
submit_btn.grid(row=7, column=0, pady=10, padx=10)

search_btn = ttk.Button(fenetre, text="Search", command=open_search, style='Gray.TButton')
search_btn.grid(row=7, column=1, pady=10, padx=10)

delete_btn = ttk.Button(fenetre, text="Delete", command=delete, style='Red.TButton')
delete_btn.grid(row=7, column=2, pady=10, padx=10)

quit_btn = ttk.Button(fenetre, text="Quit", command=fenetre.quit, style='Red.TButton')
quit_btn.grid(row=7, column=3, pady=10, padx=10)

fenetre.mainloop()
