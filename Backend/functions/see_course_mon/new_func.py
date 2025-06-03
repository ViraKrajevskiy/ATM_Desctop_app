from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from Backend.functions.see_course_mon.course_rater_func import (
    start_currency_simulation
)
from Backend.data_base.database import db
from Backend.functions.see_course_mon.see_course_1 import get_latest_rate
from Backend.functions.translate.TranslateMenu import translations

currency_simulation_started = False

class CurrencyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.usd_label = Label(font_size=20)
        self.rub_label = Label(font_size=20)
        self.eur_label = Label(font_size=20)

        self.info_label = Label(text="", font_size=16)

        exchange_btn = Button(text="1. Обмен валюты", size_hint_y=None, height=50)
        exchange_btn.bind(on_press=self.exchange_currency)

        back_btn = Button(text="2. Назад в меню", size_hint_y=None, height=50)
        back_btn.bind(on_press=lambda x: self.manager.go_to_menu())

        exit_btn = Button(text="3. Выйти из программы", size_hint_y=None, height=50)
        exit_btn.bind(on_press=lambda x: exit(0))

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(self.usd_label)
        self.layout.add_widget(self.rub_label)
        self.layout.add_widget(self.eur_label)
        self.layout.add_widget(exchange_btn)
        self.layout.add_widget(back_btn)
        self.layout.add_widget(exit_btn)
        self.layout.add_widget(self.info_label)

        self.add_widget(self.layout)

    def on_enter(self):
        global currency_simulation_started

        if not currency_simulation_started:
            start_currency_simulation()
            currency_simulation_started = True

        if db.is_closed():
            db.connect()

        # Обновление курсов
        lang = self.manager.language
        data = translations[lang]

        usd = get_latest_rate("SUM->USD")
        rub = get_latest_rate("SUM->RUB")
        eur = get_latest_rate("SUM->EUR")

        self.usd_label.text = f"{data['SeeCourseMenu'][0]} {usd} UZS"
        self.rub_label.text = f"{data['SeeCourseMenu'][1]} {rub} UZS"
        self.eur_label.text = f"{data['SeeCourseMenu'][2]} {eur} UZS"

        self.info_label.text = ""  # Очистка прошлых сообщений

    def exchange_currency(self, instance):
        self.info_label.text = ">> Функция обмена валюты пока не реализована."
