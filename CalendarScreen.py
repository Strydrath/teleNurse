from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from datetime import datetime
import calendar


class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=5, padding=10)
        self.add_widget(self.layout)

        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                       'October', 'November', 'December']
        self.date = {
            'year': datetime.now().year,
            'month': datetime.now().month,
            'day': datetime.now().day
        }
        self.calendar = calendar.monthcalendar(self.date['year'], self.date['month'])

        self.active_info = f'{self.months[self.date["month"] - 1]} {self.date["year"]}'

        self.menu = BoxLayout(orientation='horizontal', size_hint=(.7, .2), pos_hint={'center_x': .5, 'center_y': .5})
        self.info = BoxLayout(orientation='vertical')

        self.month_view = Label(text=self.active_info, size_hint=(1, .2))

        self.info.add_widget(Label(text='Calendar Screen', size_hint=(1, .2)))
        self.info.add_widget(self.month_view)

        self.menu.add_widget(Button(text='<', on_press=self.change_month, background_color=(.2, .5, .3, 1),
                                    size_hint=(.15, .3), pos_hint={'center_x': .5, 'center_y': .5}))
        self.menu.add_widget(self.info)
        self.menu.add_widget(Button(text='>', on_press=self.change_month, background_color=(.2, .5, .3, 1),
                                    size_hint=(.15, .3), pos_hint={'center_x': .5, 'center_y': .5}))

        self.calendar = Calendar(self.calendar, self.date)

        self.btnBox = BoxLayout(orientation='horizontal', size_hint=(.7, .2), pos_hint={'center_x': .5, 'center_y': .5})
        self.button = Button(text='Back', on_press=self.back, background_color=(.21, .35, .47, 1),
                             size_hint=(.5, .7), pos_hint={'center_x': .5, 'center_y': .5})

        self.btnBox.add_widget(self.button)

        self.layout.add_widget(self.menu)
        self.layout.add_widget(self.calendar)
        self.layout.add_widget(self.btnBox)

    def change_month(self, symbol):
        self.info.remove_widget(self.month_view)
        self.layout.remove_widget(self.calendar)
        self.layout.remove_widget(self.btnBox)

        if symbol.text == '<' and self.date['month'] > 1:
            self.date['month'] -= 1
        elif symbol.text == '<' and self.date['month'] == 1:
            self.date['month'] = 12
            self.date['year'] -= 1
        elif symbol.text == '>' and self.date['month'] < 12:
            self.date['month'] += 1
        elif symbol.text == '>' and self.date['month'] == 12:
            self.date['month'] = 1
            self.date['year'] += 1

        self.active_info = f'{self.months[self.date["month"] - 1]} {self.date["year"]}'
        self.month_view = Label(text=self.active_info, size_hint=(1, .2))

        self.calendar = calendar.monthcalendar(self.date['year'], self.date['month'])
        self.calendar = Calendar(self.calendar, self.date)

        self.info.add_widget(self.month_view)
        self.layout.add_widget(self.calendar)
        self.layout.add_widget(self.btnBox)

    def get_dates(self):
        pass

    def back(self, instance):
        self.manager.current = 'main'


class Calendar(Screen):
    def __init__(self, days, date, **kwargs):
        super(Calendar, self).__init__(**kwargs)
        self.layout = GridLayout(cols=7, spacing=5)
        self.add_widget(self.layout)

        self.calendar = days
        self.date = date

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for day in days:
            self.layout.add_widget(Label(text=day))

        for week in self.calendar:
            for i, day in enumerate(week):
                btn = Button()
                if i == 5 or i == 6:
                    btn.background_color = (1, 0, 0, 1)
                else:
                    btn.background_color = (.21, .35, .47)

                if (day == self.date['day'] and self.date['month'] == datetime.now().month
                        and self.date['year'] == datetime.now().year):
                    btn.background_color = (.2, .8, .2, 1)

                if day == 0:
                    btn.text = ''
                else:
                    btn.text = str(day)
                self.layout.add_widget(btn)
