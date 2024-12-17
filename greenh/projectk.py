from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
import pymysql
from pymysql import MySQLError
import re

class RentalFormApp(App):
    def build(self):
        self.title = "Formulaire de Location Professionnel"
        layout = GridLayout(cols=2, padding=20, spacing=10)

        self.fields = {}
        labels = [
            "Nom", "Prenom", "Date de Naissance", "Email", 
            "Telephone", "NIN", "Ville", "commune", "Type Appartement"
        ]
        
        self.states = [
            "Alger", "Oran", "Constantine", "Annaba", "Setif", "Jijel", "Skikda", "Chlef"
        ]
        
        self.communes = {
            'Alger': ['Bab El Oued', 'Hussein Dey', 'Bir Mourad Rais', 'El Harrach', 'Dar El Beida'],
            'Oran': ['Bir El Djir', 'Es Senia', 'Arzew', 'Ain Turk', 'Mers El Kebir'],
            'Constantine': ['El Khroub', 'Hamma Bouziane', 'Zighoud Youcef', 'Ibn Ziad', 'Didouche Mourad'],
            'Annaba': ['El Bouni', 'El Hadjar', 'Sidi Amar', 'Seraidi', 'Berrahal'],
            'Skikda': ['Azzaba', 'Collo', 'El Harrouch', 'Zitouna', 'Ramdane Djamel'],
            'Setif': ['Ain Arnat', 'El Eulma', 'Ain Oulmene', 'Bougaa', 'Ain Azel'],
            'Jijel': ['El Aouana', 'Ziama Mansouriah', 'Taher', 'El Milia', 'Sidi Marouf'],
            'Chlef': ['Tenes', 'Boukadir', 'Ouled Fares', 'Ain Merane', 'Benairia']
        }
        self.aptypes = ["F2", "F3", "F4"]

        for label_text in labels:
            layout.add_widget(Label(text=label_text))
            if label_text == "Ville":
                self.fields[label_text] = Spinner(text="Selectionner une ville",values=self.states,size_hint=(1, None),height=50)
                self.fields[label_text].bind(text=self.commune_select)
            elif label_text == "commune":
                self.fields[label_text] = Spinner(text="Selectionner une commune",values=[],size_hint=(1, None),height=50)
            elif label_text == "Type Appartement":
                self.fields[label_text] = Spinner(text="Selectionner le type",values=self.aptypes,size_hint=(1, None),height=50)
            elif label_text == "Date de Naissance":
                self.fields[label_text] = TextInput(hint_text="YYYY-MM-DD")
            else:
                self.fields[label_text] = TextInput(hint_text=f"Entrez {label_text.lower()}")
            layout.add_widget(self.fields[label_text])

        submit_button = Button(text="Valider", size_hint=(1, 0.75))
        submit_button.bind(on_press=self.submit)
        layout.add_widget(submit_button)

        search_button = Button(text="Recherche", size_hint=(1, 0.75))
        search_button.bind(on_press=self.open_search_window)
        layout.add_widget(search_button)

        return layout

    def commune_select(self, spinner, text):
        if text in self.communes:
            self.fields["commune"].values = self.communes[text]
            self.fields["commune"].text = "Selectionner une commune"
        else:
            self.fields["commune"].values = []
            self.fields["commune"].text = "Selectionner une commune"

    def connecter_bd(self):
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="aptdemands"
            )
            return conn
        except MySQLError as e:
            self.show_error("Erreur de Connexion", f"Impossible de se connecter à la base de données : {e}")
            return None

    def execute_query(self, conn, query, values=None):
        try:
            cursor = conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            conn.commit()
        except MySQLError as e:
            self.show_error("Erreur SQL", f"Erreur lors de l'exécution de la requête : {e}")

    def validate_email(self, email):
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

    def validate_phone(self, phone):
        return re.match(r'^0[567][0-9]{8}$', phone)

    def validate_nin(self, nin):
        return re.match(r'^[0-9]{18}$', nin)

    def show_error(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=message))
        close_button = Button(text="Fermer", size_hint=(1, 0.3))
        layout.add_widget(close_button)
        popup = Popup(title=title, content=layout, size_hint=(0.8, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def submit(self, instance):
        data = {key: field.text if isinstance(field, TextInput) else field.text for key, field in self.fields.items()}

        if not self.validate_email(data["Email"]):
            self.show_error("Erreur de Validation", "Adresse email invalide.")
            return
        if not self.validate_phone(data["Telephone"]):
            self.show_error("Erreur de Validation", "Numéro de téléphone invalide.")
            return
        if not self.validate_nin(data["NIN"]):
            self.show_error("Erreur de Validation", "Le NIN doit contenir exactement 18 chiffres.")
            return
        if data["Ville"] == "Selectionner une ville":
            self.show_error("Erreur de Validation", "Veuillez sélectionner une ville.")
            return
        if data["commune"] == "Selectionner une commune":
            self.show_error("Erreur de Validation", "Veuillez sélectionner une commune.")
            return
        if data["Type Appartement"] == "Selectionner le type":
            self.show_error("Erreur de Validation", "Veuillez sélectionner un type d'appartement.")
            return

        conn = self.connecter_bd()
        if conn:
            try:
                query = """
                INSERT INTO rentals (first_name, second_name, date_of_birth, email, phone, nin, commune, city, apartment_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    data["Nom"], data["Prenom"], data["Date de Naissance"],
                    data["Email"], data["Telephone"], data["NIN"], data["commune"],
                    data["Ville"], data["Type Appartement"]
                )
                self.execute_query(conn, query, values)
                self.show_error("Succès", "Les données ont été enregistrées avec succès.")
            finally:
                conn.close()

    def open_search_window(self, instance):
        search_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        search_popup = Popup(title="Search Requests", content=search_layout, size_hint=(0.8, 0.8))

        search_city_spinner = Spinner(text='Select City',values=self.states,size_hint=(1, None),height=50)
        search_commune_spinner = Spinner(text='Select Commune',values=[],size_hint=(1, None),height=50)
        search_apartment_type_spinner = Spinner(text='Select Apartment Type',values=self.aptypes,size_hint=(1, None),height=50)

        
        def update_commune_spinner(spinner, text):
            if text in self.communes:
                search_commune_spinner.values = self.communes[text]
                search_commune_spinner.text = 'Select Commune'
            else:
                search_commune_spinner.values = []
                search_commune_spinner.text = 'Select Commune'

        
        search_city_spinner.bind(text=update_commune_spinner)
        result_text = TextInput(hint_text="Results will appear here...",multiline=True,readonly=True,size_hint=(1, None),height=200)

        search_layout.add_widget(Label(text="City:"))
        search_layout.add_widget(search_city_spinner)
        search_layout.add_widget(Label(text="Commune:"))
        search_layout.add_widget(search_commune_spinner)
        search_layout.add_widget(Label(text="Apartment Type:"))
        search_layout.add_widget(search_apartment_type_spinner)

        
        button_layout = BoxLayout(orientation='horizontal',size_hint=(1, None),height=50,spacing=10)
        search_button = Button(text="Search",size_hint=(0.5, None),height=50)
        search_button.bind(
            on_press=lambda x: self.search(
                search_city_spinner.text,
                search_commune_spinner.text,
                search_apartment_type_spinner.text,
                result_text
            )
        )

        clear_button = Button(text="Clear",size_hint=(0.5, None),height=50)
        clear_button.bind(
            on_press=lambda x: self.clear_search(
                search_city_spinner,
                search_commune_spinner,
                search_apartment_type_spinner,
                result_text
            )
        )

        button_layout.add_widget(search_button)
        button_layout.add_widget(clear_button)

        search_layout.add_widget(button_layout)
        search_layout.add_widget(result_text)

        search_popup.open()

    def search(self, city, commune, apttype, result_text):
        if city == 'Select City' or commune == 'Select Commune' or apttype == 'Select Apartment Type':
            result_text.text = "Please select City, Commune, and Apartment Type."
            return

        conn = self.connecter_bd()
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
                result_text.text = ""
                if results:
                    for row in results:
                        result_text.text += f"Name: {row[0]} {row[1]}, Email: {row[2]}, Phone: {row[3]}\n"
                else:
                    result_text.text = "No results found."
            except MySQLError as e:
                result_text.text = f"Error: {e}"
            finally:
                conn.close()

    def clear_search(self, search_city_spinner, search_commune_spinner, search_apartment_type_spinner, result_text):
        search_city_spinner.text = "Select City"
        search_commune_spinner.text = "Select Commune"
        search_apartment_type_spinner.text = "Select Apartment Type"
        search_commune_spinner.values = []
        result_text.text = ""

RentalFormApp().run()