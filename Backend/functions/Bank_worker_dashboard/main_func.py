from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from Backend.functions.Bank_worker_dashboard.admin_panel_roles_crud import DefaultUserTable, RoleTable, BankWorkerTable, \
    IncasatorTable, UserTable
from Backend.functions.login_logout.login_admin import LoginScreen
from Backend.functions.Bank_worker_dashboard.admin_panel_cash_crud import *


class BankDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        btn_defaultuser = Button(text='Пользователи (DefaultUser)', size_hint_y=None, height=50)
        btn_defaultuser.bind(on_press=lambda x: setattr(self.manager, 'current', 'defaultuser_table'))

        btn_role = Button(text='Роли (Role)', size_hint_y=None, height=50)
        btn_role.bind(on_press=lambda x: setattr(self.manager, 'current', 'role_table'))

        btn_bankworker = Button(text='Работники банка (BankWorker)', size_hint_y=None, height=50)
        btn_bankworker.bind(on_press=lambda x: setattr(self.manager, 'current', 'bankworker_table'))

        btn_incasator = Button(text='Инкассаторы (Incasator)', size_hint_y=None, height=50)
        btn_incasator.bind(on_press=lambda x: setattr(self.manager, 'current', 'incasator_table'))

        btn_user = Button(text='Пользователи (User)', size_hint_y=None, height=50)
        btn_user.bind(on_press=lambda x: setattr(self.manager, 'current', 'user_table'))

        # Новая кнопка для кредитных карт (исправлено название переменной)
        btn_credit_cards = Button(text='Кредитные карты(CreditCards)', size_hint_y=None, height=50)
        btn_credit_cards.bind(on_press=lambda x: setattr(self.manager, 'current', 'credit_cards_table'))

        btn_phones = Button(text='Телефоны(PhoneNumbers)', size_hint_y=None, height=50)
        btn_phones.bind(on_press=lambda x: setattr(self.manager, 'current', 'phones_table'))

        btn_money = Button(text='Деньги (Money)', size_hint_y=None, height=50)
        btn_money.bind(on_press=lambda x: setattr(self.manager, 'current', 'money_rate'))

        btn_logout = Button(text='Выйти', size_hint_y=None, height=50)
        btn_logout.bind(on_press=lambda x: setattr(self.manager, 'current', 'language'))

        layout.add_widget(btn_defaultuser)
        layout.add_widget(btn_role)
        layout.add_widget(btn_bankworker)
        layout.add_widget(btn_incasator)
        layout.add_widget(btn_user)
        layout.add_widget(btn_credit_cards)  # Исправлено на btn_credit_cards
        layout.add_widget(btn_phones)
        layout.add_widget(btn_money)
        layout.add_widget(btn_logout)


        self.add_widget(layout)


class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(BankDashboard(name="bank_dashboard"))
        self.sm.add_widget(DefaultUserTable(name='defaultuser_table'))
        self.sm.add_widget(RoleTable(name='role_table'))
        self.sm.add_widget(BankWorkerTable(name='bankworker_table'))
        self.sm.add_widget(IncasatorTable(name='incasator_table'))
        self.sm.add_widget(UserTable(name='user_table'))
        self.sm.add_widget(PhoneNumberTable(name='phones_table'))
        self.sm.add_widget(CreditCardTable(name='credit_cards_table'))
        self.sm.add_widget(MoneyManagementScreen(name='money_rate' ))

        Window.bind(on_key_down=self.on_key_down)
        return self.sm

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if 'ctrl' in modifier and codepoint == 'b':
            self.sm.current = 'login'


if __name__ == '__main__':
    MyApp().run()
