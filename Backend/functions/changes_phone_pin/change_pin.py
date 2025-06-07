from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# Импорт модели кредитной карты
from Backend.ClassesNew.CASH.credit_cards import CreditCards
from Backend.functions.translate.TranslateMenu import *
# Предполагается, что translations уже загружены в этом модуле:
# with open('translation.json', "r", encoding="utf-8") as f:
#     translations = json.load(f)

class ChangePinLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        # Перестраиваем интерфейс при каждом входе (чтобы подтянулись переводы)
        self.build_ui()

    def build_ui(self):
        self.layout.clear_widgets()
        lang = self.manager.language
        texts = translations[lang]

        # Заголовок
        lbl_title = Label(
            text=texts.get("EnterCardNum", "Enter your card number:"),
            font_size=24,
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(lbl_title)

        # Поле для номера карты
        self.card_input = TextInput(
            hint_text=texts.get("EnterCardNum", "Enter your card number:"),
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(self.card_input)

        # Поле для старого PIN
        self.pin_input = TextInput(
            hint_text=texts.get("EnterPIN", "Enter your PIN code:"),
            password=True,
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(self.pin_input)

        # Кнопка «Далее»
        btn_next = Button(
            text=texts.get("ChangePin", "Enter your new PIN code."),
            size_hint_y=None,
            height=50
        )
        btn_next.bind(on_press=self.on_authenticate)
        self.layout.add_widget(btn_next)

        # Кнопка «Назад»
        btn_back = Button(
            text=texts.get("back_button", "Back"),
            size_hint_y=None,
            height=50
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(btn_back)

    def on_authenticate(self, instance):
        lang = self.manager.language
        texts = translations[lang]

        card_num = self.card_input.text.strip()
        pin_code = self.pin_input.text.strip()

        if not card_num or not pin_code:
            self.show_popup(texts.get("InvalidOption", "Please enter a valid number."))
            return

        # Ищем карту
        try:
            card = CreditCards.get(CreditCards.card_number == int(card_num))
        except (CreditCards.DoesNotExist, ValueError):
            self.show_popup(texts.get("KardNotCorrect", "Incorrect card number or PIN code."))
            return

        # Проверяем PIN
        if str(card.security_code) != pin_code:
            self.show_popup(texts.get("KardNotCorrect", "Incorrect card number or PIN code."))
            return

        # Авторизация успешна — сохраняем найденную карту в manager и переходим к смене PIN
        self.manager.selected_card = card
        self.manager.current = 'change_pin'

    def show_popup(self, message, title=None):
        lang = self.manager.language
        texts = translations[lang]
        popup_title = title or texts.get("KardNotCorrect", "Error")
        popup = Popup(
            title=popup_title,
            content=Label(text=message),
            size_hint=(0.6, 0.4)
        )
        popup.open()



class ChangePinScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        # Если карточка не передана — возвращаем на экран авторизации
        if not hasattr(self.manager, 'selected_card'):
            self.manager.current = 'change_pin_auth'
            return
        self.build_ui()

    def build_ui(self):
        self.layout.clear_widgets()
        lang = self.manager.language
        texts = translations[lang]

        # Заголовок
        lbl_title = Label(
            text=texts.get("ExchangeTitle", "Change PIN"),
            font_size=24,
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(lbl_title)

        # Отобразим номер карты, чтобы пользователь видел, для какой карты меняем PIN
        card = self.manager.selected_card
        lbl_cardnum = Label(
            text=f"{texts.get('EnterCardNum', 'Card Number:')} {card.card_number}",
            size_hint_y=None,
            height=30
        )
        self.layout.add_widget(lbl_cardnum)

        # Поле для нового PIN
        self.new_pin_input = TextInput(
            hint_text=texts.get("ChangePin", "Enter your new PIN code."),
            password=True,
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(self.new_pin_input)

        # Кнопка «Сохранить»
        btn_save = Button(
            text=texts.get("ExchangeMethod", "Save"),  # если нужен особый перевод, можно вынести отдельным ключом
            size_hint_y=None,
            height=50
        )
        btn_save.bind(on_press=self.on_save_pin)
        self.layout.add_widget(btn_save)

        # Кнопка «Назад» — вернуться в авторизацию смены PIN
        btn_back = Button(
            text=texts.get("back_button", "Back"),
            size_hint_y=None,
            height=50
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'change_pin_auth'))
        self.layout.add_widget(btn_back)

    def on_save_pin(self, instance):
        lang = self.manager.language
        texts = translations[lang]

        new_pin = self.new_pin_input.text.strip()
        if not new_pin:
            self.show_popup(texts.get("InvalidOption", "Please enter a valid number."))
            return

        # Обновляем PIN в объекте карточки
        card = self.manager.selected_card
        try:
            card.security_code = int(new_pin)
            card.save()
        except ValueError:
            self.show_popup(texts.get("InvalidOption", "Please enter a valid number."))
            return

        # Успешно изменили PIN — покажем сообщение и вернёмся в главное меню
        self.show_popup(
            texts.get("BackToMenu", "Press Enter to return to menu."),
            title=texts.get("ExchangeTitle", "Success")
        )
        # Стираем номер из memory, чтобы при повторном заходе приходил заново
        delattr(self.manager, 'selected_card')
        # После закрытия попапа вернём в меню
        self.manager.current = 'menu'

    def show_popup(self, message, title=None):
        lang = self.manager.language
        texts = translations[lang]
        popup_title = title or texts.get("ExchangeTitle", "Info")
        popup = Popup(
            title=popup_title,
            content=Label(text=message),
            size_hint=(0.6, 0.4)
        )
        popup.open()
        