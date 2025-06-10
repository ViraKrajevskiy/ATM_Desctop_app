from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from Backend.functions.translate.TranslateMenu import translations
from Backend.ClassesNew.CASH.credit_cards import CreditCards, PhoneNumber
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import Button


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


class PhoneLogin(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.add_widget(self.layout)

    def _popup(self, message):
        popup = Popup(title='Ошибка', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def on_pre_enter(self):
        self.layout.clear_widgets()
        texts = translations[self.manager.language]

        self.layout.add_widget(Label(text=texts["EnterCardNum"], font_size=24, size_hint_y=None, height=40))
        self.card_input = TextInput(hint_text=texts["EnterCardNum"], input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.card_input)

        self.pin_input = TextInput(hint_text=texts["EnterPIN"], password=True, input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.pin_input)

        btn_next = RoundedButton(text=texts.get("ConfirmPin"), size_hint_y=None, height=50)
        btn_next.bind(on_press=self.on_authenticate)
        self.layout.add_widget(btn_next)

        btn_back = RoundedButton(text=texts.get("back_button", "Назад/Back/Ortga"), size_hint_y=None, height=50)
        btn_back.bind(on_press=lambda _: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(btn_back)

        # Очистка полей при входе
        self.card_input.text = ''
        self.pin_input.text = ''

    def on_authenticate(self, _):
        texts = translations[self.manager.language]
        num = self.card_input.text.strip()
        pin = self.pin_input.text.strip()

        if not num or not pin or len(num) != 16 or len(pin) != 4:
            return self._popup(texts["InvalidOption"])

        try:
            card = CreditCards.get(CreditCards.card_number == int(num))
        except Exception:
            return self._popup(texts["KardNotCorrect"])

        if str(card.security_code) != pin:
            return self._popup(texts["KardNotCorrect"])

        self.manager.selected_card = card
        self.manager.current = 'phone_creen_sms'


class ChangePhoneScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = ThemedBoxLayout(orientation='vertical', spacing=10, padding=20)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.layout.clear_widgets()
        texts = translations[self.manager.language]

        card = getattr(self.manager, 'selected_card', None)

        # Если карта выбрана и привязан телефон — показываем его
        if card and card.phone_field.exists():
            current_phone = card.phone_field.get()
            self.layout.add_widget(Label(
                                       text=f"{texts.get('CurrentPhone', 'Подключённый номер')}: {current_phone.phone_number}",
                                       font_size=20, size_hint_y=None, height=40
                                   ))
        else:
            self.layout.add_widget(Label(
                                       text=texts.get("NoPhoneConnected", "Номер телефона не подключён"),
                                       font_size=20, size_hint_y=None, height=40
                                   ))

        self.layout.add_widget(Label(text=texts["EnterNewPhone"], font_size=24, size_hint_y=None, height=40))
        self.phone_input = TextInput(hint_text=texts["EnterNewPhone"], input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.phone_input)

        btn_save = RoundedButton(text=texts.get("Save", "Сохранить"), size_hint_y=None, height=50)
        btn_save.bind(on_press=self.save_new_phone)
        self.layout.add_widget(btn_save)

        btn_back = RoundedButton(text=texts.get("back_button", "Назад"), size_hint_y=None, height=50)
        btn_back.bind(on_press=lambda _: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(btn_back)

    def save_new_phone(self, _):
        texts = translations[self.manager.language]
        new_phone = self.phone_input.text.strip()

        # Добавляем +998, если пользователь ввёл только последние 9 цифр
        if new_phone.startswith('9') and len(new_phone) == 9:
            new_phone = '+998' + new_phone
        elif new_phone.startswith('998') and len(new_phone) == 12:
            new_phone = '+' + new_phone
        elif not new_phone.startswith('+998') or len(new_phone) != 13:
            return self._popup(texts.get("InvalidPhone", "Некорректный номер телефона"))

        card = getattr(self.manager, 'selected_card', None)
        if not card:
            return self._popup(texts.get("CardNotSelected", "Карта не выбрана"))

        # Удаляем старые привязки телефонов
        card.phone_field.clear()

        # Проверяем, существует ли такой телефон
        phone_obj, created = PhoneNumber.get_or_create(
            phone_number=new_phone,
            defaults={'balance': 0}
        )

        # Если телефон уже существовал — списываем 200 с его баланса (если хватает)
        if not created:
            if phone_obj.balance < 200:
                return self._popup(texts.get("NotEnoughPhoneBalance", "Недостаточно средств на телефоне"))
            phone_obj.balance -= 200
            phone_obj.save()

        # Привязываем телефон к карте
        card.phone_field.add(phone_obj)

        self.manager.current = 'menu'

    def _popup(self, msg):
        Popup(title="Ошибка", content=Label(text=msg), size_hint=(0.6, 0.4)).open()
        