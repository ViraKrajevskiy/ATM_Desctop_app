from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle

from Backend.data_base import db
from Backend.functions import start_currency_simulation, get_latest_rate
from Backend.functions.translate.TranslateMenu import translations

currency_simulation_started = False

class CurrencyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(155 / 255, 201 / 255, 207 / 255, 1)  # фон RGB
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.usd_label = Label(font_size=20)
        self.rub_label = Label(font_size=20)
        self.eur_label = Label(font_size=20)

        self.info_label = Label(text="", font_size=16)

        # Кнопки с кастомным фоном
        self.exchange_btn = self.create_rounded_button()
        self.exchange_btn.bind(on_press=self.exchange_currency)

        self.back_btn = self.create_rounded_button()
        self.back_btn.bind(on_press=lambda x: self.manager.go_to_menu())

        self.exit_btn = self.create_rounded_button()
        self.exit_btn.bind(on_press=lambda x: exit(0))

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(self.usd_label)
        self.layout.add_widget(self.rub_label)
        self.layout.add_widget(self.eur_label)
        self.layout.add_widget(self.exchange_btn)
        self.layout.add_widget(self.back_btn)
        self.layout.add_widget(self.exit_btn)
        self.layout.add_widget(self.info_label)

        self.add_widget(self.layout)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def create_rounded_button(self):
        btn = Button(
            size_hint_y=None,
            height=50,
            background_normal='',  # отключает стандартный фон
            background_color=(0, 0, 0, 0),  # полностью прозрачный фон
            color=(0, 0.2, 0.3, 1),
            font_size=16
    )

        with btn.canvas.before:
            Color(0.2, 0.5, 0.7, 1)  # цвет фона кнопки
            btn.rounded_rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[20, 20, 20, 20])

        btn.bind(pos=self.update_button_canvas, size=self.update_button_canvas)
        return btn

    def update_button_canvas(self, instance, *args):
        instance.rounded_rect.pos = instance.pos
        instance.rounded_rect.size = instance.size

    def on_enter(self):
        global currency_simulation_started

        if not currency_simulation_started:
            start_currency_simulation()
            currency_simulation_started = True

        if db.is_closed():
            db.connect()

        lang = self.manager.language
        data = translations[lang]

        usd = get_latest_rate("SUM->USD")
        rub = get_latest_rate("SUM->RUB")
        eur = get_latest_rate("SUM->EUR")

        self.usd_label.text = f"{data['SeeCourseMenu'][0]} {usd} UZS"
        self.rub_label.text = f"{data['SeeCourseMenu'][1]} {rub} UZS"
        self.eur_label.text = f"{data['SeeCourseMenu'][2]} {eur} UZS"

        self.exchange_btn.text = data['SeeCourseMenu'][3]
        self.back_btn.text = data['SeeCourseMenu'][4]
        self.exit_btn.text = data['SeeCourseMenu'][5]

        self.info_label.text = ""

    def exchange_currency(self, instance):
        self.info_label.text = ">> Функция обмена валюты пока не реализована."
