from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup




class PayByCardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pay_by_card"

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        layout.add_widget(Label(text="Оплата картой", font_size=24, size_hint_y=None, height=40))

        self.card_number_input = TextInput(hint_text="Номер карты или последние 4 цифры", multiline=False, input_filter='int')
        layout.add_widget(self.card_number_input)

        self.card_password_input = TextInput(hint_text="Пароль", multiline=False, password=True)
        layout.add_widget(self.card_password_input)

        self.phone_input = TextInput(hint_text="Номер телефона", multiline=False, input_filter='int')
        layout.add_widget(self.phone_input)

        self.amount_input = TextInput(hint_text="Сумма пополнения", multiline=False, input_filter='int')
        layout.add_widget(self.amount_input)

        pay_button = Button(text="Оплатить", size_hint_y=None, height=50)
        pay_button.bind(on_press=self.process_payment)
        layout.add_widget(pay_button)

        self.add_widget(layout)

    def process_payment(self, instance):
        card_number = self.card_number_input.text.strip()
        password = self.card_password_input.text.strip()
        phone = self.phone_input.text.strip()
        amount_text = self.amount_input.text.strip()

        if not (card_number and password and phone and amount_text):
            self.show_popup("Ошибка", "Все поля обязательны")
            return

        try:
            amount = int(amount_text)
        except ValueError:
            self.show_popup("Ошибка", "Сумма должна быть числом")
            return

        try:
            atm = self.manager.atm  # Предполагается, что ATM передан через ScreenManager
            result = pay_with_card_to_phone(card_number, password, phone, amount, atm)
            self.show_popup("Успех", f"Переведено {result['amount']} пользователю {result['to_user']}")
        except Exception as e:
            self.show_popup("Ошибка", str(e))

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()
