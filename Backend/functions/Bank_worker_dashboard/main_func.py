from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from Backend.functions.Bank_worker_dashboard.admin_panel_roles_crud import DefaultUserTable, RoleTable, BankWorkerTable, \
    IncasatorTable, UserTable
from Backend.functions.login_logout.login_admin import LoginScreen


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

        layout.add_widget(btn_defaultuser)
        layout.add_widget(btn_role)
        layout.add_widget(btn_bankworker)
        layout.add_widget(btn_incasator)
        layout.add_widget(btn_user)

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

        Window.bind(on_key_down=self.on_key_down)
        return self.sm

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if 'ctrl' in modifier and codepoint == 'b':
            self.sm.current = 'login'


if __name__ == '__main__':
    MyApp().run()
