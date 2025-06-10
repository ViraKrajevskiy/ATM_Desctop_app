# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.uix.textinput import TextInput
# from kivy.uix.popup import Popup
# from kivy.graphics import Color, RoundedRectangle
#
# import re
#
# from Backend.ClassesNew.CASH.tranzaction import TranzactionMoney
# from Backend.functions.translate.TranslateMenu import translations
#
#
# from peewee import DoesNotExist
# from datetime import datetime
#
# def pay_with_card_to_phone(card_input: str, card_password: str, phone_number: str, amount: int, atm):
#
#     # Шаг 1: Поиск карты
#     try:
#         card = CardMoney.get(
#             (CardMoney.card_number.endswith(card_input) | (CardMoney.card_number == card_input))
#         )
#     except DoesNotExist:
#         raise ValueError("Карта не найдена.")
#
#     # Шаг 2: Проверка пароля
#     if card.password != card_password:
#         raise ValueError("Неверный пароль от карты.")
#
#     # Шаг 3: Проверка баланса
#     if card.balance < amount:
#         raise ValueError("Недостаточно средств на карте.")
#
#     # Шаг 4: Списание с карты
#     card.balance -= amount
#     card.save()
#
#     # Шаг 5: Пополнение ATM
#     try:
#         nominal = MoneyNominal.get(MoneyNominal.money_nominal == 1)  # или динамически определить
#     except DoesNotExist:
#         raise ValueError("Номинал 1 не найден в базе.")
#
#     atm_wallet_entry, _ = WalletMoney.get_or_create(
#         wallet=atm.wallet,
#         money=nominal,
#         defaults={"quantity": 0}
#     )
#     atm_wallet_entry.quantity += amount // nominal.money_nominal
#     atm_wallet_entry.save()
#
#     # Шаг 6: Найти пользователя по номеру телефона
#     try:
#         recipient = BaseUser.get(BaseUser.phone_number == phone_number)
#     except DoesNotExist:
#         raise ValueError("Пользователь с таким номером телефона не найден.")
#
#     # Шаг 7: Пополнить кошелёк пользователя
#     user_wallet_entry, _ = WalletMoney.get_or_create(
#         wallet=recipient.wallet,
#         money=nominal,
#         defaults={"quantity": 0}
#     )
#     user_wallet_entry.quantity += amount // nominal.money_nominal
#     user_wallet_entry.save()
#
#     return {
#         "статус": "успешно",
#         "время": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "получатель": recipient.username,
#         "номер телефона": phone_number,
#         "сумма": amount,
#         "карта": card.card_number[-4:],
#     }
#
#
# class RoundedButton(Button):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.background_normal = ''
#         self.background_color = (0, 0, 0, 0)
#         with self.canvas.before:
#             Color(0.2, 0.5, 0.8, 1)
#             self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
#         self.bind(pos=self.update_rect, size=self.update_rect)
#
#     def update_rect(self, *args):
#         self.rect.pos = self.pos
#         self.rect.size = self.size
#
# class ThemedBoxLayout(BoxLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         with self.canvas.before:
#             Color(0.9, 0.9, 0.9, 1)
#             self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
#         self.bind(pos=self.update_rect, size=self.update_rect)
#
#     def update_rect(self, *args):
#         self.rect.pos = self.pos
#         self.rect.size = self.size
#
# class PaymentMethodScreen(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.layout = ThemedBoxLayout(orientation='vertical', spacing=20, padding=40)
#         self.add_widget(self.layout)
#
#     def on_pre_enter(self):
#         self.layout.clear_widgets()
#         texts = translations[self.manager.language]
#
#         title = Label(text=texts["SelectPaymentMethod"], font_size=24, size_hint_y=None, height=50)
#         self.layout.add_widget(title)
#
#         btn_card = RoundedButton(text=texts["PayWithCard"], size_hint_y=None, height=60)
#         btn_card.bind(on_press=self.select_card)  # привязка к методу
#         self.layout.add_widget(btn_card)
#
#         btn_cash = RoundedButton(text=texts["PayWithCash"], size_hint_y=None, height=60)
#         btn_cash.bind(on_press=self.select_cash)  # привязка к методу
#         self.layout.add_widget(btn_cash)
#
#         btn_back = RoundedButton(text=texts["BackToMenu"], size_hint_y=None, height=60)
#         btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
#         self.layout.add_widget(btn_back)
#
#     def select_card(self, instance):
#         self.manager.get_screen('card_payphones').payment_method = 'card'
#         self.manager.current = 'card_payphones'
#
#     def select_cash(self, instance):
#         self.manager.get_screen('cash_payment').payment_method = 'cash'
#         self.manager.current = 'phone_entry'
#
#
#
# from Backend.ClassesNew.CASH.wallet import WalletMoney
#
#
#
# def generate_receipt(nominal: int, quantity: int, total: int, transaction):
#     return {
#         "Чек ID": transaction.id,
#         "Тип оплаты": "Наличные",
#         "Номинал": nominal,
#         "Количество купюр": quantity,
#         "Общая сумма": total,
#         "Дата": transaction.created_at.strftime("%Y-%m-%d %H:%M"),
#         "Банкомат ID": transaction.atm.id,
#         "Пользователь ID": transaction.user.id
#     }
#
#
# def transfer_cash_to_atm(user, user_wallet_id: int, atm, money_id: int, quantity: int):
#     # 1. Проверка, хватает ли у пользователя
#     wallet_money = WalletMoney.get_or_none(wallet=user_wallet_id, money=money_id)
#     if not wallet_money or wallet_money.quantity < quantity:
#         raise ValueError("Недостаточно купюр")
#
#     # 2. Уменьшаем у пользователя
#     wallet_money.quantity -= quantity
#     wallet_money.save()
#
#     # 3. Переводим в кошелёк банкомата
#     atm_wallet = atm.wallet
#     atm_entry, _ = WalletMoney.get_or_create(wallet=atm_wallet, money=money_id, defaults={'quantity': 0})
#     atm_entry.quantity += quantity
#     atm_entry.save()
#
#     # 4. Создаём транзакцию
#     total_amount = wallet_money.money.money_nominal * quantity
#     transaction = TranzactionMoney.create(
#         user=user,
#         atm=atm,
#         payment_type='cash',
#         amount=total_amount
#     )
#
#     return generate_receipt(wallet_money.money.money_nominal, quantity, total_amount, transaction)
#
