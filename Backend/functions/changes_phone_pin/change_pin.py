from kivy.uix.popup import Popup

from Backend.ClassesNew.CASH.credit_cards import CreditCards
from Backend.functions.translate.TranslateMenu import translations
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class RoundedButton(Button):
    def __init__(self, bg_color=(0.2, 0.5, 0.7, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ThemedBoxLayout(BoxLayout):
    def __init__(self, bg_color=(0.6078, 0.7882, 0.8117, 1), **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size



# Экран авторизации по PIN перед сменой
class ChangePinLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = ThemedBoxLayout(orientation='vertical', spacing=10, padding=20)

        self.label = Label(text="Введите текущий PIN", font_size=20, size_hint_y=None, height=40)
        self.pin_input = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
        self.button = RoundedButton(text="Продолжить", size_hint_y=None, height=50)
        self.button.bind(on_press=self.check_pin)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.pin_input)
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)

    def check_pin(self, *args):
        pin = self.pin_input.text
        if pin == '1234':
            self.manager.current = 'change_pin'
        else:
            self.label.text = "Неверный PIN. Повторите."

    def on_pre_enter(self):
        self.layout.clear_widgets()
        texts = translations[self.manager.language]

        self.layout.add_widget(Label(text=texts["EnterCardNum"], font_size=24, size_hint_y=None, height=40))
        self.card_input = TextInput(hint_text=texts["EnterCardNum"], input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.card_input)

        self.pin_input  = TextInput(hint_text=texts["EnterPIN"], password=True, input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.pin_input)

        btn_next = RoundedButton(text=texts["ChangePin"], size_hint_y=None, height=50)
        btn_next.bind(on_press=self.on_authenticate)
        self.layout.add_widget(btn_next)

        btn_back = RoundedButton(text=texts.get("back_button", "Назад/Back/Ortga"), size_hint_y=None, height=50)
        btn_back.bind(on_press=lambda _: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(btn_back)

    def on_authenticate(self, _):
        texts = translations[self.manager.language]
        num, pin = self.card_input.text.strip(), self.pin_input.text.strip()
        if not num or not pin:
            return self._popup(texts["InvalidOption"])
        try:
            card = CreditCards.get(CreditCards.card_number == int(num))
        except Exception:
            return self._popup(texts["KardNotCorrect"])
        if str(card.security_code) != pin:
            return self._popup(texts["KardNotCorrect"])
        self.manager.selected_card = card
        self.manager.current = 'change_pin'

    def _popup(self, msg):
        texts = translations[self.manager.language]
        Popup(title=texts["KardNotCorrect"], content=Label(text=msg), size_hint=(0.6,0.4)).open()




# Экран смены PIN
class ChangePinScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from Backend.functions.main_menu.front_main_menu import ThemedBoxLayout

        self.layout = ThemedBoxLayout(orientation='vertical', spacing=10, padding=20)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        if not hasattr(self.manager, 'selected_card'):
            self.manager.current = 'change_pin_auth'
            return
        self.build_ui()



    def build_ui(self):
        self.layout.clear_widgets()

        texts = translations[self.manager.language]
        card = self.manager.selected_card

        self.layout.add_widget(Label(text=texts["ChangePin"], font_size=24, size_hint_y=None, height=40))
        self.layout.add_widget(Label(text=f"{texts['EnterCardNum']} {card.card_number}", size_hint_y=None, height=30))

        self.new_pin = TextInput(hint_text=texts["ChangePin"], password=True, input_filter='int',
                             multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.new_pin)

        self.confirm_pin = TextInput(hint_text=texts["InvalidOptionRange"], password=True,
                                 input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.confirm_pin)

        btn_save = RoundedButton(text=texts["ChangePin"], size_hint_y=None, height=50)
        btn_save.bind(on_press=self.on_save)
        self.layout.add_widget(btn_save)

        btn_back = RoundedButton(text=texts.get("back_button", "Назад/Back/Ortga"), size_hint_y=None, height=50)
        btn_back.bind(on_press=lambda _: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(btn_back)


    def _popup(self, msg):
        texts = translations[self.manager.language]
        Popup(title=texts["Error"], content=Label(text=msg), size_hint=(0.6, 0.4)).open()

    def on_save(self, _):
        texts = translations[self.manager.language]
        n, c = self.new_pin.text.strip(), self.confirm_pin.text.strip()
        if not n or not c:
            return self._popup(texts["InvalidOption"])
        if n != c:
            return self._popup(texts["PINMismatch"])
        card = self.manager.selected_card
        try:
            card.security_code = int(n)
            card.save()
        except Exception as e:
            return self._popup(f"{texts['InvalidOption']}\n{str(e)}")

        popup = Popup(
                title=texts("ExchangeTitle","back"),
            content=Label(text=texts["BackToMenu"]),
            size_hint=(0.6, 0.4))

        def on_popup_dismiss(*args):
            if hasattr(self.manager, 'selected_card'):
                delattr(self.manager, 'selected_card')
            self.manager.current = 'language'

        popup.bind(on_dismiss=on_popup_dismiss)
        popup.open()
        