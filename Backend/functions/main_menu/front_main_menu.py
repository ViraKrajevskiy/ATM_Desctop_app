import os
from kivy.graphics import Color, RoundedRectangle

from Backend.functions.changes_phone_pin.change_phone import PhoneLogin, ChangePhoneScreen
from Backend.functions.changes_phone_pin.change_pin import ChangePinLoginScreen, ChangePinScreen
from Backend.functions.main_menu.about_page import AboutScreen




from Backend.functions.see_course_mon.front_end_main import CurrencyScreen
from Backend.functions.translate.TranslateMenu import translations
from Backend.functions.Bank_worker_dashboard.main_func import *

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(0.2, 0.5, 0.7, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ThemedBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.6078, 0.7882, 0.8117, 1)
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



current_dir = os.path.dirname(os.path.abspath(__file__))  # папка скрипта
file_path = os.path.join(current_dir, 'translation.json')

with open(file_path, 'r', encoding='utf-8') as f:
    data = f.read()


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = None
        self.layout = ThemedBoxLayout(orientation='vertical', spacing=10, padding=20)
        self.label = Label(font_size=24)
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    def on_enter(self):
        # Активируем клавиатуру при входе на экран
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_key_down)

    def on_leave(self):
        # Деактивируем клавиатуру при выходе с экрана
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.on_key_down)
            self._keyboard = None

    def _keyboard_closed(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.on_key_down)
            self._keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        # Обработка Alt+1 для перехода на экран login
        if 'alt' in modifiers and (text == '1' or keycode[1] == '1'):
            self.manager.current = 'change_pins'
            return True
        return False

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
            2: 'change_pin_auth',
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

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = 'en'
        self.current_user = None

    def switch_to_screen(self, screen_name):
        self.current = screen_name

    def go_to_menu(self):
        self.get_screen('menu').set_language(self.language)
        self.current = 'menu'

class InfoScreen(Screen):
    def __init__(self, text_key='', **kwargs):
        super().__init__(**kwargs)
        self.text_key = text_key
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.label = Label(text='', font_size=20)
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        # получение текста из словаря translations
        lang = getattr(self.manager, 'language', 'en')
        text = translations.get(lang, {}).get(self.text_key, 'No info available')
        self.label.text = text

class BankingApp(App):
    def build(self):
        from Backend.functions.phone.pay_hone_number.pay_phone import PhoneTopUpStartScreen, PhoneTopUpScreen
        sm = MyScreenManager()
        # sm.add_widget(CardPaymentScreen(name='cardpayphone0'))
        sm.add_widget(LanguageScreen(name='language'))
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(CurrencyScreen(name='currency'))
        sm.add_widget(LoginScreen(name='change_pins'))
        sm.add_widget(AboutScreen(name='about'))
        # Экран авторизации перед сменой PIN
        sm.add_widget(ChangePinLoginScreen(name='change_pin_auth'))
        # Непосредственный экран «Смена PIN»
        sm.add_widget(ChangePinScreen(name='change_pin'))

        sm.add_widget(InfoScreen(name='transactions', text_key='Transactions'))
        sm.add_widget(ChangePhoneScreen(name ='phone_creen_sms'))
        sm.add_widget(PhoneLogin(name='connect_sms'))


        sm.add_widget(WalletCard(name='wal_card'))


        # sm.add_widget(PaymentMethodScreen(name ='pay_phone' ))

        sm.add_widget(BankDashboard(name='bank_dashboard'))
        sm.add_widget(DefaultUserTable(name='defaultuser_table'))
        sm.add_widget(RoleTable(name='role_table'))
        sm.add_widget(IncasatorTable(name='incasator_table'))
        sm.add_widget(UserTable(name='user_table'))
        sm.add_widget(PhoneNumberTable(name='phones_table'))
        sm.add_widget(CreditCardTable(name='credit_cards_table'))
        sm.add_widget(MoneyManagementScreen(name='money_rate'))
        sm.add_widget(BankWorkerTable(name='bankworker_table'))
        sm.add_widget(WalletTable(name='wallet_table'))
        sm.add_widget(AtmManagementScreen(name='atm_table'))

        sm.add_widget(PhoneTopUpStartScreen(name='pay_phone'))
        sm.add_widget(PhoneTopUpScreen(name='phone_topup_screen'))

        return sm


if __name__ == '__main__':
    BankingApp().run()