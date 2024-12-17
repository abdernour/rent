from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import Boxlayout
class fenetre(App):
         def build(delf):
             layout = Boxlayout(orientation = 'vertical')
             layout.add_widget(Button(text='button num1'))
             layout.add_widget(Button(text='button num2'))
             layout.add_widget(Button(text='button num3'))
             return layout
         
fenetre.run()
             