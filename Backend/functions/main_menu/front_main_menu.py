from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
import json

from Backend.functions.see_course_mon.front_end_main import CurrencyScreen


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(0.2, 0.5, 0.7, 1)  # Цвет кнопки
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ThemedBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.6078, 0.7882, 0.8117, 1)  # RGB(155, 201, 207)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class LanguageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = ThemedBoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text="Choose language / Выберите язык / Tilni tanlang", font_size=24))

        self.lang_map = {'English': 'en', 'Русский': 'ru', 'O‘zbekcha': 'uz'}

        for name, code in self.lang_map.items():
            btn = RoundedButton(text=name, size_hint_y=None, height=50)
            btn.bind(on_press=lambda inst, c=code: self.select_language(c))
            layout.add_widget(btn)

        self.add_widget(layout)

    def select_language(self, code):
        self.manager.language = code
        self.manager.get_screen('menu').set_language(code)
        self.manager.current = 'menu'


# Load translations
with open('translation.json', "r", encoding="utf-8") as f:
    translations = json.load(f)

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = ThemedBoxLayout(orientation='vertical', spacing=10, padding=20)
        self.label = Label(font_size=24)
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    def set_language(self, lang):
        self.lang = lang
        self.data = translations[lang]
        self.render_menu()

    def render_menu(self):
        self.layout.clear_widgets()
        self.label.text = f"{self.data['LanguageWelcome']}\n{self.data['ChooseLanguage']}"
        self.layout.add_widget(self.label)

        screen_map = {
            0: 'about',
            1: 'currency',
            2: 'change_pin',
            3: 'transactions',
            4: 'connect_sms',
            5: 'pay_phone',
            6: 'language',
        }



        for idx, item in enumerate(self.data['MenuOption']):
            btn = RoundedButton(text=item, size_hint_y=None, height=50)
            if idx in screen_map:
                btn.bind(on_press=lambda inst, s=screen_map[idx]: self.manager.switch_to_screen(s))
            elif idx == 7:
                btn.bind(on_press=lambda inst: App.get_running_app().stop())
            self.layout.add_widget(btn)


class InfoScreen(Screen):
    def __init__(self, text_key, **kwargs):
        super().__init__(**kwargs)
        self.text_key = text_key

        self.label = Label(
            text="",
            font_size=20,
            halign='center',
            valign='middle',
            size_hint_y=None
        )
        self.label.bind(texture_size=self.update_label_height)

        back_btn = Button(text="Back", size_hint_y=None, height=50)
        back_btn.bind(on_press=lambda x: self.manager.go_to_menu())

        self.layout = ThemedBoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(self.label)
        self.layout.add_widget(back_btn)
        self.add_widget(self.layout)

    def update_label_height(self, *args):
        self.label.height = self.label.texture_size[1]

    def on_enter(self):
        lang = self.manager.language
        text = translations[lang].get(self.text_key, "No content.")
        self.label.text = text
        self.label.text_size = (self.width - 40, None)  # ширина с отступами

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = 'en'

    def switch_to_screen(self, screen_name):
        self.current = screen_name

    def go_to_menu(self):
        self.get_screen('menu').set_language(self.language)
        self.current = 'menu'


class BankingApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(LanguageScreen(name='language'))
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(InfoScreen(name='about', text_key='AboutUs'))
        sm.add_widget(CurrencyScreen(name='currency'))  # имя соответствует screen_map
        sm.add_widget(InfoScreen(name='change_pin', text_key='ChangePin'))
        sm.add_widget(InfoScreen(name='transactions', text_key='Transactions'))
        sm.add_widget(InfoScreen(name='connect_sms', text_key='ConnectSMS'))
        sm.add_widget(InfoScreen(name='pay_phone', text_key='LoginCardMOney'))  # Заглушка
        return sm


if __name__ == '__main__':
    BankingApp().run()
