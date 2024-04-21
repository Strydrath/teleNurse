## Starting point of Android app
## Using Kivy for GUI
## Using Python for logic
## Using SQLite for database

## App implements support for a nurse giving visits to patients
## App will have 3 screens:
## Calendar with planned visits
## List of patients with details
## List of visits with details

## Database has 6 tables:
## patients
## addresses
## visits
## medications
## actions to take during visit
## times of day for medications 

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView

from db import Database


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.layout.add_widget(Label(text='Main Screen'))
        self.layout.add_widget(Button(text='Patients', on_press=self.patients))
        #self.layout.add_widget(Button(text='Visits', on_press=self.visits))
        #self.layout.add_widget(Button(text='Calendar', on_press=self.calendar))
        self.layout.add_widget(Button(text='Exit', on_press=self.exit))

    def patients(self, instance):
        self.manager.current = 'patients'

    '''
    def visits(self, instance):
        self.manager.current = 'visits'

    def calendar(self, instance):
        self.manager.current = 'calendar'
    '''
    def exit(self, instance):
        App.get_running_app().stop()
    
class PatientsScreen(Screen):
    def __init__(self, **kwargs):
        super(PatientsScreen, self).__init__(**kwargs)
        # show all patients
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.layout.add_widget(Label(text='Patients Screen'))
        self.layout.add_widget(Button(text='Add Patient', on_press=self.add_patient))
        self.layout.add_widget(Button(text='Back', on_press=self.back))
        self.patients = Database('nurse.db').get_patients()
        for patient in self.patients:
            self.layout.add_widget(Label(text=str(patient)))
            self.layout.add_widget(Button(text='Details', on_press=self.details))
        self.layout.add_widget(Button(text='Back', on_press=self.back))
    
    def add_patient(self, instance):
        self.manager.current = 'add_patient'
    
    def details(self, instance):
        self.manager.current = 'patient_details'




    def back(self, instance):
        self.manager.current = 'main'

def main():
    # establish connection to database
    db = Database('nurse.db')
    db.create_connection()
    db.create_tables()
    db.insert_address((1, 'ul. Kowalska 1', 'Warszawa', '00-001'))
    db.insert_address((2, 'ul. Nowa 2', 'Kraków', '00-002'))
    db.insert_patient(('Jan', 'Kowalski', '1990-01-01', '90010112345', 1))
    db.insert_patient(('Anna', 'Nowak', '1995-02-02', '95020212345', 2))
    db.insert_visit(('2020-01-01', '12:00', 1))
    db.insert_visit(('2020-02-02', '13:00', 2))

    class NurseApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(MainScreen(name='main'))
            sm.add_widget(PatientsScreen(name='patients'))
            return sm

    NurseApp().run()

if __name__ == '__main__':
    main()
