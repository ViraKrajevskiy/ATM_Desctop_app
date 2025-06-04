from wsgiref import headers

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

# импорт моделей
from Backend.ClassesNew.ROLE.base_user_m import DefaultUser, Role
from Backend.ClassesNew.ROLE.bank_worker import BankWorker
from Backend.ClassesNew.ROLE.user import User
from Backend.ClassesNew.ROLE.incasator import Incasator
from Backend.functions.login_logout.login_admin import LoginScreen


class DefaultUserTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_back = Button(text='Назад', size_hint_y=None, height=40)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))
        layout.add_widget(btn_back)

        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'First Name', 'Surname', 'Last Name', 'Created At']
        for h in headers:
            lbl = Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30)
            grid.add_widget(lbl)

        for user in DefaultUser.select():
            for value in [str(user.id), user.first_name, user.surname, user.last_name, str(user.created_at)]:
                lbl = Label(text=value, size_hint_y=None, height=30)
                grid.add_widget(lbl)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)




class RoleTable(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_back = Button(text='Назад', size_hint_y=None, height=40)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))
        layout.add_widget(btn_back)

        scroll = ScrollView()
        grid = GridLayout(cols=3, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Name', 'Access']
        for h in headers:
            lbl = Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30)
            grid.add_widget(lbl)

        for role in Role.select():
            for value in [str(role.id), role.name, str(role.access)]:
                lbl = Label(text=value, size_hint_y=None, height=30)
                grid.add_widget(lbl)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)


class BankWorkerTable(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_back = Button(text='Назад', size_hint_y=None, height=40)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))
        layout.add_widget(btn_back)

        scroll = ScrollView()
        grid = GridLayout(cols=3, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Login', 'Password']  # обязательно объявить

        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True))

    # пример вывода данных
        for worker in BankWorker.select():
            grid.add_widget(Label(text=str(worker.id)))
            grid.add_widget(Label(text=worker.login))
            grid.add_widget(Label(text=worker.password))

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

class IncasatorTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_back = Button(text='Назад', size_hint_y=None, height=40)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))
        layout.add_widget(btn_back)

        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'First Name', 'Surname', 'Last Name', 'Created At']
        for h in headers:
            lbl = Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30)
            grid.add_widget(lbl)

        for user in DefaultUser.select():
            for value in [str(user.id), user.first_name, user.surname, user.last_name, str(user.created_at)]:
                lbl = Label(text=value, size_hint_y=None, height=30)
                grid.add_widget(lbl)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)



class UserTable(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_back = Button(text='Назад', size_hint_y=None, height=40)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))
        layout.add_widget(btn_back)

        scroll = ScrollView()
        grid = GridLayout(cols=3, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Connect DefaultUser ID', 'Wallet Count']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True))

        for user in User.select():
            grid.add_widget(Label(text=str(user.id)))
            grid.add_widget(Label(text=str(user.connect.id) if user.connect else "None"))
            wallets_count = user.wallet.count() if hasattr(user, 'wallet') else 0
            grid.add_widget(Label(text=str(wallets_count)))

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)


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
    