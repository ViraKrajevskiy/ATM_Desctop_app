from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from Backend.functions.main_menu.front_main_menu import RoundedButton


from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from Backend.functions.main_menu.front_main_menu import RoundedButton


class PhoneTopUpStartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.phone_input = TextInput(hint_text="Номер телефона", multiline=False)
        self.card_input = TextInput(hint_text="Номер карты", multiline=False)
        self.login_input = TextInput(hint_text="Login (special_identificator)", multiline=False)

        self.submit_btn = RoundedButton(text="Продолжить", size_hint=(None, None), size=(200, 50))
        self.submit_btn.bind(on_press=self.proceed_to_topup)

        self.back_btn = RoundedButton(text="Назад", size_hint=(None, None), size=(200, 50))
        self.back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu_screen'))

        layout.add_widget(Label(text="Введите номер телефона"))
        layout.add_widget(self.phone_input)
        layout.add_widget(Label(text="Введите номер карты"))
        layout.add_widget(self.card_input)
        layout.add_widget(Label(text="Введите логин владельца"))
        layout.add_widget(self.login_input)
        layout.add_widget(self.submit_btn)
        layout.add_widget(self.back_btn)

        self.add_widget(layout)

    def proceed_to_topup(self, instance):
        from Backend.ClassesNew.CASH.credit_cards import CreditCards, PhoneNumber

        phone_text = self.phone_input.text.strip()
        card_text = self.card_input.text.strip()
        login = self.login_input.text.strip()

        if not all([phone_text, card_text, login]):
            print("Пожалуйста, заполните все поля")
            return

        try:
            self.card = CreditCards.get(
                (CreditCards.card_number == card_text) &
                (CreditCards.special_identificator == login)
            )
        except CreditCards.DoesNotExist:
            print("Карта не найдена или логин не совпадает")
            return

        try:
            self.phone = PhoneNumber.get(PhoneNumber.phone_number == phone_text)
        except PhoneNumber.DoesNotExist:
            print("Номер телефона не найден")
            return

        # Проверка связи через M2M
        if self.phone not in self.card.phones:
            print("Этот номер телефона не привязан к данной карте")
            return

        self.manager.get_screen('phone_topup_screen').set_data(self.card, self.phone)
        self.manager.current = 'phone_topup_screen'
        from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from Backend.functions.main_menu.front_main_menu import RoundedButton


class PhoneTopUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.card = None
        self.phone = None

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.amount_input = TextInput(hint_text="Сумма пополнения", multiline=False)
        self.confirm_btn = RoundedButton(text="Пополнить", size_hint=(None, None), size=(200, 50))
        self.confirm_btn.bind(on_press=self.perform_topup)

        self.back_btn = RoundedButton(text="Назад", size_hint=(None, None), size=(200, 50))
        self.back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu_screen'))

        layout.add_widget(Label(text="Введите сумму пополнения"))
        layout.add_widget(self.amount_input)
        layout.add_widget(self.confirm_btn)
        layout.add_widget(self.back_btn)

        self.result_label = Label(text="")
        layout.add_widget(self.result_label)

        self.add_widget(layout)

    def set_data(self, card, phone):
        self.card = card
        self.phone = phone

    def perform_topup(self, instance):
        from peewee import IntegrityError

        try:
            amount = int(self.amount_input.text.strip())
            if amount <= 0:
                self.result_label.text = "Сумма должна быть положительной"
                return
        except ValueError:
            self.result_label.text = "Введите корректную сумму"
            return

        if self.card.balance < amount:
            self.result_label.text = "Недостаточно средств на карте"
            return

        try:
            self.card.balance -= amount
            self.card.save()

            self.phone.balance += amount
            self.phone.save()

            self.result_label.text = f"Телефон {self.phone.phone_number} пополнен на {amount}₽"
            self.amount_input.text = ""
        except IntegrityError as e:
            self.result_label.text = "Ошибка при пополнении. Повторите попытку."
            print(f"DB error: {e}")
            