from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from Backend.functions.phone.pay_hone_number.pay_phone import transfer_cash_to_atm
from Backend.ClassesNew.CASH.wallet import WalletMoney


class CashPaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nominal_inputs = {}
        self.build_ui()

    def build_ui(self):
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.title = Label(text="💵 Выберите номиналы и введите количество", font_size=24, size_hint_y=None, height=50)
        self.layout.add_widget(self.title)

        self.inputs_layout = BoxLayout(orientation='vertical', spacing=10)
        self.layout.add_widget(self.inputs_layout)

        self.pay_button = Button(text="Оплатить", size_hint_y=None, height=50)
        self.pay_button.bind(on_press=lambda instance: self.on_pay_button_pressed())
        self.layout.add_widget(self.pay_button)

        self.back_button = Button(text="Назад", size_hint_y=None, height=50)
        self.back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'pay_phone'))
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def on_enter(self):
        self.refresh_inputs()

    def refresh_inputs(self):
        self.inputs_layout.clear_widgets()
        self.nominal_inputs.clear()

        user = getattr(self.manager, "current_user", None)
        if not user or not user.wallet:
            self.show_error("Пользователь или кошелёк не найден.")
            return

        wallet_id = user.wallet.id
        wallet_money_qs = WalletMoney.select().where(WalletMoney.wallet == wallet_id).join(WalletMoney.money)

        has_money = False
        for entry in wallet_money_qs:
            has_money = True
            nominal = entry.money.money_nominal
            money_id = entry.money.money_id
            available = entry.quantity

            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            label = Label(text=f"{nominal} сум — в наличии: {available}", size_hint_x=0.6)
            input_field = TextInput(hint_text="Количество", input_filter='int', multiline=False, size_hint_x=0.4)

            row.add_widget(label)
            row.add_widget(input_field)
            self.inputs_layout.add_widget(row)

            self.nominal_inputs[money_id] = (entry, input_field)

        if not has_money:
            self.inputs_layout.add_widget(Label(text="Нет доступных купюр в кошельке."))

    def on_pay_button_pressed(self):
        user = getattr(self.manager, "current_user", None)
        atm = getattr(self.manager, "selected_atm", None)

        if not user or not atm:
            self.show_error("Пользователь или банкомат не найден.")
            return

        total_sum = 0
        commission_rate = 0.01
        used_bills = {}

        try:
            for money_id, (entry, input_field) in self.nominal_inputs.items():
                quantity_str = input_field.text.strip()
                if not quantity_str:
                    continue

                if not quantity_str.isdigit():
                    raise ValueError(f"Неверный ввод для номинала {entry.money.money_nominal}.")

                quantity = int(quantity_str)
                if quantity <= 0:
                    continue
                if quantity > entry.quantity:
                    raise ValueError(f"Недостаточно купюр номинала {entry.money.money_nominal}.")

                used_bills[money_id] = quantity
                total_sum += quantity * entry.money.money_nominal

            if not used_bills:
                raise ValueError("Выберите хотя бы один номинал и введите корректное количество.")

            transfer_cash_to_atm(
                user=user,
                atm=atm,
                bills=used_bills,
                commission_rate=commission_rate
            )

            self.show_receipt({
                "Сумма перевода": f"{total_sum} сум",
                "Комиссия": f"{int(total_sum * commission_rate)} сум",
                "Итого поступило на банкомат": f"{int(total_sum * (1 - commission_rate))} сум"
            })

            self.refresh_inputs()

        except Exception as e:
            self.show_error(str(e))

    def show_receipt(self, receipt_data: dict):
        text = '\n'.join(f"{key}: {value}" for key, value in receipt_data.items())
        layout = BoxLayout(orientation='vertical', padding=20)
        layout.add_widget(Label(text=text))
        popup = Popup(title="🧾 Чек", content=layout, size_hint=(0.8, 0.6))
        popup.open()

    def show_error(self, message):
        layout = BoxLayout(orientation='vertical', padding=20)
        layout.add_widget(Label(text=message))
        popup = Popup(title="Ошибка", content=layout, size_hint=(0.7, 0.4))
        popup.open()
        