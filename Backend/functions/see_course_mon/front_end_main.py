from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from Backend.data_base.database import db
from Backend.functions.see_course_mon.course_rater_func import start_currency_simulation
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

        # Кнопки сохраняем как поля
        self.exchange_btn = Button(size_hint_y=None, height=50)
        self.exchange_btn.bind(on_press=self.exchange_currency)

        self.back_btn = Button(size_hint_y=None, height=50)
        self.back_btn.bind(on_press=lambda x: self.manager.go_to_menu())

        self.exit_btn = Button(size_hint_y=None, height=50)
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

        # обновляем тексты кнопок в соответствии с языком
        self.exchange_btn.text = data['SeeCourseMenu'][3]  # "Начать конвертацию"
        self.back_btn.text = data['SeeCourseMenu'][4]      # "Вернуться на выбор языка"
        self.exit_btn.text = data['SeeCourseMenu'][5]      # "Выход из программы"

        self.info_label.text = ""  # очистка старых сообщений

    def exchange_currency(self, instance):
        self.info_label.text = ">> Функция обмена валюты пока не реализована."

    # def exchange_currency(self, instance):
    #     # Пока заглушка с сообщением
    #     self.info_label.text = ">> Функция обмена валюты пока не реализована."
# Флаг для запуска симуляции курса валют только один раз
#
# class CurrencyScreen(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#         # Метки для отображения курсов валют
#         self.usd_label = Label(font_size=20)
#         self.rub_label = Label(font_size=20)
#         self.eur_label = Label(font_size=20)
#
#         # Информационная метка для сообщений пользователю
#         self.info_label = Label(text="", font_size=16)
#
#         # Кнопка запуска обмена валюты (пока заглушка)
#         exchange_btn = Button(text='Начать конвертацию', size_hint_y=None, height=50)
#         exchange_btn.bind(on_press=self.exchange_currency)
#
#         # Кнопка возврата в меню выбора языка
#         back_btn = Button(text='Вернуться на выбор языка', size_hint_y=None, height=50)
#         back_btn.bind(on_press=lambda x: self.manager.go_to_menu())
#
#         # Кнопка выхода из приложения
#         exit_btn = Button(text='Выход из программы', size_hint_y=None, height=50)
#         exit_btn.bind(on_press=lambda x: exit(0))
#
#         # Вертикальный layout для расположения всех виджетов
#         self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
#         self.layout.add_widget(self.usd_label)
#         self.layout.add_widget(self.rub_label)
#         self.layout.add_widget(self.eur_label)
#         self.layout.add_widget(exchange_btn)
#         self.layout.add_widget(back_btn)
#         self.layout.add_widget(exit_btn)
#         self.layout.add_widget(self.info_label)
#
#         self.add_widget(self.layout)
#
#     def on_enter(self):
#         global currency_simulation_started
#
#         # Запуск симуляции курса валют только при первом входе на экран
#         if not currency_simulation_started:
#             start_currency_simulation()
#             currency_simulation_started = True
#
#         # Подключение к базе, если закрыто соединение
#         if db.is_closed():
#             db.connect()
#
#         # Получение языка из менеджера экранов и переводов
#         lang = self.manager.language
#         data = translations[lang]
#
#         # Получение последних курсов валют из базы или сервиса
#         usd = get_latest_rate("SUM->USD")
#         rub = get_latest_rate("SUM->RUB")
#         eur = get_latest_rate("SUM->EUR")
#
#         # Обновление текста меток с курсами валют и переводом
#         self.usd_label.text = f"{data['SeeCourseMenu'][0]} {usd} UZS"
#         self.rub_label.text = f"{data['SeeCourseMenu'][1]} {rub} UZS"
#         self.eur_label.text = f"{data['SeeCourseMenu'][2]} {eur} UZS"
#
#         # Очистка информационного поля
#         self.info_label.text = ""

